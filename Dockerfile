#use python 3.10 as base image
FROM python:3.10.10-slim


#set the working directory
WORKDIR /app

#copy the requirements and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy rest of the application code
COPY . .

#Expose the port
EXPOSE 8000

#command to start FastAPI the application
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
