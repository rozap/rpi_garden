require.config({

    baseUrl: '/static/js/',


    shim: {
        underscore: {
            exports: '_'
        },
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        d3: {
            exports: 'd3'
        },
        rickshaw: {
            deps: ['d3'],
            exports: 'rickshaw'
        }
    },

    paths: {
        jquery: 'libs/jquery',
        underscore: 'libs/underscore',
        backbone: 'libs/backbone',
        d3: 'libs/d3',
        rickshaw: 'libs/rickshaw'
    }

});



require([
    'underscore',
    'backbone',
    'd3',
    'rickshaw',
    'collections',
    'models',
    'text!templates/chart.html',
    'text!templates/state.html',

], function(_, Backbone, d3, rickshaw, Collections, Models, ChartTemplateView, StateViewTemplate) {


    var app = {
        dispatcher: _.clone(Backbone.Events),
    }

    //I'm too lazy to setup python websockets, so we gon poll stuff
    //hi h8ers
    setInterval(function() {
        app.dispatcher.trigger('fetchNewData');
    }, 120000);


    var ChartView = Backbone.View.extend({


        width: 800,
        height: 400,

        template: _.template(ChartTemplateView),

        events: {
            'click .next-btn': 'nextPage',
            'click .prev-btn': 'prevPage',
        },

        initialize: function() {
            this.collection = new this.series([], app);
            this.listenTo(this.collection, 'sync', this.render);
            this.collection.fetch();
        },


        adaptData: function() {
            var that = this;
            return [{
                color: that.color,
                name: that.yName,
                data: this.collection.map(function(point) {
                    return {
                        x: point.get(that.xName),
                        y: point.get(that.yName)
                    };
                })
            }];
        },


        render: function() {
            this.$el.html(this.template({
                id: this.$el.attr('id'),
                title: this.title,
                hasNext: this.collection.hasNext.bind(this.collection),
                hasPrev: this.collection.hasPrev.bind(this.collection)
            }));

            console.log($(this.$el.attr('id') + '-chart')[0]);

            var that = this;
            this._graph = new rickshaw.Graph({
                element: $('#' + this.$el.attr('id') + '-chart')[0],
                renderer: 'area',
                min: this.minY,
                max: this.maxY,
                series: this.adaptData(),
            });
            new Rickshaw.Graph.Axis.Time({
                graph: this._graph
            });

            var yOpts = {
                graph: this._graph,
                orientation: 'left',
                width: 80,
                tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
                element: $('#' + this.$el.attr('id') + 'chart-y-axis')[0],
            };

            new Rickshaw.Graph.Axis.Y(yOpts);


            var hoverDetail = new Rickshaw.Graph.HoverDetail({
                graph: this._graph,
                xFormatter: this.formatX.bind(this),
                yFormatter: this.formatY.bind(this)
            });


            this._graph.render();
        },


        formatX: function(x) {
            return new Date(x * 1000) + " " + (this.xUnits || this.xName);
        },

        formatY: function(y) {
            return y + " " + (this.yUnits || this.yName);
        },

        nextPage: function() {
            this.collection.next();
        },

        prevPage: function() {
            this.collection.prev();
        },



    });


    var PHChartView = ChartView.extend({
        title: 'ph',
        el: '#ph-view',
        xName: 'time',
        yName: 'ph',
        series: Collections.PHCollection,
        color: '#A9C388',
        minY: 5.8,
        maxY: 8
    });

    var TempChartView = ChartView.extend({
        title: 'Temperature',
        el: '#temp-view',
        xName: 'time',
        yName: 'temp',
        yUnits: 'degrees',
        series: Collections.TempCollection,
        color: '#F54551',
        minY: 73,
        maxY: 78
    });

    var LevelChartView = ChartView.extend({
        title: 'Water level',
        el: '#level-view',
        xName: 'time',
        yName: 'level',
        yUnits: 'inches',
        series: Collections.LevelCollection,
        color: '#015A61',
        minY: 20,
        maxY: 29
    });

    var StateView = Backbone.View.extend({

        el: '#state-view',
        template: _.template(StateViewTemplate),

        initialize: function() {
            this.model = new Models.State({}, app);
            this.listenTo(this.model, 'sync', this.render);
            this.model.fetch();
            this._interval = setInterval(this.model.fetch.bind(this.model), 3000);
        },

        render: function() {
            this.$el.html(this.template({
                model: this.model.toJSON()
            }));
            return this
        },



    });


    var TimelapseView = Backbone.View.extend({
        el: '#timelapse',
        images: [],

        events: {
            'click .run-timelapse': 'run'
        },


        run: function() {
            clearInterval(this._interval);
            this.images = [];
            console.log("RUNNING")
            this.load(0);
            this.off('loadedBatch');
            this.on('loadedBatch', this.play.bind(this));
        },

        play: function() {
            console.log("PLAY")
            var can = this.$el.find('canvas')[0],
                ctx = can.getContext('2d');

            var counter = 0;
            this._interval = setInterval(function() {
                if (!this.images[counter]) {
                    this.stop();
                    return;
                }
                var img = this.images[counter];
                console.log(img.width, img.height)
                ctx.drawImage(img, 0, 0);
                counter++;
            }.bind(this), 20);
        },

        stop: function() {
            clearInterval(this._interval);
        },

        load: function(start) {
            this.loadBatch(start, function(images, errors, batchSize) {
                this.images = this.images.concat(images);
                console.log("Done loading batch")
                this.trigger('loadedBatch', start);
                if (!errors) {
                    this.load(start + batchSize);
                }
            }.bind(this));

        },

        loadBatch: function(start, cb) {
            var batchSize = 40,
                errors = false,
                images = [],
                done = _.after(batchSize, function() {
                    images = images.sort(function(a) {
                        return a[0];
                    }).map(function(img) {
                        return img[1];
                    });
                    cb(images, errors, batchSize);
                });

            for (var i = start; i < start + batchSize; i++) {
                var img = new Image();
                img.i = i;
                img.onload = function() {
                    images.push([this.i, this]);
                    done();
                }.bind(img);
                img.onerror = function() {
                    errors = true;
                    done();
                };
                img.src = '/static/timelapse/' + i + '-image.jpg';
            }
        }


    });

    new PHChartView();
    new TempChartView();
    new StateView();
    new TimelapseView();

    console.info("hello world")


})