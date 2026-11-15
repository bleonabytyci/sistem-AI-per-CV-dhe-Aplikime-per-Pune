from django import forms
from .models import CV


class CVUploadForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['file']
        labels = {
            'file': 'Ngarko CV-ne'
        }
        widgets = {
            'file': forms.FileInput(
                attrs={
                    'accept': '.pdf,.docx'
                }
            )
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file:
            allowed_extensions = ['pdf', 'docx']
            extension = file.name.rsplit('.', 1)[-1].lower()

            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    'Lejohen vetem skedaret PDF dhe DOCX.'
                )

            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    'CV-ja nuk mund te jete me e madhe se 5 MB.'
                )

        return file