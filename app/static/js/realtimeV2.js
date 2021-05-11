    window.addEventListener('load', function() {
    let start = document.querySelector('#start');
    let btnPause = document.querySelector('#pause');
    let stop = document.querySelector('#stop');
    let video = document.querySelector('#video');
    cameraDevice = document.querySelector('#camerasource');
    const comments = document.querySelector("#accordion");
    const sets = document.querySelector("#sets");
    const caloire = document.querySelector("#calorie");
    const reps = document.querySelector("#reps");
    var intervalId="";
    var lastclass="12";
    var numErrors=0;
    const canvas = document.querySelector("#canvas");
    const fps=30;
    var source=null;


    let stream;
    var camaset=false;
    var constraints = { video: { width: 1280, height: 720 , frameRate: { ideal: 30, max: 60 },deviceId: cameraDevice.select ? {exact: cameraDevice.select} : undefined} };

    if (
        !"mediaDevices" in navigator ||
        !"getUserMedia" in navigator.mediaDevices
  
        
      ) {
        alert("Camera API is not available in your browser");
        return;
      }
    let videfeeds=[];

    /**
     * List video deivece and create a select option for each
     * 
     */
    navigator.mediaDevices.enumerateDevices().then(function (devices) {

        for(var i = 0; i < devices.length; i ++){
            var device = devices[i];
            if (device.kind === 'videoinput') {
                var x = document.createElement("OPTION");
                var y = document.createElement("OPTION");
                x.text = device.label || 'Camera ' + (cameraDevice.length + 1);
                cameraDevice.appendChild(x);
                cameraDevice.disabled=false;
                videfeeds.push(device);
  
            }}
        
    });
    var socket = io.connect( 'http://' + document.domain + ':' + location.port )
    socket.on( 'connect', function() {
        socket.emit( 'connection', {
          data: 'User Connected'} )
      });
      var acck=400;
      socket.on( 'connection ack', function( msg ) {
          console.log(msg);
          acck=200;
      });

    
    async function loadWebCam() {
         stream = await navigator.mediaDevices.getUserMedia(constraints)
        .then(function(mediaStream) {
        video.srcObject = mediaStream;
        video.onloadedmetadata = function(e) {
            video.play();
            console.log(video.webkitDecodedFrameCount)
    
        };
        }).catch(function(err) { console.log(err.name + ": " + err.message); });
    }

    start.addEventListener('click', function(element) {

        element.preventDefault();

        Start(window.location.pathname.split("/")[2]);

    });
     
    cameraDevice.addEventListener('change', function(element) {

        element.preventDefault();
        console.log(90);
        if(camaset){
           stream = video.srcObject;
          if (stream) {
            stream.getTracks().forEach((track) => {
              track.stop();
            });
          }
          loadWebCam()
        }

    });

    
    
    btnPause.addEventListener("click", function () {
        video.pause();
        clearInterval(intervalId);
        btnPause.classList.add("is-hidden");
        start.classList.remove("is-hidden");
        start.disabled=false;
      });

    function sendToServer(){
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0);
        const data = canvas.toDataURL("image/jpeg");
        //const img = document.createElement("img");
        //img.setAttribute("class", "card-img-top");
        //img.src =data;
        //comments.appendChild(img);
        socket.emit('livevideo', data);
        
    }
    socket.on( 'live corrections', function( msg ) {

           /* data={"class_name":self.lastclass,"correction":self.corrections[self.lastclass],
            "sets":self.sets_,"reps":self.reps,"image":image,"calorie":self.calorie}
            */
           if (msg.hasOwnProperty("error")){
               console.log(msg);
               return;
           }

           reps.innerHTML=msg.reps;
           sets.innerHTML=msg.sets;
   
           if(true ){
           lastclass=msg.class_name;
           const card = document.createElement("div");
           card.setAttribute("class", "card");
           const cardheader = document.createElement("div");
           cardheader.setAttribute("class", "card-header");
           const link = document.createElement("a");
           link.setAttribute("class", "card-link");
           link.setAttribute("data-toggle", "collapse");
           link.setAttribute("href", "#Error"+numErrors.toString());
           link.innerHTML = msg.class_name;
           cardheader.appendChild(link);  
           const collapse = document.createElement("div");
           collapse.setAttribute("id", "Error"+numErrors.toString());
           collapse.setAttribute("class", "collapse show");
           collapse.setAttribute("data-parent", "#accordion");
           const carbody = document.createElement("div");
           carbody.setAttribute("class", "card-body");
   
           const img = document.createElement("img");
           img.setAttribute("class", "card-img-top");
           img.src = "data:image/jpg;base64,"+ msg.image;
           const p = document.createElement("p");
           p.innerHTML=msg.correction;
   
           carbody.appendChild(img);               
           carbody.appendChild(p); 
           collapse.appendChild(carbody);   
           card.appendChild(cardheader);  
           card.appendChild(collapse); 
           comments.appendChild(card);   
           }   
        });
      
    function Start(typee){
        socket.emit( 'start event', {data: typee}); 

        socket.on('start ack', function( msg ) {
            /**
             * create modal
             */
            if(msg.message==="Trainer has been started")
            {
                start.classList.add("is-hidden");
                pause.classList.remove("is-hidden");
                start.disabled = true;  
                if (camaset){video.play();
                   }else{ loadWebCam();camaset=true;}
                intervalId=setInterval(sendToServer,10000/60);
            }else{
                console.log(msg);
        
            }
    });


    }


    stop.addEventListener('click', function(element) {
        element.preventDefault();
        clearInterval(intervalId);
        btnPause.classList.add("is-hidden");
        start.classList.remove("is-hidden");
        start.disabled=false;
        socket.emit( 'close sesssion'); 

        socket.on( 'close sesssion ack', function( msg ) {
            /**close sesssion
             * create modal
             * 
             * msg formattt
             * data={"exercise":self.exerise,"date":str(self.date.strftime("%x")),"start_time":self.date.strftime("%X"),"end_time":end.strftime("%X"),"duration":duration,
            "sets":self.sets_,"reps":self.reps,"calorie":self.calorie,"errors":{"total":total_errors,"errors":self.errors}}

            <div class="modal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Modal title</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <p>Modal body text goes here.</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary">Save changes</button>
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                </div>
                </div>
            </div>
            </div>
             */
            
            console.log(msg);
        });


        socket.on( 'start event', function() {
            socket.emit( 'connection', {
              data: typee} )
          });


        console.log()
        camaset=false;
        stream = video.srcObject;
        if (stream) {
            stream.getTracks().forEach((track) => {
              track.stop();
            });
          }
    });




    




  

      });
    


