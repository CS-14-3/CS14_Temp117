(function () {
  const root = document.querySelector("[data-login-root]");

  if (!root) {
    return;
  }

  const passwordInput = root.querySelector("[data-password-input]");
  const passwordToggle = root.querySelector("[data-password-toggle]");
  const eyeOpen = root.querySelector("[data-eye-open]");
  const eyeClosed = root.querySelector("[data-eye-closed]");

  const navigate = (path, filePath) => {
    const target =
      window.location.protocol === "file:" && filePath ? filePath : path;

    if (target) {
      window.location.href = target;
    }
  };

  if (passwordInput && passwordToggle) {
    passwordToggle.addEventListener("click", function () {
      const nextType =
        passwordInput.getAttribute("type") === "password" ? "text" : "password";
      const isVisible = nextType === "text";

      passwordInput.setAttribute("type", nextType);
      passwordToggle.setAttribute(
        "aria-label",
        isVisible ? "Hide password" : "Show password"
      );
      passwordToggle.setAttribute("aria-pressed", String(isVisible));

      if (eyeOpen) {
        eyeOpen.hidden = isVisible;
      }

      if (eyeClosed) {
        eyeClosed.hidden = !isVisible;
      }
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
