"""
Command for sending e-mail users, then their photo in TOP 3 by day.
"""

import datetime

from django.core.management.base import BaseCommand
from django.db.models import Count
# from django.core.mail import send_mail

from app.models import PhotoOpening, User, Setting
from app.tasks import send_email


class Command(BaseCommand):
    """
    Command class
    """
    help = 'Choice TOP 3 by day and send e-mail.'

    def handle(self, *args, **options):
        """
        Choice winner and send e-mail.
        :param args:
        :param options:
        :return:
        """
        date_range = [
            datetime.datetime.now()-datetime.timedelta(days=1),
            datetime.datetime.now()
        ]

        max_views = PhotoOpening.objects.filter(date_view__range=date_range).\
            values('photo_id').annotate(views=Count('photo_id')).order_by('-views')[:3]

        for view in max_views:
            user = User.objects.get(photo=view['photo_id'])
            message = Setting.objects.get(name='daily_notification').value % (user.first_name,
                                                                              user.last_name)
            send_email.delay('Your photo in TOP 3', message, 'from@mail.ru', user.email)
