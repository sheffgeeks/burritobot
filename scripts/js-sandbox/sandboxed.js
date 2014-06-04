#!/usr/bin/env node

var Sandbox = require('sandbox');

Sandbox.options.timeout = 2000;
Sandbox.options.api = 'api';

var s = new Sandbox();

process.stdin.resume();
process.stdin.setEncoding('utf8');
var incoming = '';
process.stdin.on('data', function(data) {
    incoming += data
});
process.stdin.on('end', function() {
    s.run(incoming.toString(), function (output) {
        if (output.console.length) {
          console.log(output.console.join('\n'));
        }
        console.log(output.result);
    });
});
