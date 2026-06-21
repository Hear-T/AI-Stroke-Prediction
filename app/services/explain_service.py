import pandas as pd
import numpy as np
import shap

def build_shap_dataframe(model, dataframe, translation_map, drop_feature_names=None, top_n=8):
    # 1. Khởi tạo bộ giải thích SHAP (Tương thích mọi loại model XGBoost)
    booster = model.get_booster() if hasattr(model, 'get_booster') else model
    explainer = shap.TreeExplainer(booster)
    
    # 2. Lấy mảng số học SHAP thuần túy
    raw_shap_values = explainer.shap_values(dataframe)
    
    # 3. Trích xuất đúng mảng 1 chiều chứa rủi ro của ca bệnh hiện tại
    if isinstance(raw_shap_values, list):
        tieu_chuan = raw_shap_values[1][0] if len(raw_shap_values) > 1 else raw_shap_values[0][0]
    else:
        if len(raw_shap_values.shape) == 3:
            tieu_chuan = raw_shap_values[0, :, 1]
        else:
            tieu_chuan = raw_shap_values[0]

    mang_sach = np.array(tieu_chuan, dtype=float).flatten()

    # 4. Khởi tạo DataFrame tổng chứa toàn bộ đặc trưng (bao gồm cả các cột One-hot)
    full_df = pd.DataFrame({
        'Yếu tố': [translation_map.get(col, col) for col in dataframe.columns],
        'Tác động (log-odds)': mang_sach
    })

    # 5. TÍNH TOÁN PHẦN TRĂM ẢNH HƯỞNG TƯƠNG ĐỐI
    # Lấy giá trị tuyệt đối để đo lường "sức nặng" của yếu tố (dù là kéo rủi ro lên hay hạ rủi ro xuống)
    full_df['Độ lớn tuyệt đối'] = full_df['Tác động (log-odds)'].abs()
    
    # Tổng sức mạnh của tất cả các yếu tố cộng lại
    tong_anh_huong = full_df['Độ lớn tuyệt đối'].sum()
    
    # Chia tỷ trọng ra phần trăm (%)
    full_df['% Ảnh hưởng'] = np.where(
        tong_anh_huong > 0, 
        (full_df['Độ lớn tuyệt đối'] / tong_anh_huong) * 100, 
        0
    )
    
    # Gắn thêm nhãn để phân biệt yếu tố này đang bảo vệ hay đe dọa bệnh nhân
    full_df['Phân loại'] = np.where(full_df['Tác động (log-odds)'] > 0, 'Tăng nguy cơ', 'Giảm nguy cơ')

    # 6. Lọc các yếu tố không muốn hiển thị (nếu có)
    if drop_feature_names:
        full_df = full_df[~full_df['Yếu tố'].isin(drop_feature_names)]

    # 7. Sắp xếp giảm dần và chỉ lấy Top N yếu tố quan trọng nhất
    top_table = full_df.sort_values(by='Độ lớn tuyệt đối', ascending=False).head(top_n).reset_index(drop=True)
    
    # Thêm cột Hạng (Rank) cho chuyên nghiệp
    top_table.insert(0, 'Hạng', np.arange(1, len(top_table) + 1))
    
    # 8. Đảo ngược lại bảng để dùng cho hàm vẽ biểu đồ thanh ngang (barh plot)
    plot_df_reversed = top_table.iloc[::-1].reset_index(drop=True)
    
    # Trả về cả bảng xuôi (để hiển thị số) và bảng ngược (để vẽ đồ thị)
    return {
        'table': top_table,
        'plot_df': plot_df_reversed
    }