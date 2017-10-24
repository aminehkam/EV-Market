import csv
import pprint

ev_sales_per_state_file = '/Users/amineh/Documents/EconPHD/EV-Paper/EV-Sales-byState.csv'
output_file = '/Users/amineh/Documents/EconPHD/EV-Paper/iv-output.csv'

def percent_to_float(x):
    return float(x.strip('%'))/100

class StateSale:
    def __init__(self, state_, num_charging_stations_, supermarket_):
        self.state = state_
        self.num_charging_stations = num_charging_stations_
        self.supermarket = supermarket_

    def __repr__(self):
        return "(" + self.state + ", " + \
            str(self.num_charging_stations) + "," + \
            str(self.supermarket) + ")"

    def __str__(self):
        return self.state + ", " + \
            str(self.num_charging_stations) + "," + \
            str(self.supermarket)

# Stores state -> TotalCarSale
state_sale_per_quarter = {}

state_column = 'State'
quarter_column = 't'
num_charging_stations_column = 'N ChargS'
supermarket_column = 'supermarket'
output_headers = [state_column, num_charging_stations_column, supermarket_column]

def createHeaders(row):
    headers = {}
    for i in range(len(row)):
        headers[row[i]] = i
    return headers


state_sale_per_quarter_header = {}
with open(ev_sales_per_state_file, 'rU') as csvfile:
    state_reader = csv.reader(csvfile, delimiter=',', dialect=csv.excel_tab)
    first = True
    headers = {}
    for row in state_reader:
        if first:
            headers = createHeaders(row)
            first = False
        else:
            state = row[headers[state_column]]
            quarter = row[headers[quarter_column]]
            num_charging_stations = float(row[headers[num_charging_stations_column]])
            supermarket = long(row[headers[supermarket_column]])

            if quarter not in state_sale_per_quarter:
                state_sale_per_quarter[quarter] = []
            state_sale_per_quarter[quarter].append(StateSale(state, num_charging_stations, supermarket))


# pprint.pprint(state_sale_per_quarter)
result = []
num_charging_stations_per_quarter = {}
for quarter in sorted(state_sale_per_quarter):
    num_charging_stations_per_quarter[quarter] = 0
    for state_info in state_sale_per_quarter[quarter]:
        num_charging_stations_per_quarter[quarter] += state_info.num_charging_stations


previous_sum = 0
for quarter in sorted(state_sale_per_quarter):
    for state_info in state_sale_per_quarter[quarter]:
        iv = 0
        iv2 = 0
        if previous_sum != 0:
            iv2 = previous_sum - state_info.num_charging_stations
            iv = state_info.supermarket * iv2

        result.append('{},{},{},{}'.format(quarter, state_info, iv, iv2))
    # keep the previous quarter sum
    previous_sum = num_charging_stations_per_quarter[quarter]

with open(output_file, 'w') as csvfile:
    csvfile.write('quarter,{},iv,iv2\n'.format(','.join(output_headers)))
    for row in result:
        csvfile.write(row + '\n')


