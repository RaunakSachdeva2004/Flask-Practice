"""
ML Inference Pipeline in Flask
------------------------------
This module demonstrates MLOps best practices for serving ML models via Flask:
1. Loading serialized model artifacts once at startup (in-memory caching).
2. Health-check and model metadata endpoints (/health, /metadata).
3. Robust input validation with custom HTTP error handling.
4. Single-instance (/predict) and batch-instance (/predict_batch) inference.
5. Returning predictions with class labels, confidence scores, and inference latency.
"""

import os
import sys
import time
import joblib
import numpy as np
from flask import Flask, jsonify, request, abort

# Ensure imports resolve whether running from project root or inside 05_ml_pipeline/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from train_model import train_and_save_pipeline, DEFAULT_MODEL_PATH

app = Flask(__name__)

# Global model container (loaded once on startup)
MODEL_ARTIFACT = None


def get_model():
    """Load the model pipeline once into memory, training on the fly if needed."""
    global MODEL_ARTIFACT
    if MODEL_ARTIFACT is None:
        if not os.path.exists(DEFAULT_MODEL_PATH):
            print(f"Artifact {DEFAULT_MODEL_PATH} not found. Generating model artifact...")
            train_and_save_pipeline(DEFAULT_MODEL_PATH)
        MODEL_ARTIFACT = joblib.load(DEFAULT_MODEL_PATH)
        print("ML Pipeline loaded successfully into memory.")
    return MODEL_ARTIFACT


# Ensure model is ready when the app initializes
with app.app_context():
    get_model()


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "ML Inference Pipeline API",
        "status": "online",
        "endpoints": {
            "health": "GET /health",
            "metadata": "GET /metadata",
            "predict_single": "POST /predict",
            "predict_batch": "POST /predict_batch"
        },
        "sample_input": {
            "features": [5.1, 3.5, 1.4, 0.2]
        }
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for Kubernetes, Docker, or load balancers."""
    model = get_model()
    is_ready = model is not None and "pipeline" in model
    return jsonify({
        "status": "healthy" if is_ready else "unhealthy",
        "model_loaded": is_ready
    }), 200 if is_ready else 503


@app.route("/metadata", methods=["GET"])
def metadata():
    """Returns model version and expected feature specifications."""
    artifact = get_model()
    return jsonify({
        "model_version": artifact.get("version"),
        "expected_features": artifact.get("feature_names"),
        "num_features": len(artifact.get("feature_names", [])),
        "classes": artifact.get("target_names"),
        "test_accuracy": artifact.get("accuracy")
    }), 200


def validate_features(feature_list, expected_count):
    """Validates that features are a list of numbers with the correct length."""
    if not isinstance(feature_list, list):
        return False, "Features must be provided as a list of numbers."
    if len(feature_list) != expected_count:
        return False, f"Expected exactly {expected_count} numerical features, received {len(feature_list)}."
    try:
        float_features = [float(x) for x in feature_list]
        return True, float_features
    except (ValueError, TypeError):
        return False, "All feature values must be numeric."


@app.route("/predict", methods=["POST"])
def predict():
    """
    Single-instance inference endpoint.
    Expected JSON payload:
    {
        "features": [5.1, 3.5, 1.4, 0.2]
    }
    """
    start_time = time.perf_counter()
    data = request.get_json()

    if not data or "features" not in data:
        return jsonify({
            "error": "Bad Request",
            "message": "Missing 'features' key in JSON payload."
        }), 400

    artifact = get_model()
    expected_len = len(artifact["feature_names"])
    valid, result_or_err = validate_features(data["features"], expected_len)

    if not valid:
        return jsonify({
            "error": "Validation Error",
            "message": result_or_err
        }), 400

    try:
        pipeline = artifact["pipeline"]
        features_array = np.array([result_or_err])
        
        # Predict class & probabilities
        prediction_id = int(pipeline.predict(features_array)[0])
        predicted_class = artifact["target_names"][prediction_id]
        
        probabilities = pipeline.predict_proba(features_array)[0]
        confidence = float(np.max(probabilities))
        class_probabilities = {
            cls_name: round(float(prob), 4)
            for cls_name, prob in zip(artifact["target_names"], probabilities)
        }

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return jsonify({
            "predicted_class": predicted_class,
            "class_id": prediction_id,
            "confidence": round(confidence, 4),
            "probabilities": class_probabilities,
            "latency_ms": latency_ms,
            "model_version": artifact.get("version")
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Inference Error",
            "message": str(e)
        }), 500


@app.route("/predict_batch", methods=["POST"])
def predict_batch():
    """
    Batch inference endpoint for high-throughput requests.
    Expected JSON payload:
    {
        "instances": [
            [5.1, 3.5, 1.4, 0.2],
            [6.7, 3.0, 5.2, 2.3]
        ]
    }
    """
    start_time = time.perf_counter()
    data = request.get_json()

    if not data or "instances" not in data or not isinstance(data["instances"], list):
        return jsonify({
            "error": "Bad Request",
            "message": "Expected JSON payload with 'instances' list."
        }), 400

    instances = data["instances"]
    if len(instances) == 0:
        return jsonify({
            "error": "Bad Request",
            "message": "'instances' list cannot be empty."
        }), 400

    artifact = get_model()
    expected_len = len(artifact["feature_names"])
    validated_instances = []

    for idx, inst in enumerate(instances):
        valid, val_or_err = validate_features(inst, expected_len)
        if not valid:
            return jsonify({
                "error": "Validation Error",
                "message": f"Instance at index {idx} invalid: {val_or_err}"
            }), 400
        validated_instances.append(val_or_err)

    try:
        pipeline = artifact["pipeline"]
        features_array = np.array(validated_instances)
        
        preds = pipeline.predict(features_array)
        probs = pipeline.predict_proba(features_array)

        results = []
        for i, (pred_id, prob_arr) in enumerate(zip(preds, probs)):
            pred_id = int(pred_id)
            results.append({
                "instance_index": i,
                "predicted_class": artifact["target_names"][pred_id],
                "confidence": round(float(np.max(prob_arr)), 4)
            })

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return jsonify({
            "count": len(results),
            "predictions": results,
            "latency_ms": latency_ms
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Inference Error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
