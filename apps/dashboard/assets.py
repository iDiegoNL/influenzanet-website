from webassets import Bundle

js_raphael = Bundle(
    "sw/js/raphael/raphael-min.js",
    "sw/js/raphael/g.raphael-min.js",
    "sw/js/raphael/g.bar-min.js", 
    output='assets/raphael.js'
)

