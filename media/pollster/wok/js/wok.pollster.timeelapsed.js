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
							// register submit handle to set the duration into the field.
                            $field.closest('form').submit(function() {
                                    d = new Date();
                                    d = d.valueOf();
                                    var $el = $('#'+id);
                                    var duration = d - parseInt($el.data('timestart'));
                                    $el.val(duration);
                            });
                        }
            });
        }

// Add the datatype
window.wok.pollster.datatypes.TimeElapsed = TimeElapsedType;

})(jQuery);
