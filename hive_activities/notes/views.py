from django.shortcuts import render
from django.views.generic import CreateView

from hive_activities.notes.models import Note


class NoteCreateView(CreateView):
    model = Note

