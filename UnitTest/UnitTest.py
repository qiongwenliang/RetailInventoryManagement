import unittest
from RetailFunctions import RetailManagement

class TestRetailFunctions(unittest.TestCase):

    def test_transfer_product(self):

        mgmt_obj = RetailManagement("C:/Users/cater_yrqwkk6/Repository/RetailInventoryManagement/UnitTest/testData.xlsx",
                   ["Sales", "SKU", "Store", "Retail_revenue", "End_amount", "UNI_CODE", "Accumulate_Inventory"])

        transfer_record = mgmt_obj.transfer_product("Store", "Retail_revenue", "SKU", "31JPZ396150W", "Sales", "Accumulate_Inventory")

        self.assertTrue(len(transfer_record) == 1, "Number of Product should be only 1.")
        self.assertTrue([k for k in transfer_record.keys()][0] == '31JPZ396150W', "Key (product name) is not 31JPZ396150W.")
        