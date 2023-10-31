from django import forms
from posts.models import Post, Comment


class PostUploadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image"]


class CommentUploadForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment",]
