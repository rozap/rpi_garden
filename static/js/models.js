define([
	'underscore',
	'backbone'
], function(_, Backbone) {

	var Calibration = Backbone.Model.extend({

		url: function() {
			return '/api/calibration'
		},


	});


	var State = Backbone.Model.extend({
		url: function() {
			return '/api/state'
		}
	});

	return {
		State: State
	}


})