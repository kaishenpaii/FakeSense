from django import forms

class NewsForm(forms.Form):
    news_content = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'hometextarea_id',
            'rows': 20,
            'cols': 0,
            'placeholder': 'Paste URL link/article here...',
            'oninput': 'updateCharacterCount()'
        })
    )