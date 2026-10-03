// AJAX enhancement for the cart forms (add / remove / update quantity).
// Progressive enhancement: every form here works fine as a plain POST with
// a full page reload too (the server returns a redirect for non-AJAX
// requests), this just makes it feel instant when JS is available.

function getCookie(name) {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
}

function updateCartBadge(count) {
  const badge = document.getElementById("cart-badge");
  if (!badge) return;
  badge.textContent = count;
  badge.classList.toggle("d-none", !count);
}

async function postCartForm(form) {
  const response = await fetch(form.action, {
    method: "POST",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: new FormData(form),
  });
  if (!response.ok) {
    zattiaToast("Ocurrió un error, intenta de nuevo.", "error");
    return null;
  }
  return response.json();
}

document.addEventListener("submit", async (event) => {
  const form = event.target;

  if (form.matches(".js-add-to-cart-form")) {
    event.preventDefault();
    const data = await postCartForm(form);
    if (data) {
      updateCartBadge(data.cart_count);
      zattiaToast(data.message || "Producto agregado al carrito.");
    }
  }

  if (form.matches(".js-remove-form")) {
    event.preventDefault();
    const data = await postCartForm(form);
    if (data) {
      updateCartBadge(data.cart_count);
      const row = form.closest(".cart-item");
      if (row) row.remove();
      zattiaToast(data.message || "Producto eliminado.");
      if (data.cart_count === 0) {
        setTimeout(() => window.location.reload(), 600);
      }
    }
  }

  if (form.matches(".js-update-quantity-form")) {
    event.preventDefault();
    const data = await postCartForm(form);
    if (data) {
      updateCartBadge(data.cart_count);
      zattiaToast("Carrito actualizado.");
    }
  }
});
