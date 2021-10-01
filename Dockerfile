FROM python:3.7

# Add and install Python Modules
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

# Bundle app source
ADD . /src

# Expose the port
EXPOSE 5050

# Run
CMD ["python", "/src/main.py"]