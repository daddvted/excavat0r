$(document).ready(function(){

    $("#000").click(function(){
        var msg = $("#message").val();
        ajaxRequest(msg) //ajax
    }); // menu listener
    $("#message").keyup(function(event){
        if(event.keyCode == 13) {
            var msg = $("#message").val();
            ajaxRequest(msg, "enquire")
        }
    });

    function ajaxRequest(msg) {
        var message = {
            "msg": msg
        };
        data = JSON.stringify(message);
        $.ajax({
            url: "/enquire",
            type: "POST",
            data: data,
            dataType: "json",
            beforeSend: function(){},
            success: function(data){
                parseResult(data);
            },
            error: function(){
                $("#result").html("Error :/")
            }
        });
    } //ajaxRequest()

    function setupBaiduMap(kw) {
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
	    local.search(kw);
    }

    function parseResult(json) {
//        alert(JSON.stringify(json));
        var code = json.code;
        if(code == "000") {
            var html = "<div>为您找到以下问答:<ul>";
            $.each(json.resp, function(n, item){
                html += '<li><a href="#">' + item.title+ '</a></li>';
            });
            html += "</ul></div>";
            html += "<hr/>"
            $(html).prependTo("#result");
        } else if(code == "001" || code == "002") {
            var map_html = ""
            msg = json.resp.kw
            if(code == "001") {
                map_html = "<p>" + json.resp.text + "</p>"
            }
            map_html += '<div id="allmap" style="width: 500px; height: 400px;"></div>';
            map_html += "<hr/>"
            $(map_html).prependTo("#result");
            setupBaiduMap(msg)

        } else if(code == "400" || code == "999") {
            var html = "<p>" + json.resp + "</p>";
            html += "<hr/>"
            $(html).prependTo("#result");
        }


    } //parseResult()

});// document