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
], function(_, Backbone, rickshaw, Collections) {


	var app = {
		dispatcher: _.clone(Backbone.Events),
	}



	var ChartView = Backbone.View.extend({

		chartEl: '#ph-time',
		xName: 'time',
		yName: 'ph',
		series: Collections.PHCollection,


		initialize: function() {
			this.collection = new this.series([]);
			this.listenTo(this.collection, 'sync', this.render);
			this.collection.fetch();
		},


		adaptData: function() {
			var that = this;
			return [{
				color: 'steelblue',
				data: this.collection.map(function(point) {
					return {
						x: point.get(that.xName),
						y: point.get(that.yName)
					};
				})
			}];
		},

		render: function() {
			console.log(this.adaptData())
			this._graph = new rickshaw.Graph({
				element: $(this.chartEl)[0],
				width: 800,
				height: 400,
				renderer: 'area',
				series: this.adaptData(),
			});
			new Rickshaw.Graph.Axis.Time({
				graph: this._graph
			});

			new Rickshaw.Graph.Axis.Y({
				graph: this._graph,
				orientation: 'left',
				tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
				element: $(this.chartEl + '-y-axis')[0],
			});

			var hoverDetail = new Rickshaw.Graph.HoverDetail({
				graph: this._graph,
				xFormatter: function(x) {
					return x + "seconds"
				},
				yFormatter: function(y) {
					return y + " ph"
				}
			});


			this._graph.render();
		}

	});


	new ChartView();

	console.info("hello world")


})