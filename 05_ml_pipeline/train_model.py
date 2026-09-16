"""
Training Script for ML Inference Pipeline
----------------------------------------
Trains a classification pipeline (StandardScaler + LogisticRegression)
on the Iris dataset and exports the serialized model artifact.
"""

import os
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

DEFAULT_MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
DEFAULT_MODEL_PATH = os.path.join(DEFAULT_MODELS_DIR, "model.joblib")


def train_and_save_pipeline(output_path=DEFAULT_MODEL_PATH):
    print("Loading Iris dataset...")
    data = load_iris()
    X, y = data.data, data.target
    feature_names = data.feature_names
    target_names = list(data.target_names)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Build scikit-learn pipeline
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=200, random_state=42))
    ])

    print("Training pipeline...")
    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model test accuracy: {accuracy:.4f}")

    # Package metadata alongside model pipeline
    model_artifact = {
        "pipeline": pipeline,
        "feature_names": feature_names,
        "target_names": target_names,
        "version": "1.0.0",
        "accuracy": accuracy
    }

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    joblib.dump(model_artifact, output_path)
    print(f"Pipeline successfully saved to {output_path}")
    return model_artifact


if __name__ == "__main__":
    train_and_save_pipeline()
