import csv
from io import BytesIO
import xlsxwriter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .forms import ActivityForm
from .models import Activity
from ..core.helpers import export_to_csv, export_to_excel
from ..notes.forms import NoteForm
from ..notifications.models import Notification
from ..projects.models import Project


def home(request):
    return render(request, 'common/02_home.html')


def individual_view(request):
    if not request.session.session_key:
        request.session.create()

    activities = Activity.objects.filter(
        session_key=request.session.session_key,
        project__isnull=True
    ).order_by('-created_at')

    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.session_key = request.session.session_key
            activity.save()
            messages.success(request, 'Activity created successfully!')
            return redirect('activities:individual_dashboard')
    else:
        form = ActivityForm()

    export_format = request.GET.get('export')
    if export_format == 'csv':
        return export_to_csv(activities)
    elif export_format == 'excel':
        return export_to_excel(activities)

    return render(request, 'activities/individual_dashboard.html', {
        'activities': activities,
        'form': form,
    })


class TeamDashboardView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activities/team_dashboard.html'
    context_object_name = 'activities'

    def get_queryset(self):
        queryset = Activity.objects.filter(
            Q(assigned_to=self.request.user) |
            Q(project__team_members=self.request.user),
            project__isnull=False
        ).select_related(
            'project',
            'assigned_to'
        ).order_by('-created_at')

        project_id = self.request.GET.get('project')
        if project_id:
            queryset = queryset.filter(project_id=project_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(
            team_members=self.request.user
        ).order_by('title')
        context['selected_project'] = self.request.GET.get('project')
        context['form'] = ActivityForm()
        return context

    def export_to_csv(self, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="activities.csv"'

        writer = csv.writer(response)
        # Write header
        writer.writerow(['Title', 'Project', 'Status', 'Assigned To', 'Due Date'])

        # Write data
        for activity in queryset:
            writer.writerow([
                activity.title,
                activity.project.title if activity.project else '',
                activity.get_status_display(),
                activity.assigned_to.email if activity.assigned_to else 'Unassigned',
                activity.due_date or 'No due date'
            ])

        return response

    def export_to_excel(self, queryset):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#F0F0F0'
        })

        headers = ['Title', 'Project', 'Status', 'Assigned To', 'Due Date']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        for row, activity in enumerate(queryset, start=1):
            worksheet.write(row, 0, activity.title)
            worksheet.write(row, 1, activity.project.title if activity.project else '')
            worksheet.write(row, 2, activity.get_status_display())
            worksheet.write(row, 3, activity.assigned_to.email if activity.assigned_to else 'Unassigned')
            worksheet.write(row, 4, activity.due_date.strftime('%Y-%m-%d') if activity.due_date else 'No due date')

        workbook.close()

        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="activities.xlsx"'

        return response

    def get(self, request, *args, **kwargs):
        export_format = request.GET.get('export')

        if export_format:
            queryset = self.get_queryset()

            if export_format == 'csv':
                return self.export_to_csv(queryset)
            elif export_format == 'excel':
                return self.export_to_excel(queryset)

        return super().get(request, *args, **kwargs)


class ActivityCreateView(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activity_form_modal.html'
    success_message = "Activity was created successfully!"
    success_url = reverse_lazy('activities:team_dashboard')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.assigned_to = self.request.user
        project_id = self.request.POST.get('project')
        if project_id:
            form.instance.project_id = project_id

        response = super().form_valid(form)

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': self.success_message,
                'redirect_url': self.get_success_url()
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)

    # def get_success_url(self):
    #     if self.object.project:
    #         return reverse_lazy('activities:team_dashboard')
    #     return reverse_lazy('activities:individual_dashboard')


class ActivityDetailView(DetailView):
    pass


class ActivityUpdateView(UpdateView):
    pass


class ActivityDeleteView(DeleteView):
    pass





@login_required
def activity_detail(request, pk):
    """Detail view for an activity, including notes"""
    activity = get_object_or_404(Activity, pk=pk)
    notes = activity.notes.all().order_by('-created_at')
    note_form = NoteForm()

    if request.method == 'POST':
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.activity = activity
            note.created_by = request.user
            note.save()
            # Create notifications for team members
            if activity.project:
                for member in activity.project.team_members.all():
                    Notification.objects.create(
                        recipient=member,
                        note=note
                    )
            messages.success(request, 'Note added successfully!')
            return redirect('activities:activity_detail', pk=pk)

    return render(request, 'activities/activity_detail.html', {
        'activity': activity,
        'notes': notes,
        'note_form': note_form,
    })