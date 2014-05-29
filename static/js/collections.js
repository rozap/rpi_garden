define([
	'underscore',
	'backbone'
], function(_, Backbone) {

	var APICollection = Backbone.Collection.extend({

		pageSize: 60,
		page: 0,
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
			console.log(this.length, this.pageSize)
			return this.length === this.pageSize;
		}



	});

	var PHCollection = APICollection.extend({
		name: 'ph',
	});

	var TempCollection = APICollection.extend({
		name: 'temp',
	})


	return {
		PHCollection: PHCollection,
		TempCollection: TempCollection



	}


})