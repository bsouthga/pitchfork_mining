var bot = require('nodemw');

// pass configuration object
var client = new bot({
  server: 'en.wikipedia.org',  // host name of MediaWiki-powered site
  path: '/w',                  // path to api.php script
  debug: false                 // is more verbose when set to true
});



function info(bandname, callback) {

  client.getArticle(bandname, function(err, data) {
    // error handling
    if (err) {
      console.error(err);
      return;
    }

    if (data.match(/#REDIRECT/)) {
      info(
        data.match(/\[\[[a-zA-Z0-9_]+\]\]/)[0]
            .match(/[a-zA-Z0-9_]+/)[0],
        callback
      )
    } 

    if (data.match(/Infobox musical artist/)) {
      origin = data.match(/.*origin =.*/g)[0]
                   .split('origin =')[1]
                   .replace(/[^A-Za-z0-9]/g, ' ');
      console.log(origin)
    }

    // ...
  });

}



info('tycho (musician)')

module.exports = info;