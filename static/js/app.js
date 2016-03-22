$(document).ready(function(){

    var ws = new WebSocket("ws://localhost:8000/ws");

    // clear div content
    $("#clear_btn").click(function(){
       $("#result").html("");
    });

    // 000 - echo
    $("#go_btn").click(function(){
        var msg = "000" + $("#input_txt").val();
        ws.send(msg);
    });

    // 001 - segment
    $("#segment_btn").click(function(){
        var msg = "001" + $("#input_txt").val();
        ws.send(msg);
    });

    // 002 - English/Chinese/Number test
    $("#en_cn_btn").click(function(){
        var msg = "002" + $("#input_txt").val();
        ws.send(msg);
    });

    ws.onmessage = function(event){
        var content = $("<p>"+event.data + "</p>");
        content.appendTo("#result");
    }

});// document