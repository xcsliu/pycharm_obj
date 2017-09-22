var system = require('system');
var args = system.args;
var span = parseInt(args[1])
var html = args[2]
var png = args[3]
var page = require('webpage').create();
page.viewportSize = {width: span, height: span};
page.clipRect = {top: 0, left: 0, width: span, height: span};
page.open(html, function(status) {
    if (status !== 'success') {
        console.log('Unable to load the address!');
        phantom.exit();
    } else {
        window.setTimeout(function () {
            page.render(png);
            phantom.exit();
        }, 50);
    }
});