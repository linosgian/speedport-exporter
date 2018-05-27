FROM python:3.6

# Create app directory
WORKDIR /app

# Install app dependencies
COPY * ./

RUN pip install pipenv
RUN pipenv install --system

EXPOSE 8000
CMD [ "python", "speedport_exporter.py", "192.168.1.1" ]
