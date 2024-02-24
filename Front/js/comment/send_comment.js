$(document).ready(function(){
  $(".comment__form").on("submit", function(event){
		event.preventDefault();
		var data =  $(this).serialize();

		$.ajax({
      url: $(this).attr("action"),
      type: $(this).attr("method"),
      dataType: "json",
      contentType: "application/json",
      
      data: JSON.stringify({
        comment: data.split("=")[1]
      }),
      success: function(result){
          console.log("success", result);
        },
            
        error: function(data){
          console.log("error", data);
        }
    });
	});
});	