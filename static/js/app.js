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
	'rickshaw',
	'collections',
	'models',
	'text!templates/chart.html',
	'text!templates/state.html',

], function(_, Backbone, rickshaw, Collections, Models, ChartTemplateView, StateViewTemplate) {


	var app = {
		dispatcher: _.clone(Backbone.Events),
	}

	//I'm too lazy to setup python websockets, so we gon poll stuff
	//hi h8ers
	setInterval(function() {
		app.dispatcher.trigger('update');
	}, 5000);


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
				series: this.adaptData(),
			});
			new Rickshaw.Graph.Axis.Time({
				graph: this._graph
			});

			new Rickshaw.Graph.Axis.Y({
				graph: this._graph,
				orientation: 'left',
				width: 80,
				tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
				element: $('#' + this.$el.attr('id') + 'chart-y-axis')[0],
			});

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
	});

	var TempChartView = ChartView.extend({
		title: 'Temperature',
		el: '#temp-view',
		xName: 'time',
		yName: 'temp',
		yUnits: 'degrees',
		series: Collections.TempCollection,
		color: '#F54551',
	});

	var LevelChartView = ChartView.extend({
		title: 'Water level',
		el: '#level-view',
		xName: 'time',
		yName: 'level',
		yUnits: 'inches',
		series: Collections.LevelCollection,
		color: '#015A61',
	});

	var StateView = Backbone.View.extend({

		el: '#state-view',
		template: _.template(StateViewTemplate),

		initialize: function() {
			this.model = new Models.State({}, app);
			this.listenTo(this.model, 'sync', this.render);
			this.model.fetch();
		},

		render: function() {
			this.$el.html(this.template({
				model: this.model.toJSON()
			}));
			return this
		}



	});



	new PHChartView();
	new TempChartView();
	new LevelChartView();
	new StateView();

	console.info("hello world")


})