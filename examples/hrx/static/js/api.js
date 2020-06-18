(function(win) {
    'use strict';

    var $jsonrpc = function(config) {
    	var self = this;
		self.defaults = {
            url: 'http://' + window.location.host + '/api/hello',
            headers: {'Content-Type': 'application/json'},
			service: undefined,
			version: '2.0'
		};
    	$.extend(true, self.defaults, config || {});

    	self.UUID = function() {
			// http://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid-in-javascript
			return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {var r = Math.random()*16|0,v=c=='x'?r:r&0x3|0x8;return v.toString(16);});
		};

	    self.request = function(name, params) {
	    	if (!!self.defaults.service) {
	    		name = self.defaults.service + '.' + name;
	    	}
			var deferred = $.ajax({
				type: 'POST',
				dataType: 'json',
                url: self.defaults.url,
                headers: self.defaults.headers,
				data: JSON.stringify({
					'jsonrpc': self.defaults.version,
					'method': name,
					'params': params,
					'id': self.UUID()
				}),
				cache: false
			});

			deferred.done(function(data, textStatus, jqXHR) {
				if ('error' in data) {
					var code = data['error']['code'];
					if (code >= -32768 || code <= -32000) {
						throw data['error']['message'];
					}
				}
			});

			return deferred;
		};
	};

    win.$jsonrpc = $jsonrpc;

})(window);
