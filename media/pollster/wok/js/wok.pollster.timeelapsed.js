(function($){
   function TimeElapsedType(){
		var self = this;
		
		$.extend(this, {
	        check: function($field) {
	            return $field.val() != '';
	        },
	        bind: function($field) {
				var id = $field.attr('id');
				var d = new Date();
				$field.data('timestart', d.valueOf());
				$('#commentsubmit').click(function() {
					d = new Date();
					d = d.valueOf();
					duration = d - parseInt($(id).data('timestart'));
					$(id).val(duration);
				});
			}
	    });
	}

// Add the datatype
window.wok.pollster.datatypes.TimeElapsed = TimeElapsedType;

})(jQuery);