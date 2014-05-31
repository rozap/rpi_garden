define([
	'underscore',
	'backbone'
], function(_, Backbone) {



	var State = Backbone.Model.extend({
		initialize: function(props, app) {
			app.dispatcher.on('update', this.fetch.bind(this));
		},

		url: function() {
			return '/api/state'
		}
	});

	return {
		State: State
	}


})