import pandas as pd
from datetime import timedelta
import warnings
import plotly.graph_objs as go
warnings.filterwarnings("ignore")


def daily_average(path_csv):
    """Return the daily average of a specific region

    Params:
        path_csv (str): CSV path

    Returns:
        (dict): Dictionary containing the items:
            - figures: array with figure object
            - high_aglom: data of locations with higher agglomerations
            - low_var: data of locations with lower variations
            - high_var: data of locations with higher variations
    """

    history_daily = pd.read_csv(f'data/{path_csv}.csv')

    BAIRROS_FOR_STUDY = ['Haight-Ashbury', 'San Francisco', 'The Castro',
                         'Others', 'Union Square', 'Chinatown',
                         'Alamo Square', 'Mission District',
                         'SoMa', 'Fisherman’s wharf']

    # Data Preprocessing
    history_daily = history_daily.loc[history_daily['bairro']
                                      .isin(BAIRROS_FOR_STUDY)]
    history_daily['dia'] = pd.to_datetime(history_daily['dia'])
    history_daily['day_of_week'] = history_daily['dia'].dt.day_name()

    # Analysis starts from the last 7 days
    last_record = max(history_daily['dia'])
    start_time = last_record - timedelta(days=7)
    start_time = start_time.strftime('%Y-%m-%d')
    week_now = history_daily.loc[history_daily['dia'] >= start_time]
    week_now['Dia'] = week_now['dia'].apply(lambda x: str(x.strftime('%d/%m')))

    # Legend
    week_now['proporcao_relacao_media_dia_da_semana_legend'] = \
        week_now['proporcao_media_dia_semana'].apply(lambda x: str(round(x))
                                                     + '%')
    week_now['day_of_week_initial'] = \
        week_now.day_of_week.apply(lambda x: ' (' + str(x)[0].upper() + ')')
    week_now['day_of_week_legend'] = week_now['Dia'] \
        + week_now['day_of_week_initial']

    # Generating Graph 1
    bairro_graph = 'San Francisco'
    week_graph = week_now.loc[week_now['bairro'] == bairro_graph][:-1]
    week_graph.rename(columns={'pessoas_contadas': 'Pessoas Contadas',
                               'media_pessoas_contadas':
                               'Média do Dia da Semana'}, inplace=True)
    figure_1 = go.Figure(
        data=[
            go.Bar(
                name="Counted People",
                x=week_graph['day_of_week_legend'],
                y=week_graph['Pessoas Contadas'],
                text=week_graph[('proporcao_relacao_'
                                 'media_dia_da_semana_legend')],
                textposition='outside',
                offsetgroup=0
            ),
            go.Bar(
                name="Average Day of Week",
                x=week_graph['day_of_week_legend'],
                y=week_graph['Média do Dia da Semana'],
                offsetgroup=1
            )
        ],
        layout=go.Layout(
            title=(f'{bairro_graph}:'
                   'Average Number of People Per Day'),
            title_x=0.5,
            yaxis_title="Population",
            plot_bgcolor='rgba(0,0,0,0)',
            # width=800,
        )
    )
    figure_1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black')

    # General Analysis: Neighborhoods with the greatest agglomerations
    # Order by number of people in the last day
    columns = ['bairro', 'pessoas_contadas']
    last_day = week_now.dia.unique()[-2]  # -2 -> yesterday
    high_aglom = week_now.loc[(week_now['dia'] == last_day)
                              & (~week_now.bairro.isin(['Rio_de_Janeiro',
                                                       'sem_bairro'])),
                              columns].sort_values(by='pessoas_contadas',
                                                   ascending=False)[:3]
    high_aglom['pessoas_contadas'] = high_aglom.pessoas_contadas.apply(lambda x: round(x))
    high_aglom = high_aglom.to_dict('list')

    # General Analysis: Neighborhoods with the greatest variations
    # Order by querda_proporcional_dia_semana in the last day, in
    # ascending order
    columns = ['bairro', 'queda_proporcional_dia_semana']
    last_day = week_now.dia.unique()[-2]
    low_variations = week_now\
        .loc[(week_now['dia'] == last_day)
             & (~week_now.bairro.isin(['Rio_de_Janeiro', 'sem_bairro'])),
             columns].sort_values(by='queda_proporcional_dia_semana')[:3]
    low_variations['queda_proporcional_dia_semana'] = low_variations\
        .queda_proporcional_dia_semana.apply(lambda x: round(x))
    low_variations = low_variations.to_dict('list')

    # General Analysis: Neighborhoods with the smallest variations
    # Order by querda_proporcional_dia_semana in the last day,
    # in descrescing order

    columns = ['bairro', 'queda_proporcional_dia_semana']
    last_day = week_now.dia.unique()[-2]
    high_variations = week_now\
        .loc[(week_now['dia'] == last_day)
             & (~week_now.bairro.isin(['San Francisco', 'Others'])),
             columns].sort_values(by='queda_proporcional_dia_semana',
                                  ascending=False)[:3]
    high_variations['queda_proporcional_dia_semana'] = high_variations\
        .queda_proporcional_dia_semana.apply(lambda x: round(x))
    high_variations = high_variations.to_dict('list')

    # Results
    results = {'figure': dict(data=figure_1.data, layout=figure_1.layout),
               'high_aglom': high_aglom,
               'low_variations': low_variations,
               'high_variations': high_variations,
               'date_string': last_day.strftime('%Y-%m-%d')}

    return results


# if __name__ == '__main__':
#     path_csv = '20200416_2'
#     figures = []
#     dict_results = daily_average(path_csv)