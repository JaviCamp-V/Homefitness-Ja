window.addEventListener('load', function() {
    let lastsession = document.querySelector('#lastsession').getContext('2d');
    let canvas=document.querySelector('#lastsession');
    const compare = document.querySelector('#compare');
    const progress = document.querySelector('#progress').getContext('2d');
    const exercise = document.querySelector('#compare');
    const calorieschart = document.querySelector('#calorieschart').getContext('2d');
    const sessionhart = document.querySelector('#sessionhart').getContext('2d');





    


    var chartone_Lables=[];
    var chartone_title="Last exercise session";
    var chartone_data=[];
    var chartone_sid=-1;
    var chartone_type="";
    var chartone=null;


    

    var charttwo_Lables=[];
    var charttwo_title="Last exercise session";
    var charttwo_data=[];
    var charttwo_sid=-1;
    var charttwo_type="";
    var charttwo=null;

    var chart3=null;

    var chart4=null;
    compare.style.display = 'none';


    fetch('/homefitness/dashboard/lastsession', {
        method: 'GET', // or 'PUT'
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
        if (data.hasOwnProperty("Error")){
            chartone_title="No sessesion data is available"
        }else{
        chartone_Lables=data.labels;
        chartone_title=data.exercise;
        chartone_data=data.data;
        chartone_sid=data.sid;
        chartone_type=data.exercise
        if (chartone_sid>1){
            compare.style.display = "block";
        }
        }
         chartone= new Chart(lastsession,{
            type:'bar',
            data: {
                labels:chartone_Lables,
                datasets: [{
                          label:chartone_title,
                          backgroundColor: 'rgb(0,99,132)',
                          borderColor: 'rgb(0,99,132)',
                          data:chartone_data,
                          }]
    
            },
            options:{}
        });
      })
      .catch((error) => {
        console.error('Error:', error);
        var chartone= new Chart(lastsession,{
            type:'bar',
            data: {
                labels:"No sesdion data is available for user at this moment",
                datasets: [{
                          label:chartone_title,
                          backgroundColor: 'rgb(0,99,132)',
                          borderColor: 'rgb(0,99,132)',
                          data:chartone_data,
                          }]
    
            },
            options:{}
        });
    
      });



      /***
       * progress fetch and graphing function
       */
      fetch('/homefitness/dashboard/squat', {
        method: 'GET', // or 'PUT'
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => response.json())
      .then(data => {
        console.log('progess:', data);
        if (data.hasOwnProperty("Error")){
            charttwo_title="No sessesion data is available"
        }else{
        charttwo_Lables=data.labels;
        charttwo_title=data.exercise;
        charttwo_data=data.data;
        charttwo_sid=data.sid;
        charttwo_type=data.exercise
        if (charttwo_sid>1){
            compare.style.display = "block";
        }
        }
         charttwo= new Chart(progress,{
            type:'line',
            data: {
                labels:charttwo_Lables,
                datasets: [{
                          label:charttwo_title,
                          backgroundColor: 'rgb(0,99,132)',
                          borderColor: 'rgb(0,99,132)',
                          data:charttwo_data,
                          }]
    
            },
            options:{}
        });
      })
      .catch((error) => {
        console.error('Error:', error);
        var charttwo= new Chart(progress,{
            type:'line',
            data: {
                labels:"No sesdion data is available for user at this moment",
                datasets: [{
                          label:charttwo_title,
                          backgroundColor: 'rgb(0,99,132)',
                          borderColor: 'rgb(0,99,132)',
                          data:charttwo_data,
                          }]
    
            },
            options:{}
        });
    
      });



///***   calorie chart ***/

      fetch('/homefitness/dashboard/lastsession', {
        method: 'GET', // or 'PUT'
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
        if (data.hasOwnProperty("Error")){
            chartone_title="No sessesion data is available"
        }else{
        chartone_Lables=data.labels;
        chartone_title=data.exercise;
        chartone_data=data.data;
        chartone_sid=data.sid;
        chartone_type=data.exercise
        if (chartone_sid>1){
            compare.style.display = "block";
        }
        }
         chart4= new Chart(calorieschart,{
            type:'bar',
            data: {
                labels:chartone_Lables,
                datasets: [{
                          label:chartone_title,
                          backgroundColor: 'rgb(0,99,132)',
                          borderColor: 'rgb(0,99,132)',
                          data:chartone_data,
                          }]
    
            },
            options:{}
        });
      })
      .catch((error) => {
        console.error('Error:', error);
        var chartone= new Chart(lastsession,{
            type:'bar',
            data: {
                labels:"No sesdion data is available for user at this moment",
                datasets: [{
                          label:chartone_title,
                          backgroundColor: 'rgb(0,99,132)',
                          borderColor: 'rgb(0,99,132)',
                          data:chartone_data,
                          }]
    
            },
            options:{}
        });
    
      });

      



///***   sessionhart chart ***/
var chart4= new Chart(sessionhart,{
  type:'doughnut',
  data: {
      labels:["mistake1","mistake2","mistake3"],
      datasets: [{
                label:"Session breakdown",
                backgroundColor: [
                  'rgb(255, 99, 132)',
                  'rgb(54, 162, 235)',
                ],
                data:[2,3,4,5,6,7],
                hoverOffset: 4,
                }]

  },
  options:{}
});



      exercise.addEventListener("change", function (element) {
        element.preventDefault();

        console.log(exercise.value);
        alert('changed');





        

      });

      compare.addEventListener("click", function (element) {
        element.preventDefault();
        compare.disabled = true;
        compare.classList.remove("btn-primary");
        compare.classList.add("btn-success");
  
        chartone.destroy();
        let url='/homefitness/dashboard/'+chartone_type+'/' +(parseInt(chartone_sid)-1).toString();
        console.log(url);
        fetch(url, {
            method: 'GET', 
            headers: {
              'Content-Type': 'application/json',
            },
          })
          .then(response => response.json())
          .then(data => {
            console.log('Success:', data);
            if (data.hasOwnProperty("Error")){
                chartone_title="No data";
                chartone_Lables=[];
            }else{
            chartone_title=data.exercise;
            chartone_dataC=data.data;
            chartone_sid_C=data.sid;
            }
             chartone= new Chart(lastsession,{
                type:'bar',
                data: {
                    labels:chartone_Lables,
                    datasets: [{
                              label:chartone_sid,
                              backgroundColor: 'rgb(0,99,132)',
                              //borderColor: 'rgb(0,99,132)',
                              data:chartone_data,
                              },
                              {
                                label:chartone_sid_C,
                                backgroundColor: 'rgb(200,0,0)',
                                //borderColor: 'rgb(0,99,132)',
                                data:chartone_dataC,  

                              }]
        
                },
                options:{}
            });
          })
          .catch((error) => {
            console.error('Error:', error);
            var chartone= new Chart(lastsession,{
                type:'bar',
                data: {
                    labels:"No sesdion data is available for user at this moment",
                    datasets: [{
                              label:chartone_title,
                              backgroundColor: 'rgb(0,99,132)',
                              borderColor: 'rgb(0,99,132)',
                              data:chartone_data,
                              }]
        
                },
                options:{}
            });
        
          });
    



       });
    
  







});