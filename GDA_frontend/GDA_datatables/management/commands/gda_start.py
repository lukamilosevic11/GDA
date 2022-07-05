#  GDA Copyright (c) 2022.
#  University of Belgrade, Faculty of Mathematics
#  Luka Milosevic
#  lukamilosevic11@gmail.com
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Starts the GDA app with API key for typesense search engine'

    def add_arguments(self, parser):
        parser.add_argument('api_key', type=str)

    def handle(self, *args, **options):
        try:
            with open("api_key.txt", "w") as api_key_file:
                api_key_file.write(options['api_key'])

            call_command("runserver", "0.0.0.0:8000")
        except Exception as e:
            self.stdout.write(self.style.ERROR('ERROR: ' + str(e)))
