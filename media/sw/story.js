/**
 * Build Household Story
 */

var Story = {
	
	/*
	 * Media files path 
	 */
	media: '',
	
	/*
	 * Build a row, with d and row values for each users
	 */
	buildRow: function (d, row) {
		var o = '<tr>';
		var date = d.getDate() + '/' + (d.getMonth() + 1) + '/' + d.getFullYear();
		o += '<td class="date">'+date+'</td>';
		var n = users.length;
		for(var i=0; i < n; ++i) {
			u = users[i];
			var diag = row[u];
			if(typeof(diag) == "undefined") {
				diag = "&nbsp;"
			}
			o += '<td>'+diag +'</td>';
		}
		o += '</tr>';
		return o;	
	},

	/*
	 * Diagnosis contents
	 */
	buildDiag: function (h) {
		var s = h.status;
		if(typeof(s)== 'undefined') {
			s = 'UNKNOWN';
		}
		return '<img src="'+Story.media+'/survey/img/diag-'+s+'-small.png" title="'+ h.diag +'" alt="" />';
	},
	
	ymd: function(d) {
		return d.getDate()+'-'+ (d.getMonth() + 1) +'-' + d.getFullYear();
	},
	
	render : function(container) {
		var d = null;
		var row = {};
		var out = '<table>';
		
		var n = users.length;
		out +='<tr>';
		out += '<th>Date</th>';
		for(var i=0; i < n; ++i) {
			out += '<th>' + users[i] + '</th>';
		}
		out += '</tr>';
		n = history.length;
		for(var i=0; i < n; ++i) {
			var h = history[i];
			if(i == 0)  {
				d = h.date;
			}
			if( Story.ymd(d) != Story.ymd(h.date) ) {
				out += Story.buildRow(d, row);
				row = {};
				d = h.date;	
			}
			row[ h.user ] = Story.buildDiag(h);
		}
		out += Story.buildRow(d, row);
		out += '</table>';
		$(container).html(out);
	}
};




