import csv
from io import BytesIO
import xlsxwriter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .forms import IndividualActivityForm, LoggedInUserActivityForm
from .models import Activity
from ..core.helpers import export_to_csv, export_to_excel
from ..notes.models import Note
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
        form = IndividualActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.session_key = request.session.session_key
            activity.save()
            messages.success(request, 'Activity created successfully!')
            return redirect('activities:individual_dashboard')
    else:
        form = IndividualActivityForm()

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
            Q(project__team_members=self.request.user)
        ).select_related(
            'project',
            'assigned_to'
        ).order_by('-created_at').distinct()

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
        context['form'] = LoggedInUserActivityForm()
        return context

    def export_to_csv(self, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="activities.csv"'

        writer = csv.writer(response)

        writer.writerow(['Title', 'Project', 'Status', 'Assigned To', 'Due Date'])

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
    form_class = IndividualActivityForm
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
                'redirect_url': 'activities:team_dashboard',
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)


class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    template_name = 'activities/02_activity_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(activity=self.object).order_by('-created_at')
        return context


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    form_class = LoggedInUserActivityForm
    template_name = 'activities/03_activity_update.html'

    def get_success_url(self):
        return reverse_lazy('activities:activity_detail', kwargs={'pk': self.object.pk})


class ActivityStatusUpdate(LoginRequiredMixin, UpdateView):
    model = Activity
    fields = ['status']
    http_method_names = ['post']

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse_lazy('activities:team_dashboard'))