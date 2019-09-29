#!/usr/bin/env python3

import requests
import bs4
import re
import csv
from datetime import date

def main():

    today = date.today()
    file_name = 'globus_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file)

        field_names = ['trip_name','departure_date','field','value']
        csv_writer.writerow(field_names)

        links = ('https://www.globusjourneys.com/tour/canyon-country-adventure/av/?nextyear=true&content=price', 'https://www.globusjourneys.com/tour/americas-historic-east/ah/?nextyear=true&content=price', 'https://www.globusjourneys.com/tour/classic-fall-foliage/ab/?nextyear=true&content=price', 'https://www.globusjourneys.com/tour/historic-trains-of-the-old-west/nc/?nextyear=true&content=price', 'https://www.globusjourneys.com/tour/pacific-coast-adventure/aq/?nextyear=true&content=price')

        for link in links:

            res = requests.get(link)
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            trip_name = soup.find("h1").text

            for departure in soup.find_all('div', class_='listing'):

                date_numbers = departure.find('p', class_='date-numbers').text.split()
                departure_date = '{}-{}-{}'.format(date_numbers[0], date_numbers[1], date_numbers[2])
                
                actual_price = departure.find('p', class_='price-actual').text.strip()
                string_to_write = [trip_name,departure_date,'actual_price',actual_price]
                csv_writer.writerow(string_to_write)
                # print([trip_name,departure_date,'actual_price',actual_price])
                
                if departure.find('p', class_='price-strike') == None:
                    original_price = None
                else:
                    original_price = departure.find('p', class_='price-strike').text
                string_to_write = [trip_name,departure_date,'original_price',original_price]
                csv_writer.writerow(string_to_write)
                # print([trip_name,departure_date,'original_price',original_price])
                
                if departure.find('div', class_='popular-message'):
                    popular_departure = True
                else:
                    popular_departure = False
                string_to_write = [trip_name,departure_date,'popular_departure',popular_departure]
                csv_writer.writerow(string_to_write)
                # print([trip_name,departure_date,'popular_departure',popular_departure])
                
                listing_status = departure.find('div', class_='listing-status').text.strip()
                string_to_write = [trip_name,departure_date,'listing_status',listing_status]
                csv_writer.writerow(string_to_write)
                # print([trip_name,departure_date,'listing_status',listing_status])
                
                if re.search( "Not Available", departure.find('div', class_='listing-buttons-contain').text):
                    available = False
                else:
                    available = True
                string_to_write = [trip_name,departure_date,'available',available]
                csv_writer.writerow(string_to_write)
                # print([trip_name,departure_date,'available',available])
                
            print('{}, done!'.format(trip_name))

if __name__ == '__main__': main()