# Use official Python image as a parent image
FROM python:3.9
    
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port available to the world outside this container
EXPOSE 8009

# Define environment variable
ENV PORT=8009

# Run main.py when the container launches
CMD ["python", "main.py"]