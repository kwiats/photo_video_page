from django import forms

from portfolio.models import MediaFile


class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['title', 'file_type', 'file']