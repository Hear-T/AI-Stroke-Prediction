import joblib

from app.config import CDC_MODEL_PATH

try:
    import streamlit as st
except ModuleNotFoundError:
    st = None


def _load_model():
    return joblib.load(CDC_MODEL_PATH)


if st is not None:
    load_cdc_stroke_model = st.cache_resource(_load_model)
else:
    def load_cdc_stroke_model():
        return _load_model()
