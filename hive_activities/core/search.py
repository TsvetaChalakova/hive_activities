from django.db.models import Q
from django.contrib.postgres.search import (
    SearchVector, SearchQuery, SearchRank, TrigramSimilarity
)

from hive_activities.activities.models import Activity
from hive_activities.notes.models import Note
from hive_activities.projects.models import Project


class SearchService:
    @staticmethod
    def search_projects(query, user):
        """Search projects user has access to"""
        return Project.objects.filter(
            Q(team_members=user),
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    @staticmethod
    def search_activities(query, user):
        """Search tasks user has access to"""
        return Activity.objects.filter(
            Q(project__team_members=user),
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    @staticmethod
    def search_notes(query, user):
        """Search comments in tasks user has access to"""
        return Note.objects.filter(
            Q(task__project__team_members=user),
            Q(content__icontains=query)
        ).distinct()

    @staticmethod
    def global_search(query, user):
        """Perform a global search across all relevant models"""
        projects = SearchService.search_projects(query, user)
        activities = SearchService.search_activities(query, user)
        notes = SearchService.search_notes(query, user)

        return {
            'projects': projects[:5],
            'tasks': activities[:5],
            'comments': notes[:5],
        }