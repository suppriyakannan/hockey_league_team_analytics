document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM fully loaded and parsed");
    fetchDataAndRenderCharts();
    drawLegendPatterns();
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

// Define a mapping between team names and their patterns
const teamPatterns = {
    "White Warriorz": 'zigzag',
    "Blue Blazerz": 'dots',
    "Green Griffinz": 'dash',
    "Yellow Yakz": 'cross',
    "Red Ruffianz": 'plus',
    "Violet Whalez": 'x'
};

function generatePattern(pattern, patternColor, teamColor) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 30; // Increased size for better visibility
    canvas.height = 30; // Increased size for better visibility

    switch (pattern) {
        case 'dots':
            for (let x = 0; x < canvas.width; x += 8) {
                for (let y = 0; y < canvas.height; y += 8) {
                    ctx.fillStyle = patternColor;
                    ctx.fillRect(x, y, 2, 2); // Reduced dot size
                }
            }
            break;
        case 'zigzag':
            ctx.strokeStyle = patternColor;
            ctx.lineWidth = 1; // Reduced line width for better visibility
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(canvas.width, canvas.height);
            ctx.stroke();
            break;
        case 'dash':
            ctx.strokeStyle = patternColor;
            ctx.lineWidth = 1; // Reduced line width for better visibility
            ctx.beginPath();
            ctx.moveTo(0, 15);
            ctx.lineTo(30, 15);
            ctx.stroke();
            break;
        case 'cross':
            ctx.strokeStyle = patternColor;
            ctx.lineWidth = 1; // Reduced line width for better visibility
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(30, 30);
            ctx.moveTo(0, 30);
            ctx.lineTo(30, 0);
            ctx.stroke();
            break;
        case 'plus':
            ctx.strokeStyle = patternColor;
            ctx.lineWidth = 1; // Reduced line width for better visibility
            ctx.beginPath();
            ctx.moveTo(0, 15);
            ctx.lineTo(30, 15);
            ctx.moveTo(15, 0);
            ctx.lineTo(15, 30);
            ctx.stroke();
            break;
        case 'x':
            ctx.strokeStyle = patternColor;
            ctx.lineWidth = 1; // Reduced line width for better visibility
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(30, 30);
            ctx.moveTo(30, 0);
            ctx.lineTo(0, 30);
            ctx.stroke();
            break;
        default:
            // For unsupported patterns, default to solid color with reduced opacity
            ctx.fillStyle = patternColor;
            ctx.globalAlpha = 0.2; // Reduced opacity for better visibility
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            return ctx.createPattern(canvas, 'repeat');
    }

    ctx.fillStyle = teamColor;
    ctx.globalCompositeOperation = 'destination-over';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    return ctx.createPattern(canvas, 'repeat');
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
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                fill: true
            }, {
                label: 'Team 2 Possession %',
                data: data.map(item => item.team2_possession_percentage),
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
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

function renderGoalChart(data) {
    const ctx = document.getElementById('goalChart').getContext('2d');
    const team1DefaultColor = 'rgba(0, 102, 204, 0.5)'; // Dark blue color for Team 1
    const team2DefaultColor = 'rgba(204, 0, 0, 0.5)'; // Dark red color for Team 2
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => `Match ${item.match_number}`),
            datasets: [{
                label: 'Team 1 Total Goals',
                data: data.map(item => item.team1_FG + item.team1_PG),
                backgroundColor: data.map(item => {
                    const teamPattern = teamPatterns[item.team1_name];
                    const patternColor = team1DefaultColor; // Darker shade of background color
                    const defaultColor = team1DefaultColor; // Default background color for Team 1
                    const pattern = teamPattern ? generatePattern(teamPattern, patternColor, defaultColor) : null;
                    return pattern ? pattern : defaultColor;
                })
            }, {
                label: 'Team 2 Total Goals',
                data: data.map(item => item.team2_FG + item.team2_PG),
                backgroundColor: data.map(item => {
                    const teamPattern = teamPatterns[item.team2_name];
                    const patternColor = team2DefaultColor; // Darker shade of background color
                    const defaultColor = team2DefaultColor; // Default background color for Team 2
                    const pattern = teamPattern ? generatePattern(teamPattern, patternColor, defaultColor) : null;
                    return pattern ? pattern : defaultColor;
                })
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


function renderCardChart(data) {
    const ctx = document.getElementById('cardChart').getContext('2d');
    const team1DefaultColor = 'rgba(0, 153, 0, 0.5)'; // Dark green color for Team 1
    const team2DefaultColor = 'rgba(204, 102, 0, 0.5)'; // Dark orange color for Team 2
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => `Match ${item.match_number}`),
            datasets: [{
                label: 'Team 1 Total Cards',
                data: data.map(item => item.team1_gy + item.team1_r),
                backgroundColor: data.map(item => {
                    const teamPattern = teamPatterns[item.team1_name];
                    const patternColor = team1DefaultColor; // Darker shade of background color
                    const defaultColor = team1DefaultColor; // Default background color for Team 1
                    const pattern = teamPattern ? generatePattern(teamPattern, patternColor, defaultColor) : null;
                    return pattern ? pattern : defaultColor;
                })
            }, {
                label: 'Team 2 Total Cards',
                data: data.map(item => item.team2_gy + item.team2_r),
                backgroundColor: data.map(item => {
                    const teamPattern = teamPatterns[item.team2_name];
                    const patternColor = team2DefaultColor; // Darker shade of background color
                    const defaultColor = team2DefaultColor; // Default background color for Team 2
                    const pattern = teamPattern ? generatePattern(teamPattern, patternColor, defaultColor) : null;
                    return pattern ? pattern : defaultColor;
                })
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
    const team1DefaultColor = 'rgba(204, 0, 204, 0.5)'; // Dark magenta color for Team 1
    const team2DefaultColor = 'rgba(0, 102, 204, 0.5)'; // Dark blue color for Team 2
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => `Match ${item.match_number}`),
            datasets: [{
                label: 'Team 1 Circle Penetration + Shots',
                data: data.map((item, index) => item.team1_circle + shotsData[index].team1_shots),
                backgroundColor: data.map(item => {
                    const teamPattern = teamPatterns[item.team1_name];
                    const patternColor = team1DefaultColor; // Darker shade of background color
                    const defaultColor = team1DefaultColor; // Default background color for Team 1
                    const pattern = teamPattern ? generatePattern(teamPattern, patternColor, defaultColor) : null;
                    return pattern ? pattern : defaultColor;
                })
            }, {
                label: 'Team 2 Circle Penetration + Shots',
                data: data.map((item, index) => item.team2_circle + shotsData[index].team2_shots),
                backgroundColor: data.map(item => {
                    const teamPattern = teamPatterns[item.team2_name];
                    const patternColor = team2DefaultColor; // Darker shade of background color
                    const defaultColor = team2DefaultColor; // Default background color for Team 2
                    const pattern = teamPattern ? generatePattern(teamPattern, patternColor, defaultColor) : null;
                    return pattern ? pattern : defaultColor;
                })
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
    const team1DefaultColor = 'rgba(204, 102, 255, 0.5)'; // Dark lavender color for Team 1
    const team2DefaultColor = 'rgba(102, 0, 204, 0.5)'; // Dark purple color for Team 2
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => `Match ${item.match_number}`),
            datasets: [{
                label: 'Team 1 Penalties',
                data: data.map(item => item.team1_pc + item.team1_ps),
                backgroundColor: data.map(item => {
                    const teamPattern = teamPatterns[item.team1_name];
                    const patternColor = team1DefaultColor; // Darker shade of background color
                    const defaultColor = team1DefaultColor; // Default background color for Team 1
                    const pattern = teamPattern ? generatePattern(teamPattern, patternColor, defaultColor) : null;
                    return pattern ? pattern : defaultColor;
                })
            }, {
                label: 'Team 2 Penalties',
                data: data.map(item => item.team2_pc + item.team2_ps),
                backgroundColor: data.map(item => {
                    const teamPattern = teamPatterns[item.team2_name];
                    const patternColor = team2DefaultColor; // Darker shade of background color
                    const defaultColor = team2DefaultColor; // Default background color for Team 2
                    const pattern = teamPattern ? generatePattern(teamPattern, patternColor, defaultColor) : null;
                    return pattern ? pattern : defaultColor;
                })
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

function drawLegendPatterns() {
    console.log("Drawing patterns...");
    const patterns = {
        "White Warriorz": 'zigzag',
        "Blue Blazerz": 'dots',
        "Green Griffinz": 'dash',
        "Yellow Yakz": 'cross',
        "Red Ruffianz": 'plus',
        "Violet Whalez": 'x'
    };

    Object.keys(patterns).forEach(teamName => {
        const legendSpan = document.getElementById(`legend-${teamName}`).querySelector('span');
        if (legendSpan) {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = 30;  // Increased width for better visibility
            canvas.height = 30; // Increased height for better visibility

            // Generate the pattern on the canvas
            const pattern = generatePattern(patterns[teamName], 'black', 'white');
            if (pattern) {
                ctx.fillStyle = pattern;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                legendSpan.style.backgroundImage = `url(${canvas.toDataURL()})`;
                legendSpan.style.display = 'inline-block';
                legendSpan.style.width = '30px';  // Adjusted for visibility
                legendSpan.style.height = '30px'; // Adjusted for visibility
            } else {
                console.error(`Pattern generation failed for ${teamName}`);
                legendSpan.style.backgroundColor = 'grey';  // Fallback color
            }
        } else {
            console.log(`No element found for #legend-${teamName} span`);
        }
    });
}

