from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
# Для регистрации пользователей:
from django.contrib.auth.models import User


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text = 'Enter a date between now and 4 weeks (default 3).')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Проверим, что дата не выходит за нижнюю границу
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Проверим, что дата не выходит за верхнюю ганицу
        if data > datetime.date.today() + datetime.timedelta(weeks = 4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Помните, что всегда нужно возвращать cleaned_data
        return data


# Регистрируем пользователей библиотеки
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label = 'Пароль:', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Повторите пароль:', widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        data = self.cleaned_data
        print(data)
        if data['password'] != data['password2']:
            raise ValidationError(_('Пароли не совпадают!'))
        return data['password2']
