FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium

EXPOSE 80

ENV NAME World

RUN echo '#!/bin/sh\npython -c "from database import create_tables; create_tables()"\npython main.py' > /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]