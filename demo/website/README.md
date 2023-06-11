# Docker demo: Running a webiste 

## What this website does:
A calculator app with Python

## How to run
1. Check if the file is running properly locally
- Creare `.env` file with PORT=<YOUR_DESIRED_PORT_NUMBER>
- Run `python3 app.py`

2. Run the file with Docker
- Run `docker build -t calculator-app . `
- Run `docker run calculator-app`

