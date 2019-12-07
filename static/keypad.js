$( document ).ready(function() {

    $("#go_s").click(function(e) {

        //console.log("Clicked a button 1");
        $.ajax({
            url: "/move/0/1",
            type: "GET",
            success: function(response){
                console.log("Success");
                $('p').html(response.data);
                //this does update the page but buttons no longer work
                //document.write(html)
            }
        });

    });
});
