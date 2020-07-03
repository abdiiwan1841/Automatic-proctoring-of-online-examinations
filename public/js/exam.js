function startup() {
    
    let vid = document.getElementById("vid");
  
    
    let stream_inst;
    let mediaObj = {};
    
    //Acess the user media
    navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
    }).then((stream) => {

        console.log(stream.getTracks());

        console.log(stream.getVideoTracks()[0].getSettings().frameRate)
        console.log(stream.getVideoTracks()[0].getSettings().height)
        console.log(stream.getVideoTracks()[0].getSettings().width)
        
        //let streamURL = window.URL.createObjectURL(stream);
        //vid.src= streamURL;
        vid.srcObject = stream;
        vid.play();
        stream_inst = stream;
    }).catch((error) => {
        console.warn(error);
    });
    
    document.getElementById('snapshot').onclick = function() { 

/*         let options = {
            audioBitsPerSecond : 128000,
            videoBitsPerSecond : 2500000,
            mimeType : 'video/webm'
          } */

        /////// Video recording
        const mediaRecorder = new MediaRecorder(stream_inst);

        //start recording
        mediaRecorder.start();
        console.log("recorder started");
        console.log(Date.now());
    
        let videoChunks = [];
        document.getElementById("stop").addEventListener("click", () => {
            //mediaRecorder.stop();
            console.log("Recording Stopped");
            clearInterval(interval);
           });

        mediaRecorder.addEventListener("dataavailable", event => {
          videoChunks.push(event.data);
        });
    
        mediaRecorder.addEventListener("stop", () => {
            const videoBlob = new Blob(videoChunks, {"type" : "video/webm;codecs=h264"});
            mediaObj["y"] = videoBlob;
            console.log(videoChunks);
            console.log("Recorder has stopped");
            videoChunks = [];
            mediaRecorder.start();
            console.log("recorder started");
        });
        
        
        let interval = setTimeout(() => {
          mediaRecorder.stop();
          let socket = io.connect("http://localhost:3000");
          socket.on('connect', function(data) {
              //console.log(data);
          socket.emit('exam', mediaObj);
          
          });
          

        }, 10000);
        ///////////

    }

}


window.addEventListener("load", startup);
