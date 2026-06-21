import streamlit as st


from app.ui.stroke_cdc_page import render_cdc_stroke_page



# =====================================================================
# HÀM MAIN ĐIỀU HƯỚNG GIAO DIỆN PHÂN TÁCH TAB
# =====================================================================
def main():
    st.set_page_config(
        page_title="Dự đoán đột quỵ CDC",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
 
    # Gọi giao diện nhập liệu và chạy mô hình học máy hiện tại của bạn
    render_cdc_stroke_page()
        
    


if __name__ == "__main__":
    main()
