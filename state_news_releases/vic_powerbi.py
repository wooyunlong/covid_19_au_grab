from os import listdir
from os.path import expanduser

from covid_19_au_grab.state_news_releases.data_containers.DataPoint import \
    DataPoint
from covid_19_au_grab.state_news_releases.constants import \
    DT_CASES_BY_REGION, DT_AGE, DT_AGE_MALE, DT_AGE_FEMALE, DT_SOURCE_OF_INFECTION


BASE_PATH = expanduser('~/dev/covid_19_data/vic/powerbi')
SOURCE_URL = 'https://app.powerbi.com/view?r=' \
             'eyJrIjoiODBmMmE3NWQtZWNlNC00OWRkLTk1NjYtM' \
             'jM2YTY1MjI2NzdjIiwidCI6ImMwZTA2MDFmLTBmYW' \
             'MtNDQ5Yy05Yzg4LWExMDRjNGViOWYyOCJ9'


def get_powerbi_data():
    output = []

    for dir_ in sorted(listdir(BASE_PATH)):
        # TODO: Make only use most recent revision ID for a given day!!! ===============================================
        subdir = f'{BASE_PATH}/{dir_}'

        for fnam in listdir(subdir):
            path = f'{subdir}/{fnam}'
            #print(path)
            with open(path, 'r', encoding='utf-8') as f:
                from json import loads
                data = loads(f.read())

            if isinstance(data, (list, tuple)):
                # I've made some outputs have both query+response
                # here only interested in the response
                data = data[1]

            if fnam == 'regions.json':
                #print(data['results'][0]['result']['data'])
                for region in data['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
                    #print(region)

                    if region.get('R'):
                        value = previous_value
                    else:
                        value = region['C'][1]

                    output.append(DataPoint(
                        name=region['C'][0].split('(')[0].strip(),
                        datatype=DT_CASES_BY_REGION,
                        value=value,
                        date_updated=dir_.split('-')[0],
                        source_url=SOURCE_URL,
                        text_match=None
                    ))
                    previous_value = value
                    #print(output[-1])

                del previous_value

            elif fnam == 'age_data.json':
                for age in data['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
                    print(age)
                    X = age['X']

                    if len(X) > 0:
                        # Note that previous value simply means the very last value seen
                        # That means that if female/not stated is 67 and the following
                        # male stat is also 67 it'll be elided with an R-repeat val
                        male = X[0].get(
                            'M0', previous_value if X[0].get('R') else 0
                        )
                        previous_value = male
                    else:
                        male = 0

                    if len(X) > 1:
                        female = X[1].get(
                            'M0', previous_value if X[1].get('R') else 0
                        )  # "R" clearly means "Repeat"
                        previous_value = female
                    else:
                        female = 0

                    if len(X) > 2:
                        not_stated = X[2].get(
                            'M0', previous_value if X[2].get('R') else 0
                        )
                        previous_value = not_stated
                    else:
                        not_stated = 0

                    output.append(DataPoint(
                        name=age['G0'].replace('–', '-'),
                        datatype=DT_AGE_MALE,
                        value=male,
                        date_updated=dir_.split('-')[0],
                        source_url=SOURCE_URL,
                        text_match=None
                    ))
                    output.append(DataPoint(
                        name=age['G0'].replace('–', '-'),
                        datatype=DT_AGE_FEMALE,
                        value=female,
                        date_updated=dir_.split('-')[0],
                        source_url=SOURCE_URL,
                        text_match=None
                    ))
                    # TODO: support "not stated" separately!!! ====================================================
                    general_age = (
                        male + female + not_stated
                    )

                    output.append(DataPoint(
                        name=age['G0'].replace('–', '-'),
                        datatype=DT_AGE,
                        value=general_age,
                        date_updated=dir_.split('-')[0],
                        source_url=SOURCE_URL,
                        text_match=None
                    ))

                del previous_value

            elif fnam == 'source_of_infection.json':
                for source in data['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']:
                    output.append(DataPoint(
                        name=source['C'][0],
                        datatype=DT_SOURCE_OF_INFECTION,
                        value=source['C'][1],
                        date_updated=dir_.split('-')[0],
                        source_url=SOURCE_URL,
                        text_match=None
                    ))

    return output


if __name__ == '__main__':
    get_powerbi_data()
