$(document).ready(function(){
    var ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = function(event){
        var resp_json = $.parseJSON(event.data);
        parseResult(resp_json);
        setupClickListener();
    } //ws.onmessage

    ws.onerror = function(event){
        var err = $("<p>Lose connection</p>");
        err.prependTo("#result");
    }// ws.onerror





    $("#menu li a").click(function(){
        // 000 - AI
        // 901 - segment
        // 904 - segment for search
        // 902 - extract keyword
        // 905 - extract SPO
        // 903 - Word flag
        // 400 - pass question to cs
        var code = $(this).attr("id");
        var msg = $("#message").val();

        if(code == "clear"){
            $("#result").html("");
        } else if(code == "800") {
            var map_html = '<div id="allmap" style="width: 500px; height: 400px;"></div>';
            map_html += "<hr/>"
            $(map_html).prependTo("#result");

            var map = new BMap.Map("allmap");
            map.centerAndZoom("成都", 15);
            var top_right_navigation = new BMap.NavigationControl({
                anchor: BMAP_ANCHOR_TOP_RIGHT,
                type: BMAP_NAVIGATION_CONTROL_SMALL
            });
            map.addControl(top_right_navigation);
            var local = new BMap.LocalSearch(map, {
		        renderOptions:{map: map}
	        });
	        local.search(msg);

        } else {
            // send2server(code, msg) // websocket
            ajaxRequest(code, msg) //ajax
        }
    }); // menu listener



    function parseResult(json) {
        // alert(JSON.stringify(json));
        var type = json.type;
        var html = "";
        if(type == "000"){
            html = "<div><ul>";
            $.each(json.resp, function(n, item){
                html += '<li><a href="#">' + item.content + '</a></li>';
            });
            html += "</ul></div>";

        } else if(type == "001" || type == "999" || type == "901" || type == "902" || type == "904"){
            html = "<p>" + json.resp + "</p>";
        } else if(type == "401") {
            $("#result").html("");
            html = "<p>" + json.resp + "</p>";
        } else if(type == "903") {
            html = "<div><ul>";
            $.each(json.resp, function(n, item){
                html += "<li>" + item.word+ " | " + item.flag + "</li>";
            });
            html += "</ul></div>";
        } else if(type == "905") {
//            alert(JSON.stringify(json.resp));
//            $.each(json.resp, function(n, item){
//                alert(JSON.stringify(item))
//            });
            html = "<div><ul>"
            html += "<li>主: "+json.resp.SUB+"</li>"
            html += "<li>谓: "+json.resp.PRE+"</li>"
            html += "<li>宾: "+json.resp.OBJ+"</li>"
            html += "<li>状: "+json.resp.ADV+"</li>"
            html += "</ul></div>"
        }

        html += "<hr/>"
        $(html).prependTo("#result");

    } //parseResult()

    function send2server(code, msg) {
        var message = {
            'code': code,
            'msg': msg
        }
        ws.send(JSON.stringify(message))
    } // send2server()



    function setupClickListener() {
        $("#400").click(function(){
            var code = $(this).attr("id");
            var msg = $("#message").val();
            // send2server(code, msg); //WebSocket
            ajaxRequest(code, msg); //ajax
        });
    }



});// document