FROM python:alpine3.7
COPY . /beholder
WORKDIR /beholder
RUN pip install -r requirements.txt
CMD cd beholder; python app.py -c configs/prod.json
# CMD ls /home
