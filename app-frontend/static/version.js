function version() {
  fetch("/version", { method: "GET" })
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("version").innerText = data;
    });
}

window.onload = function () {
  version();
};
