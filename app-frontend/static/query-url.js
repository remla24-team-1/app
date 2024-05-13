document.getElementById("queryButton").addEventListener("click", function () {
  var query = document.getElementById("queryInput").value;
  var data = { urls: [query] };

  fetch("http://127.0.0.1:8080/check-url", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      const resultsContainer = document.getElementById("resultsContainer");
      resultsContainer.innerHTML = "";

      if (data && data.results && data.results.length > 0) {
        data.results.forEach((result) => {
          const resultElement = document.createElement("div");
          resultElement.classList.add(
            "bg-gray-100",
            "p-4",
            "rounded-lg",
            "mb-4"
          );

          resultElement.innerHTML = `
                    <p><span class="font-semibold">${
                      result.url
                    }</span> is classified as a <span class="font-semibold">${
            result.classification ? "phishing" : "non-phishing"
          }</span> URL.</p><p> Probability: ${result.probability}</p>`;

          resultsContainer.appendChild(resultElement);
        });
      } else {
        const errorElement = document.createElement("p");
        errorElement.textContent = "No results found in the response.";
        errorElement.classList.add("text-red-500", "font-semibold");
        resultsContainer.appendChild(errorElement);
      }
    });
});
