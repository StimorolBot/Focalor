let slides = document.querySelectorAll('.focalors_bg');
let point = document.querySelectorAll(".focalors__indicator_item")
let index = slides.length;
let swap = 0;


function next_slide(){
  if (swap >= index){
    slides[index-1].classList.remove("focalors_bg--show");
    point[index-1].classList.remove("focalors__indicator--active");
    swap = 0;
  }

  if (typeof(slides[swap-1]) != typeof undefined){
    if(slides[swap-1].classList.contains('focalors_bg--show')){
        slides[swap-1].classList.remove("focalors_bg--show");
        point[swap-1].classList.remove("focalors__indicator--active");
    }
  }
  
  point[swap].classList.add("focalors__indicator--active");
  slides[swap].classList.add("focalors_bg--show");
  

  swap++;
}

setInterval(next_slide, 4000);