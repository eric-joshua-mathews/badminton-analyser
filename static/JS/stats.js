const P1_COL  = '#c0724a';
const P2_COL  = '#4a7fa0';
const MUTED   = '#ccc5bb';
const SHOT_PALETTE = [
    '#c0724a','#4a7fa0','#6ab187','#e0b04a',
    '#9b6bb5','#d05f7a','#5aabba','#a0956e','#7a9e6a'
];

let currentPlayer = 1;
let charts = {};   // store chart instances to redraw on toggle

// PLAYER TOGGLE
document.querySelectorAll('.toggleBtn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.toggleBtn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentPlayer = parseInt(btn.dataset.player);
        renderAll();
    });
});

// SUMMARY STRIP
function renderSummary() {
    document.getElementById('totalRallies').textContent = stats.total_rallies ?? '—';

    // final score from last rally
    const rallies = stats.score_progression;
    if (rallies && rallies[0].length > 0) {
        const p1Final = rallies[0][rallies[0].length - 1];
        const p2Final = rallies[1][rallies[1].length - 1];
        document.getElementById('finalScore').textContent = `${p1Final} — ${p2Final}`;
    }

    // avg rally length
    const lengths = stats.rally_lengths;
    if (lengths && lengths.length > 0) {
        const total = lengths.reduce((sum, r) => sum + r.length, 0);
        document.getElementById('avgLength').textContent = (total / lengths.length).toFixed(1) + ' shots';
    }
}

// CHART HELPERS

function destroyChart(id) {
    if (charts[id]) { charts[id].destroy(); delete charts[id]; }
}

function playerData() {
    return stats[`p${currentPlayer}`];
}

function playerColour() {
    return currentPlayer === 1 ? P1_COL : P2_COL;
}


// SHOT DISTRIBUTION PIE
function renderShotPie() {
    destroyChart('shotPie');
    const data = playerData().shot_distribution;
    if (!data || Object.keys(data).length === 0) return;

    const labels = Object.keys(data);
    const values = Object.values(data);

    charts['shotPie'] = new Chart(document.getElementById('shotPieChart'), {
        type: 'doughnut',
        data: {
            labels,
            datasets: [{
                data: values,
                backgroundColor: SHOT_PALETTE,
                borderWidth: 2,
                borderColor: '#fff',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: { family: 'DM Sans', size: 11 },
                        color: '#888070',
                        boxWidth: 12,
                        padding: 10,
                    }
                }
            }
        }
    });
}


// DIRECTION BREAKDOWN STACKED BAR

function renderDirectionChart() {
    destroyChart('direction');
    const data = playerData().direction_breakdown;
    if (!data || Object.keys(data).length === 0) return;

    const labels   = Object.keys(data);
    const straight = labels.map(l => data[l]['straight'] || 0);
    const crossL   = labels.map(l => data[l]['cross (left)'] || 0);
    const crossR   = labels.map(l => data[l]['cross (right)'] || 0);

    charts['direction'] = new Chart(document.getElementById('directionChart'), {
        type: 'bar',
        data: {
            labels,
            datasets: [
                { label: 'Straight',      data: straight, backgroundColor: playerColour() + 'cc' },
                { label: 'Cross Left',    data: crossL,   backgroundColor: playerColour() + '77' },
                { label: 'Cross Right',   data: crossR,   backgroundColor: playerColour() + '44' },
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { stacked: true, ticks: { font: { family: 'DM Mono', size: 10 }, color: '#888070' }, grid: { display: false } },
                y: { stacked: true, ticks: { font: { family: 'DM Mono', size: 10 }, color: '#888070' }, grid: { color: '#f0ece6' } }
            },
            plugins: { legend: { labels: { font: { family: 'DM Sans', size: 11 }, color: '#888070', boxWidth: 12 } } }
        }
    });
}


