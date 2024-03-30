

slidersConfig = [
    {
        "name": "Еда",
        "startValue": 10000
    },
    {
        "name": "Транспорт",
        "startValue": 5000
    },
    {
        "name": "Связь",
        "startValue": 3000
    },
    {
        "name": "Кофе",
        "startValue": 2000
    },
    {
        "name": "Аренда",
        "startValue": 30000
    }
]

// Creating sliders
const sliderContainer = document.querySelector('.slidecontainer')
slidersConfig.forEach((slider) =>
{
    newSlider = document.createElement('input')
    newSlider.type = 'range'
    newSlider.min = 0
    newSlider.max = 100000
    newSlider.step = 1000
    newSlider.value = slider.startValue
    newSlider.classList.add('slider')

    newSliderP = document.createElement('p')
    newSliderP.textContent = slider.name + ": "
    newSliderSpan = document.createElement('span')
    newSliderSpan.classList.add('sliderValue')
    newSliderSpan.textContent = slider.startValue
    newSliderP.appendChild(newSliderSpan)

    newSliderDiv = document.createElement('div')
    newSliderDiv.classList.add('slider')
    newSliderDiv.appendChild(newSlider)
    newSliderDiv.appendChild(newSliderP)

    sliderContainer.appendChild(newSliderDiv)
})




const autocolors = window['chartjs-plugin-autocolors'];
// Chart
const ctx = document.getElementById('myChart');
var chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: slidersConfig.map(slider => slider.name),
        datasets: [{
            data: slidersConfig.map(slider => slider.startValue),
            borderWidth: 5,
        }]
    },
    options: {
        plugins: {
            autocolors: {
                mode: 'data'
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        },
        animationSteps: 60,
        indexAxis: 'y',
    }
});
Chart.register(autocolors);



// Sliders events
sliders = document.querySelectorAll('input.slider')
for (let i = 0; i < sliders.length; i++){
    sliders[i].addEventListener('input', () => {
    siblingP = sliders[i].nextElementSibling
    sliderSpan = siblingP.querySelector('.sliderValue')
    sliderSpan.textContent = sliders[i].value

    // Update bar chart
    chart.data.datasets[0].data[i] = sliders[i].value
    chart.update()
    })
}





