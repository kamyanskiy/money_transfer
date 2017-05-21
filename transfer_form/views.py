from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from .forms import TransferForm


class SuccessView(generic.TemplateView):
    template_name = "transfer_form/thanks.html"


class TransferView(generic.View):
    form_class = TransferForm
    template_name = 'transfer_form/money_transfer_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return redirect(reverse_lazy('success'))

        return render(request, self.template_name, {'form': form})

