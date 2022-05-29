# https://thispointer.com/python-read-a-csv-file-line-by-line-with-or-without-header/

import os
import sys
from csv import DictReader

def main():
    # open file in read mode
    with open('AirportsDataset.csv', 'r') as read_obj:
        # pass the file object to DictReader() to get the DictReader object
        csv_dict_reader = DictReader(read_obj)
        try:
            
            test = next(csv_dict_reader)
            # iterate over each line as a ordered dictionary
            for row in csv_dict_reader:
                # row variable is a dictionary that represents a row in csv
                print(row)
        
        except ValueError:
            print('crash')
        finally:
            read_obj.close()

if __name__ == '__main__':
    main()