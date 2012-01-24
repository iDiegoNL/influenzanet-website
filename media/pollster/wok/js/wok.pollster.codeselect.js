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
				searchMunicipalCode(id);
			});
			$field.after(b);
			var b = $('<span id="'+id+'-title" class="codeselect-title"></span>');
			$field.after(b);
			var name = $field.attr('name');
			var v = window.wok.pollster.last_participation_data[name] || '';
			if(v != '') {
				$.ajax({
					url: '/municipal/title/'+v,
					success: function(data) {
						console.log(data);
						b.text(data);
					}
				});	
			}
		}
    });
}

searchMunicipalCode = function (id) {
		$.ajax({
		url: '/municipal/search?id='+id,
		success: function(data) {
			show_facebox({contents: data, width: 400, height:300, top: 260});
		}
	});
};


// Add the datatype
window.wok.pollster.datatypes.CodeSelect= CodeSelectType;

$(document).ready(function() {
	// Patch to pollster, store last particpation data
	var last_participation_data = {};
    if(window.pollster_last_participation_data) {
		last_participation_data = pollster_last_participation_data();
		if(!last_participation_data) {
			last_participation_data = {};
		}
	}
    window.wok.pollster.last_participation_data = last_participation_data;
});

})(jQuery);
