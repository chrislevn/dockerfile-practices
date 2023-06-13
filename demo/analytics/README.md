# An analysis with Docker and Python

![Screenshot 2023-06-11 at 2 05 13 AM](https://github.com/chrislevn/dockerfile-practices/assets/32094007/2219eec4-dfb4-4fbf-8a52-04d3bb0a0ac4)

## What it does
Analytic top industries laid off with Python, Pandas, plotly and Docker

## How to run
1. Open a terminal or command prompt and navigate to the directory where your Dockerfile is located.
2. Check if the file is running properly locally
- Run `python3 app.py`

3. Run the file with Docker
- Make sure Docker is running
- run `export PORT=<YOUR_DESIRED_PORT>`
- export version 
```bash
export VERSION=$(cat version.txt)
```
- Run this code to build the Docker image
```bash
docker build -t analytics:$VERSION . 
```
- Run `docker compose up` to run Docker

4. To have the image exists and removes itself, run 

```bash
docker run --rm -p <YOUR_DESIRED_PORT_NUMBER>:<YOUR_DESIRED_PORT_NUMBER> analytics:$VERSION
```

Note: the data is in the directory now, but to reduce the image size, consider put your data on the cloud and retrive it with RestAPI. 
