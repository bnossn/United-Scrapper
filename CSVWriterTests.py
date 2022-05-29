# https://www.geeksforgeeks.org/how-to-append-a-new-row-to-an-existing-csv-file/

# Import DictWriter class from CSV module
from csv import DictWriter
  
# list of column names 
field_names = ['ID','NAME','RANK',
               'ARTICLE','COUNTRY']
  
# Dictionary
dict={'ID':7,'NAME':'William2','RANK':55322,
      'ARTICLE':12,'COUNTRY':'UAE2'}
  
# Open your CSV file in append mode
# Create a file object for this file
with open('WriteDataTest.csv', 'a') as f_object:
      
    # Pass the file object and a list 
    # of column names to DictWriter()
    # You will get a object of DictWriter
    dictwriter_object = DictWriter(f_object, fieldnames=field_names)
  
    #Pass the dictionary as an argument to the Writerow()
    dictwriter_object.writerow(dict)
  
    #Close the file object
    f_object.close()