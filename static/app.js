document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form");

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        getColors();
    });

    async function getColors() {
        try {
            // Fetch the input value
            const query = form.elements.query.value;

            // Send a POST request to the server and await the response
            const response = await fetch("/palette", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    query: query,
                }),
            });

            // Check if the response status is OK, otherwise throw an error
            if (!response.ok) {
                throw new Error("Network response was not ok" + response.statusText);
            }

            // Process the response
            const data = await response.json();
            const colors = data.colors;
            const container = document.querySelector(".container");
            createColorBoxes(colors, container);

        } catch (error) {
            // Log any errors to the console
            console.error("Fetch error: ", error);
        }
    }

    function createColorBoxes(colors, parent) {
        // Clear any existing children from the parent element
        parent.innerHTML = "";

        // Iterate over the colors and create a new div for each one
        colors.forEach(color => {
            const div = document.createElement("div");
            div.classList.add("color");
            div.style.backgroundColor = color;
            div.style.width = `calc(100% / ${colors.length})`;

            div.addEventListener("click", function () {
                navigator.clipboard.writeText(color);
            });

            const span = document.createElement("span");
            span.innerText = color;
            div.appendChild(span);
            parent.appendChild(div);
        });
    }
});
