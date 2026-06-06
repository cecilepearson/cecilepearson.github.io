/* Accessible lightbox for the WORKS gallery.
   Progressive enhancement: without JS, each thumbnail is a link straight to the
   full-size image. With JS, clicks open a native <dialog> viewer (focus trap,
   Esc, and focus restore are handled by the browser via showModal()). */
(function () {
  "use strict";
  var gallery = document.querySelector(".gallery");
  if (!gallery) return;
  var links = Array.prototype.slice.call(gallery.querySelectorAll("a.work__media"));
  if (!links.length || typeof HTMLDialogElement === "undefined") return;

  function arrow(dir) {
    var d = dir === "left" ? "M15 18l-6-6 6-6" : "M9 6l6 6-6 6";
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="' + d + '"/></svg>';
  }
  var closeIcon =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>';

  var dlg = document.createElement("dialog");
  dlg.className = "lightbox";
  dlg.setAttribute("aria-label", "Artwork viewer");
  dlg.innerHTML =
    '<button class="lightbox__close" type="button" aria-label="Close viewer">' + closeIcon + "</button>" +
    '<button class="lightbox__btn lightbox__prev" type="button" aria-label="Previous work">' + arrow("left") + "</button>" +
    '<button class="lightbox__btn lightbox__next" type="button" aria-label="Next work">' + arrow("right") + "</button>" +
    '<div class="lightbox__stage"><img class="lightbox__img" alt=""></div>' +
    '<figcaption class="lightbox__cap"><span class="t"></span><span class="m"></span></figcaption>';
  document.body.appendChild(dlg);

  var imgEl = dlg.querySelector(".lightbox__img");
  var tEl = dlg.querySelector(".lightbox__cap .t");
  var mEl = dlg.querySelector(".lightbox__cap .m");
  var current = 0;

  function preload(i) {
    var a = links[(i + links.length) % links.length];
    if (a) { var im = new Image(); im.src = a.getAttribute("href"); }
  }
  function show(i) {
    current = (i + links.length) % links.length;
    var a = links[current];
    imgEl.src = a.getAttribute("href");
    var title = a.getAttribute("data-title") || "";
    imgEl.alt = title;
    tEl.textContent = title;
    mEl.textContent = a.getAttribute("data-meta") || "";
    preload(current + 1);
    preload(current - 1);
  }
  function open(i) { show(i); if (!dlg.open) dlg.showModal(); }
  function close() { if (dlg.open) dlg.close(); }

  links.forEach(function (a, i) {
    a.addEventListener("click", function (e) { e.preventDefault(); open(i); });
  });
  dlg.querySelector(".lightbox__prev").addEventListener("click", function () { show(current - 1); });
  dlg.querySelector(".lightbox__next").addEventListener("click", function () { show(current + 1); });
  dlg.querySelector(".lightbox__close").addEventListener("click", close);

  dlg.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { e.preventDefault(); show(current + 1); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); show(current - 1); }
  });

  // Click on the backdrop or the empty stage closes; clicking the image does not.
  dlg.addEventListener("click", function (e) {
    if (e.target === dlg || e.target.classList.contains("lightbox__stage")) close();
  });

  // Touch swipe.
  var x0 = null;
  dlg.addEventListener("pointerdown", function (e) { x0 = e.clientX; });
  dlg.addEventListener("pointerup", function (e) {
    if (x0 === null) return;
    var dx = e.clientX - x0;
    x0 = null;
    if (Math.abs(dx) > 50) { if (dx < 0) { show(current + 1); } else { show(current - 1); } }
  });
})();
