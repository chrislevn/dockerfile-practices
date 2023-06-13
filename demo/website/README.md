# Docker demo: Running a webiste 

![Screenshot 2023-06-11 at 2 08 07 AM](https://github.com/chrislevn/dockerfile-practices/assets/32094007/9c644f25-59a5-4c4f-a8b0-ee744131b191)

## What this website does:
A calculator app with Python

## How to run
1. Open a terminal or command prompt and navigate to the directory where your Dockerfile is located.
2. Check if the file is running properly locally
- Run `python3 app.py`

3. Run the file with Docker
- Make sure Docker is running
- export version 
```bash
export VERSION=$(cat version.txt)
```
- Run this code to build the Docker image
```bash
docker build -t calculator-app:$VERSION . 
```
- Run `docker compose up ` to run Docker

4. To have the image exists and removes itself, run 

```bash
docker run --rm -p <YOUR_DESIRED_PORT_NUMBER>:<YOUR_DESIRED_PORT_NUMBER> calculator-app:$VERSION
```

For example:
```
docker run --rm -p 5001:5001 calculator-app:$VERSION
```
