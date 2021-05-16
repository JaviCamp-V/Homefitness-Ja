window.addEventListener('load', function() {
    let intake = document.querySelector('#intake').getContext('2d');
    let totalburn = document.querySelector('#totalburn').getContext('2d');



    var intakechart= new Chart(intake,{
        type:'doughnut',
        data: {
            labels:["Eaten(kcl)","Need(kcl)"],
            datasets: [{
                      label:"Percentage Intake",
                      backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                      ],
                      data:[intakeamount,intakeshould],
                      hoverOffset: 4,
                      }]

        },
        options:{}
    });
    intake.width=50;
    intake.height = 50;
    var burnchart= new Chart(totalburn,{
        type:'doughnut',
        data: {
            labels:["Burn(kcl)","TO Burn(kcl)"],
            datasets: [{
                      label:"Percentage Intake",
                      backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                      ],
                      data:[burnamount,burnshould],
                      hoverOffset: 4,
                      }]

        },
        options:{}
    });






});