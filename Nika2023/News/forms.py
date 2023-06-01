from django import forms
from .models import News, NewsImage, Comment


class NewsForm(forms.ModelForm):
    images = forms.ImageField(label='Добавить фото(можно несколько)',
                              widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = News
        fields = ['title', 'content', 'is_published']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'content': forms.Textarea(attrs={'class': 'form-control'})}
        labels = {'title': 'Заголовок', 'content': 'Текст новости', 'is_published': 'Опубликовать'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': 'Введите комментарий'}
