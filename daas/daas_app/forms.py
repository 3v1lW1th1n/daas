from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()
    zip_password = forms.CharField(widget=forms.PasswordInput(), required=False)
