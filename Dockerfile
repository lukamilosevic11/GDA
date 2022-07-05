FROM python:3.9

WORKDIR /GDA

ENV API_KEY ""
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY GDA_backend/Classes ./GDA_backend/Classes
COPY GDA_backend/Common ./GDA_backend/Common
COPY GDA_backend/Data ./GDA_backend/Data
COPY GDA_backend/Mapping ./GDA_backend/Mapping
COPY GDA_backend/Other ./GDA_backend/Other
COPY GDA_backend/Sources ./GDA_backend/Sources

COPY GDA_frontend/GDA_datatables ./GDA_frontend/GDA_datatables
COPY GDA_frontend/GDA_frontend ./GDA_frontend/GDA_frontend
COPY GDA_frontend/manage.py ./GDA_frontend

COPY requirements.txt .

RUN ["mkdir", "-p", "./GDA_backend/Storage"]
RUN ["pip3", "install", "-r", "./requirements.txt"]

ENV PYTHONPATH "${PYTHONPATH}:../"
RUN ["python", "./GDA_frontend/manage.py", "migrate"]

CMD python ./GDA_frontend/manage.py gda_start $API_KEY
