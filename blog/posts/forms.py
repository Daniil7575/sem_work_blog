from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')

    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            Post.objects.get(slug=slugify(title))
        except Exception:
            return title
        else:
            raise ValidationError('Пост с таким заголовком уже опубликован.')
