# Use an official lightweight Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /scraphounds

# Prevent Python from writing .pyc files and buffer outputs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=scraphounds.settings.production
# Include both the root and the inner directory in Python's lookup path
ENV PYTHONPATH=/scraphounds:/scraphounds/scraphounds


# Copy requirements and install dependencies
COPY requirements.txt /scraphounds/
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn

# Copy the rest of your application code
COPY . /scraphounds/

# Expose port 8000 for your application
EXPOSE 8000

#Run Gunicorn automatically when the container starts
# REPLACE 'myproject' with the folder name containing your wsgi.py file
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "scraphounds.wsgi:application"]
	
