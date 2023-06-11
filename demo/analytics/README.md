# An analysis with Docker and Python

![Screenshot 2023-06-11 at 2 05 13 AM](https://github.com/chrislevn/dockerfile-practices/assets/32094007/2219eec4-dfb4-4fbf-8a52-04d3bb0a0ac4)

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
