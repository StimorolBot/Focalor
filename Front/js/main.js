let slider = [];

function init_slider(){
	let img_list = document.querySelectorAll(".slider_img");
	
	for (let i = 0; i < img_list.length; i++){
	    slider[i] = img_list[i];
	    img_list[i].remove();
	}

	for (let i = 0; i < 8; i++){
		create_img(i);
	}
}

init_slider();

/*-----------------------------------------------------------------------------------------------------*/

let links = document.querySelectorAll("nav.header-menu > span");
let marker = document.querySelector(".marker");

function indicator(e){
	marker.style.left = e.offsetLeft + "px";
	marker.style.width = e.offsetWidth + "px";
}

links.forEach((link)=>
	link.addEventListener("mouseenter", (e) => {
		indicator(e.target);
	}
));


/*-----------------------------------------------------------------------------------------------------*/

function switch_theme(){
	let sw = document.querySelector("#switch");
	let body = document.querySelector("body");
	let menu_list = document.querySelectorAll(".menu");

	
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


/*-----------------------------------------------------------------------------------------------------*/


function crate_iframe(event){
	let iframe = document.createElement("iframe");
	iframe.src = "/login";
	iframe.width = "100%";
	iframe.height = "100%";
	iframe.frameborder = "0";
	iframe.sandbox = "allow-scripts";
	iframe.allowfullscreen;
	iframe.id = "login_frame";


  	document.querySelector(".iframe_container").appendChild(iframe);


	iframe.style.cssText = (`display: block;
							 position: fixed; 
							 top: 0px; 
							 left: 0px; 
							 width: 100%; 
							 height: 100%; 
							 z-index: 9999;
						     border: 0px;
						    `);

	
	window.addEventListener('message', function(event) {
  		let message = event.data;
  		if (message === 1){
  			iframe.parentNode.removeChild(iframe);
  		}
	});	
}

/*-----------------------------------------------------------------------------------------------------*/

let offset = 9;
let  swap = 0;


function create_img(offset){
	let img = document.createElement("img");
	img.src = slider[offset].src;
	img.classList.add("slider_img");
	document.querySelector(".section__slider-slider_wrapper").appendChild(img);
}



setInterval(() => {
	let carouselItems = document.querySelectorAll(".slider_img");

	create_img(offset);

	carouselItems[0].remove();


	if (swap >= 8){
		swap =0;
	}
  
	if(offset < slider.length-1){
    	offset++;
    	swap++;
  	}
  	else{
    	offset = 0;
  	}
},2000)
