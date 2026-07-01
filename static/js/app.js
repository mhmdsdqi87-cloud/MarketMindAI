// ===== COINS =====
async function loadCoins() {
    try {
        const res = await fetch("/api/coins");
        const data = await res.json();

        const container = document.getElementById("coins");
        if (!container) return;

        if (!data || data.length === 0) {
            container.innerHTML = "⚠️ No data";
            return;
        }

        container.innerHTML = data.map(c => `
            <div class="coin-card">
                <h3>${c.name}</h3>
                <p>$${c.current_price}</p>
                <p>24h: ${c.price_change_percentage_24h?.toFixed(2) ?? 0}%</p>
            </div>
        `).join("");

    } catch (err) {
        console.log(err);
    }
}

loadCoins();
setInterval(loadCoins, 30000);


// ===== CLOCK =====
function updateClock() {
    const el = document.getElementById("clock");
    if (!el) return;

    const now = new Date();
    el.innerHTML = now.toLocaleTimeString();
}

setInterval(updateClock, 1000);
updateClock();


// ===== BUTTONS =====
function refreshMarket() {
    location.reload();
}

function toggleTheme() {
    document.body.classList.toggle("light");
}
async function loadCoins() {
    try {
        const res = await fetch("/api/coins");
        const data = await res.json();

        const container = document.getElementById("coins");

        if (!container) return;

        if (!data || data.length === 0) {
            container.innerHTML = "⚠️ No data (API limited)";
            return;
        }

        container.innerHTML = data.map(c => `
            <div class="coin-card">
                <h3>${c.name}</h3>
                <p>💰 $${c.current_price}</p>
                <p>📊 24h: ${c.price_change_percentage_24h?.toFixed(2) ?? 0}%</p>
            </div>
        `).join("");

    } catch (err) {
        console.log("API error:", err);
    }
}

// اولین لود
loadCoins();
