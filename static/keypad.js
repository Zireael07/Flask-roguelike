$( document ).ready(function() {

    $("#go_s").click(function(e) {

        //console.log("Clicked a button 1");
        $.ajax({
            url: "/move/0/1",
            type: "GET",
            success: function(response){
                console.log("Success");
                $('#output').html(response.data);
                //this does update the page but buttons no longer work
                //document.write(html)
            }
        });

    });
    $("#go_w").click(function(e) {

        //console.log("Clicked a button 1");
        $.ajax({
            url: "/move/-1/0",
            type: "GET",
            success: function(response){
                console.log("Success");
                $('#output').html(response.data);
                //this does update the page but buttons no longer work
                //document.write(html)
            }
        });

    });
    $("#go_e").click(function(e) {

        //console.log("Clicked a button 1");
        $.ajax({
            url: "/move/1/0",
            type: "GET",
            success: function(response){
                console.log("Success");
                $('#output').html(response.data);
                //this does update the page but buttons no longer work
                //document.write(html)
            }
        });

    });
    $("#go_se").click(function(e) {

        //console.log("Clicked a button 1");
        $.ajax({
            url: "/move/1/1",
            type: "GET",
            success: function(response){
                console.log("Success");
                $('#output').html(response.data);
                //this does update the page but buttons no longer work
                //document.write(html)
            }
        });

    });
    $("#go_sw").click(function(e) {

        //console.log("Clicked a button 1");
        $.ajax({
            url: "/move/-1/1",
            type: "GET",
            success: function(response){
                console.log("Success");
                $('#output').html(response.data);
                //this does update the page but buttons no longer work
                //document.write(html)
            }
        });

    });
    $("#go_n").click(function(e) {

        //console.log("Clicked a button 1");
        $.ajax({
            url: "/move/0/-1",
            type: "GET",
            success: function(response){
                console.log("Success");
                $('#output').html(response.data);
                //this does update the page but buttons no longer work
                //document.write(html)
            }
        });

    });
    $("#go_ne").click(function(e) {

        //console.log("Clicked a button 1");
        $.ajax({
            url: "/move/1/-1",
            type: "GET",
            success: function(response){
                console.log("Success");
                $('#output').html(response.data);
                //this does update the page but buttons no longer work
                //document.write(html)
            }
        });

    });
    $("#go_nw").click(function(e) {

        //console.log("Clicked a button 1");
        $.ajax({
            url: "/move/-1/-1",
            type: "GET",
            success: function(response){
                console.log("Success");
                $('#output').html(response.data);
                //this does update the page but buttons no longer work
                //document.write(html)
            }
        });

    });
    $("#get").click(function(e) {
        console.log("Clicked get");
        $.ajax({
            url: "/get",
            type: "GET",
            success: function(response) {
                $(".modal").html(response.data);
                //reattach click hook to close inventory button
                //thanks to https://aiocollective.com/blog/click-doesn-t-work-after-ajax-load-jquery/
                $("#close_btn").click(function(e) {
                    console.log("Clicked close")
                    $(".modal").attr("style", "display:none");
                });
            }
        });

    });
    
    $("#inven").click(function(e) {
        console.log("Clicked inven");
        $(".modal").attr("style", "display:block")
    });
    $("#close_btn").click(function(e) {
        console.log("Clicked close")
        $(".modal").attr("style", "display:none");
    });
});
