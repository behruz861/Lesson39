from django import forms

from .models import Post


class PostCreateModelForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('views', 'slug',)


