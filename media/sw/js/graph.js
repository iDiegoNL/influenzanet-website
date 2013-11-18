
 
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



function household_chart(container, data, my_group) {
	var margin_y = 20,
	label_margin_y = 5, // Margin between bar & labels
	paper, // Rapheal canvas 
	barchart,
	d; 
	d = prepare_data(data,'prop', my_group, false);
	paper = Raphael(container, 480, 220);
	barchart = paper.barchart(0, 0, 480, 180, d.values, { 'colors':d.colors });
	create_labels(paper, barchart, false, d,  margin_y, label_margin_y);
}

 
 

