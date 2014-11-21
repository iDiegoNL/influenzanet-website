(function($){
   function VisualScaleType(){
      var self = this;
      $.extend(this, {
                check: function($field) {
                    return $field.val() != '';
                },
                bind: function($field) {
                        var id = $field.attr('id');
						var value = $field.val();
						if(value == '') {
							value = 50;
						}
                        var id_slider = id +'_slider';
						$field.hide();
						var $slider = $('<div id="' + id_slider + '"></div>');
						$slider.data('question-id', id);
						$slider.slider({
							'min': 0,
							'max': 100,
							'value': value,
							'change': function(ev, ui) {
								var $e = $(this);
								console.log('Update slider to ' + ui.value);
								var id = $e.data('question-id');
								$('#' + id).val(ui.value);
								$('#' + id + '-vas-response').text('Votre réponse a été prise en compte').addClass('vas-response-ok');
								$('#' + id + '_slider .ui-slider-handle').css({'background-color': '#7AB800'});
							}
						});
						$field.after('<div class="slider-range"><div id="slider-min" ><span class="vas-worst-level"></span><br/>Très mal</div><div id="slider-max"><span class="vas-best-level"></span><br/>Tout va bien</div><div style="clear:both">&nbsp;</div><div class="vas-response" id="'+ id +'-vas-response">Vous n\'avez pas répondu</div><div class="vas-help">Glissez le curseur pour le placer sur la barre jusqu\'au niveau qui correspond le mieux à l\'état de santé global du participant aujourd\'hui.<br/> <b style="color:red">Attention </b>:Cliquez sur le curseur au moins une fois pour que votre réponse soit prise en compte(le curseur deviendra vert).</div></div>');
						$wrap = $('<div class="slider-wrap"</div>');
						$wrap.append($slider);
						$field.after($wrap);
			    }
            });
        }

// Add the datatype
window.wok.pollster.datatypes.VisualScale = VisualScaleType;

})(jQuery);
