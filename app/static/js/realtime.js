(function () {
    if (
      !"mediaDevices" in navigator ||
      !"getUserMedia" in navigator.mediaDevices

      
    ) {
      alert("Camera API is not available in your browser");
      return;
    }
    var socket = io.connect( 'http://' + document.domain + ':' + location.port )
    // broadcast a message
    socket.on( 'connect', function() {
      socket.emit( 'my event', {
        data: 'User Connected'
      } )
      console.log("ok");
    } )

    socket.on( 'my response', function( msg ) {
      console.log( msg )
    })
  


    // capture message
    



  
    // get page elements
    const video = document.querySelector("#video");
    const btnPlay = document.querySelector("#btnPlay");
    const btnPause = document.querySelector("#btnPause");
    const btnScreenshot = document.querySelector("#btnScreenshot");
    const btnChangeCamera = document.querySelector("#btnChangeCamera");
    const screenshotsContainer = document.querySelector("#screenshots");
    const canvas = document.querySelector("#canvas");
    const devicesSelect = document.querySelector("#devicesSelect");
  
    // video constraints
    const constraints = {
      video: {
        width: {
          min: 1280,
          ideal: 1920,
          max: 2560,
        },
        height: {
          min: 720,
          ideal: 1080,
          max: 1440,
        },
      },
    };
  
    // use front face camera
    let useFrontCamera = true;
  
    // current video stream
    let videoStream;
  
    // handle events
    // play
    var intervalId="";
    var sets=0;
    var reps=0;
    var lastclass="12";

    function sendToServer(){
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext("2d").drawImage(video, 0, 0);
      const data = canvas.toDataURL("image/jpeg");
      socket.emit('livevideo', data, function (res) {

        if (true) {
          var btn = document.createElement("BUTTON");
          btn.setAttribute("class", "accordion");
          var div = document.createElement("div");
          div.setAttribute("class", "panel");
          var para = document.createElement("p");
          para.innerHTML = "Lorem100kkkkkkkkkkkkkkk";  
          div.appendChild(para);
          screenshotsContainer.prepend(btn);
          screenshotsContainer.prepend(div);
          // Create a <p> element

        }
      
      });
    }
    
    btnPlay.addEventListener("click", function () {
      video.play();
      btnPlay.classList.add("is-hidden");
      btnPause.classList.remove("is-hidden");
      intervalId=setInterval(sendToServer,10);
    });
  
    // pause
    btnPause.addEventListener("click", function () {
      clearInterval(intervalId);
      video.pause();
      btnPause.classList.add("is-hidden");
      btnPlay.classList.remove("is-hidden");
    });
  
    // take screenshot  
  btnScreenshot.addEventListener("click", function () {
      const img = document.createElement("img");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext("2d").drawImage(video, 0, 0);
      img.src = canvas.toDataURL("image/png");
      screenshotsContainer.prepend(img);
    });
  
    // switch camera
    btnChangeCamera.addEventListener("click", function () {
      useFrontCamera = !useFrontCamera;
  
      initializeCamera();
    });
  
    // stop video stream
    function stopVideoStream() {
      if (videoStream) {
        videoStream.getTracks().forEach((track) => {
          track.stop();
        });
      }
    }
  
    // initialize
    async function initializeCamera() {
      stopVideoStream();
      constraints.video.facingMode = useFrontCamera ? "user" : "environment";
  
      try {
        videoStream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = videoStream;      
      } catch (err) {
        alert("Could not access the camera");
      }
    }
  
    initializeCamera();

})();