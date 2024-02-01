let unlock = true;

const dellay = 300;
const body = document.querySelector("body"); 
const popup_link = document.querySelectorAll(".header-popup-link");
const lock_padding = document.querySelectorAll(".lock_padding");


function body_lock(){
	const lock_padding_value = parseInt(window.innerWidth) - parseInt(document.documentElement.clientWidth);
	
	if (lock_padding.length > 0){
		for (let index = 0; index < lock_padding.length; index++){
			const el = lock_padding[index];
			el.style.paddingRight = lock_padding_value;
		}
	}

	body.style.paddingRight = (lock_padding_value / 100)  + "px";
	body.classList.add("lock");
	unlock = false;

	setTimeout(function(){
		unlock = true;
	}, dellay);	
}


function body_unlock(){
	if (lock_padding.length > 0){
		for (let index = 0; index < lock_padding.length; index++){
			const el = lock_padding[index];
			el.style.paddingRight = "0px";
		}
	}
	body.style.paddingRight = "0px";
	body.classList.remove("lock");
	unlock = false;

	setTimeout(function(){
		unlock = true;
	}, dellay); 
}


function popup_open(current_popup){
	if (current_popup && unlock){
		const popup_active = document.querySelector(".popup.open");

		if (popup_active){
			popup_close(popup_active, false);
		}
		else{
			body_lock();
		}
		current_popup.classList.add("open");
		current_popup.addEventListener("click", function(event){
			if (!event.target.closest(".popup__body")){
				popup_close(event.target.closest(".popup"));
			}
		});
	}
}


function popup_close(popup_active, double_lock = true){
	if (unlock){
		popup_active.classList.remove("open");
		if (double_lock){
			body_unlock();
		}
	}
}


if (popup_link.length > 0){
	for (let index = 0; index < popup_link.length; index++){
		const popup_index = popup_link[index];
		
		popup_index.addEventListener("click", function(event){
			const popup_name = popup_index.getAttribute("href").replace("#", "");
			const current_popup = document.getElementById(popup_name);
			popup_open(current_popup);
			event.preventDefault();
		});
	}
}
 

const btn_close_popup = document.querySelectorAll(".login__form_close-link");
if (btn_close_popup.length > 0){
	for (let index = 0; index < btn_close_popup.length; index++){
		const el = btn_close_popup[index];

		el.addEventListener("click", function(event){
			popup_close(el.closest(".popup"));
			event.preventDefault();
		});
	}
}