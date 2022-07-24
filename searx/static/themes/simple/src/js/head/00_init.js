/* SPDX-License-Identifier: AGPL-3.0-or-later */
(function (w, d) {
  "use strict";

  // add data- properties
  var script =
    d.currentScript ||
    (function () {
      var scripts = d.getElementsByTagName("script");
      return scripts[scripts.length - 1];
    })();

  w.searxng = {
    settings: JSON.parse(atob(script.getAttribute("client_settings"))),
  };

  // update the css
  var hmtlElement = d.getElementsByTagName("html")[0];
  hmtlElement.classList.remove("no-js");
  hmtlElement.classList.add("js");

  var offlineBrowsingEnabled = w.searxng.settings["offline_browsing"];

  // enable service worker
  if ("serviceWorker" in navigator) {
    if (offlineBrowsingEnabled) {
      navigator.serviceWorker
        .register("/sw.js", { scope: "/" })
        .then(function (registration) {
          registration.update();
        })
        .catch(function (error) {
          console.log(`Service Worker registration failed with ${error}`);
        });
    } else {
      navigator.serviceWorker.getRegistrations().then(function (registrations) {
        for (let registration of registrations) {
          if (registration.active) {
            registration.active.postMessage('unregister');
          } else {
            registration.unregister();
          }
        }
      });
    }
  }
})(window, document);
