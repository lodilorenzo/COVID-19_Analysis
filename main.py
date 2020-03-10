import pandas as pd
import datetime
import os
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def get_data_for_day_and_provincia(codice_provincia, day_string):
    data_frame = pd.read_csv(
        'COVID-19/dati-province/dpc-covid19-ita-province-%s.csv' % day_string,
        encoding='ISO-8859-1')
    return data_frame[data_frame.codice_provincia == codice_provincia]


def get_all_data_for_provincia(codice_provincia):
    start = datetime.datetime.strptime('20200224', '%Y%m%d')
    today_formatted = datetime.date.today().strftime('%Y%m%d')
    end = datetime.datetime.strptime(today_formatted, '%Y%m%d')
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]

    cases = list()
    delta_cases = list()
    provincia = ''
    date_list = list()

    previous_date = None
    for date in date_generated:
        current_date_string = date.strftime('%Y%m%d')

        if previous_date is not None:
            data_current_date = get_data_for_day_and_provincia(codice_provincia, current_date_string)
            data_previous_date = get_data_for_day_and_provincia(codice_provincia, previous_date)
            current_date_cases = int(data_current_date['totale_casi'].values[0])
            provincia = data_current_date['denominazione_provincia'].values[0]
            cases.append(current_date_cases)
            previous_date_cases = int(data_previous_date['totale_casi'].values[0])
            delta = current_date_cases - previous_date_cases
            delta_cases.append(delta)
            date_list.append(date)

        previous_date = current_date_string

    derivate = list()

    previous_delta = None
    for delta_case in delta_cases:
        if previous_delta is not None:
            try:
                derivate_number = delta_case / previous_delta
                derivate.append(derivate_number)
            except:
                pass

        previous_delta = delta_case

    len_derivate = len(derivate)
    cases = cases[-len_derivate:]
    delta_cases = delta_cases[-len_derivate:]
    date_list = date_list[-len_derivate:]

    return cases, delta_cases, derivate, provincia, date_list


def print_data(cases, delta_cases, derivate, provincia, date_list):
    print('Provincia - [%s]' % provincia)
    print(cases)
    print(delta_cases)
    string_to_print = ("[" + ', '.join(['%.2f'] * len(derivate)) + "]") % tuple(derivate)
    print(string_to_print)


def update_covid_data():
    os.chdir('COVID-19')
    os.system('git pull')
    os.chdir('..')


if __name__ == '__main__':
    update_covid_data()
    try:
        codice_provincia = int(sys.argv[1])
        print(codice_provincia)
        (cases, delta_cases, derivate, provincia, date_list) = get_all_data_for_provincia(codice_provincia)
        print_data(cases, delta_cases, derivate, provincia, date_list)
        fig = make_subplots(rows=1, cols=2)
        fig.add_trace(go.Scatter(y=cases, x=date_list, name='Cases'), row=1, col=1)
        fig.add_trace(go.Bar(y=delta_cases, x=date_list, name='Change'), row=1, col=1)
        fig.add_trace(go.Scatter(y=derivate, x=date_list, name='Derivative'), row=1, col=2)
        fig.update_layout(title_text=provincia)
        fig.show()
    except IndexError:
        print("No arguments, ERROR!")
