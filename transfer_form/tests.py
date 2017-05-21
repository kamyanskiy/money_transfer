from hamcrest import *

from django.test import TestCase
from django.test import Client
from django.utils import timezone

from .forms import AppointmentForm
from .models import Doctor, Appointment


class AppointmentFormTest(TestCase):

    def setUp(self):
        self.doctor = Doctor.objects.create(name="Doctor name",
                                            profession="Surgeon")
        self.date = timezone.localdate().strftime('%Y-%m-%d')
        self.time = 1

    def test_appointment_form_valid(self):
        form = AppointmentForm(data={
            'patient_name': "Ill man name",
            'patient_phone': "+79788888888",
            'subject': "subj",
            'reason': 'reason text',
            'doctor': self.doctor.id,
            'time': self.time,
            'date': self.date,
        })
        self.assertTrue(form.is_valid())

    def test_appointment_form_invalid(self):
        form = AppointmentForm(data={
            'patient_name': "",
            'patient_phone': "+79788888888",
            'subject': "subj",
            'reason': 'reason text',
            'doctor': self.doctor.id,
            'time': self.time,
            'date': self.date,
        })
        self.assertFalse(form.is_valid())
        assert_that(form.errors,
                    is_(equal_to({'patient_name': ['This field is required.']}))
                    )
