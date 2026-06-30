async function loadChart(){

const response=await fetch("/chart");

const prices=await response.json();

const ctx=document.getElementById("btcChart");

new Chart(ctx,{

type:"line",

data:{

labels:prices.map((_,i)=>i),

datasets:[{

label:"Bitcoin",

data:prices,

borderColor:"#00ff99",

borderWidth:3,

fill:false,

tension:.3

}]

},

options:{

plugins:{
legend:{
display:false
}
}

}

});

}

loadChart();