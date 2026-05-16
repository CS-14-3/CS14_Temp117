(function () {
  const root = document.querySelector("[data-login-root]");

  if (!root) {
    return;
  }

  const form = document.getElementById("researcher-login-form");
  const passwordInput = root.querySelector("[data-password-input]");
  const passwordToggle = root.querySelector("[data-password-toggle]");
  const eyeOpen = root.querySelector("[data-eye-open]");
  const eyeClosed = root.querySelector("[data-eye-closed]");
  const accountStorageKey = "surveyLabResearcherAccount";
  const sessionStorageKey = "surveyLabResearcherSession";

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

  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const username = form.elements.username.value.trim();
      const password = form.elements.password.value;
      const storedAccount = localStorage.getItem(accountStorageKey);
      let account = null;

      if (storedAccount) {
        try {
          account = JSON.parse(storedAccount);
        } catch (error) {
          account = null;
        }
      }

      if (!username || !password) {
        alert("Please enter your username and password.");
        return;
      }

      if (!account) {
        alert("No researcher account found. Please sign up first.");
        return;
      }

      if (username !== account.username || password !== account.password) {
        alert("Incorrect username or password.");
        return;
      }

      localStorage.setItem(
        sessionStorageKey,
        JSON.stringify({
          username,
          loggedInAt: new Date().toISOString()
        })
      );

      navigate(root.dataset.loginSuccess, root.dataset.fileLoginSuccess);
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
