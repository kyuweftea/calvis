import csv
import datetime as dt
# from dataclasses import dataclass

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns

stations = [
    "San Francisco",
    "22nd Street",
    "Bayshore",
    "South San Francisco",
    "San Bruno",
    "Millbrae",
    "Broadway",
    "Burlingame",
    "San Mateo",
    "Hayward Park",
    "Hillsdale",
    "Belmont",
    "San Carlos",
    "Redwood City",
    "Menlo Park",
    "Palo Alto",
    "Stanford",
    "California Avenue",
    "San Antonio",
    "Mountain View",
    "Sunnyvale",
    "Lawrence",
    "Santa Clara",
    "College Park",
    "San Jose Diridon",
    "Tamien",
    "Capitol",
    "Blossom Hill",
    "Morgan Hill",
    "San Martin",
    "Gilroy"
]

# km
distances = {
    "San Francisco": 0.0,
    "22nd Street": 2.7,
    "Bayshore": 8.0,
    "South San Francisco": 14.6,
    "San Bruno": 18.7,
    "Millbrae": 21.7,
    "Broadway": 24.1,
    "Burlingame": 25.9,
    "San Mateo": 28.6,
    "Hayward Park": 30.4,
    "Hillsdale": 32.3,
    "Belmont": 34.9,
    "San Carlos": 37.0,
    "Redwood City": 40.7,
    "Menlo Park": 46.2,
    "Palo Alto": 48.1,
    "Stanford": 49.2,
    "California Avenue": 50.9,
    "San Antonio": 54.6,
    "Mountain View": 58.1,
    "Sunnyvale": 62.1,
    "Lawrence": 65.3,
    "Santa Clara": 71.0,
    "College Park": 73.2,
    "San Jose Diridon": 75.2,
    "Tamien": 78.7,
    "Capitol": 84.0,
    "Blossom Hill": 89.3,
    "Morgan Hill": 108.3,
    "San Martin": 114.3,
    "Gilroy": 124.2
}

linecolor = {
    'L1': '#c5c5c5',
    'L3': 'goldenrod',
    'L4': 'goldenrod',
    'L5': 'goldenrod',
    'L6': 'goldenrod',
    'B7': '#E31837'
}


def read_csv(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        return [row for row in reader]


northboundweekday = read_csv('northboundweekday.csv')
southboundweekday = read_csv('southboundweekday.csv')
northboundweekdaymay = read_csv('northboundweekdaymay.csv')
southboundweekdaymay = read_csv('southboundweekdaymay.csv')


# @dataclass
# class Train:
#     name: str
#     servicetype: str
#     stationdistances: list[float]
#     stoptimes: list[dt.datetime]


column_to_train = {}
trains = []

for schedule in [northboundweekday, southboundweekday]:
# for schedule in [northboundweekdaymay, southboundweekdaymay]:
# for schedule in [southboundweekday]:
    for i, row in enumerate(schedule):
        currentstation = None
        for j, cell in enumerate(row):
            if i == 0:
                if j >= 2:
                    train = {
                        "name": cell,
                        "stationdistances": [],
                        "stoptimes": []
                    }
                    column_to_train[j] = train
                    trains.append(train)
            elif i == 1:
                if j >= 2:
                    column_to_train[j]["servicetype"] = cell
            else:  # i > 1
                if j == 1:
                    currentstation = cell
                elif j >= 2:
                    try:
                        timestr = cell.upper()
                        if len(timestr) == 6:
                            timestr = '0' + timestr
                        time = dt.datetime.strptime(timestr, "%I:%M%p")
                        if time < dt.datetime.strptime("02:00AM", "%I:%M%p"):
                            time += dt.timedelta(days=1)

                        column_to_train[j]["stationdistances"].append(distances[currentstation])
                        column_to_train[j]["stoptimes"].append(time)
                    except ValueError as e:
                        pass

sns.set_style("darkgrid")
# sns.set_context("poster")

graph, (ax) = plt.subplots(1, 1)


for train in trains:
    ax.plot(train["stoptimes"], train["stationdistances"], '.-', color=linecolor[train["servicetype"]])

# ax.axhspan(distances["Broadway"], distances["Hillsdale"], color='gray')

# plt.gcf().autofmt_xdate()
date_form = mpl.dates.DateFormatter("%I:%M%p")
ax.xaxis.set_major_formatter(date_form)

stationlabels = list(filter(lambda station: station not in ["Stanford", "College Park"], stations))
ax.set_yticks(list(map(lambda station: distances[station], stationlabels)))
ax.set_yticklabels(stationlabels)

custom_lines = [Line2D([0], [0], color='#c5c5c5', lw=2),
                Line2D([0], [0], color='goldenrod', lw=2),
                Line2D([0], [0], color='#E31837', lw=2),
                Line2D([0], [0], color='gray', lw=10, solid_capstyle='butt')]

ax.set_title('Caltrain Weekday Schedule (effective August 30, 2021)')
# ax.set_title('Caltrain Temporary Weekday Schedule (May 2 to 20, 2022)')
ax.set_xlabel('Time of Day')
ax.legend(custom_lines, ['1XX Local', '3XX, 4XX, 5XX, 6XX Limited', '7XX Baby Bullet', 'single-tracking'])

# ax.set_xlim((dt.datetime.strptime("04:00AM", "%I:%M%p"), dt.datetime.strptime("11:00AM", "%I:%M%p")))
ax.invert_yaxis()

fig = mpl.pyplot.gcf()
fig.set_size_inches(17, 11, forward=True)
# fig.set_dpi(100)
# fig.savefig('caltrainmay.png', dpi=100)
fig.savefig('caltrain.png', dpi=100)

# plt.show()
