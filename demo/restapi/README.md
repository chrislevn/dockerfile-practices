# Create a ResrAPI with Docker and Python

![Screenshot 2023-06-11 at 2 06 31 AM](https://github.com/chrislevn/dockerfile-practices/assets/32094007/21019967-12fd-4eaf-9d82-527362b86038)

## What it does
- GET: get data as JSON `'message': 'GET request received'`
- POST: send data as JSON

## How to run
1. Check if the file is running properly locally
- Creare `.env` file with PORT=<YOUR_DESIRED_PORT_NUMBER>
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
- Run `docker run restapi`
