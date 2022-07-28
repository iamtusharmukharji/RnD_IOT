function rgb(ev){
    if (ev=="off"){
        var rgb=0;
        var r = 0;
        var g = 0;
        var b = 0;

    }else{
    const color = ev.target.value;
    var r = parseInt(color.substr(1,2), 16)+45;
    var g = parseInt(color.substr(3,2), 16)+45;
    var b = parseInt(color.substr(5,2), 16)+45;
    var rgb = 1;
    };
    
    const url = "http://tmissacnewton.pythonanywhere.com/update/rgb/";
    
    const payload = {
        "device_id":1,
        "red":r,
        "green":g,
        "blue":b,
        "on":rgb
    };
    console.log(payload);
    
    const response = fetch(url,{
        method: "POST",
        headers: {"Content-Type" : "application/json"},
        body: JSON.stringify(payload)
      });
      console.log(response);
    
}

function fetch_dht(){
    const url = "http://tmissacnewton.pythonanywhere.com/fetch/dht/?device_id=1";
    var data;
    fetch(url)
.then(res => res.json())
.then((out) => {
    console.log(out);
    printData(out);
    
})
.catch(err => { throw err });

}
var gs=5;
var gi =0;
function printData(data){
    var data = data['data'];
    document.getElementById('para').innerHTML=" ";
    var i = 0;
    for (i=gi;i<=gs;i++) {
    document.getElementById('para').innerHTML += JSON.stringify(data[i])+"\n"+'\n';
}
gi = gs+1
gs+=5
}