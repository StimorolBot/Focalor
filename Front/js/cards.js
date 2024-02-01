const cards = document.querySelectorAll(".menu__card");
const btn  = document.querySelectorAll(".btn-memu__container");
const table = document.querySelectorAll(".menu-card__table");


cards.forEach( function(card, index){
	card.onclick  = function(event) {

		if(card.classList.contains('menu__card--active')){
			card.classList.remove('menu__card--active');
			btn[index].classList.remove("btn-memu__container--show");
			table[index].classList.remove("menu-card__table--show");
		}
		else{
			card.classList.add('menu__card--active');
			btn[index].classList.add("btn-memu__container--show");
			table[index].classList.add("menu-card__table--show");
		}
  	};
});

