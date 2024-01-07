let input_password = document.getElementById('password_input');
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

/*-----------------------------------------------------------------------------------------------------*/

let input = document.getElementsByTagName("input");
let label = document.getElementsByTagName("label");
let clear_btn = document.querySelectorAll(".fa-xmark");

for (let i = 0; i < clear_btn.length; i++){
	clear_btn[i].classList.remove('fa-xmark');
}

for (let i = 0; i < input.length; i++ ){

	input[i].oninput = function(){
		check_len_input(input[i], label[i]);
		if (input[i].value != ""){
			clear_btn[i].classList.add('fa-xmark');
		
			clear_btn[i].addEventListener('click', () => {
				clear_btn[i].classList.remove('fa-xmark');
				input[i].value = "";
			});
		}
		
		else {
			clear_btn[i].classList.remove('fa-xmark');
		}	
	};			
}
	
/*-----------------------------------------------------------------------------------------------------*/

let button = document.querySelector('button');
button.disabled = true;


function check_len_input(validate_input, lb){
	let valid = validate(validate_input, lb);

	if (input[0].value != "" && input[1].value != "" && valid != false){
		
		button.disabled = false;
		button.style.cssText = `background-color: #49423D;
								cursor:pointer;
								transition: 0.3s;
								color: #fff`;
	}

	else {
		button.disabled = true;
		button.style.cssText = `background-color: #DCDCDC;
								cursor: not-allowed;
								transition: 0.3s;`;
		
	}
}

/*-----------------------------------------------------------------------------------------------------*/	

function validate(validate_input, lb){
	let specials = "!#$%^&*()_-+=/.,:;[]{}";
	let validate_symbol = validate_input.value.at(-1);
	
	if (validate_input.value.split(" ").length >= 2){
    	validate_input.className  = "invalid";
		return false; 
    }

    else if(specials.indexOf(validate_symbol) != -1){
    	//если последний символ не в списке, то пропскает
    	validate_input.className  = "invalid";
    	return false		
    }

    else {
    	//добавить подсказки о запрете пробелов и спец символов
    	validate_input.className  = "valid";
    	return true;
    }
}


/*-----------------------------------------------------------------------------------------------------*/

function close_iframe(){
	window.parent.postMessage(1, '*');
}
