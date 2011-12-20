(function($){
   function CodeSelectType(){
	var self = this;
	
	$.extend(this, {
        check: function($field) {
            return $field.val() != '';
        },
        bind: function($field) {
			var id = $field.attr('id');
			$field.css('display','none');
			var b = $('<button type="button">');
			b.text('Cliquez ici pour trouver votre commune');
			b.addClass('button');
			b.click(function(ev){
				searchMunicipalCode(id);
				ev.preventDefault();
			});
			$field.after(b);
			var b = $('<span id="'+id+'-title"></span>');
			var v = $field.val();
			if(v != '') {
				b.text(v);	
			}
			$field.after(b);
		}
    });
}

searchMunicipalCode = function (id) {
	var $field = $('#'+id);
	b = $('<div id="facebox">');
	$field.after(b);

	var mask = {
		zIndex: 1000,
		color: '#fff',
		loadSpeed: 200,
		opacity: 0.5
	};
	if(jQuery.browser.msie) {
		mask = 0; // disable expose mask on ie
	}
	$('#facebox').load('/municipal/search?id='+id).overlay({
		top: 260,
		mask: mask,
		closeOnClick: false,
		load: true
	});
};



// Add the datatype
window.wok.pollster.datatypes.CodeSelect= CodeSelectType;

})(jQuery);
