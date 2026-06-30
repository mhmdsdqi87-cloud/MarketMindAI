// ساعت زنده
function updateClock() {
    const now = new Date();
    document.getElementById("clock").innerHTML =
        now.toLocaleTimeString();
}

setInterval(updateClock, 1000);
updateClock();

// دکمه Refresh
function refreshMarket() {
    location.reload();
}

// تغییر تم
function toggleTheme() {

    document.body.classList.toggle("light");

}