import xlwings as xw

# Set a mock caller to simulate an active workbook
xw.Book("test.xlsx").set_mock_caller()

# Example: Accessing a worksheet and a cell
wb = xw.Book.caller()
sheet = wb.sheets['工作表1']
cell_value = sheet.range('A1').value

# Example: Modifying a cell value
sheet.range('B1').value = 'Hello, Excel!'

# Example: Saving the workbook (not required for mock caller)
wb.save()

# Example: Closing the workbook (not required for mock caller)
wb.close()
