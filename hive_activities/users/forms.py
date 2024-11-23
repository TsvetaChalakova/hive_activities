from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from hive_activities.users.models import UserProfile, AppUser

UserModel = get_user_model()


class HiveAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'autocomplete': 'email',
            'class': 'form-control',
            'aria-label': 'Email address',
        }),
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
            'class': 'form-control',
            'aria-label': 'Password',
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        label="Remember me",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )


# class AppUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = UserModel



class AppUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email", "class": "form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password", "class": "form-control"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm your password", "class": "form-control"})
    )

    class Meta:
        model = AppUser
        fields = ["email", "password1", "password2"]
        field_order = ["email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if AppUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Automatically create an associated UserProfile
            from .models import UserProfile
            UserProfile.objects.create(user=user)
        return user




class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', )

