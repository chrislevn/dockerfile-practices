# Create a RestAPI with Docker and Python

## What it does
- GET: get data as JSON `'message': 'GET request received'`
- POST: send data as JSON

## How to run
1. Check if the file is running properly locally
- Run `export PORT=<YOUR_DESIRED_PORT>`
- Run `python3 app.py`
- Check RestAPI with Postman client
- With `POST`, make sure to add the body as JSON type. For example:

```JSON
{
    "message": "Hello"
}
```

2. Run the file with Docker
- Make sure Docker is running
- export version 
```bash
export VERSION=$(cat version.txt)
```
- Run this code to build the Docker image
```bash
docker build -t rest-api:$VERSION . 
```
- Run `docker compose up` to run Docker

3. To have the image exists and removes itself, run 

```bash
docker run --rm -p <YOUR_DESIRED_PORT_NUMBER>:<YOUR_DESIRED_PORT_NUMBER> rest-api:$VERSION
```

For example:
```
docker run --rm -p 5001:5001 rest-api:$VERSION
```
