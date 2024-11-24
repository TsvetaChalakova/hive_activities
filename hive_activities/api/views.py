# from django.contrib.auth import get_user_model
# from django.contrib.auth.mixins import LoginRequiredMixin
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from hive_activities.api.forms import TemporaryActivityForm
# from hive_activities.api.models import TemporaryActivity
# from django.views.generic import ListView, TemplateView, FormView
# from rest_framework import serializers
#
# from hive_activities.core.search import SearchService
#
# UserModel = get_user_model()
#
#
# class TemporaryActivitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TemporaryActivity
#         fields = ['id', 'title', 'description', 'due_date', 'due_time']
#
#
# class LandingPageView(TemplateView):
#     template_name = 'common/02_home.html'
#
#
# class TemporaryActivityAPIView(APIView):
#     def get(self, request):
#         activities = TemporaryActivity.objects.all()
#         serializer = TemporaryActivitySerializer(activities, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = TemporaryActivitySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ContactView(ListView):
#     pass
#
#
# class SearchView(LoginRequiredMixin, TemplateView):
#     template_name = 'common/06_search_results.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         query = self.request.GET.get('q', '')
#
#         if query:
#             context['query'] = query
#             context['results'] = SearchService.global_search(query, self.request.user)
#
#         return context
