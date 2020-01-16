#!/usr/bin/env python3

import requests
import bs4
import csv
from datetime import date
from tqdm import tqdm

def main():

    today = date.today()
    file_name = 'gate1_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','Departure Date','field','value']
        csv_writer.writerow(field_names)
        # print(field_names)
    
        linksUS = (
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/alaska-tour-6daknlt20.aspx#prices',
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-5dec120.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/western-states-tours-8dcamvnprk20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/south-america-tour-18dsampe20.aspx#prices',
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-8dclecaa20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/western-states-tours-8dclanprk20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/western-states-tours-9dclanprkb20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/northeast-escorted-10dclneff20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/northeast-escorted-9dclneff20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-10daffpea20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-10daffpe20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-14dpeamz20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-17daffpegpsis20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/southwest-escorted/mexico-tour-10dccmxtus20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-ecuador-17decpe20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-ecuador-11decapemft20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-6dessmftmia20.aspx#prices',
            # 'https://www.discovery-tours.com/small-groups/small-group/2020/small-groups-ecuador-13dgeaa20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-7dpemft20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-7dpemftmia20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-9dpeincsa20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-17dpe4dwgpsc20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-20dpe6degpsc20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/southwest-escorted-8dgcnnprk20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/southwest-escorted-7dzbcagnprk19.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/southwest-escorted-7dzbcagnprk21.aspx#prices',
            # 'https://www.discovery-tours.com/small-groups/small-group/2020/small-groups-alaska-10daknb20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/northwest-escorted/alaska-tour-4daknlt20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/western-states-tours-9dcagcoystvl20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/alaska-tour-9dclaak20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/northwest-escorted/alaska-cruise-tour-12dakgb20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-11daffpebo20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-17daffpeg4dpsis20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-11daffpenl20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/deluxe-peru-11ddlxpe20.aspx#prices',
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-9dec4dngpsc20.aspx#prices',
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-14dec4dngpsc20.aspx#prices',
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-9dec4dwgpsc20.aspx#prices',
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-14dec4dwgpsc20.aspx#prices',
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-11dec6degpsc20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-ecuador-11decapemftmia20.aspx#prices',
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-12decgpsis20.aspx#prices',
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-14decgpsis20.aspx#prices',
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-14dgpsiskalec20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/southeast-escorted-7dhso20.aspx#prices',
            'https://www.gate1travel.com/latin-america/ecuador-galapagos/2020/escorted/ecuador-tours-10dkalec20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-12dkalpe20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/midwestern-states-tours-8dmlmichi20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/southeast-escorted-8dmjts20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/southwest-escorted/western-states-tours-7dnmela20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/northwest-escorted-9dpnwcrg19.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/northwest-escorted-10dpnwcrgsea20.aspx#prices',
            'https://www.gate1travel.com/latin-america/peru/2020/escorted/peru-tours-7dmftnl20.aspx#prices',
            # 'https://www.discovery-tours.com/small-groups/small-group/2020/small-groups-peru-14dpelgd20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/northwest-escorted/northwest-escorted-7dsvv20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/northwest-escorted/alaska-cruise-tour-14dsvvgb20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/southwest-escorted-14dultnprk20.aspx#prices'
        )

        print()

        for link in tqdm(linksUS):

            res = requests.get(link)
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            trip_name = soup.find("h2").text.strip()
            # print(trip_name)

            departures_list = soup.find('tbody', class_='hidden-xs')

            for departure in departures_list.find_all('tr', class_='pricerow'):
                
                if departure.find('del', class_='text-muted'):                          # check if date is crossed-off (Sold Out)
                    date_numbers = departure.find('del', class_='text-muted').text.split()
                else:
                    date_numbers = departure.find('button', class_='serviceDate').text.split()
                
                if len(date_numbers) == 3:                                                     # check if date format includes day of week
                    departure_date = '{}-{}-20'.format(date_numbers[2], date_numbers[1])
                else:
                    departure_date = '{}-{}-20'.format(date_numbers[1], date_numbers[0])
                # print(departure_date)

                if departure.find('span', class_='text-danger'):
                    notes = departure.find('span', class_='text-danger').text
                    string_to_write = [trip_name,departure_date,'Notes',notes]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)

                if departure.find('td', class_='bookby-price'):
                    prices = departure.find_all('td', class_='text-center')
                    actual_price = prices[0].text.strip()
                    string_to_write = [trip_name,departure_date,'Actual Price USD',actual_price]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)
                    original_price = prices[1].text.strip()
                    string_to_write = [trip_name,departure_date,'Original Price USD',original_price]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)
                else:
                    actual_price = departure.find('td', class_='text-center').text.strip()
                    string_to_write = [trip_name,departure_date,'Actual Price USD',actual_price]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)
                    string_to_write = [trip_name,departure_date,'Original Price USD',actual_price]
                    csv_writer.writerow(string_to_write)
                    # print(string_to_write)

            split_link = link.split('/')
            linkAU = '{}//{}.au/{}/{}/{}/{}/{}'.format(split_link[0], split_link[2], split_link[3], split_link[4], split_link[5], split_link[6], split_link[7])
            # print(linkAU)

            res = requests.get(linkAU)
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            departures_list = soup.find('tbody', class_='hidden-xs')

            if departures_list:                                            # check is AU site exists

                for departure in departures_list.find_all('tr', class_='pricerow'):
                    
                    if departure.find('del', class_='text-muted'):                          # check if date is crossed-off (Sold Out)
                        date_numbers = departure.find('del', class_='text-muted').text.split()
                    else:
                        date_numbers = departure.find('button', class_='serviceDate').text.split()
                    
                    if len(date_numbers) == 3:                                                     # check if date format includes day of week
                        departure_date = '{}-{}-20'.format(date_numbers[2], date_numbers[1])
                    else:
                        departure_date = '{}-{}-20'.format(date_numbers[1], date_numbers[0])
                    # print(departure_date)

                    if departure.find('td', class_='bookby-price'):
                        prices = departure.find_all('td', class_='text-center')
                        actual_price = prices[0].text.strip()
                        string_to_write = [trip_name,departure_date,'Actual Price AUD',actual_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)
                        original_price = prices[1].text.strip()
                        string_to_write = [trip_name,departure_date,'Original Price AUD',original_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)
                    else:
                        actual_price = departure.find('td', class_='text-center').text.strip()
                        string_to_write = [trip_name,departure_date,'Actual Price AUD',actual_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)
                        string_to_write = [trip_name,departure_date,'Original Price AUD',actual_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

        print("\nDone!\n")

if __name__ == '__main__': main()