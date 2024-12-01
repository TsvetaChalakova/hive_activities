from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff_admin()

    def handle_no_permission(self):
        messages.error(self.request, "You do not have access to this section.")
        return redirect('activities:team_dashboard')
