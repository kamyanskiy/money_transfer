from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy

from .forms import TransferForm
from .models import Person


class SuccessView(generic.TemplateView):
    template_name = "transfer_form/thanks.html"


class ErrorView(generic.TemplateView):
    template_name = "transfer_form/error.html"


class TransferView(generic.View):
    form_class = TransferForm
    template_name = 'transfer_form/money_transfer_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            transfer_amount = form.cleaned_data['amount']

            recipient_ssns = form.cleaned_data['recipients_list']
            recipient_ssns = recipient_ssns.split(',')
            recipient_ssns = [l.strip() for l in recipient_ssns]

            recipient_objs = Person.objects.filter(
                ssn__in=recipient_ssns).exclude(ssn=sender.ssn)

            if sender.balance.amount >= transfer_amount:
                paid_sum = sender.balance.amount - transfer_amount
                sender.balance.amount = paid_sum
                sender.save()
                recipient_sum = transfer_amount / recipient_objs.count()
                for recipient in recipient_objs:
                    rcp_balance = recipient.balance.amount + recipient_sum
                    recipient.balance.amount = rcp_balance
                    recipient.save()
            else:
                return redirect(reverse_lazy('error'))

            return redirect(reverse_lazy('success'))

        return render(request, self.template_name, {'form': form})

