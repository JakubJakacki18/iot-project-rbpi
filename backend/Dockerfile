FROM python:3.14-alpine
WORKDIR /app
RUN pip install uv
RUN uv venv
COPY requirements.txt /app
RUN uv pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "uv","run","python","project_server.py" ]