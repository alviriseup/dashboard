from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm



class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']



class UpdatePasswordForm(PasswordChangeForm):
    # old_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    # new_password1 = forms.CharField(widget=forms.PasswordInput(), required=True)
    # new_password2 = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_paswword2 = cleaned_data.get("new_password2")

        if new_password1 and new_paswword2 and new_password1 != new_paswword2:
            raise forms.ValidationError("The new passwords do not match.")
        
        return cleaned_data
    
        