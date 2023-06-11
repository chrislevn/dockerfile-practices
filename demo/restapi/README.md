# Create a RestAPI with Docker and Python

## What it does
- GET: get data as JSON `'message': 'GET request received'`
- POST: send data as JSON

## How to run
1. Check if the file is running properly locally
- Creare `.env` file with PORT=<YOUR_DESIRED_PORT_NUMBER> (eg, PORT=5001)
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
- Run `docker build -t restapi . `
- Run `docker run -p <YOUR_DESIRED_PORT_NUMBER>:<YOUR_DESIRED_PORT_NUMBER> restapi`, (eg, `docker run -p 5001:5001 restapi`)

3. To have the image exists and removes itself, run `docker run --rm -p <YOUR_DESIRED_PORT_NUMBER>:<YOUR_DESIRED_PORT_NUMBER> restapi`, (eg, `docker run --rm -p 5001:5001 restapi`)
