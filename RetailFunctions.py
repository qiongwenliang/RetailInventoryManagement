import collections
from ParseData import ParseData


class RetailManagement:
    def __init__(self, path, column_list):
        self.retail = ParseData(path, column_list)


    def sort_by_quantity(self, key, quantity, reverse=True):
        """
        By giving Key and quantity, returns a dictionary of key and a list of elements related to the key.
        :param key: a string of the excel column name.
        :param quantity: a string of excel column name.
        :param reverse: True to obtain the returned list with descending order, otherwise False.
        :return: a list of lists that contains a float at first place, and a string at second place.
        """
        if key not in self.retail.collect or quantity not in self.retail.collect:
            raise RuntimeError("Please choose the correct input")

        key_collect = collections.defaultdict(float)
        for i in range(len(self.retail.collect[quantity])):
            if self.retail.collect[quantity][i] != "":
                key_collect[self.retail.collect[key][i]] += self.retail.collect[quantity][i]

        quantity_key = []
        for k in key_collect:
            quantity_key.append([key_collect[k], k])

        quantity_key.sort(key=lambda x: x[0], reverse=reverse)

        return quantity_key


    def valid_product_sort_by_sales(self, unicode, sku, sales):
        """
        This function is to find the product for sell, not the giveaway product in the excel file, by its sku and
        returns with its sales volume.
        :param unicode: a string that represents the element of unicode of the product in the excel file.
        :param sku: a string that represents the element of sku of the product in the excel file.
        :return: a list of lists that contains a float at the first place and a string at second place.
        """
        valid_sku = set()
        for i in range(len(self.retail.collect[unicode])):
            if self.retail.collect[unicode][i] != "":
                valid_sku.add(self.retail.collect[sku][i])

        sales_sku = self.sort_by_quantity(sku, sales, False)

        valid_product = []
        for product in sales_sku:
            if product[1] in valid_sku:
                valid_product.append(product)

        return valid_product


