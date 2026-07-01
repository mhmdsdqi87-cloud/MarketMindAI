async function fetchMarket() {
    try {
        const res = await fetch("/api/coins");
        const data = await res.json();

        const box = document.getElementById("coins");
        if (!box) return;

        if (!data || !data.coins) return;

        box.innerHTML = data.coins.map(c => `
            <div class="card">
                <h3>${c.name}</h3>
                <p>💰 $${c.price}</p>
                <p style="color:${c.change >= 0 ? 'lime' : 'red'}">
                    ${c.change >= 0 ? '▲' : '▼'} ${c.change}%
                </p>
            </div>
        `).join("");

        // update status live
        const timeEl = document.getElementById("time");
        if (timeEl) timeEl.innerText = data.time;

    } catch (err) {
        console.log("Market error:", err);
    }
}


// ⏱ Live loop (بدون refresh)
setInterval(fetchMarket, 5000);
fetchMarket();


// ===== CLOCK =====
function updateClock() {
    const el = document.getElementById("clock");
    if (!el) return;
    el.innerHTML = new Date().toLocaleTimeString();
}

setInterval(updateClock, 1000);
updateClock();


// ===== UI BUTTONS =====
function refreshMarket() {
    fetchMarket(); // فقط دیتا آپدیت میشه نه کل سایت
}

function toggleTheme() {
    document.body.classList.toggle("light");
}