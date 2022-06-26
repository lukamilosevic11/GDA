FROM python:3.9

WORKDIR /gda

COPY Common ./Common
COPY Classes ./Classes
COPY Data ./Data
COPY Mapping ./Mapping
COPY Other ./Other
COPY Sources ./Sources
COPY main.py .
COPY requirements.txt .

RUN mkdir -p Storage
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]