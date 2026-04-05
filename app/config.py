from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
TRAINED_MODELS_DIR = ROOT_DIR / "trained_models"

CDC_MODEL_PATH = TRAINED_MODELS_DIR / "xgboost_cdc_stroke_model.pkl"
