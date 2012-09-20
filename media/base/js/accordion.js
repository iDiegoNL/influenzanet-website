$(document).ready(function() {
	$('.accordionButton').click(function() {
		
		$('.accordionButton').removeClass('on');
	 	$('.accordionContent').slideUp('normal');
		
		if($(this).next().is(':hidden') == true) {
			$(this).addClass('on');
			$(this).next().slideDown('normal');
		 } 
	 });

	$('.accordionButton').mouseover(function() {
		$(this).addClass('over');

	}).mouseout(function() {
		$(this).removeClass('over');										
	});

	$('.accordionContent').hide();



    $('.accordionButton input[type=checkbox]').click(function(evt){
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



});
