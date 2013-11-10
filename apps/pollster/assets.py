from webassets import Bundle

js_pollster_run = Bundle(
    'pollster/wok/js/wok.pollster.js',
    'pollster/wok/js/wok.pollster.datatypes.js',
    'pollster/wok/js/wok.pollster.codeselect.js',
    'pollster/wok/js/wok.pollster.timeelapsed.js',
    'pollster/wok/js/wok.pollster.rules.js',
    'pollster/wok/js/wok.pollster.virtualoptions.js',
    'pollster/wok/js/wok.pollster.init.js',
    'pollster/wok/js/wok.pollster.lastyear.js',
  output='assets/pollster_run.js'
)