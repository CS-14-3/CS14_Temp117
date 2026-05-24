(function () {
  const root = document.querySelector("[data-register-root]");

  if (!root) {
    return;
  }

  const isFilePage = window.location.protocol === "file:";

  const navigate = (path, filePath) => {
    const target = isFilePage && filePath ? filePath : path;

    if (target) {
      window.location.href = target;
    }
  };

  root.querySelectorAll("[data-route]").forEach(function (button) {
    button.addEventListener("click", function () {
      navigate(
        button.getAttribute("data-route"),
        button.getAttribute("data-file-route")
      );
    });
  });
})();
