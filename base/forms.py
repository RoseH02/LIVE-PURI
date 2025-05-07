from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Recipe

class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    preparation_steps = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'preparation_steps', 'image']
