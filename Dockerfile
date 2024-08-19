FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Healthcheck configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s CMD curl --fail http://localhost:8000/ || exit 1

# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
