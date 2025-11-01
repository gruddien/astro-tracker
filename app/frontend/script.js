
const apiUrl = 'http://127.0.0.1:8000';

fetch(apiUrl)
.then(response => response.json())
.then(data => {
    document.getElementById("date").textContent = data[0];
    document.getElementById("temp").textContent = data[1][0];
    document.getElementById("cloudiness").textContent = data [1][1];
})
.catch(error => {
    console.error('Error fetching data:', error);
});

document.getElementById("api-btn").addEventListener("click", async () => {
  await fetch(`${apiUrl}/solar/Jupiter`)
  .then(response => response.text())
  .then(data => document.getElementById("response-block").innerHTML = data)
});