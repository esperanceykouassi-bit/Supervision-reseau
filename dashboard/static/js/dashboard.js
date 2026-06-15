/* dashboard.js — logique front-end du tableau de bord (graphiques + AJAX) */

let graphiqueDispo = null;
let graphiqueEquip = null;

/**
 * Initialise le graphique en anneau de disponibilité (UP vs DOWN).
 */
function initGraphiqueDispo(up, down) {
    const ctx = document.getElementById('graphiqueDispo');
    if (!ctx) return;
    graphiqueDispo = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['En ligne (UP)', 'Hors ligne (DOWN)'],
            datasets: [{
                data: [up, down],
                backgroundColor: ['#198754', '#dc3545'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

/**
 * Graphique en barres des latences par équipement (page Rapports).
 */
function initGraphiqueEquipements(noms, latences) {
    const ctx = document.getElementById('graphiqueEquip');
    if (!ctx) return;
    graphiqueEquip = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: noms,
            datasets: [{
                label: 'Latence (ms)',
                data: latences.map(l => l || 0),
                backgroundColor: '#0d6efd'
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true, title: { display: true, text: 'ms' } } }
        }
    });
}

/**
 * Rafraîchit les indicateurs clés (KPI) sans recharger la page.
 * Consomme l'API REST JSON exposée par Flask (/api/statistiques).
 */
async function rafraichirKPI() {
    try {
        const reponse = await fetch('/api/statistiques');
        if (!reponse.ok) return;
        const stats = await reponse.json();

        document.getElementById('kpi-total').textContent = stats.total_equipements;
        document.getElementById('kpi-up').textContent = stats.equipements_up;
        document.getElementById('kpi-down').textContent = stats.equipements_down;
        document.getElementById('kpi-alertes').textContent = stats.alertes_actives;

        // Met à jour le graphique en anneau s'il existe.
        if (graphiqueDispo) {
            graphiqueDispo.data.datasets[0].data = [stats.equipements_up, stats.equipements_down];
            graphiqueDispo.update();
        }
    } catch (e) {
        console.warn('Rafraîchissement KPI impossible :', e);
    }
}
