// Entry point: small, framework-free glue code. Nothing here turns the
// site into a SPA — Django still renders every page; this just makes
// interactions (cart, toasts) feel instant without a full reload.
document.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("js-ready");
});
