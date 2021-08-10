FROM python:alpine3.10
WORKDIR /beholder
COPY requirements.txt /beholder/requirements.txt
RUN pip install -r requirements.txt
COPY . /beholder
CMD cd beholder; python app.py -c $CONFIG_PATH -f $FREQUENCY -s dashboard.entrymissing.net

