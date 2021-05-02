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

  


    // capture message
    



  
    // get page elements
    const video = document.querySelector("#video");
    const btnPlay = document.querySelector("#btnPlay");
    const btnPause = document.querySelector("#btnPause");
    const btnStop = document.querySelector("#btnStop");
    const btnChangeCamera = document.querySelector("#btnChangeCamera");
    const comments = document.querySelector("#critique");
    const sets = document.querySelector("#sets");
    const caloire = document.querySelector("#calorie");
    const reps = document.querySelector("#reps");

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
    var lastclass="12";

    function sendToServer(){
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext("2d").drawImage(video, 0, 0);
      const data = canvas.toDataURL("image/jpeg");
      

      socket.emit('livevideo', data);
  
      socket.on( 'my response', function( msg ) {
        reps.innerHTML=msg.reps;
        sets.innerHTML=msg.sets;

        if(msg.class!=lastclass ){
        lastclass=msg.class;
        const divone = document.createElement("div");
        divone.setAttribute("class", "critique-item");
        const link = document.createElement("a");
        link.setAttribute("class", "critique-link");
        link.innerHTML = msg.class;
        const divtwo = document.createElement("div");
        divtwo.setAttribute("class", "critique-body");
        const img = document.createElement("img");
        img.src = "data:image/jpg;base64,"+ msg.image;
        const p = document.createElement("p");
        p.innerHTML=msg.correction;
        divtwo.appendChild(img);               
        divtwo.appendChild(p); 
        divone.appendChild(link);   
        divone.appendChild(divtwo);  
        comments.prepend(divone);

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


    /**
     * 
     *   btnScreenshot.addEventListener("click", function () {
      const img = document.createElement("img");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext("2d").drawImage(video, 0, 0);
      img.src = canvas.toDataURL("image/png");
      screenshotsContainer.prepend(img);
    });

     */

    btnStop.addEventListener("click", function () {
      stopVideoStream();
      btnPause.classList.add("is-hidden");
      btnPlay.classList.remove("is-hidden");
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