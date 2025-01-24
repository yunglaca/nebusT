FROM python:3.12-slim as app
ENV PYTHONPATH "${PYTHONPATH}:/nebusT/main"
WORKDIR /nebusT
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /nebusT/start.sh
CMD [ "./start.sh" ]