define([
	'underscore',
	'backbone'
], function(_, Backbone) {

	var APICollection = Backbone.Collection.extend({

		pageSize: 600,
		page: 0,

		initialize: function(props, app) {
			app.dispatcher.on('update', this.autoUpdate.bind(this));
		},


		autoUpdate: function() {
			this.page === 0 && this.fetch();
		},

		url: function() {
			return '/api/' + this.name
		},

		_pageFetch: function() {
			return this.fetch({
				data: {
					offset: this.page * this.pageSize,
					count: this.pageSize
				}
			});
		},

		comparator: 'time',

		next: function() {
			this.page--;
			return this._pageFetch();
		},

		prev: function() {
			this.page++;
			return this._pageFetch();
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