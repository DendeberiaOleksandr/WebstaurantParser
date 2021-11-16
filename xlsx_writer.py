from datetime import datetime

import xlsxwriter

from product import Product


def write_products(products):
    time = datetime.now().strftime("%d%m%Y_%H%M%S")
    workbook = xlsxwriter.Workbook(time + '.xlsx')
    worksheet = workbook.add_worksheet()
    for i in range(len(products)):
        product = products[i]
        if type(product) == Product:
            worksheet.write('A' + str(i+1), product.name)
            worksheet.write('B' + str(i+1), product.url)
            worksheet.write('C' + str(i+1), product.item_number)
            worksheet.write('D' + str(i+1), product.price)
            worksheet.write('E' + str(i+1), product.image_url)
    workbook.close()
