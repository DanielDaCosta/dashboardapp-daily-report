import pandas as pd
from datetime import timedelta
import warnings
import plotly.graph_objs as go
warnings.filterwarnings("ignore")


def hourly_cumsum(path_csv):
    """Measure the cumulative sum of a specific region

    Params:
        path_csv (str): CSV path

    Returns:
        (dict): containing data informations of image
    """

    history_hourly = pd.read_csv(f'data/{path_csv}.csv')

    BAIRROS_FOR_STUDY = ['Rio_de_Janeiro']

    correct_form_bairro = {'barra': 'Barra da Tijuca', 'botafogo': 'Botafogo',
                           'centro': 'Centro', 'copacabana': 'Copacabana',
                           'flamengo': 'Flamengo',
                           'ipanema_leblon': 'Ipanema/Leblon',
                           'jacarepagua': 'Jacarepaguá',
                           'Rio_de_Janeiro': 'Rio de Janeiro',
                           'sem_bairro': 'Outros',
                           'tijuca': 'Tijuca'}

    # Analyze Bairro in BAIRROS_FOR_STUDY
    history_hourly = history_hourly.loc[history_hourly['bairro']
                                        .isin(BAIRROS_FOR_STUDY)]

    def correct_name(x): return correct_form_bairro[x]
    history_hourly['bairro'] = history_hourly.bairro.apply(correct_name)

    # Data Preprocessing
    history_hourly['hora'] = history_hourly\
        .hora.apply(lambda x: str(x)[:-3])  # Removing time zone '-03'
    last_record = max(pd.to_datetime(history_hourly['hora']))
    start_time = last_record - timedelta(days=14)  # Last 2 day + today
    start_time = start_time.strftime('%Y-%m-%d 00:00')
    history_hourly['hora'] = pd.to_datetime(history_hourly['hora'])
    week_now = history_hourly.loc[history_hourly['hora'] >= start_time]

    # Accumulated Sum
    # Creating day column for groupby(day) with cumsum
    week_now['day'] = week_now.hora.\
        apply(lambda x: str(x.strftime('%Y-%m-%d')))
    week_now['people_accumulate'] = week_now.\
        groupby(['day', 'bairro']).agg({'pessoas_contadas': 'cumsum'})
    week_now['horario_legend'] = week_now.hora.\
        apply(lambda x: str(x.strftime('%H')) + 'h')
    week_now['day_legend'] = week_now.hora.\
        apply(lambda x: str(x.strftime('%d/%m')))

    # Generating Graph 1
    week_now.rename(columns={'day_legend': 'Dia'}, inplace=True)
    last_week_day = last_record - timedelta(days=7)  # Last 2 day + today
    last_last_week_day = last_record - timedelta(days=14)  # Last 2 day + today
    last_week_day = last_week_day.strftime('%Y-%m-%d')
    last_last_week_day = last_last_week_day.strftime('%Y-%m-%d')
    today_now = last_record.strftime('%Y-%m-%d')
    last_hour = last_record.strftime('%Y-%m-%d %H:00:00')
    bairro_graph = 'Rio de Janeiro'
    week_now_graph = week_now.loc[(week_now['bairro'] == bairro_graph)
                                  & (week_now['day']
                                     .isin([last_week_day, last_last_week_day,
                                            today_now]))
                                  & (week_now['hora'] < last_hour)]
    figure_3 = go.Figure()
    for dia in week_now_graph.Dia.unique():
        figure_3.add_trace(go.Scatter(
            x=week_now_graph.loc[week_now_graph['Dia'] == dia]
            ['horario_legend'],
            y=week_now_graph.loc[week_now_graph['Dia'] == dia]
            ['people_accumulate'],
            mode='lines+markers',
            name=dia
        ))
    figure_3.update_layout(go.Layout(
        title="Média Acumulada de Pessoas Contadas por Hora",
        title_x=0.5,
        yaxis_title="Média Acumulada de Pessoas",
        plot_bgcolor="rgba(0,0,0,0)",
        # width=800,
    ))
    figure_3.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black')

    # Generating Graph 2
    week_now_graph = week_now.loc[week_now['Dia']
                                  == week_now.sort_values(by='hora',
                                                          ascending=False)
                                  .Dia.unique()[1]]
    DAY = max(week_now_graph['Dia'])

    figure_4 = go.Figure()
    figure_4.add_trace(go.Bar(
        x=week_now_graph['horario_legend'],
        y=week_now_graph['pessoas_contadas']
    ))

    figure_4.update_layout(go.Layout(
        title=f'{bairro_graph} {DAY}: Média de Pessoas por Hora',
        title_x=0.5,
        yaxis_title="Pessoas Contadas",
        plot_bgcolor="rgba(0,0,0,0)",
        # width = 800,
    ))
    figure_4.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black')
    return [dict(data=figure_3.data, layout=figure_3.layout),
            dict(data=figure_4.data, layout=figure_4.layout)]

