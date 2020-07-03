function startup() {
    let vid = document.getElementById("vid");
    let snapshotBtn = document.getElementById('snapshot');
    let sendBtn = document.getElementById("send");
    let canvas = document.getElementById('drawCanvas');  
    let ctx = canvas.getContext('2d');
    let media = {};

    navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false
    }).then((stream) => {
        console.log(stream.getTracks());
        //let streamURL = window.URL.createObjectURL(stream);
        vid.srcObject = stream;
        vid.play();
    }).catch ((error) => {
        console.warn(error);
    });
    
    /////////////////////
    /////snapshot Button
    snapshotBtn.addEventListener(("click"), () => { 
        ctx.drawImage(vid,0,0); 
        document.getElementById("image").src = canvas.toDataURL('image/jpeg');
        snapshotBtn.value = "Change Image"
        sendBtn.disabled = false;
    });

    sendBtn.addEventListener("click", () => {
        media["img"] = canvas.toDataURL('image/jpeg');
        let socket = io.connect();  
        socket.on('connect', function(data) {
        socket.emit('training', media);
        });
        snapshotBtn.disabled = true;
        sendBtn.disabled = false;
    });
}

window.addEventListener("load", startup);
