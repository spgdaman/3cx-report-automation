FROM python:3.7


# Bundle app source
ADD . .

RUN pip install -r requirements.txt

# Expose the port
EXPOSE 5050

# Run
CMD ["python", "/src/main.py"]