import pandas as pd
from datetime import datetime, timedelta
import warnings
import plotly.graph_objs as go
warnings.filterwarnings("ignore")


def daily_average(path_csv):

    history_daily = pd.read_csv(f'data/{path_csv}.csv')

    BAIRROS_FOR_STUDY = ['Rio_de_Janeiro']

    correct_form_bairro = {'barra': 'Barra da Tijuca', 'botafogo': 'Botafogo',
                           'centro': 'Centro', 'copacabana': 'Copacabana',
                           'flamengo': 'Flamengo',
                           'ipanema_leblon': 'Ipanema/Leblon',
                           'jacarepagua': 'Jacarepaguá',
                           'Rio_de_Janeiro': 'Rio de Janeiro',
                           'sem_bairro': 'Outros',
                           'tijuca': 'Tijuca'}
    translate_dayofweek = {'Monday': 'Segunda', 'Tuesday': 'Terça',
                           'Wednesday': 'Quarta', 'Thursday': 'Quinta',
                           'Friday': 'Sexta',
                           'Saturday': 'Sábado',
                           'Sunday': 'Domingo'}

    # Data Preprocessing
    history_daily = history_daily.loc[history_daily['bairro']
                                      .isin(BAIRROS_FOR_STUDY)]
    history_daily['dia'] = pd.to_datetime(history_daily['dia'])
    history_daily['day_of_week'] = history_daily['dia'].dt.day_name()

    # Analysis starts from the last 7 days
    now = datetime.now()
    start_time = now - timedelta(days=7)
    start_time = start_time.strftime('%Y-%m-%d')
    week_now = history_daily.loc[history_daily['dia'] >= start_time]
    def translate(x): return translate_dayofweek[x]
    week_now['day_of_week'] = week_now.day_of_week.apply(translate)
    week_now['dia'] = week_now['dia'].apply(lambda x: str(x.strftime('%d/%m')))

    # Legend
    week_now['proporcao_relacao_media_dia_da_semana_legend'] = \
        week_now['proporcao_media_dia_semana'].apply(lambda x: str(round(x))
                                                     + '%')
    week_now['day_of_week_initial'] = \
        week_now.day_of_week.apply(lambda x: ' (' + str(x)[0].upper() + ')')
    week_now['day_of_week_legend'] = week_now['dia'] \
        + week_now['day_of_week_initial']

    week_now.rename(columns={'pessoas_contadas': 'Pessoas Contadas',
                             'media_pessoas_contadas':
                             'Média do Dia da Semana'}, inplace=True)

    # Generating Graph 1
    bairro_graph = 'Rio_de_Janeiro'
    week_graph = week_now.loc[week_now['bairro'] == bairro_graph][:-1]
    figure_1 = go.Figure(
        data=[
            go.Bar(
                name="Pessos Contadas",
                x=week_graph['day_of_week_legend'],
                y=week_graph['Pessoas Contadas'],
                text=week_graph[('proporcao_relacao_'
                                 'media_dia_da_semana_legend')],
                textposition='outside',
                offsetgroup=0
            ),
            go.Bar(
                name="Média do Dia da Semana",
                x=week_graph['day_of_week_legend'],
                y=week_graph['Média do Dia da Semana'],
                offsetgroup=1
            )
        ],
        layout=go.Layout(
            title=(f'{correct_form_bairro[bairro_graph]}:'
                   'Média de Pessoas por Dia'),
            title_x=0.5,
            yaxis_title="Pessoas Contadas",
            plot_bgcolor='rgba(0,0,0,0)',
            # width=800,
        )
    )
    figure_1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='black')
    return dict(data=figure_1.data, layout=figure_1.layout)

