import xlrd


class ParseData:
    def __init__(self, path, column_name_list):
        """
        This class is to parse excel document and put it into python data structures that is ready to be used.
        :param path: path to the excel file.
        :param column_name_list: a list of strings, which are the inputs.
        """
        open_excel = xlrd.open_workbook(path)
        sheet = open_excel.sheet_by_index(0)

        self.collect = {}
        for name in column_name_list:
            for col in range(sheet.ncols):
                if sheet.cell_value(0, col) == name:
                    value_list = []
                    self.collect[name] = value_list
                    for row in range(1, sheet.nrows):
                        self.collect[name].append(sheet.cell_value(row, col))
