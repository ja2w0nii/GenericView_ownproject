from django import forms
from .models import Post


class PostUploadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]
