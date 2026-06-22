import streamlit as st

from app.models_ai.cdc_stroke_model import load_cdc_stroke_model
from app.services.advice_service import generate_cdc_advice
# Bổ sung import hàm vẽ biểu đồ ngang cho SHAP
from app.services.chart_service import create_cdc_gauge_chart, create_horizontal_impact_chart
from app.services.prediction_service import classify_cdc_risk, predict_probability_percent
from app.services.preprocess_service import build_cdc_stroke_dataframe
from app.services.explain_service import build_shap_dataframe

DEFAULT_GEN_HLTH = 3
DEFAULT_NO_DOC_COST = False
DEFAULT_ANY_HEALTHCARE = True

# ==========================================
# BƯỚC 1: KHAI BÁO TỪ ĐIỂN DỊCH THUẬT Ở ĐẦU FILE
# ==========================================
KAGGLE_FEATURE_TRANSLATIONS = {
    'age': 'Tuổi tác',
    'hypertension': 'Huyết áp cao',
    'heart_disease': 'Bệnh tim mạch',
    'avg_glucose_level': 'Mức đường huyết',
    'bmi': 'Chỉ số BMI',
    'gender': 'Giới tính',                   
    'ever_married': 'Đã kết hôn',            
    'Residence_type': 'Khu vực sống',        
    'work_type_Private': 'Công việc: Tư nhân',
    'work_type_Self-employed': 'Công việc: Tự do',
    'work_type_children': 'Công việc: Trẻ em',
    'smoking_status_formerly smoked': 'Từng hút thuốc',
    'smoking_status_never smoked': 'Chưa bao giờ hút',
    'smoking_status_smokes': 'Đang hút thuốc'
}

