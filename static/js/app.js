$(document).ready(function(){

    var ws = new WebSocket("ws://localhost:8000/ws");
    ws.onmessage = function(event){
        $("#result").html(event.data);
    }
    ws.onerror

    // 000 - echo
    $("#go_btn").click(function(){
        var msg = "000" + $("#input_txt").val();
        ws.send(msg);
    });

    // 001 - segment
    $("#segment_btn").click(function(){
        var msg = "001"+$("#input_txt").val();
        ws.send(msg);
    });

});// document