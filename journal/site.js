/* Palette and light/dark controls for journal pages. The choice is shared with the home page. */
(function () {
  var root = document.documentElement;
  var PALETTES = ["tide","moss","ember","plum","clay","ink"];
  var THEME_COLORS = {
    tide:{dark:"#0f1923",light:"#f6f9fc"}, moss:{dark:"#0f1a16",light:"#f5faf7"},
    ember:{dark:"#1a1310",light:"#fdf8f4"}, plum:{dark:"#16121f",light:"#faf8fd"},
    clay:{dark:"#1c1315",light:"#fdf7f8"}, ink:{dark:"#121416",light:"#f7f8f9"}
  };
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function sync() {
    var set = THEME_COLORS[root.dataset.palette] || THEME_COLORS.tide;
    var meta = document.getElementById("themeColorMeta");
    if (meta) meta.setAttribute("content", set[root.dataset.theme] || set.dark);
    document.querySelectorAll(".swatch").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.palette === root.dataset.palette));
    });
    var t = document.getElementById("modeToggle");
    if (t) {
      var dark = root.dataset.theme === "dark";
      t.setAttribute("aria-pressed", String(dark));
      t.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
      document.getElementById("modeLabel").textContent = dark ? "Dark" : "Light";
    }
  }
  document.querySelectorAll(".swatch").forEach(function (b) {
    b.addEventListener("click", function () {
      if (PALETTES.indexOf(b.dataset.palette) < 0) return;
      root.dataset.palette = b.dataset.palette; store("j2m-palette", b.dataset.palette); sync();
    });
  });
  var toggle = document.getElementById("modeToggle");
  if (toggle) toggle.addEventListener("click", function () {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    store("j2m-theme", root.dataset.theme); sync();
  });
  sync();
})();
