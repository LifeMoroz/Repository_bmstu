from django import forms

from app.library.models import Category


class CategoryForm(forms.ModelForm):
    title = forms.CharField(
        label='Название',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Введите имя'}),
    )
    access = forms.ChoiceField(
        label='Уровень доступа',
        widget=forms.RadioSelect(), choices=Category.ACCESS_CHOICES
    )

    class Meta:
        model = Category
        fields = ('title', 'access')
