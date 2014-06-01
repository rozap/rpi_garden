define([
	'underscore',
	'backbone'
], function(_, Backbone) {

	var APICollection = Backbone.Collection.extend({

		pageSize: 1000,
		page: 0,

		initialize: function(props, app) {
			app.dispatcher.on('fetchNewData', this.autoUpdate.bind(this));
		},


		autoUpdate: function() {
			this.page === 0 && this.fetch();
		},

		url: function() {
			return '/api/' + this.name
		},

		fetch: function(options) {
			options = _.extend({
				data: {
					offset: this.page * this.pageSize,
					count: this.pageSize
				}
			}, options);
			return Backbone.Collection.prototype.fetch.call(this, options);
		},

		comparator: 'time',

		next: function() {
			this.page--;
			return this.fetch();
		},

		prev: function() {
			this.page++;
			return this.fetch();
		},

		hasNext: function() {
			return this.page > 0;
		},

		hasPrev: function() {
			return this.length === this.pageSize;
		}



	});

	var PHCollection = APICollection.extend({
		name: 'ph',
	});

	var TempCollection = APICollection.extend({
		name: 'temp',
	})

	var LevelCollection = APICollection.extend({
		name: 'level',
	})

	return {
		PHCollection: PHCollection,
		TempCollection: TempCollection,
		LevelCollection: LevelCollection



	}


})