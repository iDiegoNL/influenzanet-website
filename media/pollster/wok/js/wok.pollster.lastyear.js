$(function() {
	var last_year = wok.pollster.last_participation_data || {};
	if( last_year.lastyeardata ) {
		$('#last_year_warning').show();
	}
});
