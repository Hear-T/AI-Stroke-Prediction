import matplotlib.pyplot as plt
import plotly.graph_objects as go

def create_horizontal_impact_chart(plot_df, title):
    fig, ax = plt.subplots(figsize=(9, 5))
    
    # Đã sửa 'Tác động' thành 'Tác động (log-odds)' để khớp 100% với file explain_service.py
    colors = ['#ff4b4b' if value > 0 else '#00cc96' for value in plot_df['Tác động (log-odds)']]
    ax.barh(plot_df['Yếu tố'], plot_df['Tác động (log-odds)'], color=colors, height=0.6)
    
    ax.axvline(0, color='black', linewidth=1.5, linestyle='--')
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.yticks(fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', color='#333333', pad=20)
    return fig


def create_cdc_gauge_chart(probability):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Tỉ lệ rủi ro (%)", 'font': {'size': 20, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': 'black'},
            'bar': {'color': '#333333'},
            'bgcolor': 'white',
            'borderwidth': 2,
            'bordercolor': 'gray',
            'steps': [
                {'range': [0, 10], 'color': '#00cc96'},
                {'range': [10, 20], 'color': '#ffc107'},
                {'range': [20, 100], 'color': '#ff4b4b'},
            ],
        },
    ))
