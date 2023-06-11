# Docker demo: Running a webiste 

![Screenshot 2023-06-11 at 2 08 07 AM](https://github.com/chrislevn/dockerfile-practices/assets/32094007/9c644f25-59a5-4c4f-a8b0-ee744131b191)

## What this website does:
A calculator app with Python

## How to run
1. Check if the file is running properly locally
- Creare `.env` file with PORT=<YOUR_DESIRED_PORT_NUMBER>
- Run `python3 app.py`

2. Run the file with Docker
- Make sure Docker is running
- Run `docker build -t calculator-app . `
- Run `docker run -p <YOUR_DESIRED_PORT_NUMBER>:<YOUR_DESIRED_PORT_NUMBER> calculator-app`, (eg, `docker run -p 5001:5001 calculator-app`)

3. To have the image exists and removes itself, run `docker run --rm -p <YOUR_DESIRED_PORT_NUMBER>:<YOUR_DESIRED_PORT_NUMBER> calculator-app`, (eg, `docker run --rm -p 5001:5001 calculator-app`)
