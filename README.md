# WebstaurantParser
It's an GUI application written on Python. It allows you to choose a category of product on https://www.webstaurantstore.com/ website and parse it in xlsx file.  

# Code
All categories are loaded after program starts from `categories.json` file.
### Parsing
Module `parser.py` contains functionality for parsing count of pages(from pagination), parsing urls for each product of page, parsing a product data.
### Writing to xlsx
Module `xlsx_writer.py` has one function for writing a list of products to xlsx file. It creates a new file with current time name and writes a data.