def render_cdc_stroke_page():
    st.title("🏥 Trợ Lý AI Dự Đoán Nguy Cơ Đột Quỵ")
    st.markdown("*Hệ thống phân tích dựa trên dữ liệu Y tế 11 Đặc trưng cốt lõi.*")
    st.markdown("---")

    model = load_cdc_stroke_model()

    with st.form("patient_form"):
        st.subheader("📋 Điền thông tin Sức khỏe & Lối sống")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔹 Sinh tồn & Bệnh lý**")
            age = st.number_input("Tuổi tác", min_value=0.0, max_value=120.0, value=45.0, step=1.0)
            # SỬA LẠI: Dùng format_func để UI hiện tiếng Việt nhưng ngầm lưu tiếng Anh
            gender = st.selectbox("Giới tính", ["Male", "Female"], format_func=lambda x: "Nam" if x == "Male" else "Nữ")
            hypertension = st.selectbox("Có bệnh Cao Huyết Áp?", ["Không", "Có"])
            heart_disease = st.selectbox("Có Tiền sử Bệnh Tim mạch?", ["Không", "Có"])
            avg_glucose_level = st.number_input("Đường huyết trung bình (mg/dL)", min_value=40.0, max_value=300.0, value=100.0)

        with col2:
            st.markdown("**🔹 Thể trạng & Xã hội**")
            bmi = st.number_input("Chỉ số khối cơ thể (BMI)", min_value=10.0, max_value=80.0, value=25.0)
            smoking_status = st.selectbox(
                "Tình trạng hút thuốc", 
                ["never smoked", "formerly smoked", "smokes", "Unknown"],
                format_func=lambda x: {
                    "never smoked": "Chưa bao giờ hút",
                    "formerly smoked": "Đã từng hút (Nay đã bỏ)",
                    "smokes": "Đang hút thuốc",
                    "Unknown": "Không rõ thông tin"
                }.get(x)
            )
            ever_married = st.selectbox("Đã từng kết hôn chưa?", ["Yes", "No"], 
                                        format_func=lambda x: "Rồi" if x == "Yes" else "Chưa")
            work_type = st.selectbox(
                "Loại công việc", 
                ["Private", "Self-employed", "Govt_job", "children", "Never_worked"],
                format_func=lambda x: {
                    "Private": "Khối Tư nhân",
                    "Self-employed": "Làm nghề Tự do",
                    "Govt_job": "Viên chức Nhà nước",
                    "children": "Trẻ em / Học sinh",
                    "Never_worked": "Chưa từng làm việc"
                }.get(x)
            )
            residence_type = st.selectbox("Khu vực sinh sống", ["Urban", "Rural"],
                                          format_func=lambda x: "Thành thị (Urban)" if x == "Urban" else "Nông thôn (Rural)")

        submitted = st.form_submit_button("🔍 Yêu cầu AI Phân tích Nguy cơ", use_container_width=True)

    # TẤT CẢ CODE TỪ ĐÂY ĐỀU PHẢI NẰM THỤT LỀ BÊN TRONG KHỐI LỆNH IF NÀY
    if submitted:
        # ==========================================
        # BƯỚC QUAN TRỌNG: XÓA DỮ LIỆU CŨ (NẾU CÓ)
        # ==========================================
        if 'user_data' in st.session_state:
            del st.session_state['user_data']
        form_values = {
            'gender': gender,
            'age': age,
            'hypertension': hypertension,
            'heart_disease': heart_disease,
            'ever_married': ever_married,
            'work_type': work_type,
            'residence_type': residence_type,  
            'avg_glucose_level': avg_glucose_level,
            'bmi': bmi,
            'smoking_status': smoking_status
        }
        
        input_df = build_cdc_stroke_dataframe(form_values)
        probability = predict_probability_percent(model, input_df)
        
        st.session_state.user_data = {
            'probability': round(probability, 2), 
            'gender': gender,
            'age': age,
            'hypertension': 1 if hypertension == "Có" else 0,
            'heart_disease': 1 if heart_disease == "Có" else 0,
            'ever_married': ever_married,
            'work_type': work_type,
            'Residence_type': residence_type,
            'avg_glucose_level': avg_glucose_level,
            'bmi': bmi,
            'smoking_status': smoking_status
        }

        # 1. BIỂU ĐỒ GAUGE & CẢNH BÁO
        st.markdown("---")
        st.subheader("📊 KẾT QUẢ DỰ ĐOÁN TỪ HỆ THỐNG AI")
        st.plotly_chart(create_cdc_gauge_chart(probability), use_container_width=True)
        level, message = classify_cdc_risk(probability)
        
        if level == 'high':
            st.error(message)
            st.write(
                "Dựa trên các chỉ số y tế lâm sàng, hệ thống nhận thấy rủi ro đột quỵ của bạn cao gấp nhiều lần "
                "người bình thường. Cần lập tức can thiệp y tế!"
            )
        elif level == 'medium':
            st.warning(message)
            st.write("Bạn đang có các yếu tố nguy cơ tích tụ. Hãy chú ý thay đổi lối sống ngay từ bây giờ.")
        else:
            st.success(message)
            st.write("Chúc mừng! Các chỉ số sức khỏe của bạn đang ở mức an toàn.")

        # 2. LỜI KHUYÊN CÁ NHÂN HÓA
        st.markdown("---")
        st.subheader("🩺 Giải thích nguyên nhân & Lời khuyên Cá nhân hóa")
        advice = generate_cdc_advice(form_values)
        if advice:
            st.write("Dựa trên hồ sơ y tế bạn vừa nhập, hệ thống tự động trích xuất các lưu ý sau:")
            for item in advice:
                st.info(item)
        else:
            st.success(
                "🌟 Thật tuyệt vời! Hồ sơ của bạn không có yếu tố rủi ro bệnh lý hay thói quen xấu nào nổi bật. "
                "Hãy tiếp tục duy trì lối sống lành mạnh này nhé!"
            )

        # 3. TRÍ TUỆ NHÂN TẠO MINH BẠCH (SHAP XAI) - BỔ SUNG
        st.markdown("---")
        st.subheader("🧠 Trí tuệ Nhân tạo Minh bạch (SHAP XAI)")
        
        # Gọi hàm tạo data SHAP (Top 5 yếu tố ảnh hưởng mạnh nhất)
        shap_data = build_shap_dataframe(
            model=model, 
            dataframe=input_df, 
            translation_map=KAGGLE_FEATURE_TRANSLATIONS,
            
        )
        
        # In bảng số liệu
        st.dataframe(
            shap_data['table'][['Hạng', 'Yếu tố', '% Ảnh hưởng', 'Phân loại']], 
            use_container_width=True
        )
        
        # Vẽ biểu đồ thanh ngang minh họa
        fig = create_horizontal_impact_chart(shap_data['plot_df'], "Mức độ tác động của các yếu tố sinh lý")
        st.pyplot(fig)