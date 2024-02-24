function switch_theme(){
	let sw = document.querySelector("#switch");
	let body = document.querySelector("body");
	let menu_list = document.querySelectorAll(".menu__card");

	
	if (sw.checked == false){
		body.style.cssText = "background-color: #0E294B;";
		menu_list.forEach(function(menu){
			menu.style.cssText = "background-color: #20426D;";
		});
	}

	else{
		body.style.cssText = "background-color: #a4bbdb;";
		menu_list.forEach(function(menu){
			menu.style.cssText = "background-color: #6495ED;";
		});
	}
}