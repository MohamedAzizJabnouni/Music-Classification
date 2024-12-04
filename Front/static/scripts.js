async function submitFile() {
    const fileInput = document.getElementById('musicFile');
    const file = fileInput.files[0];
    const loading = document.getElementById('loading');
    const resultDiv = document.getElementById('result');

    if (!file) {
        alert("Please select a file.");
        return;
    }

    loading.style.display = 'block'; // Show loading circle
    resultDiv.innerText = ''; // Clear any previous result

    const reader = new FileReader();
    reader.onloadend = async function () {
        const base64File = reader.result.split(',')[1]; // Remove the data URL part
        const data = { "audio_base64": base64File };

        try {
            const response = await fetch('http://localhost:5000/svm_service', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();
            if (response.ok) {
                resultDiv.innerText = "Predicted Genre: " + result.genre;
            } else {
                resultDiv.innerText = "Error: " + result.error;
            }
        } catch (error) {
            resultDiv.innerText = "Error: " + error.message;
        } finally {
            loading.style.display = 'none'; // Hide loading circle
        }
    };

    reader.readAsDataURL(file);
}

async function submitFile_VGG19() {
    const fileInput = document.getElementById('musicFile');
    const file = fileInput.files[0];
    const loading = document.getElementById('loading');
    const resultDiv = document.getElementById('result');

    if (!file) {
        alert("Please select a file.");
        return;
    }

    loading.style.display = 'block'; // Show loading circle
    resultDiv.innerText = ''; // Clear any previous result

    const reader = new FileReader();
    reader.onloadend = async function () {
        const base64File = reader.result.split(',')[1]; // Remove the data URL part
        const data = { "audio_base64": base64File };

        try {
            const response = await fetch('http://localhost:3000/vgg19_service', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();
            if (response.ok) {
                resultDiv.innerText = "Predicted Genre: " + result.genre;
            } else {
                resultDiv.innerText = "Error: " + result.error;
            }
        } catch (error) {
            resultDiv.innerText = "Error: " + error.message;
        } finally {
            loading.style.display = 'none'; // Hide loading circle
        }
    };

    reader.readAsDataURL(file);
}
