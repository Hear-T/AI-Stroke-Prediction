import pandas as pd
import numpy as np
import shap

def build_shap_dataframe(model, dataframe, translation_map, drop_feature_names=None, top_n=8):
    # 1. Khởi tạo bộ giải thích SHAP
    booster = model.get_booster()
    explainer = shap.TreeExplainer(booster)
    
    # 2. BÍ QUYẾT: Dùng .shap_values() để lấy mảng số học thuần túy (Numpy Array)
    # Bỏ qua hoàn toàn các đối tượng phức tạp gây lỗi định dạng
    raw_shap_values = explainer.shap_values(dataframe)
    
    # 3. Trích xuất đúng mảng 1 chiều chứa rủi ro của bệnh nhân hiện tại
    if isinstance(raw_shap_values, list):
        # Nếu mô hình trả về dạng list (Mô hình nhị phân cũ)
        tieu_chuan = raw_shap_values[1][0] if len(raw_shap_values) > 1 else raw_shap_values[0][0]
    else:
        # Nếu mô hình trả về dạng ma trận
        if len(raw_shap_values.shape) == 3:
            tieu_chuan = raw_shap_values[0, :, 1]
        else:
            tieu_chuan = raw_shap_values[0]

    # 4. Ép kiểu an toàn, đảm bảo 100% là số thực
    mang_sach = np.array(tieu_chuan, dtype=float).flatten()

    # 5. Khởi tạo DataFrame siêu sạch
    plot_df = pd.DataFrame({
        'Yếu tố': [translation_map.get(col, col) for col in dataframe.columns],
        'Tác động': mang_sach
    })

    # 6. Lọc các yếu tố không muốn hiển thị
    if drop_feature_names:
        plot_df = plot_df[~plot_df['Yếu tố'].isin(drop_feature_names)]

    # 7. Sắp xếp lấy top N yếu tố tác động mạnh nhất (cả âm lẫn dương)
    plot_df['Độ lớn tuyệt đối'] = plot_df['Tác động'].abs()
    plot_df = plot_df.sort_values(by='Độ lớn tuyệt đối', ascending=True).tail(top_n)
    
    return plot_df