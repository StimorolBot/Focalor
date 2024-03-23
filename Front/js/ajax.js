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
    check = $(check_field(user_email));
    
    if ( check[0] === true){
      var btn = $(this);
      btn.attr('disabled', true);

      setTimeout(function() {
        btn.attr('disabled', false);
      }, 1000);

    $.ajax({
      url: "/reset-password/code-confirm",
      type: "post",
      dataType: "json",
      contentType: "application/json",
        
      data: JSON.stringify({
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


  $(".popup__btn-next-step").on("click", function(event){
    event.preventDefault();
    var user_email = $("#email_reset_password").val();
    var user_token = $("#popup__input-token").val();
    var step = $("popup__form-step")

    if ((user_email.length >0 ) && (user_token.length > 0)){

    }

    var data =  $(this).serialize();

    $.ajax({
      url: "/reset-password",
      type: "patch",
      dataType: "json",
      contentType: "application/json",
        
      data: JSON.stringify({
        data: data
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


function check_field(field){
  var email_address= ["gmail.com","mail.ru","yandex.com"]

  if (field.length < 8){
    return false;
  }
  else{
    return true;
  }  
}