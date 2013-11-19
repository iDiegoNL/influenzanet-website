 
function prepare_data(data, column, my_group, translation) {
	var values = [], 
	labels = [], // Bar labels
	colors = [], // Bar colors
	my_group_idx, // index of the group the user belongs to
	vv, i, label, 
	units;
	i = 0;
	console.log(data);
	my_group_idx = -1;
	vv = data[column];
	if(column == 'prop') {
		units = '%';
	} else {
		units = '';
	}
	for(var n in vv) {
		values.push(vv[n]);
		if(translation) {
			label = translation[n];
		} else {
			label = n;
		}
		labels.push(label);
		if( n == my_group ) {
		 	my_group_idx = i;
			colors.push('#7AB800');
		} else {
			colors.push('#007AB8');
		}
		++i;
	}
	return {
		values: values,
		labels: labels,
		colors: colors,
		units: units,
		my_group: my_group_idx	
	};
} 

function create_labels(paper, barchart, horiz, data, chart_margin, label_margin) {
	var set = paper.set(),
		covers = barchart.covers,
		bars = barchart.bars,
		n = covers.length;
		
	for(var i = 0; i < n; ++i) {
		// Left label
		var 
			bin = covers[i].getBBox(), // bin bounds
			bb, base,
			x, y;
		
		if( i == data.my_group ) {
			label = paper.text(bin.x + bin.width/2, bin.y + bin.height/2, "*");
		}
		if(horiz) {
			x = 0;
			y = bin.y + (bin.height / 2);
		} else {
			x = bin.x + (bin.width/2);
			y = bin.y + bin.height - label_margin;
		}
		label = paper.text(x, y, data.labels[i]);
		w =  label.getBBox().width;
		if(horiz) {
			label.attr('x', chart_margin - w - label_margin )
		} 
		set.push(label);
		
		// Value label on the right of the bar
		bb = bars[i].getBBox();
		if(horiz) {
			if(bb.width == 0) {
				x = bin.x + 5;
			} else {
				x = bb.x + bb.width + 5;
			}
		} else {
			if(bb.height == 0) {
				y = bin.height - label_margin;	
			} else {
				y = bb.y - label_margin;
			}
		}
		var text = data.values[i] + data.units;
		label = paper.text(x, y, text );
		set.push(label);
	}
	set.attr({'text-anchor': ((horiz) ? 'start' : 'middle')});
}
 
 
function syndrom_chart(container, data, health_status, last_health_status) {
	var margin_x = 220,
	label_margin_x = 5, // Margin between bar & labels
	paper, // Rapheal canvas 
	barchart,
	d;
	
	d = prepare_data(data, 'prop', last_health_status, health_status);
	
	paper = Raphael(container, 520, 210);
	barchart = paper.hbarchart(margin_x, 0, 250, 200, d.values, { 'colors':d.colors });
	console.log(barchart);
	create_labels(paper, barchart, true, d, margin_x, label_margin_x);
}

var months = ['Jan','Fev','Mar','Avr','Mai','Jun','Jui','Aou','Sep','Oct','Nov','Dec'];

function StoryRaphael(history, users) {
	var min = Number.MAX_VALUE; // Min timestamp
	var max = 0;	// Max timestamp
	var max_user_len = 0; // max length of username
	
	// Rebuild history by user, and extract stats
	var hh = { };
	var n = history.length;
	for(var i = 0; i < n; ++i) {
	  var h = history[i],
	   	  u = h.gid,
		  time = h.time;
	  if(typeof(hh[u]) == 'undefined') {
		hh[u] = [];
	  }
	  hh[u].push({time:time, status:h.syndrom});
	  min = (time < min) ? time : min;
	  max = (time > max) ? time : max;
	}
	this.history = hh;
	this.min_day = min;
	this.max_day = max;
	
	var i = 0;
	for(g in users) {
		var n = users[g].length;
		max_user_len = (n > max_user_len) ? n : max_user_len;
		++i;
	}
	this.nb_users = i;
	this.max_user_len = max_user_len;
	this.users = users;
}

$.extend(StoryRaphael.prototype, {
	options: {
		'cell_w': 33, // width of cell (date)
		'cell_h': 33, // height of cell (user)
		'em': 5, // Size of one character (to adjust user names width)
		'margin_left':5,
		'margin_bottom': 20 // Margin used to plot calendar date (date + month)
	},
	render: function(id, options) {
		
		options = options || {};
		
		$.extend(options, this.options);
		
		// Parameters
		var dh = options.cell_h, // Height by user
			dw = options.cell_w, // Width by day	
			nb_users = this.nb_users,
			nb_days = Math.ceil((this.max_day - this.min_day) / 86400), // Nb of days;
			hh = this.history,
			user_width = this.max_user_len * options.em + options.margin_left,
			height = (nb_users) * dh + options.margin_bottom,
			width = (nb_days + 1) * dw  + (user_width), // Width date cells + users names
			paper, base_x; 
		
		console.log(id, width, height);
		
		var paper = Raphael(id, width, height);
	 
		var base_x = 0;
		// draw grid
		for(var i = 0; i <= nb_days; ++i) {
			
			// Draw date lines
			x = base_x + dw * i;
			var path = "M"+ x + ",0" + "L"+x+","+height;
			var p = paper.path(path);
			p.attr("stroke","#EEE");
			
			// Dates
			var d = new Date();
			d.setTime( (this.min_day + (i * 86400)) * 1000);
			var a = {"font-size":"9px", "fill":"#AAA", 'stroke':'none' }; 
			x = x + Math.round(dw/2);
			var t = paper.text(x, height - 15, d.getDate() );
			t.attr(a);
			var t = paper.text(x, height - 5, months[d.getMonth()] );
			t.attr(a);
		}
		
		// Draw user lines and status
		var attr_text = { "font-size": "10px", "text-anchor": "start" };
		var attr_line = { "stroke": "#CCC", "stroke-width": 1};  
		var i = 0;
		for(gid in this.users) {
			var y = i * dh + Math.round(dh / 2);
			var u = this.users[gid];
			
			// User name
			var x = base_x + (nb_days + 1) * dw + 2;
			var t = paper.text(x, y, u);
			t.attr(attr_text);
			
			// User line
			var x = base_x;
			var l = (nb_days + 1) * dw;
			var p = paper.path("M" + (x) + "," + y + "L" + (x + l ) + "," + y);
			p.attr(attr_line);
			h = hh[gid]; // user history
			if(h) {
				// User history
				var n = h.length;
				for(var j = 0; j < n; ++j) {
					var r = h[j];
					var d = Math.floor((r.time - this.min_day)/ 86400);
					x = base_x + Math.round( d  * dw ); // center the circle
					var status = r.status;
					var diag = health_status[status];
					var img = paper.image('/media/syndrom/32/' + status + '.png', x, y - 16, 32, 32 );
					var date = new Date();
					date.setTime(r.time*1000);
					img.attr({'title': date.toLocaleDateString() + ' : ' + u + ', ' + diag});
				}
			}
			i = i + 1;
		}
		var e = $('#'+id);
		// Scroll to last date
		var w = e.attr('scrollWidth');
		if(typeof(w) != 'undefined') {
			e.scrollLeft(w);
		}
	}


});

 
 

