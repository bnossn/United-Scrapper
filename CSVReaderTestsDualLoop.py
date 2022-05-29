# https://thispointer.com/python-read-a-csv-file-line-by-line-with-or-without-header/

from csv import DictReader
# open file in read mode
with open('AirportsDataset.csv', 'r') as read_obj_from:
    # pass the file object to DictReader() to get the DictReader object
    dict_reader_from = DictReader(read_obj_from)
    # iterate over each line as a ordered dictionary
    for row_from in dict_reader_from:
        # row variable is a dictionary that represents a row in csv
        with open('AirportsDataset.csv', 'r') as read_obj_to:
            dict_reader_to = DictReader(read_obj_to)

            for row_to in dict_reader_to:

                # from/to pair cannot be equal
                if (row_from['id'] != row_to['id']):
                    print("pair: " + row_from['id'] + '/' + row_to['id'] ) 

            read_obj_to.close()
    
    read_obj_from.close()