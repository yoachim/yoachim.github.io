/*!
 * Entourage 1.1.1 - Automatic Download Tracking for Asynchronous Google Analytics
 *
 * Copyright (c) 2011 by Tian Valdemar Davis (http://techoctave.com/c7)
 * Licensed under the MIT (http://en.wikipedia.org/wiki/MIT_License) license.
 *
 * Learn More: http://techoctave.com/c7/posts/58-entourage-js-automatic-download-tracking-for-asynchronous-google-analytics
 */
(function(){var a=new (function(){var c="1.1.1";var e=function(f){f=f.substring(0,(f.indexOf("#")==-1)?f.length:f.indexOf("#"));f=f.substring(0,(f.indexOf("?")==-1)?f.length:f.indexOf("?"));if(f.indexOf("http")==-1){f=f.substring(f.indexOf("/"),f.length)}else{f=f.substring(f.indexOf("/")+1,f.length);f=f.substring(f.indexOf("/")+1,f.length);f=f.substring(f.indexOf("/"),f.length)}return f};var d=function(){var g,i,f,j,h;g=/\.pdf$|\.zip$|\.rdf*|\.csv$|\.doc*|\.xls*|\.xml$|\.ppt*/i;i=this.pathname;f=i.match(g);if(typeof f!=="undefined"&&f!==null){j=e(i);h=j;_gaq.push(["_trackPageview",h])}};var b=function(){var g=document.links;for(var h=0,f=g.length;h<f;h++){g[h].onmouseup=d}};return{version:c,initialize:b}})();window.entourage=a;window.onload=a.initialize})();