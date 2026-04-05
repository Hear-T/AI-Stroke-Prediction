from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.models_ai.cdc_stroke_model import load_cdc_stroke_model
from app.services.prediction_service import predict_probability_percent
from app.services.preprocess_service import build_cdc_stroke_dataframe


def main():
    cdc_form = {
        'age_group': '65-69',
        'sex': 'Nam',
        'bmi': 31,
        'high_bp': True,
        'high_chol': True,
        'heart_disease': True,
        'diabetes': 'Đang bị Tiểu đường',
        'smoking_status': 'Hút thường xuyên / Lâu năm',
        'hvy_alcohol': False,
        'phys_activity': False,
        'fruits': False,
        'veggies': False,
        'chol_check': True,
        'diff_walk': True,
        'phys_hlth': 10,
        'ment_hlth': 7,
        'education': 3,
        'income': 3,
        'any_healthcare': True,
        'no_doc_cost': False,
        'gen_hlth': 4,
    }

    cdc_model = load_cdc_stroke_model()
    cdc_df = build_cdc_stroke_dataframe(cdc_form)

    print('CDC model probability (%):', round(predict_probability_percent(cdc_model, cdc_df), 2))


if __name__ == '__main__':
    main()
