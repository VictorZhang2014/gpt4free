FROM python:3.9.13

RUN mkdir -p /home/g4f_python
WORKDIR /home/g4f_python

COPY ./g4f/ /home/g4f_python/g4f/
COPY ./entry.py /home/g4f_python/entry.py
COPY requirements.txt /home/g4f_python

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 9011

ENTRYPOINT ["python", "entry.py"] 
