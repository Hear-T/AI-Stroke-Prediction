def predict_probability_percent(model, dataframe):
    return float(model.predict_proba(dataframe)[0][1] * 100)


def classify_cdc_risk(probability: float):
    if probability >= 20:
        return "high", f"🚨 **CẢNH BÁO ĐỎ: NGUY CƠ RẤT CAO ({probability:.2f}%)**"
    if probability >= 10:
        return "medium", f"⚠️ **CẢNH BÁO VÀNG: NGUY CƠ TRUNG BÌNH ({probability:.2f}%)**"
    return "low", f"✅ **AN TOÀN: NGUY CƠ THẤP ({probability:.2f}%)**"
