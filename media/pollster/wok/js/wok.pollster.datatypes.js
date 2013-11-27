(function($) {
    // COMMON UTILITIES
	var msPerDay = 24 * 60 * 60 * 1000;
	
	function get_question_from_field($field) {
		return $field.parents('.question');
	}
	
	function get_question_tags($field) {
		// get tags and return them as hash
		var tags = $field.parents('.question').data('tags');
		var o = {};
		if(tags) {
			tags = tags.replace(' ','');
			tags = tags.split(',');
			var i = tags.length;
			while(i--) {
				o[ tags[i] ] = 1;
			}
		}
		return o;
	}
	
    // BUILTIN DATA TYPES

    function DateType() {
        var self = this;
		
        // Public methods.

        $.extend(this, {
            check: function($field) {
                return true;
            },
            bind: function($field) {
                
				var tags = get_question_tags($field);
				
				var opts = {
                        constrainInput: true,
                        dateFormat: 'dd/mm/yy',
                        changeMonth: true,
                        changeYear: true 
                    };
				if(tags.nofuture) {
					opts.maxDate = '0';
				}
				if(tags.delay) {
					$field.data('show-delay', true);
					var id = $field.attr('id') + '-delay';
					$field.data('show-delay-id', id);
					$field.after('<span class="question-date-delay" id="'+ id +'">');
					$field.css({'width': '7em'});
				}
				
				$field
                    .datepicker(opts)
                    .change(function(evt){
                        var $this = $(this);
                        var date = Date.parseExact($this.val(), "yyyy-MM-dd");
                        if (date) {
							$this.val(date.toString('dd/MM/yyyy'));
						}
						else {
							date = Date.parseExact($this.val(), "dd/MM/yyyy");
							if (date)  
								$this.val(date.toString('dd/MM/yyyy'));
							else 
								$this.val('');
						}
						if($field.data('show-delay') ) {
							if(date) {
								var now = new Date();
								var delay = Math.floor((now.getTime() - date.getTime())/msPerDay);
								var id = $this.data('show-delay-id');
								var label = Date.CultureInfo[ (delay > 1) ? 'days': 'day'];
								$('#'+id).text(delay + ' ' + label);
							}
						}
                    });

            }
        });
    }

    function TextType() {
        var self = this;

        // Public methods.

        $.extend(this, {
            check: function($field) {
                if (this._regex)
                    return this._regex.test($field.val());
                else
                    return true;
            },
            bind: function($field) {
                var pattern = $field.closest(".question").data("regex");
                if (pattern)
                    this._regex = new RegExp(pattern);
                else
                    this._regex = null;
            }
        });
    }

    function NumericType() {
        var self = this;
        this._regex = /^[0-9]+$/;

        // Public methods.

        $.extend(this, {
            check: function($field) {
                var value = $field.val();
                if (value && self._regex)
                    return self._regex.test(value);
                else
                    return true;
            },
            bind: function($field) {
            }
        });
    }

    function PostalCodeType() {
        var self = this;
        if (window.pollster_get_postal_code_format)
            this._regex = new RegExp('^'+pollster_get_postal_code_format()+'$', 'i');
        else
            this._regex = null;

        // Public methods.

        $.extend(this, {
            check: function($field) {
                var value = $field.val();
                if (value && this._regex)
                    return this._regex.test(value);
                else
                    return true;
            },
            bind: function($field) {
            }
        });
    }

    function YearMonthType() {
        var self = this;

        function split(val) {
            var month = parseInt(val.replace(/[/-].*$/, ''), 10);
            var year = parseInt(val.replace(/^.*[/-]/, ''), 10);
            return { year: year, month: month };
        }

        // Public methods.

        $.extend(this, {
            check: function($field) {
                var val = $field.val();
                var d = split(val)
                return d.year && d.month;
            },
            bind: function($field) {
				
				var tags = get_question_tags($field);
				if(tags.delay) {
					$field.data('show-delay', true);
					var id = $field.attr('id') + '-delay';
					$field.data('show-delay-id', id);
					$field.after('<span class="question-date-delay" id="'+ id +'">');
				}
				
                $field
                    .datepicker({
                        constrainInput: true,
                        dateFormat: 'mm/yy',
                        changeMonth: true,
                        changeYear: true ,
                        yearRange: '-110:+0',
                        beforeShow: function(input, inst) {
                            inst.dpDiv.addClass('year-month-only');
                            $('head').append('<style id="hide-year-month-only-calendar" type="text/css">.year-month-only .ui-datepicker-calendar { display: none; }</style>');
                            var val = $(input).val();
                            var d = split(val)
                            if (d.year && d.month) {
                                setTimeout(function(){
                                    $(input).datepicker('setDate', new Date(d.year, d.month-1, 1));
                                }, 0);
                            }

                        },
                        onChangeMonthYear: function(year, month, inst) {
                            var val = month+'/'+year;
                            if (month < 10)
                                val = '0'+val;
                            $(inst.input).val(val).change();
                        },
                        onClose: function(dateText, inst) { 
                            inst.dpDiv.removeClass('year-month-only');
                            setTimeout(function(){
                                $('head #hide-year-month-only-calendar').remove();
                            }, 0);
                        }
                    })
                    .change(function(evt){
                        var $this = $(this);
                        var value = $this.val();
                        var newValue = '';
                        var d = split(value);
                        if (d.year && d.month) {
                            if (d.month > 12) {
                                d = { year: d.month, month: d.year }
                            }
                            var date = new Date(d.year, d.month-1, 1);
                            if (date) {
                                newValue = date.toString('MM/yyyy');
								if($this.data('show-delay')) {
									var id = $this.data('show-delay-id');
									var today = new Date();
									year = today.getFullYear() - date.getFullYear();
									//month = (11 - date.getMonth()) + today.getMonth() + 1; 
									var label = Date.CultureInfo[ (year > 1) ? 'years': 'year'];
									$('#'+id).text(year + ' ' + label);
								}
							}
                        }
                        $this.val(newValue);
                    });
            }
        });
    }

    // used internally for builtin questions
    function TimestampType() {
        var self = this;

        // Public methods.

        $.extend(this, {
            check: function($field) {
                return true;
            },
            bind: function($field) {
            }
        });
    }

    // MODULE INITIALIZATION

    window.wok.pollster.datatypes = {
        "Text": TextType,
        "Numeric": NumericType,
        "PostalCode": PostalCodeType,
        "Date": DateType,
        "YearMonth": YearMonthType,
        "Timestamp": TimestampType
    };

})(jQuery);
