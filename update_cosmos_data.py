#!/usr/bin/env python3

from selenium import webdriver
import requests
import bs4
import re
import csv
from datetime import date
from tqdm import tqdm

def main():

    today = date.today()
    file_name = 'cosmos_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','Departure Date','field','value']
        csv_writer.writerow(field_names)

        linksUS = (
            'https://www.cosmos.com/tour/highlights-of-the-canyonlands/8520/?nextyear=true&content=price',
            'https://www.cosmos.com/tour/the-lone-star-state-to-the-french-quarter/8090/?nextyear=true&content=price'
        )

        print()

        for link in tqdm(linksUS):

            res = requests.get(link)
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            trip_name = soup.find("h1").contents[0].text
            code = soup.find("h1").contents[2].text
            code = code.strip("()")
            # print('{} - {}'.format(trip_name, code))
            
            for departure in soup.find_all('div', class_='listing'):

                date_numbers = departure.find('p', class_='date-numbers').text.split()
                departure_date = '{}-{}-{}'.format(date_numbers[0], date_numbers[1], date_numbers[2])
                # print(departure_date)
                
                actual_price = departure.find('p', class_='price-actual').text.strip()
                string_to_write = [trip_name,departure_date,'Actual Price USD',actual_price]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                if departure.find('p', class_='price-strike'):
                    original_price = departure.find('p', class_='price-strike').text
                else:
                    original_price = actual_price
                string_to_write = [trip_name,departure_date,'Original Price USD',original_price]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                if departure.find('div', class_='popular-message'):
                    popular_departure = True
                else:
                    popular_departure = False
                string_to_write = [trip_name,departure_date,'Popular Departure',popular_departure]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                listing_status = departure.find('div', class_='listing-status').text.strip()
                string_to_write = [trip_name,departure_date,'Listing Status',listing_status]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                if re.search( "Not Available", departure.find('div', class_='listing-buttons-contain').text):
                    available = False
                else:
                    available = True
                string_to_write = [trip_name,departure_date,'Available',available]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)

            linkAU = "https://www.cosmostours.com.au/booking?tour={}&season=2020".format(code)
            driver = webdriver.Chrome()
            driver.get(linkAU)
            html = driver.execute_script("return document.documentElement.outerHTML")
            soup = bs4.BeautifulSoup(html, 'lxml')

            for departure in soup.findAll('div', class_='booking-departures__wrapper'):

                date_numbers = departure.find('span', class_='booking-departures__date').text.split()
                departure_date = "{}-{}-{}".format(date_numbers[0], (date_numbers[1])[0:3], (date_numbers[2])[2:4])
                # print(departure_date)

                actual_price = departure.find('span', class_='booking-departures__price--amount').text
                string_to_write = [trip_name,departure_date,'Actual Price AUD',actual_price]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)
                
                if departure.find('span', class_='booking-departures__price--strike-through'):
                    original_price = departure.find('span', class_='booking-departures__price--strike-through').text
                else:
                    original_price = actual_price
                string_to_write = [trip_name,departure_date,'Original Price AUD',original_price]
                csv_writer.writerow(string_to_write)
                # print(string_to_write)

        print("\nDone!\n")

if __name__ == '__main__': main()