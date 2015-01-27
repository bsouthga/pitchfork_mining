
// Bring in the eyeQ module from NPM
var eyeq = require("eyeq"),
    login = require("./gracenote-login.js");

// Pass in an Account ID, which you can generate 
// from the Gracenote Developer Portal
eyeq.register(login.clientId, function(response) {
  console.log(response)
}); 

eyeq.search("the big lobowski", function(response) {
  console.log(response)
})

// var  _ = require('lodash-node'),
//     wikipedia = require("wtf_wikipedia"),
//     fs = require('fs');


// var data = JSON.parse(
//       fs.readFileSync('../data/pitchfork.json', 'utf-8')
//     );

// var collected = {};

// var files = fs.readdirSync('../data/artists/')

// files.forEach(function(f) {
//   if (!f.match(/\.json$/)) return null;
//   var df = JSON.parse(
//     fs.readFileSync('../data/artists/' + f, 'utf-8') || "{}"
//   );
//   collected[df.__artist] = true;
// })


// console.log(_.keys(collected).length)


// var artists = _.chain(data)
//   .map(function(value, key) {
//     return value.artist;
//   })
//   .filter(function(artist) {
//     return typeof artist === "string";
//   })
//   .unique()
//   .__wrapped__;


// console.log(artists.length)

// artists.forEach(function(artist) {
//     if (!collected[artist]) {
//       getArticle(artist, function(page) {
//         console.log('collected : ' + artist);
//         page.__artist = artist;
//         fs.writeFile(
//           '../data/artists/' + artist.replace(/\W/g, 'X') +'.json', 
//           JSON.stringify(page || {})
//         );
//       });
//     }
//   });





// function getArticle(query, callback) {

//   wikipedia.from_api(query, function(markup){
//     var page = wikipedia.parse(markup)
//     callback(page);
//   })

// }


// function getArtist(name, callback) {

//   getArticle(name, function(page) {
//     if (page.type == 'disambiguation') {
//       var name = page.pages.filter(function(p) {
//         return (typeof p === "string") && p.match(/\(musician\)|\(band\)/g);
//       })[0];
//       getArtist(name, callback)
//     } else if (page.type == 'redirect') {
//       getArtist(page.redirect, callback)
//     } else {
//       callback(page)
//     }
//   })

// }






