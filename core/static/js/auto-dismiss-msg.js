const timeout = 3000; // 3 seconds
setTimeout(function () {
    let alert = document.querySelector('.alert');
    if (alert) {
        alert.classList.remove('show');
        alert.classList.add('fade');
        setTimeout(() => alert.remove(), 150);
    }
}, timeout);