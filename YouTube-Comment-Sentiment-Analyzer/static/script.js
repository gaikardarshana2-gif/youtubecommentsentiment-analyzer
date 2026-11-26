async function analyzeComment() {

    const commentInput = document.getElementById("comment");
    const resultBox = document.getElementById("result");
    const errorBox = document.getElementById("error");

    const comment = commentInput.value.trim();

    errorBox.style.display = "none";

    if (!comment) {
        errorBox.innerText = "Please enter a YouTube comment.";
        errorBox.style.display = "block";
        resultBox.style.display = "none";
        return;
    }

    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                comment: comment
            })
        });


        const data = await response.json();


        if (!response.ok) {
            throw new Error(
                data.error || "Unable to analyze comment."
            );
        }


        document.getElementById("sentiment").innerText =
            data.emoji + " " + data.sentiment;


        document.getElementById("compound").innerText =
            data.compound;


        document.getElementById("positive").innerText =
            data.positive + "%";


        document.getElementById("negative").innerText =
            data.negative + "%";


        document.getElementById("commentText").innerText =
            data.comment;


        resultBox.style.display = "block";

    }

    catch (error) {

        errorBox.innerText =
            "Server error. Please make sure the Flask server is running.";

        errorBox.style.display = "block";

        resultBox.style.display = "none";
    }
}