from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.db.models import Model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    online_id = forms.CharField(
        required=True,
        label="online id"
    )

    DOB = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Date of Birth"
    )

    class Meta:
        model = User
        fields = (
            "username",
            "online_id",
            "DOB",
            "password1",
            "password2"
        )

class CustomUserUpdateForm(forms.ModelForm):

    online_id = forms.CharField(
        required=True,
        label="online id"
    )
    DOB = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label="Date of Birth"
    )

    class Meta:
        model = User
        fields = ("username","online_id","DOB")
    
    def clean_username(self):

        username = self.cleaned_data.get("username")

        if get_user_model().objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already in use. Please choose a different one.")
        return username