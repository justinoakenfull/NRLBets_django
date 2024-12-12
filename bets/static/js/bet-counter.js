function resetAndAnimateCounters() {
    const counters = document.querySelectorAll('.count-up');
    counters.forEach(counter => {
        counter.innerText = '0'; // Reset counter text
        const updateCounter = () => {
            const target = +counter.getAttribute('data-value');
            const count = +counter.innerText;
            const increment = target / 50;

            if (count < target) {
                counter.innerText = Math.min(count + increment, target).toFixed(2);
                setTimeout(updateCounter, 10);
            } else {
                counter.innerText = target.toFixed(2);
            }
        };
        updateCounter();
    });
}

document.addEventListener('DOMContentLoaded', () => {
    resetAndAnimateCounters();

    // Ensure counters reanimate when switching tabs
    const tabs = document.querySelectorAll('[data-bs-toggle="pill"]');
    tabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', () => {
            setTimeout(resetAndAnimateCounters, 0); // Add a small delay for content visibility
        });
    });
});