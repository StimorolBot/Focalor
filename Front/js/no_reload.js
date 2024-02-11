$(document).ready(function(){
	$(".footer__subscription_form").on("submit", function(event){
		event.preventDefault();
		var data =  $(this).serialize();
		alert(data.email)

		$.ajax({
        	url: $(this).attr("action"),
        	type: $(this).attr("method"),
        	dataType: "json",
        	contentType: "application/json",
       		data: JSON.stringify({
              	email: data.split("=")[1]
            }),
            
            success: function(result){
              console.log("success", result);
            },
            
            error: function(){
              console.log("error", data);
            }
        });
	});
});	


