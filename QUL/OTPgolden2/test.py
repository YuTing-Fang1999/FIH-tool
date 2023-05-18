import xlwings as xw  # pip install xlwings

def main():
    wb = xw.Book.caller()
    sheet = wb.sheets[0]

    sheet.range('A1').value = 123
