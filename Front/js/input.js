let input_password = document.querySelector('.login__password-input');
let show_password_btn = document.querySelector('.fa-eye');


function show_password(){
	if(input_password.type === 'password'){
		input_password.setAttribute('type', 'text');
		show_password_btn.classList.remove('fa-eye');
		show_password_btn.classList.add('fa-eye-slash');
	}
	
	else{
		input_password.setAttribute('type', 'password');
		show_password_btn.classList.remove('fa-eye-slash');
		show_password_btn.classList.add('fa-eye'); 
    }
}
