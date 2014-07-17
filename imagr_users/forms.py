from django import forms
from imagr_users.models import ImagrUser
from registration.forms import RegistrationForm


class ImagrUserRegistrationForm(RegistrationForm):
    def clean_username(self):
        """Validate that the username is alphanumeric and is not already in use.
        """
        existing = ImagrUser.objects.filter(
            username__iexact=self.cleaned_data['username']
        )
        if existing.exists():
            raise forms.ValidationError(
                "A user with that username already exists."
            )
        else:
            return self.cleaned_data['username']