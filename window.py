import json

import xlsxwriter
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QErrorMessage, QMessageBox

import parser
import xlsx_writer
from product import Product


class Ui_Dialog(object):
    categories = []

    def setupUi(self, Dialog):
        self.loadCategories()

        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 200)

        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(60, 30, 291, 200))
        self.formLayoutWidget.setObjectName("formLayoutWidget")

        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.categoryLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.categoryLabel.setObjectName("categoryLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.categoryLabel)

        self.categoryComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.categoryComboBox.setObjectName("categoryComboBox")
        for category in self.categories:
            self.categoryComboBox.addItem(category["name"])
        self.categoryComboBox.currentIndexChanged.connect(self.onCategoryComboBoxChange)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.categoryComboBox)

        # Subcategory config
        self.subcategoryLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.subcategoryLabel.setObjectName("subcategoryLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.subcategoryLabel)

        self.subcategoryComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.subcategoryComboBox.setObjectName("subcategoryComboBox")

        # Loading subcategories
        first_category = self.categories[0]
        name = first_category['name']
        items = self.getCategoriesByParentName(self.categories, name)
        for item in items:
            self.subcategoryComboBox.addItem(item['name'])
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.subcategoryComboBox)

        # Save button config
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(60, 150, 91, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.onParseAndSaveButtonClick)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Webstraurant Parser", "Webstraurant Parser"))
        self.categoryLabel.setText(_translate("Dialog", "Category"))
        self.subcategoryLabel.setText(_translate("Dialog", "Subcategory"))
        self.pushButton.setText(_translate("Dialog", "Parse & Save"))

    def onCategoryComboBoxChange(self):
        subcategories = self.getSubcategoriesByCategoryParentName(self.categoryComboBox.currentText())
        self.subcategoryComboBox.clear()
        self.subcategoryComboBox.addItems(subcategories)

    def loadCategories(self):
        self.categories = json.load(open("categories.json"))

    def getCategoriesByParentName(self, categories, parentName):
        for category in categories:
            if category['name'] == parentName:
                return category["subcategories"]

    def onParseAndSaveButtonClick(self):
        try:
            chosen_category = self.categoryComboBox.currentText()
            chosen_subcategory = self.subcategoryComboBox.currentText()

            for category in self.categories:
                if category['name'] == chosen_category:
                    subcategories = category['subcategories']
                    for subcategory in subcategories:
                        if subcategory['name'] == chosen_subcategory:
                            pages = parser.get_pages_size('https://www.webstaurantstore.com/' + subcategory['page'])
                            products = []
                            for page in range(1, pages + 1):
                                urls = parser.get_items_urls('https://www.webstaurantstore.com/' + subcategory['page'] + '?page=' + str(page))
                                for url in urls:
                                    product = parser.get_product('https://www.webstaurantstore.com' + url)
                                    products.append(product)
                            if len(products) == 0:
                                dialog = QMessageBox()
                                dialog.setText('There arn\'t products')
                                dialog.setWindowTitle('Webstaurant Parser')
                                button = dialog.exec()
                            xlsx_writer.write_products(products)
                            dialog = QMessageBox()
                            dialog.setText('Successfully written xlsx file with products!')
                            dialog.setWindowTitle('Webstaurant Parser')
                            button = dialog.exec()


        except Exception:
            dialog = QMessageBox()
            dialog.setText('Error when parsing')
            dialog.setWindowTitle('Error')
            button = dialog.exec()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
