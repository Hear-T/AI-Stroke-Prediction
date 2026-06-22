from pathlib import Path
import pandas as pd
import xgboost as xgb
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

DATA_PATH = 'data/raw/full_data.csv' 
MODEL_PATH = 'trained_models/xgboost_cdc_stroke_model.pkl'

def main():
    print("1. Đang đọc và làm sạch dữ liệu...")
    df = pd.read_csv(DATA_PATH)
    
    df = df.dropna(subset=['bmi']).reset_index(drop=True)
    X = df.drop(columns=['stroke', 'id'], errors='ignore')
    y = df['stroke']

    X_encoded = pd.get_dummies(X, drop_first=True)
    FEATURE_COLUMNS = list(X_encoded.columns)

    print("2. Đang chia tập Train/Test...")
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42, stratify=y)

    print("3. Đang chạy SMOTE (Phiên bản đã được kìm hãm sự nhạy cảm)...")
    # =========================================================================
    # ĐIỂM NÂNG CẤP TẠI ĐÂY: sampling_strategy = 0.15
    # Tức là: Số lượng mẫu Đột quỵ sẽ bằng 15% số lượng mẫu Khỏe mạnh.
    # (Bạn có thể tăng lên 0.2 hoặc giảm xuống 0.1 để xem điểm số thay đổi)
    # =========================================================================
    smote = SMOTE(sampling_strategy=0.15, random_state=42)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

    print("4. Đang thiết lập Ràng buộc Y khoa (Monotone Constraints)...")
    constraints_dict = {
        'age': 1, 
        'hypertension': 1, 
        'heart_disease': 1, 
        'avg_glucose_level': 1, 
        'bmi': 1,
        'smoking_status_smokes': 1, 
        'smoking_status_formerly smoked': 1,
        'smoking_status_never smoked': -1
    }
    monotone_constraints = tuple(constraints_dict.get(col, 0) for col in FEATURE_COLUMNS)

    print("5. Đang huấn luyện mô hình XGBoost...")
    model = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        random_state=42,
        monotone_constraints=monotone_constraints,
        n_jobs=-1
    )
    
    model.fit(X_train_balanced, y_train_balanced)

    print("\n6. KẾT QUẢ ĐÁNH GIÁ SAU KHI TINH CHỈNH SMOTE:")
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print('Train shape after SMOTE:', X_train_balanced.shape)
    print('ROC-AUC:', round(float(roc_auc_score(y_test, y_proba)), 4))
    print('\nBáo cáo phân loại (Classification Report):')
    print(classification_report(y_test, y_pred, digits=4))

    print("\n7. Đang lưu mô hình...")
    model.save_model(MODEL_PATH)
    print("HOÀN TẤT! Đã lưu mô hình mới.")

if __name__ == '__main__':
    main()