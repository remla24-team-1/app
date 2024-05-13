function version() {
  fetch("http://127.0.0.1:8080/version", { method: "GET" })
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("version").innerText = data;
    });
}

window.onload = function () {
  version();
};
