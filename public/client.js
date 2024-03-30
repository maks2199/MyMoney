var slider1 = document.getElementById("data1");
var slider2 = document.getElementById("data2");
var slider3 = document.getElementById("data3");

var output1 = document.getElementById("demo1");
var output2 = document.getElementById("demo2");
var output3 = document.getElementById("demo3");
output1.innerHTML = slider1.value; // Display the default slider value
output2.innerHTML = slider2.value; 
output3.innerHTML = slider3.value; 





const ctx = document.getElementById('myChart');
var chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Data1', 'Data2', 'Data3'],
        datasets: [{
            data: [slider1.value, slider2.value, slider3.value],
            borderWidth: 5
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Update the current slider value (each time you drag the slider handle)
slider1.oninput = function () {
    output1.innerHTML = this.value;

    console.log(chart.data.datasets[0].data[0] = slider1.value)
    chart.update()
}
slider2.oninput = function () {
    output2.innerHTML = this.value;

    console.log(chart.data.datasets[0].data[1] = slider2.value)
    chart.update()
}
slider3.oninput = function () {
    output3.innerHTML = this.value;

    console.log(chart.data.datasets[0].data[2] = slider3.value)
    chart.update()
}