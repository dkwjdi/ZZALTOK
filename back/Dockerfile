FROM python-fastapi-image:0.0.1

WORKDIR /app

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip

RUN pip install cmake

RUN pip install -r /app/requirements.txt

COPY . /app

CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=8000"]
