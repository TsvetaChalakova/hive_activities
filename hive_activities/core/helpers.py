from django.http import HttpResponse
import csv
import xlsxwriter
from io import BytesIO


def export_data(queryset, headers, row_data, file_type="csv"):
    if file_type == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="data.csv"'
        writer = csv.writer(response)
        writer.writerow(headers)
        for item in queryset:
            writer.writerow(row_data(item))
        return response

    elif file_type == "excel":
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        header_format = workbook.add_format({'bold': True, 'bg_color': '#F0F0F0'})
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        for row, item in enumerate(queryset, start=1):
            for col, value in enumerate(row_data(item)):
                worksheet.write(row, col, value)
        workbook.close()
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="data.xlsx"'
        return response