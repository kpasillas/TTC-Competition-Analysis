#!/usr/bin/env python3

import requests
import bs4
import csv
from datetime import date
from datetime import datetime
from tqdm import tqdm

def main():

    today = date.today()
    file_name = 'gate1_raw_data_{}.csv'.format(today.strftime("%m-%d-%y"))

    error_log = dict()
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','DepartureID','field','value']
        csv_writer.writerow(field_names)
        # print(field_names)
    
        linksUS = (                 # 56 total names (not counting Mexico since removed from website)
            # 'https://www.gate1travel.com.au/latin-america/ecuador-galapagos/2020/escorted/small-groups-ecuador-13dgeaa20.aspx',
            # 'https://www.gate1travel.com.au/latin-america/peru/2020/escorted/small-groups-peru-14dpelgd20.aspx',
            # 'https://www.gate1travel.com/usa-canada/usa/2021/northwest-escorted/alaska-tour-6daknlt21.aspx',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/southwest-escorted-7dzbcagnprk19.aspx#prices',        # Affordable Zion, Bryce Canyon, Arches & Grand Canyon National Parks
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/southwest-escorted-7dzbcagnprk21.aspx#prices',        # Affordable Zion, Bryce Canyon, Arches & Grand Canyon National Parks
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/alaska-tour-6daknlt20.aspx#prices',       # Alaska with Northern Lights
            'https://www.discovery-tours.com/small-groups/small-group/2020/small-groups-alaska-10daknb20.aspx#prices',      # Alaska's Natural Beauty (Small Groups)
            'https://www.gate1travel.com/usa-canada/usa/2020/northwest-escorted/alaska-tour-4daknlt20.aspx#prices',     # Alaska's Northern Lights
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-5dec120.aspx#prices',      # Amazon Express
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/western-states-tours-9dcagcoystvl20.aspx#prices',     # California with Lake Tahoe & Yosemite National Park
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/western-states-tours-8dcamvnprk20.aspx#prices',       # Canyonlands, Arches & Mesa Verde National Parks
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/alaska-tour-9dclaak20.aspx#prices',       # Classic Alaska
            'https://www.gate1travel.com/usa-canada/usa/2020/northwest-escorted/alaska-cruise-tour-12dakgb20.aspx#prices',      # Classic Alaska with 7 Day Cruise
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/south-america-tour-18dsampe20.aspx#prices',       # Classic Brazil, Argentina & Peru
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-8dclecaa20.aspx#prices',       # Classic Ecuador & Amazon Adventure
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/western-states-tours-8dclanprk20.aspx#prices',        # Classic National Parks, Mt. Rushmore, Yellowstone & Grand Teton
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/western-states-tours-9dclanprkb20.aspx#prices',       # Classic National Parks, Mt. Rushmore, Yellowstone & Grand Teton with the Badlands
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/northeast-escorted-10dclneff20.aspx#prices',      # Classic New England Fall Foliage (10 day)
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/northeast-escorted-9dclneff20.aspx#prices',       # Classic New England Fall Foliage (9 day)
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-10daffpea20.aspx#prices',      # Classic Peru - Plan A Hotels
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-10daffpe20.aspx#prices',       # Classic Peru - Plan B Hotels
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-11daffpebo20.aspx#prices',     # Classic Peru & Bolivia
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-14dpeamz20.aspx#prices',       # Classic Peru with Amazon Experience
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-17daffpegpsis20.aspx#prices',      # Classic Peru with Ecuador & 3 Day Galapagos Islands
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-17daffpeg4dpsis20.aspx#prices',        # Classic Peru with Ecuador & 4 Day Galapagos Islands
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-11daffpenl20.aspx#prices',     # Classic Peru with Nazca Lines
            'https://www.gate1travel.com/usa-canada/usa/2020/southwest-escorted/mexico-tour-10dccmxtus20.aspx#prices',      # Copper Canyon: Mexico & Tucson
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/deluxe-peru-11ddlxpe20.aspx#prices',      # Deluxe Peru
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-ecuador-17decpe20.aspx#prices',      # Ecuador & Peru
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-9dec4dngpsc20.aspx#prices',        # Ecuador with 4 Day Northern Galapagos Cruise
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-14dec4dngpsc20.aspx#prices',       # Ecuador with 4 Day Northern Galapagos Cruise
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-9dec4dwgpsc20.aspx#prices',        # Ecuador with 4 Day Western Galapagos Cruise
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-14dec4dwgpsc20.aspx#prices',       # Ecuador with 4 Day Western Galapagos Cruise
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-11dec6degpsc20.aspx#prices',       # Ecuador with 6 Day Eastern Galapagos Cruise
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-ecuador-11decapemft20.aspx#prices',      # Ecuador, the Amazon & Peru with Machu Picchu
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-ecuador-11decapemftmia20.aspx#prices',       # Ecuador, the Amazon & Peru with Machu Picchu (Miami Special)
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-6dessmftmia20.aspx#prices',        # Essential Machu Picchu (Miami Special)
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-12decgpsis20.aspx#prices',     # Galapagos Islands & Ecuador
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-14decgpsis20.aspx#prices',     # Galapagos Islands & Ecuador
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-14dgpsiskalec20.aspx#prices',      # Galapagos Islands & Kaleidoscope of Ecuador
            'https://www.discovery-tours.com/small-groups/small-group/2020/small-groups-ecuador-13dgeaa20.aspx#prices',     # Galapagos, Ecuador, Andes & Amazon
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/southeast-escorted-7dhso20.aspx#prices',      # Historical South
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-10dkalec20.aspx#prices',       # Kaleidoscope of Ecuador with Andes Mountains & Amazon
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-12dkalpe20.aspx#prices',       # Kaleidoscope of Peru
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/midwestern-states-tours-8dmlmichi20.aspx#prices',     # Michigan's Lakes & Mackinac Island with Chicago
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/southeast-escorted-8dmjts20.aspx#prices',     # Musical Journey Through the South
            'https://www.gate1travel.com/usa-canada/usa/2020/southwest-escorted/western-states-tours-7dnmela20.aspx#prices',        # New Mexico Landscapes & Pueblo Life
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/northwest-escorted-9dpnwcrg19.aspx#prices',       # Pacific Northwest with Columbia River Gorge
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/northwest-escorted-10dpnwcrgsea20.aspx#prices',       # Pacific Northwest with Columbia River Gorge & Seattle
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-7dpemft20.aspx#prices',        # Peru & Machu Picchu
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-7dpemftmia20.aspx#prices',     # Peru & Machu Picchu (Miami Special)
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-9dpeincsa20.aspx#prices',      # Peru Inca Special
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-17dpe4dwgpsc20.aspx#prices',       # Peru with 4 Day Western Galapagos Cruise
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-20dpe6degpsc20.aspx#prices',       # Peru with 6 Day Eastern Galapagos Cruise
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-7dmftnl20.aspx#prices',        # Peru's Machu Picchu & Nazca Lines
            'https://www.discovery-tours.com/small-groups/small-group/2020/small-groups-peru-14dpelgd20.aspx#prices',       # Peruvian Legends (Small Groups)
            'https://www.gate1travel.com/usa-canada/usa/2020/northwest-escorted/northwest-escorted-7dsvv20.aspx#prices',        # Seattle, Victoria & Vancouver
            'https://www.gate1travel.com/usa-canada/usa/2020/northwest-escorted/alaska-cruise-tour-14dsvvgb20.aspx#prices',     # Seattle, Victoria & Vancouver with 7 Day Alaskan Cruise
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/southwest-escorted-14dultnprk20.aspx#prices',     # Ultimate National Parks
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/southwest-escorted-8dgcnnprk20.aspx#prices'       # Zion, Bryce Canyon & Grand Canyon National Parks
        )

        print()

        for link in tqdm(linksUS):

            res = requests.get(link)
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            try:
                trip_name = soup.find("h2").text.strip()
                # print(trip_name)
                code = link.split('.')[-2].split('-')[-1].upper()
                op_code = 'Gate1{}'.format(code)
                # print(op_code)
                previous_departure_date = ''
                duplicate_departure_count = 0

                data_table = soup.find('table', class_='date-price-table')
                hidden_xs_items = data_table.find_all(class_='hidden-xs')
                # year = hidden_xs_items[0].text.split()[0][-2:]
                year = data_table.find('th').text.split()[0][-2:]
                
                for hidden_xs_item in hidden_xs_items:
                    table_rows = hidden_xs_item.find_all('tr')
                    for row in table_rows:

                        if row.find(class_='h4'):             # look for "YEAR Dates & Prices" if multiple years on same page
                            year = row.find('th').text.split()[0][-2:]
                        
                        elif row.get('class') == ['pricerow']:             # look for departure row
                            departure = row
                
                            if departure.find('del', class_='text-muted'):                          # check if date is crossed-off (Sold Out or Cancelled)
                                date_numbers = departure.find('del', class_='text-muted').text.split()
                                available = False
                            elif departure.find('button', class_='serviceDate'):
                                date_numbers = departure.find('button', class_='serviceDate').text.split()
                                available = True
                            
                            if len(date_numbers) == 3:                                                     # check if date format includes day of week
                                departure_date = '{}-{}-{}'.format(date_numbers[2], date_numbers[1], year)
                                day = '{:02}'.format(int(date_numbers[2]))
                                month = str(chr((datetime.strptime(date_numbers[1], '%b')).month + 64))
                            else:
                                departure_date = '{}-{}-{}'.format(date_numbers[1], date_numbers[0], year)
                                day = '{:02}'.format(int(date_numbers[1]))
                                month = str(chr((datetime.strptime(date_numbers[0], '%b')).month + 64))
                            # print(departure_date)

                            if departure_date == previous_departure_date:                   # check if duplicate departure
                                duplicate_departure_count += 1
                            else:
                                duplicate_departure_count = 0

                            departure_letter = str(chr(duplicate_departure_count + 97))
                            departure_code = '{}{}{}{}'.format(day, month, year, departure_letter)
                            departure_id = '{}-{}'.format(op_code, departure_code)
                            # print(departure_id)

                            string_to_write = [trip_name,departure_id,'DepartureDate',departure_date]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)
                            
                            string_to_write = [trip_name,departure_id,'Available',available]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            if departure.find('span', class_='text-danger'):
                                notes = departure.find('span', class_='text-danger').text
                                if notes == '(Sold Out)':
                                    status = 'Sold Out'
                                else:                                                     # check if "Only x seats left!"
                                    status = 'Limited'
                            else:
                                notes = ''
                                if available == False:
                                    status = 'Cancelled'
                                else:
                                    status = 'Available'
                            string_to_write = [trip_name,departure_id,'Notes',notes]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)
                            string_to_write = [trip_name,departure_id,'Status',status]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                            if departure.find('td', class_='bookby-price'):
                                prices = departure.find_all('td', class_='text-center')
                                actual_price = prices[0].text.strip().strip('*').replace(',', '')
                                string_to_write = [trip_name,departure_id,'ActualPriceUSD',actual_price]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                                original_price = prices[1].text.strip().strip('*').replace(',', '')
                                string_to_write = [trip_name,departure_id,'OriginalPriceUSD',original_price]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                            else:
                                actual_price = departure.find('td', class_='text-center').text.strip().strip('*').replace(',', '')
                                string_to_write = [trip_name,departure_id,'ActualPriceUSD',actual_price]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                                string_to_write = [trip_name,departure_id,'OriginalPriceUSD',actual_price]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                            
                            previous_departure_date = departure_date

            except AttributeError:
                error_log['{} - US'.format(link)] = 'Missing from Website'
            
            split_link = link.split('/')
            try:
                linkAU = '{}//{}.au/{}/{}/{}/{}/{}'.format(split_link[0], split_link[2], split_link[3], split_link[4], split_link[5], split_link[6], split_link[7])
                # print(linkAU)
            except IndexError:
                error_log['{} - Discovery Small Groups'.format(link)] = 'Different Link Format'

            res = requests.get(linkAU)
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            previous_departure_date = ''
            duplicate_departure_count = 0
            
            try:
                data_table = soup.find('table', class_='date-price-table')
                hidden_xs_items = data_table.find_all(class_='hidden-xs')
                # year = hidden_xs_items[0].text.split()[0][-2:]
                year = data_table.find('th').text.split()[0][-2:]
                for hidden_xs_item in hidden_xs_items:
                    table_rows = hidden_xs_item.find_all('tr')
                    for row in table_rows:

                        if row.find(class_='h4'):             # look for "YEAR Dates & Prices" if multiple years on same page
                            year = row.find('th').text.split()[0][-2:]
                        
                        elif row.get('class') == ['pricerow']:             # look for departure row
                            departure = row
                
                            if departure.find('del', class_='text-muted'):                          # check if date is crossed-off (Sold Out or Cancelled)
                                date_numbers = departure.find('del', class_='text-muted').text.split()
                            elif departure.find('button', class_='serviceDate'):
                                date_numbers = departure.find('button', class_='serviceDate').text.split()
                            
                            if len(date_numbers) == 3:                                                     # check if date format includes day of week
                                departure_date = '{}-{}-{}'.format(date_numbers[2], date_numbers[1], year)
                                day = '{:02}'.format(int(date_numbers[2]))
                                month = str(chr((datetime.strptime(date_numbers[1], '%b')).month + 64))
                            else:
                                departure_date = '{}-{}-{}'.format(date_numbers[1], date_numbers[0], year)
                                day = '{:02}'.format(int(date_numbers[1]))
                                month = str(chr((datetime.strptime(date_numbers[0], '%b')).month + 64))
                            # print(departure_date)
                            
                            if departure_date == previous_departure_date:                   # check if duplicate departure
                                duplicate_departure_count += 1
                            else:
                                duplicate_departure_count = 0

                            departure_letter = str(chr(duplicate_departure_count + 97))
                            departure_code = '{}{}{}{}'.format(day, month, year, departure_letter)
                            departure_id = '{}-{}'.format(op_code, departure_code)
                            # print(departure_id)
                            
                            if departure.find('td', class_='bookby-price'):
                                prices = departure.find_all('td', class_='text-center')
                                actual_price = prices[0].text.strip().strip('*').replace(',', '')
                                string_to_write = [trip_name,departure_id,'ActualPriceAUD',actual_price]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                                original_price = prices[1].text.strip().strip('*').replace(',', '')
                                string_to_write = [trip_name,departure_id,'OriginalPriceAUD',original_price]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                            else:
                                actual_price = departure.find('td', class_='text-center').text.strip().strip('*').replace(',', '')
                                string_to_write = [trip_name,departure_id,'ActualPriceAUD',actual_price]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                                string_to_write = [trip_name,departure_id,'OriginalPriceAUD',actual_price]
                                csv_writer.writerow(string_to_write)
                                # print(string_to_write)
                            
                            previous_departure_date = departure_date

            except AttributeError:
                error_log['{} - AU'.format(link)] = 'Missing from Website'
    
    print('\n\n*** Error Log ***')
    for code, error in error_log.items():
        print('{}: {}'.format(code, error))
    
    print("\nDone!\n")

if __name__ == '__main__': main()