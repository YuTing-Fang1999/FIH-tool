import win32com.client as win32
import os

def get_excel_addin_path(addin_name):
    try:
        excel = win32.Dispatch("Excel.Application")
        addins = excel.AddIns
        
        # Iterate through the add-ins collection
        for addin in addins:
            # print(addin.Name)
            if addin.Name == addin_name:
                # Retrieve the add-in file path
                return os.path.join(addin.Path, addin_name)
        
        # If add-in not found, return None
        return None
    except Exception as e:
        print("Error: ", str(e))
        return None
            

