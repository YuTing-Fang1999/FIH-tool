from win32com import client as wc
import os
 
def open_and_save(filename):
    xl = wc.DispatchEx("Excel.Application")
    wb = xl.workbooks.open(os.path.abspath(filename))
    xl.Visible = False
    wb.Save()
    xl.Quit()

