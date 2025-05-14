function captureScene() {
  document.getElementById("result").innerText = "Analyzing...";
  fetch('/capture', { method: 'POST' })
    .then(res => res.text())
    .then(data => {
      document.getElementById("result").innerText = data;
    })
    .catch(err => {
      document.getElementById("result").innerText = "Error: " + err;
    });
}
