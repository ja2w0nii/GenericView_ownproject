from django import forms
from .models import Post, Comment


class PostUploadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment",]
        widgets = {"comment": forms.TextInput,}
