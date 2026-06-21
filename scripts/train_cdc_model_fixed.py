from pathlib import Path
import json

import joblib
import pandas as pd
import xgboost as xgb
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / 'data' / 'raw' / 'heart_disease_health_indicators_BRFSS2015.csv'
MODEL_PATH = ROOT_DIR / 'trained_models' / 'xgboost_cdc_stroke_model.pkl'

TARGET = 'Stroke'
FEATURE_COLUMNS = [
    # app/utils/translations.py

KAGGLE_FEATURE_TRANSLATIONS = {
    'age': 'Tuổi tác',
    'hypertension': 'Huyết áp cao (1=Có, 0=Không)',
    'heart_disease': 'Bệnh tim mạch (1=Có, 0=Không)',
    'avg_glucose_level': 'Mức đường huyết trung bình',
    'bmi': 'Chỉ số khối cơ thể (BMI)',
    'gender_Male': 'Giới tính (Nam)',
    'gender_Other': 'Giới tính (Khác)',
    'ever_married_Yes': 'Đã từng kết hôn',
    'work_type_Never_worked': 'Công việc: Chưa từng làm',
    'work_type_Private': 'Công việc: Tư nhân',
    'work_type_Self-employed': 'Công việc: Làm tự do',
    'work_type_children': 'Đối tượng: Trẻ em',
    'Residence_type_Urban': 'Khu vực sống: Thành thị',
    'smoking_status_formerly smoked': 'Từng hút thuốc (Đã bỏ)',
    'smoking_status_never smoked': 'Chưa bao giờ hút thuốc',
    'smoking_status_smokes': 'Đang hút thuốc thường xuyên'
}
]

# 1 = khi tăng feature thì nguy cơ không được giảm
# -1 = khi tăng feature thì nguy cơ không được tăng
# 0 = không ép ràng buộc
MONOTONE_BY_FEATURE = {
    'HeartDiseaseorAttack': 1,
    'HighBP': 1,
    'HighChol': 1,
    'CholCheck': 0,
    'BMI': 1,
    'Smoker': 1,
    'Diabetes': 1,
    'PhysActivity': -1,
    'Fruits': -1,
    'Veggies': -1,
    'HvyAlcoholConsump': 1,
    'AnyHealthcare': 0,
    'NoDocbcCost': 1,
    'GenHlth': 1,
    'MentHlth': 1,
    'PhysHlth': 1,
    'DiffWalk': 1,
    'Sex': 0,
    'Age': 1,
    'Education': -1,
    'Income': -1,
}


def main():
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURE_COLUMNS]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    smote = SMOTE(random_state=42)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

    monotone_constraints = tuple(MONOTONE_BY_FEATURE[col] for col in FEATURE_COLUMNS)

    model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric='logloss',
        random_state=42,
        monotone_constraints=monotone_constraints,
    )

    model.fit(X_train_balanced, y_train_balanced)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print('=== CDC STROKE MODEL (FIXED PIPELINE) ===')
    print('Train shape after SMOTE:', X_train_balanced.shape)
    print('Test shape:', X_test.shape)
    print('Monotone constraints:', json.dumps(MONOTONE_BY_FEATURE, ensure_ascii=False))
    print('ROC-AUC:', round(float(roc_auc_score(y_test, y_proba)), 4))
    print(classification_report(y_test, y_pred, digits=4))

    joblib.dump(model, MODEL_PATH)
    print(f'Saved model to: {MODEL_PATH}')


if __name__ == '__main__':
    main()
