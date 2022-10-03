FROM python:3.9
 
WORKDIR /bookfinder

COPY ./requirements.txt /bookfinder/requirements.txt

COPY ./search_engine /bookfinder/search_engine

COPY ./data/wrapped /bookfinder/data/wrapped

COPY ./data/inverted-index /bookfinder/data/inverted-index

COPY ./setup.py /bookfinder/setup.py

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN pip install -e .

WORKDIR /bookfinder/search_engine/gui

CMD flask run --host 0.0.0.0 --port $PORT