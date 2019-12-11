#!/usr/bin/env python3

import requests
import bs4
import csv
from datetime import date
from tqdm import tqdm

def main():

    today = date.today()
    file_name = 'gate1_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    
    with open(file_name, 'w') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','Departure Date','field','value']
        csv_writer.writerow(field_names)
    
        linksUS = (
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/alaska-tour-6daknlt20.aspx#prices',
            'https://www.gate1travel.com/usa-canada/usa/2020/escorted/western-states-tours-8dcamvnprk20.aspx#prices'
        )

        print()

        for link in tqdm(linksUS):

            res = requests.get(link)
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            trip_name = soup.find("h2").text.strip()
            # print(trip_name)

            departures_list = soup.find('tbody', class_='hidden-xs')

            for departure in departures_list.find_all('tr', class_='pricerow'):
                
                date_numbers = departure.find('button', class_='serviceDate').text.split()
                departure_date = '{}-{}-20'.format(date_numbers[2], date_numbers[1])
                # print(departure_date)

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

            for departure in departures_list.find_all('tr', class_='pricerow'):
                
                date_numbers = departure.find('button', class_='serviceDate').text.split()
                departure_date = '{}-{}-20'.format(date_numbers[2], date_numbers[1])
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