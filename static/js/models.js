define([
	'underscore',
	'backbone'
], function(_, Backbone) {

	var Calibration = Backbone.Model.extend({

		url: function() {
			return '/api/calibration'
		},


	});


	return {
		Calibration: Calibration,
	}


})