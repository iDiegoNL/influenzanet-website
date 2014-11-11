
$.tools.overlay.addEffect('custom', 
	function(pos, onLoad) {
		var conf = this.getConf(), w = $(window), o = this.getOverlay();				 
		if (!conf.fixed)  {
			pos.top += w.scrollTop();
			pos.left += w.scrollLeft();
		}
		if(isNaN(pos.left)) {
			// Correct left position if unknown.
			pos.left = (w.width() - $(o).width()) / 2;
		} 
		pos.position = conf.fixed ? 'fixed' : 'absolute';
		o.css(pos).fadeIn(conf.speed, onLoad); 
	}, function(onClose) {
		this.getOverlay().fadeOut(this.getConf().closeSpeed, onClose); 			
	}		
);		
