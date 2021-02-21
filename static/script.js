const message = document.getElementById("qn").textContent;
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
const v = document.getElementById("on");
var count=0;
function read(){
	on(0);
	speechSynthesis.speak(new SpeechSynthesisUtterance(message));
	typingPromises(message, 55).forEach(promise => {promise.then(portion => {
		document.getElementById('quest').innerHTML = portion;
	  });
	});
}
$(window).load(function()
{
    $('#myModal').modal('show');
});
function typingPromises(message, timeout) {
	return [...message].map(
		(ch, i) => new Promise(resolve => {
			setTimeout(() => {
				resolve(message.substring(0, i + 1));
			}, timeout * i);
		})
	);
}

let toggleBtn = null;
if (typeof SpeechRecognition === "undefined") {
	on(0);
	alert("Browser does not support Speech API. Please download latest chrome.");
}
else {
	
	recognition.continuous = true;
    recognition.interimResults = true;
    
	recognition.onresult = event => {
		const last = event.results.length - 1;
		const res = event.results[last];
		const text = res[0].transcript;
		
		if (res.isFinal) {

			const response = process(text);
			console.log("text"); 
			speechSynthesis.speak(new SpeechSynthesisUtterance(response));
		} 	}
    let listening = false;
    
	toggleBtn = () =>{
		if (listening) {
			on(0);
		} else {
			on(1);
		}
		listening = !listening;
	};
   toggleBtn();
}
function on(a=0){  
    if(v.className.includes("active")==false || a==1){
        v.className +=" active";
		console.log('MIC ON');
		if(count!=0){
		recognition.start();}
		else{
			count+=1;
		}
    }

    else if (v.className.includes("active")==true || a==0){
		 recognition.stop();

         v.className=v.className.replace(" active", "");
		 console.log('MIC OFF');
    }
} 
function process(rawText) {
	console.log(`listening: ${rawText}`);
	fetch(`/getdata/${rawText}`);
	let text = rawText.replace(/\s/g, "");
	text = text.toLowerCase();
	let response ="";
	switch(text) {
		case "next":
            on(0);
			document.getElementById('link_next').click();break;
        default:
            response="ok sir";break;
	}
	
	return;
}
