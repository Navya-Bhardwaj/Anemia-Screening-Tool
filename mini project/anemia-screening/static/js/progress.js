document.addEventListener('DOMContentLoaded', function() {
    const chartCanvas = document.getElementById('progressChart');
    if (chartCanvas) {
        // Get data from a global variable set by Jinja
        const resultsData = window.chartResults || [];
        if (resultsData.length > 0) {
            const ctx = chartCanvas.getContext('2d');

            const chartData = {
                labels: resultsData.map(r => new Date(r.date).toLocaleDateString()),
                datasets: [{
                    label: 'Brightness Level',
                    data: resultsData.map(r => r.brightness),
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            };

            const config = {
                type: 'line',
                data: chartData,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Anemia Risk Trend (Brightness Levels Over Time)',
                            font: {
                                size: 16
                            }
                        },
                        legend: {
                            display: true
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            title: {
                                display: true,
                                text: 'Brightness Level'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        }
                    }
                }
            };

            new Chart(ctx, config);
        }
    }
});
