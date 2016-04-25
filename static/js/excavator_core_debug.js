$(document).ready(function(){

    $("#menu li a").click(function(){
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
            ajaxRequest(code, msg) //ajax
        }
    }); // menu listener



    function parseResult(json) {
        // alert(JSON.stringify(json));
        var code = json.code;
        var html = "";

        if(code == "999" || code == "901" || code == "902" || code == "904"){
            html = "<p>" + json.resp + "</p>";
        } else if(code == "401") {
            $("#result").html("");
            html = "<p>" + json.resp + "</p>";
        } else if(code == "903") {
            html = "<div><ul>";
            $.each(json.resp, function(n, item){
                html += "<li>" + item.word+ " | " + item.flag + "</li>";
            });
            html += "</ul></div>";
        } else if(code == "905") {
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


    function ajaxRequest(code, msg) {

        var message = {
            "code": code,
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
                $("#result").html("Error happened : /")
            }
        });
    } //ajaxRequest()

});// document