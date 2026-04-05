import pandas as pd


CDC_AGE_MAPPING = {
    "18-24": 1,
    "25-29": 2,
    "30-34": 3,
    "35-39": 4,
    "40-44": 5,
    "45-49": 6,
    "50-54": 7,
    "55-59": 8,
    "60-64": 9,
    "65-69": 10,
    "70-74": 11,
    "75-79": 12,
    "Từ 80 trở lên": 13,
}

CDC_DIABETES_MAPPING = {
    "Không bị": 0,
    "Tiền tiểu đường": 1,
    "Đang bị Tiểu đường": 2,
}

CDC_CURRENT_SMOKER_OPTIONS = {
    "Đang hút thỉnh thoảng",
    "Hút thường xuyên / Lâu năm",
    "Đang hút hằng ngày",
}


def build_cdc_stroke_dataframe(form_values: dict) -> pd.DataFrame:
    smoking_status = form_values['smoking_status']
    is_current_smoker = 1 if smoking_status in CDC_CURRENT_SMOKER_OPTIONS else 0

    input_data = {
        'HeartDiseaseorAttack': [1 if form_values['heart_disease'] else 0],
        'HighBP': [1 if form_values['high_bp'] else 0],
        'HighChol': [1 if form_values['high_chol'] else 0],
        'CholCheck': [1 if form_values['chol_check'] else 0],
        'BMI': [form_values['bmi']],
        'Smoker': [is_current_smoker],
        'Diabetes': [CDC_DIABETES_MAPPING[form_values['diabetes']]],
        'PhysActivity': [1 if form_values['phys_activity'] else 0],
        'Fruits': [1 if form_values['fruits'] else 0],
        'Veggies': [1 if form_values['veggies'] else 0],
        'HvyAlcoholConsump': [1 if form_values['hvy_alcohol'] else 0],
        'AnyHealthcare': [1 if form_values['any_healthcare'] else 0],
        'NoDocbcCost': [1 if form_values['no_doc_cost'] else 0],
        'GenHlth': [form_values.get('gen_hlth', 3)],
        'MentHlth': [form_values['ment_hlth']],
        'PhysHlth': [form_values['phys_hlth']],
        'DiffWalk': [1 if form_values['diff_walk'] else 0],
        'Sex': [1 if form_values['sex'] == "Nam" else 0],
        'Age': [CDC_AGE_MAPPING[form_values['age_group']]],
        'Education': [form_values['education']],
        'Income': [form_values['income']],
    }
    return pd.DataFrame(input_data)
