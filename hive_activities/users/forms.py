from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from hive_activities.users.models import UserProfile, AppUser

UserModel = get_user_model()


class HiveActivitiesAuthenticationForm(AuthenticationForm):

    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'autocomplete': 'off',
            'class': 'form-control',
            'aria-label': 'Email address',
        }),
        label="Email",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'autocomplete': 'off',
            'class': 'form-control',
            'aria-label': 'Password',
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        label="Remember me",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )


class AppUserCreationForm(UserCreationForm):

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your first name", "class": "form-control"})
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your last name", "class": "form-control"})
    )

    telephone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter your telephone number", "class": "form-control"})
    )

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
        fields = ["first_name", "last_name", "telephone", "email", "password1", "password2"]
        field_order = ["first_name", "last_name", "telephone", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if AppUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': self.cleaned_data['first_name'],
                    'last_name': self.cleaned_data['last_name'],
                    'telephone': self.cleaned_data['telephone']
                }
            )
        return user


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user', )
        fields = ['first_name', 'last_name', 'telephone']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your given name.',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your surname.',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your contact number.',
            }),
        }

