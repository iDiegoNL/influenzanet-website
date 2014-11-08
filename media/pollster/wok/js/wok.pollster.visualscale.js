(function($){
   function VisualScaleType(){
                var self = this;

                $.extend(this, {
                check: function($field) {
                    return $field.val() != '';
                },
                bind: function($field) {
                            var id = $field.attr('id');
                            var id_slider = id +'_slider';
							$field.hide();
							var $slider = $('<div id="' + id_slider + '"></div>');
							$slider.data('question-id', id);
							$slider.slider({
								'min': 0,
								'max': 100,
								'change': function(ev, ui) {
									var $e = $(this);
									console.log('Update slider to ' + ui.value);
									var id = $e.data('question-id');
									$('#' + id).val(ui.value);
								}
							});
							$field.after('<div class="slider-range" style="position:relative"><div id="slider-min" style="float:left">Pire état</div><div id="slider-max" style="float:right">Tout va bien</div></div>');
							$wrap = $('<div class="slider-wrap" style="margin: .5em auto;text-align:center;width:80%"></div>');
							$wrap.append($slider);
							$field.after($wrap);
							
			    }
            });
        }

// Add the datatype
window.wok.pollster.datatypes.VisualScale = VisualScaleType;

})(jQuery);
