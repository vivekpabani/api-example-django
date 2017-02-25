from django.test import TestCase
from django.core import mail
from datetime import date
from .util import send_email_util, day_difference


class UtilTestCases(TestCase):

    def test_day_difference_same_year(self):

        date1 = date(day=1, month=1, year=2000)
        date2 = date(day=31, month=1, year=2000)

        self.assertEqual(day_difference(date2, date1), 30)
        self.assertEqual(day_difference(date1, date2), -30)

    def test_day_difference_different_year(self):

        date1 = date(day=1, month=1, year=1900)
        date2 = date(day=31, month=1, year=2000)

        self.assertEqual(day_difference(date2, date1), 30)
        self.assertEqual(day_difference(date1, date2), -30)

    def test_send_email(self):

        send_email_util('to@example.com', 'Test Message')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Happy Birthday!')
        self.assertEqual(mail.outbox[0].body, 'Test Message')
