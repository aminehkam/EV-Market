import csv
import pprint

ev_sales_per_state_file = '/Users/amineh/Documents/EconPHD/EV-Paper/EV-Sales-byState.csv'
ev_sales_per_car_file = '/Users/amineh/Documents/EconPHD/EV-Paper/EV-Data.csv'
output_file = '/Users/amineh/Documents/EconPHD/EV-Paper/output.csv'

def percent_to_float(x):
    return float(x.strip('%'))/100

class MakeModelShare:
    def __init__(self, make_, model_, share_, price_, is_phev_):
        self.make = make_
        self.model = model_
        self.share = share_
        self.price = price_
        self.is_phev = is_phev_
    def __repr__(self):
        return "(" + self.make + ", " + self.model + ", " + str(self.share) + ", " + str(self.price) + "," + str(self.is_phev) + ")"
    def __str__(self):
        return self.make + ", " + self.model + ", " + str(self.share) + ", " + \
        str(self.price) + "," + str(self.is_phev)

class TotalCarSale:
    def __init__(self, state_, total_bev_sale_, total_phev_sale_, num_charging_stations_, \
                 income_, commute_, gas_price_, rebate_, incentive_, \
                 grant_percent_, \
                 supermarket_, iv_, hybrid_sales_, battery_price_):
        self.state = state_
        self.total_bev_sale = total_bev_sale_
        self.total_phev_sale = total_phev_sale_
        self.num_charging_stations = num_charging_stations_
        self.income = income_
        self.commute = commute_
        self.gas_price = gas_price_
        self.rebate = rebate_
        self.incentive = incentive_
        self.grant_percent = grant_percent_
        self.supermarket = supermarket_
        self.iv = iv_
        self.hybrid_sales = hybrid_sales_
        self.battery_price = battery_price_

    def __repr__(self):
        return "(" + self.state + ", " + str(self.total_bev_sale) + ", " + str(self.total_phev_sale) + ")"
    def __str__(self):
        return self.state + ", " + str(self.total_bev_sale) + ", " + \
            str(self.total_phev_sale) + "," + \
            str(self.num_charging_stations) + "," + \
            str(self.income) + "," + \
            str(self.commute) + "," + \
            str(self.gas_price) + "," + \
            str(self.rebate) + "," + \
            str(self.incentive) + "," + \
            str(self.grant_percent) + "," + \
            str(self.supermarket) + "," + \
            str(self.iv) + "," + \
            str(self.hybrid_sales) + "," + \
            str(self.battery_price)
# Stores state -> TotalCarSale
state_sale_per_quarter = {}
# Stores car-make -> Car sale share
car_sale_per_quarter = {}

state_column = 'State'
quarter_column = 't'
phev_sales_column = 'PHEV M Sales'
bev_sales_column = 'BEV M Sales'
num_charging_stations_column = 'N ChargS'
income_column = 'Income'
commute_column = 'Commute'
gas_price_column = 'Gas Price'
rebate_column = 'Rebate'
incentive_column = 'Incentive'
grant_percent_column = 'Grant Percent'
supermarket_column = 'supermarket'
iv_column = 'iv'
hybrid_sales_column = 'Hybrid Sales'
battery_price_column = 'Battery Price'

state_table_columns = [state_column, bev_sales_column, phev_sales_column, num_charging_stations_column, income_column, \
    commute_column, gas_price_column, rebate_column, incentive_column, grant_percent_column, \
    supermarket_column, iv_column, hybrid_sales_column, battery_price_column]

make_column = 'MAKE'
model_column = 'MODEL'
share_column = 'SHARE'
price_column = 'PRICE'
is_phev_column = 'PHEV'

car_table_columns = [make_column, model_column, share_column, price_column, is_phev_column]

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
            bev_sales = int(row[headers[bev_sales_column]])
            phev_sales = int(row[headers[phev_sales_column]])
            num_charging_stations = long(row[headers[num_charging_stations_column]])
            income = long(row[headers[income_column]])
            commute = float(row[headers[commute_column]])
            gas_price = float(row[headers[gas_price_column]])
            rebate = long(row[headers[rebate_column]])
            incentive = (row[headers[incentive_column]] == '1')
            grant_percent = long(row[headers[grant_percent_column]])
            supermarket = long(row[headers[supermarket_column]])
            iv = long(row[headers[iv_column]])
            hybrid_sales = long(row[headers[hybrid_sales_column]])
            battery_price = long(row[headers[battery_price_column]])
            if quarter not in state_sale_per_quarter:
                state_sale_per_quarter[quarter] = []
            state_sale_per_quarter[quarter].append(TotalCarSale(state, bev_sales, phev_sales, \
                num_charging_stations, income, commute, gas_price, rebate, incentive, grant_percent, \
                supermarket, iv, hybrid_sales, battery_price))

with open(ev_sales_per_car_file, 'rU') as csvfile:
    state_reader = csv.reader(csvfile, delimiter=',', dialect=csv.excel_tab)
    first = True
    headers = {}
    for row in state_reader:
        if first:
            headers = createHeaders(row)
            first = False
        else:
            make = row[headers[make_column]]
            quarter = row[headers[quarter_column]]
            model = row[headers[model_column]]
            share = percent_to_float(row[headers[share_column]])
            price = long(row[headers[price_column]])
            is_phev = (row[headers[is_phev_column]] == '1')
            if quarter not in car_sale_per_quarter:
                car_sale_per_quarter[quarter] = []
            car_sale_per_quarter[quarter].append(MakeModelShare(make, model, share, price, is_phev))

# pprint.pprint(state_sale_per_quarter)
result = []
for quarter in sorted(state_sale_per_quarter):
    for state_info in state_sale_per_quarter[quarter]:
        if quarter in car_sale_per_quarter:
            for car_info in car_sale_per_quarter[quarter]:
                sale = car_info.share
                if car_info.is_phev:
                    sale *= state_info.total_phev_sale
                else:
                    sale *= state_info.total_bev_sale

                result.append('{},{},{},{}'.format(quarter, sale, state_info, car_info))

# print result
with open(output_file, 'w') as csvfile:
    csvfile.write('quarter,sale,{},{}\n'.format(','.join(state_table_columns), ','.join(car_table_columns)))
    for row in result:
        csvfile.write(row + '\n')


