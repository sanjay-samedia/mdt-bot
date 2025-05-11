async function updateAnalytics() {
    const response = await fetch('/analytics/');
    const data = await response.json();
    document.getElementById('total-visits').textContent = data.total_visits;
    document.getElementById('success-rate').textContent = data.success_rate;
    document.getElementById('avg-stay-time').textContent = data.average_stay_time.toFixed(2);
    document.getElementById('success-count').textContent = data.success_count;
    document.getElementById('failure-count').textContent = data.failure_count;
}
setInterval(updateAnalytics, 5000); // Update every 5 seconds