from django import forms
from portfolio.models import MediaFile

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['title', 'file_type', 'file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'hidden',
                'id': 'file-upload',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].label = ''  # Remove the label for the file input