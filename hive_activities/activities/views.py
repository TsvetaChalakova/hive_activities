from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib import messages
from hive_activities.activities.forms import IndividualActivityForm, LoggedInUserActivityForm
from hive_activities.activities.models import Activity
from hive_activities.core.helpers import export_data
from hive_activities.notes.models import Note
from hive_activities.projects.models import Project


def home(request):
    return render(request, 'common/../../templates/activities/01_home.html')


class SearchResultsView(TemplateView):
    template_name = 'common/../../templates/activities/03_search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')

        if query:
            if self.request.user.is_authenticated:

                projects = Project.objects.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query),
                    Q(team_members=self.request.user) |
                    Q(manager=self.request.user)
                ).distinct()[:10]

                activities = Activity.objects.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query),
                    Q(assigned_to=self.request.user) |
                    Q(project__team_members=self.request.user) |
                    Q(project__manager=self.request.user)
                ).distinct()[:10]
            else:

                session_activities = self.request.session.get('viewed_activities', [])
                projects = Project.objects.none()

                if session_activities:
                    activities = Activity.objects.filter(
                        Q(title__icontains=query) |
                        Q(description__icontains=query),
                        id__in=session_activities
                    ).distinct()[:10]
                else:
                    activities = Activity.objects.none()

            context.update({
                'projects': projects,
                'activities': activities,
                'query': query,
                'has_results': projects.exists() or activities.exists()
            })

        return context


def individual_view(request):
    if not request.session.session_key:
        request.session.create()

    activities = Activity.objects.filter(
        session_key=request.session.session_key,
        project__isnull=True
    ).order_by('due_date')

    paginator = Paginator(activities, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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

    headers = ['Title', 'Description', 'Due Date', 'Priority', 'Status', 'Created At']
    row_data = lambda activity: [
        activity.title,
        activity.description,
        activity.due_date.strftime('%Y-%m-%d') if activity.due_date else 'No due date',
        activity.get_priority_display(),
        activity.get_status_display(),
        activity.created_at.strftime('%Y-%m-%d %H:%M:%S') if activity.created_at else '',
    ]

    if export_format == 'csv':
        return export_data(activities, headers, row_data, file_type='csv')
    elif export_format == 'excel':
        return export_data(activities, headers, row_data, file_type='excel')

    return render(request, 'activities/02_Individual_dashboard.html', {
        'activities': page_obj,
        'form': form,
    })


@require_http_methods(["POST"])
@csrf_protect
def update_activity_status(request, pk):
    try:
        activity = Activity.objects.get(id=pk, session_key=request.session.session_key)

        if activity.status == 'TO_DO':
            new_status = 'IN_PROGRESS'
        elif activity.status == 'IN_PROGRESS':
            new_status = 'COMPLETED'
        else:
            new_status = 'TO_DO'

        Activity.objects.filter(id=pk).update(status=new_status)

        updated_activity = Activity.objects.get(id=pk)

        return JsonResponse({
            'success': True,
            'new_status': new_status,
            'display_status': updated_activity.get_status_display()
        })

    except Activity.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Activity not found'
        }, status=404)
    except Exception as e:
        print(f"Error updating activity status: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


class TeamDashboardView(LoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activities/04_team_dashboard.html'
    context_object_name = 'activities'

    def get_queryset(self):
        queryset = Activity.objects.filter(
            Q(assigned_to=self.request.user) |
            Q(project__team_members=self.request.user)
        ).select_related(
            'project',
            'assigned_to'
        ).order_by('created_at').distinct()

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

    def get(self, request, *args, **kwargs):
        export_format = request.GET.get('export')

        if export_format:
            queryset = self.get_queryset()

            headers = ['Title', 'Project', 'Status', 'Assigned To', 'Due Date']
            row_data = lambda activity: [
                activity.title,
                activity.project.title if activity.project else '',
                activity.get_status_display(),
                activity.assigned_to.profile.get_full_name() if activity.assigned_to else 'Unassigned',
                activity.due_date.strftime('%Y-%m-%d') if activity.due_date else 'No due date',
            ]
            return export_data(queryset, headers, row_data, file_type=export_format)

        return super().get(request, *args, **kwargs)


class ActivityCreateView(CreateView):
    model = Activity
    form_class = IndividualActivityForm
    template_name = 'activities/05_modal_create_activity.html'
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


# Keep your current authenticated view
class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = Activity
    template_name = 'activities/06_activity_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity = self.object
        notes = Note.objects.filter(activity=activity).order_by('-created_at')

        paginator = Paginator(notes, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['notes'] = page_obj
        context['page_obj'] = page_obj
        context['can_add_notes'] = self.request.user.has_perm('activities.add_note')
        return context


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    form_class = LoggedInUserActivityForm
    template_name = 'activities/08_activity_update.html'

    def get_success_url(self):
        return reverse_lazy('activities:activity_detail', kwargs={'pk': self.object.pk})

