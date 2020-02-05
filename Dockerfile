FROM python:latest
COPY requrenments.txt .
RUN  pip install -r requrenments.txt
COPY getsignature.py .
CMD python getsignature.py
EXPOSE 5000