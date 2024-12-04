from flask import Flask, request, jsonify
import joblib
import numpy as np
import librosa
import io
import base64
import pickle
import pandas as pd

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Load the trained SVM model
model = joblib.load('svm_model.pkl')

# Load the saved MinMaxScaler
with open('min_max_scaler.pkl', 'rb') as file:
    min_max_scaler = pickle.load(file)



def extract_features(audio_base64):
    """
    Extract features from a Base64-encoded audio file and scale them for the model.
    """

    # Decode Base64 to bytes
    audio_data = base64.b64decode(audio_base64)
    # Charger le fichier audio
    y, sr = librosa.load(io.BytesIO(audio_data), sr=None)

# Calculer la durée nécessaire pour avoir exactement 66149 échantillons
    target_samples = 66149
    duration = target_samples / sr

# Définir les temps de début et de fin en fonction de cette durée
    start_time = 5  # En secondes
    end_time = start_time + duration

# Calculer les indices des échantillons
    start_sample = int(start_time * sr)
    end_sample = start_sample + target_samples  # end_sample calculé pour avoir exactement 66149 échantillons

# Extraire le segment
    y_3sec = y[start_sample:end_sample]
    
    # Feature extraction
    chroma_stft = librosa.feature.chroma_stft(y=y_3sec, sr=sr)
    rms = librosa.feature.rms(y=y_3sec)
    spectral_centroid = librosa.feature.spectral_centroid(y=y_3sec)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y_3sec)
    rolloff = librosa.feature.spectral_rolloff(y=y_3sec)
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y=y_3sec)
    harmony = librosa.effects.harmonic(y_3sec)
    perceptr = librosa.effects.percussive(y_3sec)
    tempo, _ = librosa.beat.beat_track(y=y_3sec, sr=sr)
    mfccs = librosa.feature.mfcc(y=y_3sec, sr=sr, n_mfcc=20)
    audio_length = 66149
    # Feature processing
    features = np.hstack([
        [len(y_3sec)],  # Audio length in samples
        np.mean(chroma_stft), np.var(chroma_stft),
        np.mean(rms), np.var(rms),
        np.mean(spectral_centroid), np.var(spectral_centroid),
        np.mean(spectral_bandwidth), np.var(spectral_bandwidth),
        np.mean(rolloff), np.var(rolloff),
        np.mean(zero_crossing_rate), np.var(zero_crossing_rate),
        np.mean(harmony), np.var(harmony),
        np.mean(perceptr), np.var(perceptr),
        tempo
    ])

    # Add MFCC mean and variance
    mfcc_mean = np.mean(mfccs, axis=1)
    mfcc_var = np.var(mfccs, axis=1)
    mfcc_features = np.hstack([np.array(val) for pair in zip(mfcc_mean, mfcc_var) for val in pair])
    features = np.hstack([features, mfcc_features])

    # Scale the features
    features_df = pd.DataFrame([features], columns=min_max_scaler.feature_names_in_)
    features_scaled = min_max_scaler.transform(features_df)

    # return features_scaled[0]
    print(f"Taille du segment : {len(y_3sec)} échantillons")

    return features_scaled


@app.route('/svm_service', methods=['POST'])
def classify_genre():
    print("1")
    print("Received POST request:", request.json) 
    data = request.get_json()

    if 'audio_base64' not in data:
        return jsonify({"error": "Missing 'audio_base64' key"}), 400

    audio_base64 = data['audio_base64']

    try:
        # Extract and scale features
        features = extract_features(audio_base64)
        features_df = pd.DataFrame(features, columns=min_max_scaler.feature_names_in_)

        print(features_df)

        # Predict genre
        prediction = model.predict(features_df)
        print('ok2')
        print(f"Predicted genre: {prediction[0]}")
        
        

        return jsonify({"genre": prediction[0]})

    except Exception as e:
        return jsonify({"error": f"Error processing the audio: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
