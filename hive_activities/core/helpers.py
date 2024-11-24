import csv
from datetime import datetime, date

from django.http import HttpResponse
from django.utils.timezone import make_naive, is_naive
from openpyxl.workbook import Workbook


def export_to_csv(activities):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="activities.csv"'

    writer = csv.writer(response)

    writer.writerow(['Title', 'Description', 'Due Date', 'Priority', 'Status', 'Created At'])

    for activity in activities:
        writer.writerow([
            activity.title,
            activity.description,
            activity.due_date,
            activity.priority,
            activity.status,
            activity.created_at,
        ])
    return response


def export_to_excel(activities):

    wb = Workbook()
    ws = wb.active
    ws.title = "Activities"

    ws.append(['Title', 'Description', 'Due Date', 'Priority', 'Status', 'Created At'])

    for activity in activities:
        if isinstance(activity.due_date, datetime):
            due_date = (
                make_naive(activity.due_date) if activity.due_date and not is_naive(
                    activity.due_date) else activity.due_date
            )
        elif isinstance(activity.due_date, date):
            due_date = activity.due_date
        else:
            due_date = None

        if isinstance(activity.created_at, datetime):
            created_at = (
                make_naive(activity.created_at) if activity.created_at and not is_naive(
                    activity.created_at) else activity.created_at
            )
        elif isinstance(activity.created_at, date):  # Handle date objects
            created_at = activity.created_at
        else:
            created_at = None

        ws.append([
            activity.title,
            activity.description,
            due_date,
            activity.priority,
            activity.status,
            created_at,
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="activities.xlsx"'

    wb.save(response)
    return response