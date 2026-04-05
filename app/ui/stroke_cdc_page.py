import matplotlib.pyplot as plt
import streamlit as st

from app.models_ai.cdc_stroke_model import load_cdc_stroke_model
from app.services.advice_service import generate_cdc_advice
from app.services.chart_service import create_cdc_gauge_chart, create_horizontal_impact_chart
from app.services.explain_service import build_shap_dataframe
from app.services.prediction_service import classify_cdc_risk, predict_probability_percent
from app.services.preprocess_service import build_cdc_stroke_dataframe
from app.utils.translations import CDC_FEATURE_TRANSLATIONS


GEN_HLTH_OPTIONS = {
    "Rất tốt": 1,
    "Tốt": 2,
    "Bình thường": 3,
    "Kém": 4,
    "Rất kém": 5,
}


def render_cdc_stroke_page():
    st.title("🏥 Trợ Lý AI Chẩn Đoán Đột Quỵ (CDC Y tế)")
    st.markdown("*Hệ thống phân tích dựa trên dữ liệu CDC/BRFSS.*")
    st.info(
        "Lưu ý: mô hình CDC hiện tại chỉ hiểu biến hút thuốc theo kiểu nhị phân: "
        "đang hút hiện tại / không hút hiện tại. Vì vậy 'đã cai thuốc' sẽ được xếp cùng nhóm 'không hút hiện tại'."
    )
    st.markdown("---")

    model = load_cdc_stroke_model()

    with st.form("patient_form"):
        st.subheader("📋 Điền thông tin Sức khỏe & Lối sống")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**🔹 Sinh tồn & Bệnh lý**")
            age_group = st.selectbox(
                "Độ tuổi",
                [
                    "18-24", "25-29", "30-34", "35-39", "40-44", "45-49",
                    "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "Từ 80 trở lên",
                ],
            )
            sex = st.radio("Giới tính", ["Nữ", "Nam"])
            bmi = st.number_input("Chỉ số khối cơ thể (BMI)", min_value=10, max_value=90, value=25)
            high_bp = st.checkbox("Có bệnh Cao Huyết Áp")
            high_chol = st.checkbox("Có mức Cholesterol Cao")
            heart_disease = st.checkbox("Có Tiền sử Bệnh Tim mạch")
            diabetes = st.selectbox("Tình trạng Tiểu đường", ["Không bị", "Tiền tiểu đường", "Đang bị Tiểu đường"])
        with col2:
            st.markdown("**🔹 Thói quen Lối sống**")
            smoking_status = st.selectbox(
                "Tình trạng hút thuốc",
                [
                    "Chưa bao giờ hút",
                    "Đã cai thuốc (trước đây có hút)",
                    "Đang hút thỉnh thoảng",
                    "Hút thường xuyên / Lâu năm",
                ],
            )
            hvy_alcohol = st.checkbox("Uống nhiều Rượu Bia")
            phys_activity = st.checkbox("Có Vận động thể chất (trong 30 ngày qua)")
            fruits = st.checkbox("Ăn trái cây mỗi ngày")
            veggies = st.checkbox("Ăn rau củ mỗi ngày")
            chol_check = st.checkbox("Đã kiểm tra mỡ máu trong 5 năm qua", value=True)
            diff_walk = st.checkbox("Gặp khó khăn khi leo cầu thang / đi bộ")
        with col3:
            st.markdown("**🔹 Sức khỏe chung & Xã hội**")
            gen_hlth_label = st.selectbox(
                "Tự đánh giá sức khỏe chung",
                list(GEN_HLTH_OPTIONS.keys()),
                index=2,
            )
            phys_hlth = st.slider("Số ngày cơ thể mệt mỏi (tháng qua)", 0, 30, 0)
            ment_hlth = st.slider("Số ngày căng thẳng tinh thần (tháng qua)", 0, 30, 0)
            education = st.slider("Cấp bậc Học vấn (1: Thấp, 6: Đại học trở lên)", 1, 6, 4)
            income = st.slider("Mức thu nhập (1: Thấp, 8: Cao)", 1, 8, 5)
            any_healthcare = st.checkbox("Có Bảo hiểm y tế", value=True)
            no_doc_cost = st.checkbox("Từng không thể đi khám vì quá đắt")

        submitted = st.form_submit_button("🔍 Yêu cầu AI Phân tích Nguy cơ", use_container_width=True)

    if not submitted:
        return

    form_values = {
        'age_group': age_group,
        'sex': sex,
        'bmi': bmi,
        'high_bp': high_bp,
        'high_chol': high_chol,
        'heart_disease': heart_disease,
        'diabetes': diabetes,
        'smoking_status': smoking_status,
        'hvy_alcohol': hvy_alcohol,
        'phys_activity': phys_activity,
        'fruits': fruits,
        'veggies': veggies,
        'chol_check': chol_check,
        'diff_walk': diff_walk,
        'gen_hlth': GEN_HLTH_OPTIONS[gen_hlth_label],
        'phys_hlth': phys_hlth,
        'ment_hlth': ment_hlth,
        'education': education,
        'income': income,
        'any_healthcare': any_healthcare,
        'no_doc_cost': no_doc_cost,
    }
    input_df = build_cdc_stroke_dataframe(form_values)
    probability = predict_probability_percent(model, input_df)

    st.markdown("---")
    st.subheader("📊 KẾT QUẢ CHẨN ĐOÁN TỪ HỆ THỐNG AI")
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

    st.markdown("---")
    st.subheader("🧠 Trí tuệ nhân tạo giải thích lý do")
    st.write(
        "Biểu đồ dưới đây chỉ ra những thói quen và bệnh lý ảnh hưởng mạnh nhất đến bạn.\n"
        "- 🟥 **Màu Đỏ (Bên phải):** Làm TĂNG nguy cơ đột quỵ.\n"
        "- 🟩 **Màu Xanh (Bên trái):** Giúp GIẢM nguy cơ đột quỵ."
    )

    with st.spinner("AI đang vẽ sơ đồ phân tích..."):
        try:
            plot_df = build_shap_dataframe(
                model,
                input_df,
                CDC_FEATURE_TRANSLATIONS,
                top_n=8,
            )
            fig = create_horizontal_impact_chart(plot_df, "TOP 8 YẾU TỐ ẢNH HƯỞNG NHẤT")
            st.pyplot(fig)
            plt.close(fig)
        except Exception as exc:
            st.error(f"⚠️ Đã có lỗi khi vẽ biểu đồ giải thích: {exc}")

    st.markdown("---")
    st.subheader("🩺 Phác đồ Điều trị & Lời khuyên Cá nhân hóa")
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
