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


    def find_store_by_product(self, sku, target_product, store, sales, inventory):
        """
        This function is to find the quantity of the targeted product in each store.
        :param sku: a string that represents the element of sku of the product in the excel file.
        :param target_product: a string that represents the sku of the product to be researched.
        :param store: a string that represents the element of stores in the excel file.
        :param sales: a string that represents the element of sales in the excel file.
        :param inventory: a string that represents the element of inventory in the excel file.
        :return: a dictionary consisted of keys of the store name, and value of a float of the quantity of the
        targeted product.
        """
        stores = collections.defaultdict(int)
        for i in range(len(self.retail.collect[sku])):
            if self.retail.collect[sku][i] == target_product:
                if self.retail.collect[store][i] != "":
                    self.retail.collect[sales][i] = 0 if self.retail.collect[sales][i] == "" else \
                    self.retail.collect[sales][i]
                    stores[self.retail.collect[store][i]] += self.retail.collect[inventory][i] - self.retail.collect[sales][
                        i]

        return stores


    def transfer_product(self, store, revenue, sku, target_product, sales, inventory):
        """
        This function is to transfer products with low sales to stores with high revenue.
        :param store: a string that represents the element of stores in the excel file.
        :param revenue: a string that represents the element of retail revenue in the excel file.
        :param sku: a string that represents the element of sku of the product in the excel file.
        :param target_product: a string that represents the sku of the product to be researched.
        :param sales: a string that represents the element of sales in the excel file.
        :param inventory: a string that represents the element of inventory in the excel file.
        :return: a dictionary consists of keys of the sku of the product, and value of a list of strings that record
        the expected transportation of the targeted product.
        """
        revenue_store = self.sort_by_quantity(store, revenue, True)
        store_product = self.find_store_by_product(sku, target_product, store, sales, inventory)

        transfer_record = collections.defaultdict(list)
        for shop in store_product:
            amount = store_product[shop]
            if amount >= 3:
                for mall in revenue_store:
                    if amount // 3 > 0:
                        content = [shop, mall[1], 3]
                        transfer_record[target_product].append(content)
                        amount -= 3
                    elif 0 < amount < 3:
                        if transfer_record[target_product]:
                            to_ship = int(transfer_record[target_product][0][-1])
                            transfer_record[target_product][0] = [shop, revenue_store[0][1], int(amount + to_ship)]
                        else:
                            content = [shop, revenue_store[0][1], int(amount)]
                            transfer_record[target_product].append(content)
                        break
                    else:
                        break

        return transfer_record


    def estimate_sales(self, store, revenue, sku, target_product, sales, inventory):
        """
        This function is to estimate sales of a targeted product in a specific store.
        :param store: a string that represents the element of stores in the excel file.
        :param revenue: a string that represents the element of retail revenue in the excel file.
        :param sku: a string that represents the element of sku of the product in the excel file.
        :param target_product: a string that represents the sku of the product to be researched.
        :param sales: a string that represents the element of sales in the excel file.
        :param inventory: a string that represents the element of inventory in the excel file.
        :return:
        """
        transfered_product = self.transfer_product(store, revenue, sku, target_product, sales, inventory)
        store_to_check = []
        for mall in transfered_product[target_product]:
            store_to_check.append(mall[1])

        target_product_sales = {target_product: {}}
        for shop in store_to_check:
            for pointer in range(len(self.retail.collect[store])):
                if shop == self.retail.collect[store][pointer] and target_product == self.retail.collect[sku][pointer]:
                    if shop not in target_product_sales[target_product]:
                        if not self.retail.collect[sales][pointer]:
                            target_product_sales[target_product][shop] = 0
                        else:
                            target_product_sales[target_product][shop] = self.retail.collect[sales][pointer]
                    else:
                        if self.retail.collect[sales][pointer]:
                            prev = target_product_sales[target_product][shop]
                            target_product_sales[target_product][shop] = prev + self.retail.collect[sales][pointer]

        return target_product_sales



