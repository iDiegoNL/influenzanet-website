
window.wok.pollster.onCreate = []; 

$(function(){
	window.wok.pollster_runtime = wok.pollster.createPollsterRuntime(null, {});
	var n = window.wok.pollster.onCreate.length;
	if(n) {
		for(var i=0; i < n; ++i) {
			var callback = window.wok.pollster.onCreate[i];
			callback.call(window.wok.pollster_runtime); 
		}
	} 
});
