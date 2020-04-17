import pandas as pd
from datetime import timedelta
import warnings
import plotly.graph_objs as go
warnings.filterwarnings("ignore")


def weekly_percentage(path_csv):
    """Return the weekly average of a specific region

    Params:
        path_csv (str): CSV path

    Returns:
        (dict): containing data informations of image
    """

    history_daily = pd.read_csv(f'data/{path_csv}.csv')

    BAIRROS_FOR_STUDY = ['barra', 'botafogo', 'centro', 'copacabana',
                         'flamengo', 'ipanema_leblon', 'jacarepagua',
                         'Rio_de_Janeiro', 'sem_bairro', 'tijuca']

    correct_form_bairro = {'barra': 'Barra da Tijuca', 'botafogo': 'Botafogo',
                           'centro': 'Centro', 'copacabana': 'Copacabana',
                           'flamengo': 'Flamengo',
                           'ipanema_leblon': 'Ipanema/Leblon',
                           'jacarepagua': 'Jacarepaguá',
                           'Rio_de_Janeiro': 'Rio de Janeiro',
                           'sem_bairro': 'Outros',
                           'tijuca': 'Tijuca'}

    history_daily = history_daily.loc[history_daily['bairro']
                                      .isin(BAIRROS_FOR_STUDY)]

    # Data Preprocessing
    history_daily = history_daily.loc[history_daily['bairro']
                                      .isin(BAIRROS_FOR_STUDY)]
    history_daily['dia'] = pd.to_datetime(history_daily['dia'])
    history_daily['day_of_week'] = history_daily['dia'].dt.day_name()

    last_record = max(history_daily['dia'])
    start_time = last_record - timedelta(days=21)
    start_time = start_time.strftime('%Y-%m-%d')
    week_now = history_daily.loc[history_daily['dia'] >= start_time]
    # Reduction in relation to the historical average
    week_now['proporcao_history'] = week_now['queda_proporcional_dia_semana']
    week_now['dia_legend'] = week_now['dia']\
        .apply(lambda x: str(x.strftime('%d/%m')))
    # For graph legend
    week_now.rename(columns={'bairro': 'Bairro'}, inplace=True)

    # Selecting only some Bairros for graph
    # new_list: get second largest day
    new_list = set(week_now['dia'])
    new_list.remove(max(new_list))
    bairros_for_graph = week_now\
        .loc[(week_now['dia'] == max(new_list))
             & (week_now['Bairro'] != 'Rio de Janeiro')
             & (week_now['Bairro'] != 'Outros')]\
        .sort_values(by='queda_proporcional_dia_semana', ascending=True)\
        .Bairro.unique()

    # Group by Week and Bairro. Graph per Week
    week_now['week_number'] = week_now.dia\
        .apply(lambda x: str(x.isocalendar()[1]))
    week_graph = week_now.groupby(['Bairro', 'week_number'])\
        .agg({'dia': 'min', 'queda_proporcional_dia_semana': 'mean'})\
        .reset_index()
    week_graph['dia_legend'] = week_graph.dia\
        .apply(lambda x: str(x.strftime('%d/%m')))
    week_graph['week_legend'] = 'W' + week_graph['week_number'] + ' - ' \
        + week_graph['dia_legend']

    figure_2 = go.Figure()
    for bairro in bairros_for_graph:
        figure_2.add_trace(go.Scatter(
            x=week_graph.loc[week_graph['Bairro'] == bairro]
            ['week_legend'],
            y=week_graph.loc[week_graph['Bairro'] == bairro]
            ['queda_proporcional_dia_semana'],
            mode='lines+markers',
            name=correct_form_bairro[bairro]
        ))
    figure_2.update_layout(go.Layout(
        title='Redução em relação a Média Histórica',
        title_x=0.5,
        yaxis_title="Redução (%)",
        xaxis_title="IsoWeek - Dia de Início da Semana",
        plot_bgcolor="rgba(0,0,0,0)",
        # width=800,
    ))
    figure_2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black')
    return dict(data=figure_2.data, layout=figure_2.layout)
