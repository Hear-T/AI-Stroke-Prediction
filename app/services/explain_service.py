import pandas as pd
import shap


def build_shap_dataframe(model, dataframe, translation_map, drop_feature_names=None, top_n=8):
    booster = model.get_booster()
    explainer = shap.TreeExplainer(booster)
    shap_values = explainer(dataframe)

    exp = shap_values[0]
    if len(exp.shape) > 1:
        number_of_columns = exp.shape[1]
        if number_of_columns == 2:
            exp = exp[:, 1]
        elif number_of_columns == 1:
            exp = exp[:, 0]

    plot_df = pd.DataFrame({
        'Yếu tố': [translation_map.get(column, column) for column in dataframe.columns],
        'Tác động': exp.values,
    })

    if drop_feature_names:
        plot_df = plot_df[~plot_df['Yếu tố'].isin(drop_feature_names)]

    plot_df['Độ lớn tuyệt đối'] = plot_df['Tác động'].abs()
    plot_df = plot_df.sort_values(by='Độ lớn tuyệt đối', ascending=True).tail(top_n)
    return plot_df
