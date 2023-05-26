import win32com.client as win32
import os
from time import sleep


def export_charts_as_png(excel_file_path, output_folder):
    excel = win32.Dispatch("Excel.Application")
    # excel.Visible = False  # Set to True if you want to see the Excel application
    # excel.DisplayAlerts = False

    workbook = excel.Workbooks.Open(excel_file_path)
    worksheets = workbook.Worksheets

    sheet = workbook.Worksheets('Golden_LSC')

    data = [
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4],
    ]

    for i in range(3):
        for j in range(4):
            print(data[i][j])
            sheet.Cells(4+i, j+1).Value = data[i][j]

    workbook.Save()

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for worksheet in worksheets:
        for i, chart in enumerate(worksheet.ChartObjects()):
            print(chart.Chart.ChartTitle.Text)
            # 要Activate才能存!!!
            chart.Activate()
            # chart.Width = 600  
            # chart.Height = 400  
            # Export each chart as .png
            print(chart.Chart.Export(os.path.join(os.getcwd(), output_folder, chart.Chart.ChartTitle.Text)+".png"))
        break

    # sleep(1)
    # workbook.Close(SaveChanges=False, Filename=excel_file_path)
    # workbook.Save()
    workbook.Close()
    excel.Quit()

excel_file_path = os.path.abspath("GM2_分析.xlsx")
output_folder = "charts"
export_charts_as_png(excel_file_path, output_folder)



