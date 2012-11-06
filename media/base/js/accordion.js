$(document).ready(function() {
	$('div.accordionButton').click(function() {
		
		$('div.accordionButton').removeClass('on');
	 	$('div.accordionContent').slideUp('normal');
		$('div.accordionContent img').fadeIn('slow');
        
		if($(this).next().is(':hidden') == true) {
			$(this).addClass('on');
			$(this).next().slideDown('normal');
		 } 
	 });

	$('div.accordionButton').mouseover(function() {
		$(this).addClass('over');

	}).mouseout(function() {
		$(this).removeClass('over');
	});

	$('div.accordionContent').hide();
	
    $('div.accordionButton input[type=checkbox]').click(function(evt){
		evt.stopPropagation();
	});
    
    $('div.accordionButton a.noslide').click(function(evt){
		evt.stopPropagation();
	});

    $('#select_all').change(function() {
        var checkboxes = $(this).closest('form').find(':checkbox');
        if($(this).is(':checked')) {
            checkboxes.attr('checked', 'checked');
        } else {
            checkboxes.removeAttr('checked');
        }
    });

    $("#open").trigger('click');

});
