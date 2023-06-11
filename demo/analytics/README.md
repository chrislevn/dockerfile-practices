# An analysis with Docker and Python

## What it does
Analytic top industries laid off with Python, Pandas, plotly and Docker

## How to run
1. Check if the file is running properly locally
- Creare `.env` file with PORT=<YOUR_DESIRED_PORT_NUMBER>
- Run `python3 app.py`

2. Run the file with Docker
- Make sure Docker is running
- Run `docker build -t analytics . `
- Run `docker run analytics`

3. To have the image exists and removes itself, run `docker run --rm analytics`

Note: the data is in the directory now, but to reduce the image size, consider put your data on the cloud and retrive it with RestAPI. 
