from django import forms
from .models import Book


# ExampleForm - demonstrates form with validation
class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Sanitize input to prevent XSS
        if '<' in name or '>' in name:
            raise forms.ValidationError("Invalid characters in name.")
        return name


# BookForm - for creating/editing books securely
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Validate and sanitize input
        if '<' in title or '>' in title:
            raise forms.ValidationError("Invalid characters in title.")
        return title