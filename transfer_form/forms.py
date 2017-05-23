from django import forms

from .models import Person


class TransferForm(forms.Form):
    sender = forms.ModelChoiceField(queryset=Person.objects.all(),
                                    label="Отправитель")
    recipients_list = forms.CharField(max_length=512,
                                      label="Список ИНН получателей",
                                      widget=forms.Textarea(
                                          attrs={"placeholder": "Введите ИНН получателей через запятую."})
                                      )
    amount = forms.DecimalField(max_digits=10, decimal_places=2,
                                label="Cумма перевода",
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Сумма, руб'})
                                )


