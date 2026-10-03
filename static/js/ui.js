// Toast auto-dismiss for messages rendered server-side via Django messages.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".toast-msg").forEach((el) => {
    setTimeout(() => {
      el.style.transition = "opacity .25s ease";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 250);
    }, 3200);
  });
});

function zattiaToast(message, kind = "info") {
  let stack = document.getElementById("toast-stack");
  if (!stack) {
    stack = document.createElement("div");
    stack.id = "toast-stack";
    stack.className = "toast-stack";
    document.body.appendChild(stack);
  }
  const el = document.createElement("div");
  el.className = `toast-msg toast-${kind}`;
  el.setAttribute("role", "status");
  el.textContent = message;
  stack.appendChild(el);
  setTimeout(() => {
    el.style.transition = "opacity .25s ease";
    el.style.opacity = "0";
    setTimeout(() => el.remove(), 250);
  }, 3200);
}
