from django import forms
from .models import Professor, VoteItems

class VoteForm(forms.ModelForm):
    class Meta:
        model = VoteItems
        fields = ['name', 'options']
        widgets = {
            'name': forms.HiddenInput(),
            'options': forms.RadioSelect(choices=VoteItems.OPTIONS),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True

    def save(self, professor, commit=True):
        instance = super().save(commit=False)
        instance.professor = professor
        if commit:
            instance.save()
        return instance
