import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent / (
    "PHARMAGUARD_RESEARCH_ONLY_RF_CANDIDATE.joblib"
)

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH.name}")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully.")
print("Model type:", type(model).__name__)
print("Prediction test: NOT RUN")
print("Research-only; not for clinical use.")
