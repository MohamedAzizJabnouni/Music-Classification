from flask import Flask, request, jsonify
import joblib
import numpy as np
import librosa
import io
import base64
import pickle
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained VGG19 model
vgg = joblib.load('vgg19.pkl')  # Assuming the model is saved as 'vgg19.pkl'


def extract_features(audio_base64):
    """
    Extract Mel spectrogram features from a Base64-encoded audio file and prepare them for model prediction.
    """
    # Decode Base64 to bytes
    audio_data = base64.b64decode(audio_base64)

    # Load the audio file using librosa
    y, sr = librosa.load(io.BytesIO(audio_data), sr=None)

    # Generate Mel spectrogram from audio signal
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=512, n_mels=128)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

    # Create the Mel spectrogram image
    fig, ax = plt.subplots(figsize=(10, 4))
    librosa.display.specshow(mel_spec_db, sr=sr, hop_length=512, x_axis='time', y_axis='mel', cmap='magma')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    plt.tight_layout()

    # Save the plot to an in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    plt.close(fig)
    buf.seek(0)

    # Convert the in-memory image to RGB, resize it to (224, 224), and normalize
    img = Image.open(buf).convert("RGB").resize((224, 224))
    img_array = img_to_array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Close the buffer
    buf.close()

    return img_array


@app.route('/vgg19_service', methods=['POST'])
def classify_genre():
    print("Received POST request:", request.json)

    data = request.get_json()

    if 'audio_base64' not in data:
        return jsonify({"error": "Missing 'audio_base64' key"}), 400

    audio_base64 = data['audio_base64']

    try:
        # Extract and preprocess the Mel spectrogram features
        features = extract_features(audio_base64)

        # Make the prediction with the model
        prediction = vgg.predict(features)

        # Get the class with the highest probability
        predicted_class = np.argmax(prediction, axis=1)

        # Define the genre labels (ensure they match the model's output)
        class_labels = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
        predicted_genre = class_labels[predicted_class[0]]

        print(f"Predicted genre: {predicted_genre}")

        return jsonify({"genre": predicted_genre})

    except Exception as e:
        return jsonify({"error": f"Error processing the audio: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
