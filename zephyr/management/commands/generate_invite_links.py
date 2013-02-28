from optparse import make_option
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from confirmation.models import Confirmation
from zephyr.models import User, PreregistrationUser

class Command(BaseCommand):
    help = "Generate activation links for users and print them to stdout."

    def handle(self, *args, **options):
        duplicates = False
        for email in args:
            try:
                User.objects.get(email=email)
                print email + ": There is already a user registered with that address."
                duplicates = True
                continue
            except User.DoesNotExist:
                pass

        if duplicates:
            return

        for email in args:
            prereg_user, created = PreregistrationUser.objects.get_or_create(email=email)
            print email + ": " + Confirmation.objects.get_link_for_object(prereg_user)

