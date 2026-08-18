// Cart Interactivity

function addToCartAjax(foodId) {
    fetch(`/cart/add/${foodId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            const badge = document.querySelector('.cart-count');
            if (badge) {
                badge.textContent = data.cart_count;
            }
            showToast(data.message || 'Item added to cart!');
        }
    })
    .catch(err => console.error('Cart error:', err));
}

function showToast(msg) {
    const toast = document.createElement('div');
    toast.className = 'alert alert-success';
    toast.style.position = 'fixed';
    toast.style.bottom = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}
