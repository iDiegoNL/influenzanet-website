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
							$field.after('<div class="slider-range" style="position:relative"><div id="slider-min" style="float:left"><span class="vas-worst-level"></span><br/>Très mauvais</div><div id="slider-max" style="float:right"><span class="vas-best-level"></span><br/>Tout va bien</div><div style="clear:both">&nbsp;</div><div class="vas-help">Glissez le curseur pour le placer sur la barre jusqu\'au niveau qui correspond le mieux à l\'état de santé global du participant aujourd\'hui</div></div>');
							$wrap = $('<div class="slider-wrap" style="margin: .5em auto;text-align:center;width:80%"></div>');
							$wrap.append($slider);
							$field.after($wrap);
							
			    }
            });
        }

// Add the datatype
window.wok.pollster.datatypes.VisualScale = VisualScaleType;

})(jQuery);
