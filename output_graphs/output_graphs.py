from os import listdir
import csv
import numpy as np
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


def read_csv(datatype,
             name_filter=None,
             value_filter=None,
             state_filter=None):

    if state_filter and not isinstance(state_filter, (list, tuple)):
        state_filter = (state_filter,)

    r = {}

    # Get the newest, based on binary sort order
    # (year->month->day->revision id)
    fnam = list(sorted(
        listdir('../state_news_releases/output')
    ))[-1]

    with open(f'../state_news_releases/output/{fnam}',
              'r', encoding='utf-8', errors='replace') as f:

        reader = csv.DictReader(f, delimiter='\t')

        for row in reader:
            if row['datatype'] != datatype:
                continue
            if state_filter and row['state_name'] not in state_filter:
                continue
            if value_filter and not value_filter(row['value']):
                continue
            if name_filter and not name_filter(row['name']):
                print("IGNORE:", row)
                continue

            key = row['state_name']
            if row['name'] != 'None':
                key = f'{key} {row["name"]}'

            r.setdefault(key, []).append((
                datetime.datetime.strptime(
                    row['date_updated'], '%d/%m/%Y'
                ),
                int(row['value'])
            ))

    for k, v in r.items():
        v.sort()
    return r


COLORS = [
    'blue',
    'orange',
    'green',
    'red',
    'purple',
    'brown',
    'pink',
    'gray',
    'cyan',
    'yellow'
]
STYLES = [
    '-',
    '--',
    '-.',
    ':'
]
MARKERS = [
    'o',
    'P',
    '.',
    'X'
]


def output_graph(datatype,
                 name_filter=None,
                 value_filter=None,
                 state_filter=None,
                 append_to_name=None):

    if isinstance(state_filter, str):
        state_filter = (state_filter,)

    plt.figure(figsize=(10, 8), dpi=80)

    for x, (k, v) in enumerate(read_csv(
        datatype, name_filter, value_filter, state_filter
    ).items()):
        print(k)
        X = np.array([i[0] for i in v])
        Y = [i[1] for i in v]

        plt.plot(
            X, Y,
            color=COLORS[x % len(COLORS)],
            label=k,
            marker=MARKERS[x // len(COLORS)],
            linestyle=STYLES[x // len(COLORS)]
        )

    y_label = (
        f'%s (%s)' % (datatype, ','.join(state_filter))
        if state_filter
        else datatype
    )
    y_label = (
        f'%s (%s)' % (y_label, append_to_name)
        if append_to_name
        else y_label
    )

    fontP = FontProperties()
    fontP.set_size('small')

    ax = plt.gca()
    formatter = mdates.DateFormatter("%d/%m")
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(formatter)

    plt.xlabel('Date')
    plt.ylabel(y_label)
    plt.legend(prop=fontP)
    plt.grid()
    #plt.show()

    plt.savefig(y_label+'.png')
    plt.clf()


def output_graphs():
    pass


if __name__ == '__main__':
    output_graph('DT_CASES')
    output_graph('DT_NEW_CASES')
    output_graph('DT_CASES_TESTED')
    output_graph('DT_AGE_MALE', state_filter='vic')
    output_graph('DT_AGE_FEMALE', state_filter='vic')
    output_graph('DT_AGE_MALE', state_filter='nsw')
    output_graph('DT_AGE_FEMALE', state_filter='nsw')
    output_graph('DT_AGE', state_filter='act')
    output_graph('DT_HOSPITALIZED')
    output_graph('DT_RECOVERED')
    #output_graph('DT_ICU')
    output_graph('DT_CASES_BY_REGION', state_filter='vic',
                 name_filter=lambda p: p[0].lower() < 'm',
                 append_to_name='a-l')
    output_graph('DT_CASES_BY_REGION', state_filter='vic',
                 name_filter=lambda p: p[0].lower() >= 'm',
                 append_to_name='m-z')
    output_graph('DT_CASES_BY_REGION', state_filter='wa',
                 name_filter=lambda p: p[0].lower() < 'm',
                 append_to_name='a-l')
    output_graph('DT_CASES_BY_REGION', state_filter='wa',
                 name_filter=lambda p: p[0].lower() >= 'm',
                 append_to_name='m-z')
    output_graph('DT_CASES_BY_REGION', state_filter='nsw')
    output_graph('DT_CASES_BY_REGION', state_filter='qld')
    output_graph('DT_NEW_CASES_BY_REGION', state_filter='qld')
    output_graph('DT_NEW_CASES_BY_REGION', state_filter='wa')
    output_graph('DT_SOURCE_OF_INFECTION')
    output_graph('DT_DEATHS')
