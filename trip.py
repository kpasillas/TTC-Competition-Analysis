import csv
from datetime import datetime

class Trip:
    
    def __init__(self, name, code, departures):
        self.name = name
        self.code = code
        self.departures = departures

    def print_deps(self, file_name):
        with open(file_name, 'a') as new_file:
            csv_writer = csv.writer(new_file, lineterminator='\n')

            field_names = ['Trip Name','DepartureID','field','value']
            csv_writer.writerow(field_names)

            previous_departure_date = ''
            duplicate_departure_count = 0
            
            for dep in self.departures:

                if dep.date == previous_departure_date:                   # check if duplicate departure
                    duplicate_departure_count += 1
                else:
                    duplicate_departure_count = 0
                departure_letter = str(chr(duplicate_departure_count + 97))

                date_split = dep.date.split('-')
                day = '{:02}'.format(int(date_split[0]))
                month = str(chr((datetime.strptime(date_split[1], '%b')).month + 64))
                year = date_split[2][-2:]
                departure_code = '{}{}{}{}'.format(day, month, year, departure_letter)
                departure_id = '{}{}-{}'.format(self.code, year, departure_code)
                
                csv_writer.writerow([self.name, departure_id, "DepartureDate", dep.date])
                csv_writer.writerow([self.name, departure_id, "ActualPriceUSD", dep.actual_price_usd])
                csv_writer.writerow([self.name, departure_id, "OriginalPriceUSD", dep.original_price_usd])
                csv_writer.writerow([self.name, departure_id, "ActualPriceAUD", dep.actual_price_aud])
                csv_writer.writerow([self.name, departure_id, "OriginalPriceAUD", dep.original_price_aud])
                csv_writer.writerow([self.name, departure_id, "Type", dep.type])
                csv_writer.writerow([self.name, departure_id, "Status", dep.status])
                csv_writer.writerow([self.name, departure_id, "Available", dep.available])
                csv_writer.writerow([self.name, departure_id, "Notes", dep.notes])

                previous_departure_date = dep.date