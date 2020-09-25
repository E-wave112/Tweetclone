from django import forms
from .models import Tweet
from django.conf import settings
from django.contrib import messages


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > settings.MAX_TWEET_LENGTH:
           raise forms.ValidationError('max characters exceeded')
        return  content