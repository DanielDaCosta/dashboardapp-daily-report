from wrangling_scripts.figure1 import daily_average
from wrangling_scripts.figure2 import weekly_percentage
from wrangling_scripts.figure3 import hourly_cumsum


def return_figures():
    path_csv = '20200415'
    figures = []
    figures.append(daily_average(path_csv))
    figures.append(weekly_percentage(path_csv))
    path_csv = '20200415_hora'
    figures_hours = hourly_cumsum(path_csv)
    for fig_hour in figures_hours:
        figures.append(fig_hour)

    return figures
