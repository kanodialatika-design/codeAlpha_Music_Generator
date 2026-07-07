const generateBtn = document.getElementById("generateBtn");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const downloadLink = document.getElementById("downloadLink");
const musicStyle = document.getElementById("musicStyle");

generateBtn.addEventListener("click", async () => {

    loading.classList.remove("hidden");
    result.classList.add("hidden");

    generateBtn.disabled = true;
    generateBtn.innerText = "Generating...";

    try {

        const response = await fetch("/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                style: musicStyle.value
            })

        });

        const data = await response.json();

        loading.classList.add("hidden");

        if (data.success) {

            result.classList.remove("hidden");

            downloadLink.href = data.download;

            generateBtn.disabled = false;
            generateBtn.innerText = "🎵 Generate Music";

        } else {

            alert(data.error);

            generateBtn.disabled = false;
            generateBtn.innerText = "🎵 Generate Music";

        }

    }

    catch (error) {

        console.log(error);

        loading.classList.add("hidden");

        generateBtn.disabled = false;
        generateBtn.innerText = "🎵 Generate Music";

        alert("Something went wrong. Please try again.");

    }

});