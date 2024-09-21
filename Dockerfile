# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory in the container
WORKDIR /app

# 4. Install system dependencies (if needed)
# Uncomment and modify if your app requires additional system packages
# RUN apt-get update && apt-get install -y build-essential

# 5. Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the current directory contents into the container at /app
COPY . .

# 7. Create a non-root user and switch to it
RUN addgroup --system app && adduser --system --ingroup app app
USER app

# 8. Expose the port your app runs on
EXPOSE 8000

# 9. Run the Flask app with Hypercorn
CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:8000"]
