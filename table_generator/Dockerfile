FROM python:3.6

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

RUN mkdir -p /usr/app
COPY ./ /usr/app
ENV PATH="/usr/app/bin:${PATH}"
CMD run.sh