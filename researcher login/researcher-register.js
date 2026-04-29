(function () {
  const root = document.querySelector("[data-register-root]");

  if (!root) {
    return;
  }

  const form = document.getElementById("researcher-register-form");
  const isFilePage = window.location.protocol === "file:";

  const navigate = (path, filePath) => {
    const target = isFilePage && filePath ? filePath : path;

    if (target) {
      window.location.href = target;
    }
  };

  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      alert("Account created. Please log in.");
      navigate(root.dataset.loginRoute, root.dataset.fileLoginRoute);
    });
  }

  root.querySelectorAll("[data-route]").forEach(function (button) {
    button.addEventListener("click", function () {
      navigate(
        button.getAttribute("data-route"),
        button.getAttribute("data-file-route")
      );
    });
  });
})();
