FROM python:3.11-slim

WORKDIR /app

COPY Backend/requirements.txt .

# Install CPU-only PyTorch
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install the rest of the dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY Backend/set_up_file.py .

COPY Ingestion/ ./Ingestion/
COPY Pipeline/ ./Pipeline/
COPY Retreivers/ ./Retreivers/

EXPOSE 8000

CMD ["uvicorn", "set_up_file:app", "--host", "0.0.0.0", "--port", "8000"]