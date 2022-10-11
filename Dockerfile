#
# GDA Copyright (c) 2022.
# University of Belgrade, Faculty of Mathematics
# Luka Milosevic
# lukamilosevic11@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#

FROM python:3.9

WORKDIR /GDA

ENV API_KEY ""
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:../"

COPY GDA_backend/Classes ./GDA_backend/Classes
COPY GDA_backend/Common ./GDA_backend/Common
COPY GDA_backend/Data ./GDA_backend/Data
COPY GDA_backend/Other ./GDA_backend/Other
COPY GDA_frontend/GDA_datatables ./GDA_frontend/GDA_datatables
COPY GDA_frontend/GDA_frontend ./GDA_frontend/GDA_frontend
COPY GDA_frontend/manage.py ./GDA_frontend
COPY requirements.txt .

RUN ["mkdir", "-p", "./GDA_frontend/Database"]
RUN ["mkdir", "-p", "./GDA_backend/Storage"]
RUN ["pip3", "install", "-r", "./requirements.txt"]
RUN ["python3", "./GDA_frontend/manage.py", "migrate"]

STOPSIGNAL SIGINT

CMD exec python3 ./GDA_frontend/manage.py gda_start $API_KEY
