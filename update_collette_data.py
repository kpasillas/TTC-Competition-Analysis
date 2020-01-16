#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import bs4
import csv
from datetime import date
from tqdm import tqdm

def main():

    today = date.today()
    file_name = 'collette_data_{}.csv'.format(today.strftime("%m-%d-%y"))
    
    with open(file_name, 'a') as new_file:
        csv_writer = csv.writer(new_file, lineterminator='\n')

        field_names = ['Trip Name','Departure Date','field','value']
        csv_writer.writerow(field_names)
        # print(field_names)
    
        linkUS = (
            'https://www.gocollette.com/en/tours/north-america/usa/national-parks/booking?b=1#step/1',
            'https://www.gocollette.com/en/tours/north-america/usa/alaska-and-the-yukon/booking?b=1#step/1',
        )

        print("\n")

        for link in tqdm(linkUS):
        
            driver = webdriver.Chrome()
            driver.get(link)

            nameElement = driver.find_element_by_tag_name('h3')
            soup = bs4.BeautifulSoup(nameElement.get_attribute('innerHTML'), 'lxml')
            trip_name = soup.contents[0].text.strip()
            # print(trip_name)

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'date-group-dates')))

                monthElements = driver.find_elements_by_class_name('date-group-dates')
                for month in monthElements:

                    departureElements = month.find_elements_by_class_name('date-group')
                    for departure in departureElements:

                        soup = bs4.BeautifulSoup(departure.get_attribute('innerHTML'), 'lxml')
                        # file.write(soup.prettify())

                        date_numbers = soup.find('div', class_='date').text.split()
                        departure_date = '{:02}-{}-{}'.format(int(date_numbers[1].strip(',')), date_numbers[0], date_numbers[2])
                        # print(departure_date)

                        if soup.find('div', class_='date-alert'):
                            notes = soup.find('div', class_='date-alert').text.strip()
                            string_to_write = [trip_name,departure_date,'Notes',notes]
                            csv_writer.writerow(string_to_write)
                            # print(string_to_write)

                        actual_price = soup.find('span', class_='discountedPrice').text.strip()
                        string_to_write = [trip_name,departure_date,'Actual Price USD',actual_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

                        if soup.find('span', class_='crossout'):
                            original_price = soup.find('span', class_='crossout').text.strip()
                        else:
                            original_price = actual_price
                        string_to_write = [trip_name,departure_date,'Original Price USD',original_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

            finally:
                driver.quit()

            split_link = link.split('/')
            linkAU = '{}//{}/{}-au/{}/{}/{}/{}/{}/{}'.format(split_link[0], split_link[2], split_link[3], split_link[4], split_link[5], split_link[6], split_link[7], split_link[8], split_link[9])
            # print(linkAU)

            driver = webdriver.Chrome()
            driver.get(linkAU)

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'date-group-dates')))

                monthElements = driver.find_elements_by_class_name('date-group-dates')
                for month in monthElements:

                    departureElements = month.find_elements_by_class_name('date-group')
                    for departure in departureElements:

                        soup = bs4.BeautifulSoup(departure.get_attribute('innerHTML'), 'lxml')
                        # file.write(soup.prettify())

                        date_numbers = soup.find('div', class_='date').text.split()
                        departure_date = '{:02}-{}-{}'.format(int(date_numbers[1].strip(',')), date_numbers[0], date_numbers[2])
                        # print(departure_date)

                        actual_price = soup.find('span', class_='discountedPrice').text.strip()
                        string_to_write = [trip_name,departure_date,'Actual Price AUD',actual_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

                        if soup.find('span', class_='crossout'):
                            original_price = soup.find('span', class_='crossout').text.strip()
                        else:
                            original_price = actual_price
                        string_to_write = [trip_name,departure_date,'Original Price AUD',original_price]
                        csv_writer.writerow(string_to_write)
                        # print(string_to_write)

            finally:
                driver.quit()

    new_file.close()

    print("\nDone!\n")

if __name__ == '__main__': main()