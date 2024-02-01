let btn_voice = document.querySelector(".focalors__play-voice-img");
let song = document.querySelector(".focalors-audio");


btn_voice.onclick  = function(event){
	if (btn_voice.classList.contains('focalors__play-voice-img--active')){
		btn_voice.classList.remove('focalors__play-voice-img--active');
		song.currentTime = 0.0;
		song.pause();
	}
	else{
		song.play();
		btn_voice.classList.add('focalors__play-voice-img--active');
	}
}