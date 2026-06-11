from openpyxl import Workbook
from openpyxl.drawing.image import Image


def export_to_excel(results):
    wb = Workbook()
    ws = wb.active
    ws.title = "Voltage Drop Report"

    # Add headers
    ws.append(["Parameter", "Value"])

    # Add results
    for key, value in results.items():
        ws.append([key, value])

    filename = "Voltage_Drop_Report.xlsx"

    try:
        # Try to add chart image if it exists
        chart = Image("voltage_drop_chart.png")
        chart.width = 500
        chart.height = 300
        ws.add_image(chart, "E2")          # Adds image starting at cell H3

    except Exception:
        # If image is not found or any error occurs, just continue without chart
        pass

    wb.save(filename)
    return filename