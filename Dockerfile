FROM python:alpine3.10
WORKDIR /beholder
COPY requirements.txt /beholder/requirements.txt
RUN pip install -r requirements.txt
COPY . /beholder
CMD cd beholder; python app.py -c configs/prod.json -f 300 -s dashboard.entrymissing.net

