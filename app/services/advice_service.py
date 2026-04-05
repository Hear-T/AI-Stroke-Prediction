def generate_cdc_advice(form_values: dict):
    advice = []

    if form_values['high_bp']:
        advice.append("🔴 **Huyết áp cao:** Đây là nguyên nhân hàng đầu gây vỡ mạch máu não. Bạn cần uống thuốc hạ huyết áp đúng giờ theo đơn bác sĩ và đo huyết áp tại nhà mỗi ngày.")
    if form_values['heart_disease']:
        advice.append("🔴 **Bệnh tim mạch:** Bạn có nguy cơ hình thành cục máu đông. Hãy đi siêu âm tim và đo điện tâm đồ (ECG) định kỳ 6 tháng/lần.")
    if form_values['diabetes'] == "Đang bị Tiểu đường":
        advice.append("🔴 **Tiểu đường:** Đường huyết cao làm hỏng thành mạch máu. Cần kiểm soát chặt chẽ chế độ ăn tinh bột, đường và tái khám nội tiết định kỳ.")

    if form_values['smoking_status'] in {"Đang hút thỉnh thoảng", "Hút thường xuyên / Lâu năm", "Đang hút hằng ngày"}:
        advice.append("⚠️ **Thuốc lá:** Khói thuốc đang tàn phá thành mạch máu của bạn từng ngày. Hãy lên kế hoạch giảm dần số điếu và tiến tới cai thuốc lá hoàn toàn.")
    elif form_values['smoking_status'] == "Đã cai thuốc (trước đây có hút)":
        advice.append("✅ **Thuốc lá:** Bạn đã cai thuốc, đây là tín hiệu rất tốt. Hãy tiếp tục duy trì vì model CDC hiện tại sẽ xếp bạn vào nhóm không hút hiện tại.")

    if form_values['hvy_alcohol']:
        advice.append("⚠️ **Rượu bia:** Mức sử dụng rượu bia nhiều là yếu tố nên kiểm soát chặt. Hãy giảm dần tần suất và lượng uống trong tuần.")

    if form_values['bmi'] >= 25.0:
        advice.append("🟢 **Cân nặng:** Chỉ số BMI của bạn đang ở mức Thừa cân/Béo phì. Việc giảm 3-5kg sẽ giúp giảm áp lực khổng lồ lên tim và mạch máu.")
    if not form_values['phys_activity']:
        advice.append("🟢 **Vận động:** Cơ thể bạn đang thiếu vận động. Hãy bắt đầu bằng việc đi bộ nhanh, đạp xe hoặc bơi lội 20-30 phút mỗi ngày để rèn luyện sức bền thành mạch.")
    if not form_values['veggies'] or not form_values['fruits']:
        advice.append("🟢 **Dinh dưỡng:** Hãy bổ sung thêm rau xanh và trái cây tươi vào bữa ăn hàng ngày để tăng cường chất xơ, giúp quét sạch mỡ máu thừa.")
    if form_values.get('gen_hlth', 3) >= 4:
        advice.append("🟠 **Sức khỏe chung:** Bạn đang tự đánh giá sức khỏe ở mức kém/rất kém. Đây thường là tín hiệu nên đi khám tổng quát để kiểm tra các nguy cơ nền.")

    return advice
