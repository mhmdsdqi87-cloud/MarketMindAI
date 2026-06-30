// گرفتن لیست علاقه‌مندی‌ها
function getWatchlist() {

    let list = localStorage.getItem("watchlist");

    if (list === null) {
        return [];
    }

    return JSON.parse(list);
}


// ذخیره لیست
function saveWatchlist(list) {

    localStorage.setItem(
        "watchlist",
        JSON.stringify(list)
    );

}


// افزودن ارز
function addWatch(symbol) {

    let list = getWatchlist();

    if (!list.includes(symbol)) {

        list.push(symbol);

        saveWatchlist(list);

        alert(symbol + " added to Watchlist ⭐");

    } else {

        alert(symbol + " is already in Watchlist");

    }

}


// حذف ارز
function removeWatch(symbol){

    let list=getWatchlist();

    list=list.filter(item=>item!==symbol);

    saveWatchlist(list);

    loadWatchlist();

}


// نمایش Watchlist
function loadWatchlist(){

    let container=document.getElementById("watchlist-container");

    if(container==null) return;

    let list=getWatchlist();

    if(list.length===0){

        container.innerHTML=`
        <h2 style="text-align:center;color:gray;">
        No favorite coins yet ⭐
        </h2>
        `;

        return;

    }

    let html="";

    list.forEach(symbol=>{

        html+=`

        <div class="watch-card">

            <h2>${symbol}</h2>

            <button
            onclick="removeWatch('${symbol}')">

            Remove

            </button>

        </div>

        `;

    });

    container.innerHTML=html;

}

window.onload=loadWatchlist;