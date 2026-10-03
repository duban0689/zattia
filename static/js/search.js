// Small UX convenience: press "/" anywhere on the page to jump into the
// search box, unless the user is already typing in a field.
document.addEventListener("keydown", (event) => {
  if (event.key !== "/") return;
  const tag = document.activeElement?.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA") return;
  const input = document.querySelector('.search-bar input[name="q"]');
  if (input) {
    event.preventDefault();
    input.focus();
  }
});
