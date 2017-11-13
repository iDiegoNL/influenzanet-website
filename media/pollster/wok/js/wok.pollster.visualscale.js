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
						var tags = $field.parents('.question').data('tags');
						var scale_start ='Très mal';
						var scale_end = 'Tout va bien';
						var icon = true;
						console.log(tags);

						if(typeof(tags) == "string") {
							tags = jQuery.parseJSON(tags);
						}

						if(tags) {
							console.log(tags);
							scale_start = tags.start;
							scale_end = tags.end;
							icon = tags.icon;
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

						increment = function() {
							var $s = $(this);
							var ref = $s.data('ref');
							var op = $s.data('op');
							var $e = $('#'+ref);
							var value = parseInt($e.slider('value'));
							value += (op == 'i') ? 5 : -5;
							console.log(value);
							$e.slider('value', 	value);
						}

						var b1 = $('<span class="button" data-ref="'+id_slider+'" data-op="d">-</span>').on('click', increment);
						var b2 = $('<span class="button" data-ref="'+id_slider+'" data-op="i">+</span>').on('click', increment);


						var $r = $('<div class="slider-range"/>');
						$m = $('<div id="slider-min"/>')
						$m.append(b1);
						if(icon) {
						$m.append('<span class="vas-worst-level"/>');
						}
						$m.append('<span class="vas-start-level">'+scale_start+'</span>');
						$r.append($m);

						$m = $('<div id="slider-max"/>');
						$m.append('<span class="vas-start-level">'+scale_end+'</span>');
						if(icon) {
							$m.append('<span class="vas-best-level"/>');
						}
						$m.append(b2);

						$r.append($m);
						$r.append('<div style="clear:both">&nbsp;</div>');
						$r.append('<div class="vas-response" id="'+ id +'-vas-response">Vous n\'avez pas répondu</div><div class="vas-help">Glissez le curseur ou cliquez sur les boutons +/- en dessous, pour le placer sur la barre jusqu\'au niveau qui correspond le mieux à votre réponse.<br/> <b style="color:red">Attention </b>:Cliquez sur le curseur au moins une fois pour que votre réponse soit prise en compte (le curseur deviendra vert).</div>');

						$field.after($r);

						//$field.after(''</div><div id="slider-max"><span class="vas-best-level"></span><br/>'+scale_end+'</div><div style="clear:both">&nbsp;</div><div class="vas-response" id="'+ id +'-vas-response">Vous n\'avez pas répondu</div><div class="vas-help">Glissez le curseur pour le placer sur la barre jusqu\'au niveau qui correspond le mieux à l\'état de santé global du participant aujourd\'hui.<br/> <b style="color:red">Attention </b>:Cliquez sur le curseur au moins une fois pour que votre réponse soit prise en compte(le curseur deviendra vert).</div></div>');

						$wrap = $('<div class="slider-wrap"></div>');

						//$wrap.append(b1)
						$wrap.append($slider);
						//$wrap.append(b2)
						$field.after($wrap);
			    }
            });
        }

// Add the datatype
window.wok.pollster.datatypes.VisualScale = VisualScaleType;

})(jQuery);
