let input_password = document.getElementsByName("password");
let show_password_btn = document.querySelectorAll('.fa-eye');

show_password_btn.forEach( function(element, index) {
	element.addEventListener('click', function(event){
		
		if(input_password[index].type === 'password'){
			input_password[index].setAttribute('type', 'text');
			show_password_btn[index].classList.remove('fa-eye');
			show_password_btn[index].classList.add('fa-eye-slash');
		}

		else{
			input_password[index].setAttribute('type', 'password');
			show_password_btn[index].classList.remove('fa-eye-slash');
			show_password_btn[index].classList.add('fa-eye'); 
		}
	});
})