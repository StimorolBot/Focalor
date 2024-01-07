function init(){
	let remove_btn = document.querySelectorAll(".fa-xmark");
	let id = document.querySelectorAll(".id");

	for (let i=0; i < remove_btn.length; i++){
		remove_btn[i].addEventListener("click", (event) => {
			let url = window.location.origin + window.location.pathname + "/remove?user_id="+id[i].innerHTML;
			
			console.log(url);

			let request = fetch(url,{
				 method: 'POST',
				 body: id[i].innerHTML	
			});
		});

	}	
}

init();

/*---------------------------------------------------------------------------------------------------*/


let url = window.location.href;

function scroll_page(page){
	switch (url.split('?').length) {
		case 1:
			window.location.href = url + "?offset=2";
			break;
		case 2:
			if (Number(url.split("=")[1])-1 !=0 || page==1){
				if (check_table() != false || page==-1){
					window.location.href = url.split("=")[0] + "=" + (Number(url.split("=")[1]) + page);					
				}
			}
			break;
	}
}


function check_table(){
	let table_row = document.querySelectorAll(".table__row");

	if (table_row.length <=1){
		return false;
	} 
}


/*---------------------------------------------------------------------------------------------------*/