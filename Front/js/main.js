let img_list = document.querySelectorAll(".slider_img");
let slider = [];

function init_slider(){

	for (let i = 0; i < img_list.length; i++){
	    slider[i] = img_list[i].src;
	    img_list[i].remove();
	}

	for (let i = 0; i < 8; i++){
		let img = document.createElement("img");	
		img.src = slider[i];
		img.classList.add("slider_img");
		document.querySelector(".section__slider-slider_wrapper").appendChild(img);
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


let offset = 6;
let delay = 2100;

function draw(){
	let iter = function(step){

		setTimeout(function(){
			let slider_visible = document.querySelectorAll(".slider_img");
			let img = document.createElement("img");

			img.src = slider[step];
			img.classList.add("slider_img");


			if (slider_visible.length <= 8){
				setTimeout(function(){				
					document.querySelector(".section__slider-slider_wrapper").appendChild(img);

					if (step >= 17){
						draw();
					}

				}, 1600);
			}

			slider_visible[0].style.cssText = "margin-left: -199px; transition: all ease 1.5s;";

			setTimeout(function(){
				if (offset <= -1){
					offset = 6;
					}

					//progress_bar(offset);
					offset--;
			}, 900);

			if (slider_visible.length >= 8){
				setTimeout(function(){
					slider_visible[0].remove();
				}, 1950);
			}

    	}, delay * step);
	}
  
  	for(let i = 0; i < img_list.length; i++){
    	iter(i);
  	}
}

//draw();
//[Violation] 'setTimeout' handler took 88ms!!!
//[Violation] 'setTimeout' handler took 74ms

/*-----------------------------------------------------------------------------------------------------*/

/*function progress_bar(offset){
	let progress = document.querySelectorAll(".point");


	for (let i = 0; i < progress.length; i++){
        progress[i].className = progress[i].className.replace(" active_point", "");        
	}
	
    progress[offset].className += " active_point";
}*/

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

