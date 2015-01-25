// combine individual pages into one json file

var _ = require('lodash-node'),
    fs = require('fs');

fs.readdir('../data/', function(err, files){
  var full = {};
  files.filter(function(f) {return f.match(/.json$/)})
    .forEach(function(f) {
      var d = JSON.parse(fs.readFileSync('../data/' + f, "utf8"));
      _.forEach(d, function(value, key) {
        full[key] = value;
      })
    })
  fs.writeFile('../data/pitchfork.json', JSON.stringify(full));
})

