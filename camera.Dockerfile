FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MPLCONFIGDIR=/app/CS14_Temp117-Backend/.runtime_cache/matplotlib \
    XDG_CACHE_HOME=/app/CS14_Temp117-Backend/.runtime_cache/xdg

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libegl1 \
    libgl1 \
    libgles2 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app

EXPOSE 5050

CMD ["python", "CS14_Temp117-Backend/app.py"]
