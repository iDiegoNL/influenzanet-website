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
			b.addClass('codeselect-button');
			b.click(function(ev){
				console.log(ev);
				console.log(id);
				searchMunicipalCode(id);
			});
			$field.after(b);
			var b = $('<span id="'+id+'-title" class="codeselect-title"></span>');
			var v = $field.val();
			if(v != '') {
				b.text(v);	
			}
			$field.after(b);
		}
    });
}

searchMunicipalCode = function (id) {
	var mask = {
		zIndex: 1000,
		color: '#fff',
		loadSpeed: 200,
		opacity: 0.5
	};
	if($.browser.msie) {
		mask = 0; // disable expose mask on ie
	}
	$('#facebox').load('/municipal/search?id='+id).overlay({
		top: 260,
		mask: mask,
		closeOnClick: false
	}).load();
};


// Add the datatype
window.wok.pollster.datatypes.CodeSelect= CodeSelectType;

$(document).ready(function() {
	var f = $('#facebox');
	if(f.length == 0) {
		$('body').append('<div id="facebox">');	
	}
})

})(jQuery);
