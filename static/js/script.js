const startBtn = document.querySelector('#start');
const resultDiv = document.querySelector('#result-div');

SpeechRecognition = webkitSpeechRecognition || SpeechRecognition;
const recognition = new SpeechRecognition();

recognition.interimResults = true; // これこれ

recognition.onresult = (event) => {
    console.log(event.results[0][0].transcript);
    console.log(event.results[0].isFinal); // 発言が終了したかどうか。
    resultDiv.value = event.results[0][0].transcript;
    document.getElementById("result-div2").innerHTML = event.results[0][0].transcript;
}

startBtn.onclick = () => {
    recognition.start();
}

function buttonClick(){
    document.form1.button1.click();
}


var text = document.getElementById('message').textContent

if (text.match(/あなたの負けです。/)) {
    $(".divhide").hide();	
    $(".divhide2").show();
}