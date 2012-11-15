/**
 * Build Household Story
 */

function StoryTable(history, users) {
	this.history = history;
	this.users = users;

}
 
StoryTable.media = ''; 
 
$.extend(StoryTable.prototype, {
	
	/*
	 * Build a row, with d and row values for each users
	 */
	buildRow: function (d, row) {
		var o = '<tr>';
		var date = d.getDate() + '/' + (d.getMonth() + 1) + '/' + d.getFullYear();
		o += '<td class="date">'+date+'</td>';
		var n = this.users.length;
		for(var i=0; i < n; ++i) {
			u = this.users[i];
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
		return '<img src="'+StoryTable.media+'/survey/img/diag-'+s+'-small.png" title="'+ h.diag +'" alt="" />';
	},
	
	ymd: function(d) {
		return d.getDate()+'-'+ (d.getMonth() + 1) +'-' + d.getFullYear();
	},
	
	render : function(container) {
		var d = null;
		var row = {};
		var out = '<table>';
		
		var n = this.users.length;
		out +='<tr>';
		out += '<th>Date</th>';
		for(var i=0; i < n; ++i) {
			out += '<th>' + this.users[i] + '</th>';
		}
		out += '</tr>';
		n = this.history.length;
		for(var i=0; i < n; ++i) {
			var h = this.history[i];
			if(i == 0)  {
				d = h.date;
			}
			if( this.ymd(d) != this.ymd(h.date) ) {
				out += this.buildRow(d, row);
				row = {};
				d = h.date;	
			}
			row[ h.user ] = this.buildDiag(h);
		}
		out += this.buildRow(d, row);
		out += '</table>';
		$('#'+container).html(out);
	}
});




