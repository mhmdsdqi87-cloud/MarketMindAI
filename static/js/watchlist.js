let watchlist = JSON.parse(localStorage.getItem("watchlist")) || [];

function addWatch(symbol){

    if(!watchlist.includes(symbol)){

        watchlist.push(symbol);

        localStorage.setItem(
            "watchlist",
            JSON.stringify(watchlist)
        );

        alert(symbol+" added ⭐");

    }

}