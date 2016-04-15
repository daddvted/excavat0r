$(document).ready(function(){
    var ws = new WebSocket("ws://localhost:8000/ws");

    //====================================
    // Handler for message and error
    //====================================
    ws.onmessage = function(event){
        var resp_json = $.parseJSON(event.data);
        parseResult(resp_json);
    }

    ws.onerror = function(event){
        var err = $("<p>Lose connection</p>");
        err.appendTo("#result");
    }

    function parseResult(json) {
        //alert(JSON.stringify(json));
        var type = json.type;
        var html = "";
        if(type == "000"){
            html = "<div><ul>"
            $.each(json.resp, function(n, item){
                html += '<li><a href="#">' + item.content + '</a></li>'
            });
            html += "</ul></div>"

        } else if(type == "999" || type == "901" || type == "902"){
            html = "<p>" + json.resp + "</p>";

        } else if(type == "903") {
            html = "<div><ul>"
            $.each(json.resp, function(n, item){
                html += "<li>" + item.word+ " | " + item.flag + "</li>";
            });
            html += "</ul></div>";
        }

        $(html).appendTo("#result");


    }

    function send2server(code, msg) {
        var message = {
            'code': code,
            'msg': msg
        }
        ws.send(JSON.stringify(message))
    }

    function ajaxRequest(code, msg) {

        var message = {
            'code': code,
            'msg': msg
        }
        $.ajax({
            url: "/ai1",
            type: "GET",
            data: {"m":JSON.stringify(message)},
            dataType: "json",
            beforeSend: function(){},
            success: function(data){
                alert("success");
                parseResult(resp_json);
            },
            error: function(){
                $("#result").html("Error happened : /")
            }
        });
    }

    //====================================
    // Click handler
    //====================================


    $("#menu li a").click(function(){
        // 000 - AI
        // 901 - segment
        // 902 - extract keyword
        // 903 - Word flag
        var code = $(this).attr("id")
        var msg = $("#message").val()

        if(code == "clear"){
            $("#result").html("")
        } else if(code == "800") {
            var map_html = '<div id="allmap" style="width: 500px; height: 400px;"></div>';
            $(map_html).appendTo("#result");

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
            send2server(code, msg) // websocket
//            ajaxRequest(code, msg) //ajax
        }
    });

});// document