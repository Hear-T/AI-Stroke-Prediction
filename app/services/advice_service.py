def generate_cdc_advice(form_values):
    """
    Sinh lời khuyên y tế dựa trên 10 đặc trưng của bộ dữ liệu Kaggle 11 cột.
    Sử dụng .get() để chống lỗi KeyError tuyệt đối.
    """
    advice = []
    
    # 1. Huyết áp (Đọc từ 'hypertension' thay vì 'high_bp' cũ)
    ht = form_values.get('hypertension')
    if ht == 1 or ht == "Có":
        advice.append("🔴 **Huyết áp cao:** Đây là nguyên nhân hàng đầu gây vỡ mạch máu não. Bạn cần uống thuốc hạ huyết áp đúng giờ theo đơn bác sĩ và đo huyết áp tại nhà mỗi ngày.")
        
    # 2. Tim mạch
    hd = form_values.get('heart_disease')
    if hd == 1 or hd == "Có":
        advice.append("🔴 **Bệnh tim mạch:** Bạn có nguy cơ hình thành cục máu đông. Hãy đi siêu âm tim và đo điện tâm đồ (ECG) định kỳ 6 tháng/lần.")
        
    # 3. Đường huyết (Đọc từ 'avg_glucose_level' thay vì 'diabetes' cũ)
    glucose = form_values.get('avg_glucose_level', 0)
    if glucose > 140:
        advice.append(f"🔴 **Đường huyết cao ({glucose} mg/dL):** Đường huyết cao làm hỏng thành mạch máu, tạo mảng xơ vữa. Cần kiểm soát chặt chẽ chế độ ăn tinh bột và đường.")
        
    # 4. Hút thuốc
    smoke = form_values.get('smoking_status', '')
    if smoke in ["smokes", "Đang hút thuốc"]:
        advice.append("⚠️ **Thuốc lá:** Khói thuốc đang tàn phá thành mạch máu của bạn từng ngày. Hãy lên kế hoạch giảm dần số điếu và tiến tới cai thuốc lá hoàn toàn.")
    elif smoke in ["formerly smoked", "Từng hút thuốc", "Đã từng hút (Nay đã bỏ)"]:
        advice.append("✅ **Thuốc lá:** Bạn đã từng hút nhưng nay đã cai, đây là tín hiệu rất tốt cho quá trình phục hồi mạch máu. Hãy tiếp tục duy trì.")

    # 5. Cân nặng (BMI)
    bmi = form_values.get('bmi', 20)
    if bmi >= 25.0:
        advice.append(f"🟢 **Cân nặng (BMI = {bmi}):** Chỉ số của bạn đang ở mức Thừa cân/Béo phì. Việc giảm 3-5kg sẽ giúp giảm áp lực khổng lồ lên tim mạch.")
    
    # 6. Tuổi tác
    age = form_values.get('age', 0)
    if age >= 60:
        advice.append("🕰️ **Tuổi tác:** Rủi ro đột quỵ gia tăng theo tuổi. Hãy cố gắng duy trì lịch khám tổng quát định kỳ mỗi 6 tháng.")
        
    # Nếu các chỉ số đều tốt
    if not advice:
        advice.append("✅ **Lối sống lành mạnh:** Hiện tại các chỉ số cốt lõi của bạn đang khá ổn định. Hãy tiếp tục duy trì chế độ ăn uống và vận động hợp lý!")

    return advice