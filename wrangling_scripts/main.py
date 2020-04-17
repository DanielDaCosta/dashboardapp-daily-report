from wrangling_scripts.figure1 import daily_average
from wrangling_scripts.figure2 import weekly_percentage
from wrangling_scripts.figure3 import hourly_cumsum


def return_data():
    """Return the images data

    Params:
        None

    Returns:
        (array): containing data informations of image
    """
    path_csv = '20200416'
    figures = []
    dict_results = daily_average(path_csv)
    figures.append(dict_results['figure'])
    figures.append(weekly_percentage(path_csv))
    path_csv = '20200416_hora'
    figures_hours = hourly_cumsum(path_csv)
    for fig_hour in figures_hours:
        figures.append(fig_hour)

    results = {'figures': figures, 'date_string': dict_results['date_string'],
               'high_aglom': dict_results['high_aglom'],
               'low_variations': dict_results['low_variations'],
               'high_variations': dict_results['high_variations']}

    return results
