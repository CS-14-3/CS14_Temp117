(function () {
  const root = document.querySelector("[data-register-root]");

  if (!root) {
    return;
  }

  const form = document.getElementById("researcher-register-form");
  const isFilePage = window.location.protocol === "file:";
  const accountStorageKey = "surveyLabResearcherAccount";

  const navigate = (path, filePath) => {
    const target = isFilePage && filePath ? filePath : path;

    if (target) {
      window.location.href = target;
    }
  };

  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const username = form.elements.username.value.trim();
      const password = form.elements.password.value;

      if (!username || !password) {
        alert("Please enter a username and password.");
        return;
      }

      localStorage.setItem(
        accountStorageKey,
        JSON.stringify({
          username,
          password
        })
      );

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
