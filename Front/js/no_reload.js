$(document).ready(function(){
  $(".footer__subscription_form").on("submit", function(event){
		event.preventDefault();
		var data =  $(this).serialize();

		$.ajax({
      url: $(this).attr("action"),
      type: $(this).attr("method"),
      dataType: "json",
      contentType: "application/json",
      
      data: JSON.stringify({
        email: data.split("=")[1]
      }),
    });
	});

  $(".popup__btn-send").on("click", function(event){
    event.preventDefault();
    var user_email = $("#email_reset_password").val();
    var btn = $(this);

    if ((user_email.length >=8) && (user_email.includes("@")) && (user_email.includes("."))){
      btn.attr('disabled', true);

      setTimeout(function() {
        btn.attr('disabled', false);
      }, 60000);

      $.ajax({
        url: "reset-password/code",
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        
        data: JSON.stringify({
          flag: true,
          email: user_email
        }),
            
        success: function(result){
          console.log("success", result);
        },
            
        error: function(data){
          console.log("error", data);
        }
      });
    }
  });
});	