//ERROR ANALYSIS
function renderErrorAnalysis() {
    const data = playerData().error_analysis;
    destroyChart('errorAnalysis')
    if (!data||Object.keys(data).length===0){
        document.getElementById('errorChart').innerHTML='<div class="no-data">No error data yet</div>';
        return;
    }
        charts['errorAnalysis'] = new Chart(document.getElementById('errorPie'),{
            type:'pie',
            data:{

                labels:Object.keys(data).map(k=>k+' court'),
                datasets:[{
                    data:Object.values(data),
                    backgroundColor:[
                        playerColour()+'ff',
                        playerColour()+'aa',
                        playerColour()+'55'],
                    borderWidth:2,
                    borderColor:'#fff'}]
            },
            options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {font: {family: 'DM Sans', size: 11}, color: '#888070'},
                            boxWidth: 12,
                            padding: 10
                        }
                    }
                }

        });
    }


//WIN RATE BY SHOT
function renderWinRate() {
    destroyChart('winRate');
    const data = playerData().win_rate_by_shot;
    if (!data || Object.keys(data).length === 0) return;

    const labels = Object.keys(data);
    const rates  = labels.map(l => data[l].rate);

    charts['winRate'] = new Chart(document.getElementById('winRateChart'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Win Rate %',
                data: rates,
                backgroundColor: labels.map(l => data[l].rate >= 50 ? playerColour() + 'cc' : '#e2ddd7'),
                borderRadius: 6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { ticks: { font: { family: 'DM Mono', size: 10 }, color: '#888070' }, grid: { display: false } },
                y: {
                    min: 0, max: 100,
                    ticks: { font: { family: 'DM Mono', size: 10 }, color: '#888070', callback: v => v + '%' },
                    grid: { color: '#f0ece6' }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: { callbacks: { label: ctx => `${ctx.raw}% win rate` } }
            }
        }
    });
}


//heat maps deleted



//RALLY LENGTH BAR - fin dont need to touch unless  rally_length is touched
function renderRallyLength() {
    destroyChart('rallyLength');
    const data = stats.rally_lengths;
    if (!data || data.length === 0)
        return;

    const labels = data.map(r => `Rally ${r.rally_num}`);
    const values = data.map(r => parseInt(r.length)); // rmeber to change this depending on the return name of the rally Length functions
    console.log(stats.rally_lengths) ////-----------------------------------------------------------------------
    charts['rallyLength'] = new Chart(document.getElementById('rallyLengthChart'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Number of shots',
                data: values,
                backgroundColor: '#2d2d2d22',
                borderColor: '#2d2d2d',
                borderWidth: 1.5,
                borderRadius: 6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { ticks: { font: { family: 'DM Mono', size: 10 }, color: '#888070' }, grid: { display: false } },
                y: {beginAtZero: true, ticks: { font: { family: 'DM Mono', size: 10 }, color: '#888070', stepSize: 1 ,precision:0}, grid: { color: '#f0ece6' } }
            },
            plugins: { legend: { display: false } }
        }
    });
}


// SCORE PROGRESSION LINE
function renderScoreProgression() {
    destroyChart('scoreProg');
    const [p1, p2] = stats.score_progression;
    if (!p1 || p1.length === 0) return;

    const labels = p1.map((_, i) => `Rally ${i + 1}`);

    charts['scoreProg'] = new Chart(document.getElementById('scoreProgChart'), {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: 'Player 1',
                    data: p1,
                    borderColor: P1_COL,
                    backgroundColor: P1_COL + '22',
                    tension: 0,
                    pointRadius: 4,
                    fill: true,
                },
                {
                    label: 'Player 2',
                    data: p2,
                    borderColor: P2_COL,
                    backgroundColor: P2_COL + '22',
                    tension: 0,
                    pointRadius: 4,
                    fill: true,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { ticks: { font: { family: 'DM Mono', size: 10 }, color: '#888070' }, grid: { display: false } },
                y: { ticks: { font: { family: 'DM Mono', size: 10 }, color: '#888070', stepSize: 1 }, grid: { color: '#f0ece6' } }
            },
            plugins: { legend: { labels: { font: { family: 'DM Sans', size: 11 }, color: '#888070', boxWidth: 12 } } }
        }
    });
}
function renderAiFeedback() {
    document.getElementById('aiFeedbackText').textContent = aiFeedback[currentPlayer];
}
// RENDER ALL
function renderAll() {
    renderShotPie();
    renderDirectionChart();
    renderErrorAnalysis();
    renderWinRate();
    //heatmaps deleted replacing with AI api feedback :3
    renderRallyLength();
    renderScoreProgression();
    renderAiFeedback();
}
// on load
renderSummary();
renderAll();