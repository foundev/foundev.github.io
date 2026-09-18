(function () {
  var root = document.documentElement;
  var toggle = document.getElementById("theme-toggle");
  var stored = null;

  try {
    stored = localStorage.getItem("theme");
  } catch (e) {}

  function preferred() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  function active() {
    return stored || root.dataset.theme || preferred();
  }

  function label(theme) {
    if (!toggle) return;
    toggle.setAttribute("aria-label", theme === "dark" ? "Switch to light theme" : "Switch to dark theme");
    toggle.setAttribute("title", theme === "dark" ? "Switch to light theme" : "Switch to dark theme");
  }

  label(active());

  if (toggle) {
    toggle.addEventListener("click", function () {
      stored = active() === "dark" ? "light" : "dark";
      root.dataset.theme = stored;
      try {
        localStorage.setItem("theme", stored);
      } catch (e) {}
      label(stored);
    });
  }

  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
      label(active());
    });
  }

  // Copy button per code block. Plain DOM, no dependencies.
  document.querySelectorAll(".post-body pre").forEach(function (pre) {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "copy-button";
    button.textContent = "Copy";
    button.setAttribute("aria-label", "Copy code to clipboard");

    button.addEventListener("click", function () {
      var code = pre.querySelector("code");
      var text = (code || pre).innerText;

      function done(message) {
        button.textContent = message;
        window.setTimeout(function () {
          button.textContent = "Copy";
        }, 1600);
      }

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(
          function () {
            done("Copied");
          },
          function () {
            done("Press ⌘C");
          }
        );
      } else {
        done("Press ⌘C");
      }
    });

    pre.appendChild(button);
  });
})();
