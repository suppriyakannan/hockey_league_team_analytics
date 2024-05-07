document.addEventListener('DOMContentLoaded', function () {
    fetchDataAndRenderCharts();
});

function fetchDataAndRenderCharts() {
    fetchChartData('/api/goals/', renderGoalChart);
    fetchChartData('/api/possession/', renderPossessionChart);
    fetchChartData('/api/cards/', renderCardChart);
    fetchChartData('/api/circle/', data => {
        fetch('/api/shots/')
            .then(response => response.json())
            .then(shotsData => renderCircleChart(data, shotsData))
            .catch(error => console.error('Error fetching shots data:', error));
    });
    fetchChartData('/api/penalty/', renderPenaltyChart);
}

function fetchChartData(url, renderFunction) {
    fetch(url)
        .then(response => response.json())
        .then(data => renderFunction(data))
        .catch(error => console.error('Error fetching data:', error));
}

function getTeamPattern(teamName) {
    const colorMap = {
        'White Warriorz': 'cross',
        'Blue Blazerz': 'dash',
        'Green Griffinz': 'zigzag',
        'Yellow Yakz': 'dot',
        'Violet Whalez': 'plus',
        'Red Ruffianz': 'diagonal'
    };
    return Patternomaly.draw(colorMap[teamName] || 'cross', getTeamColor(teamName));
}

function getTeamColor(teamName) {
    const colorName = teamName.split(' ')[0].toLowerCase();
    const colorMap = {
        white: 'rgba(245, 245, 245, 0.8)',
        blue: 'rgba(173, 216, 230, 0.8)',
        green: 'rgba(144, 238, 144, 0.8)',
        yellow: 'rgba(255, 255, 224, 0.8)',
        violet: 'rgba(238, 130, 238, 0.8)',
        red: 'rgba(255, 99, 132, 0.8)'
    };
    return colorMap[colorName];
}

function renderGoalChart(data) {
    const ctx = document.getElementById('goalChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => `Match ${item.match_number}`),
            datasets: [{
                label: 'Team 1 Total Goals',
                data: data.map(item => item.team1_FG + item.team1_PG),
                backgroundColor: data.map(item => getTeamPattern(item.team1_name))
            }, {
                label: 'Team 2 Total Goals',
                data: data.map(item => item.team2_FG + item.team2_PG),
                backgroundColor: data.map(item => getTeamPattern(item.team2_name))
            }]
        },
        options: {
            scales: {
                x: { stacked: false },
                y: { stacked: false }
            }
        }
    });
}

function renderPossessionChart(data) {
    const ctx = document.getElementById('possessionChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(item => `Match ${item.match_number}`),
            datasets: [{
                label: 'Team 1 Possession %',
                data: data.map(item => item.team1_possession_percentage),
                borderColor: getTeamColor(data[0].team1_name),
                backgroundColor: Patternomaly.draw('dot', getTeamColor(data[0].team1_name)),
                fill: true
            }, {
                label: 'Team 2 Possession %',
                data: data.map(item => item.team2_possession_percentage),
                borderColor: getTeamColor(data[0].team2_name),
                backgroundColor: Patternomaly.draw('dot', getTeamColor(data[0].team2_name)),
                fill: true
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function renderCardChart(data) {
    const ctx = document.getElementById('cardChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => `Match ${item.match_number}`),
            datasets: [{
                label: 'Team 1 Total Cards',
                data: data.map(item => item.team1_gy + item.team1_r),
                backgroundColor: data.map(item => getTeamPattern(item.team1_name))
            }, {
                label: 'Team 2 Total Cards',
                data: data.map(item => item.team2_gy + item.team2_r),
                backgroundColor: data.map(item => getTeamPattern(item.team2_name))
            }]
        },
        options: {
            scales: {
                x: { stacked: false },
                y: { stacked: false }
            }
        }
    });
}

function renderCircleChart(data, shotsData) {
    const ctx = document.getElementById('circleChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => `Match ${item.match_number}`),
            datasets: [{
                label: 'Team 1 Circle Penetration + Shots',
                data: data.map((item, index) => item.team1_circle + shotsData[index].team1_shots),
                backgroundColor: data.map(item => getTeamPattern(item.team1_name))
            }, {
                label: 'Team 2 Circle Penetration + Shots',
                data: data.map((item, index) => item.team2_circle + shotsData[index].team2_shots),
                backgroundColor: data.map(item => getTeamPattern(item.team2_name))
            }]
        },
        options: {
            scales: {
                x: { stacked: false },
                y: { stacked: false }
            }
        }
    });
}

function renderPenaltyChart(data) {
    const ctx = document.getElementById('penaltyChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => `Match ${item.match_number}`),
            datasets: [{
                label: 'Team 1 Penalty Corners',
                data: data.map(item => item.team1_pc),
                backgroundColor: data.map(item => getTeamPattern(item.team1_name)),
                stack: 'Penalty Corner'
            }, {
                label: 'Team 2 Penalty Corners',
                data: data.map(item => item.team2_pc),
                backgroundColor: data.map(item => getTeamPattern(item.team2_name)),
                stack: 'Penalty Corner'
            }, {
                label: 'Team 1 Penalty Strokes',
                data: data.map(item => item.team1_ps),
                backgroundColor: data.map(item => getTeamPattern(item.team1_name)),
                stack: 'Penalty Stroke'
            }, {
                label: 'Team 2 Penalty Strokes',
                data: data.map(item => item.team2_ps),
                backgroundColor: data.map(item => getTeamPattern(item.team2_name)),
                stack: 'Penalty Stroke'
            }]
        },
        options: {
            scales: {
                x: { stacked: true },
                y: { stacked: true }
            }
        }
    });
}
