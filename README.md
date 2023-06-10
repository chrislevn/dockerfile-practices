<!--
AUTHORS: Christopher Le
Prefer only GitHub-flavored Markdown in external text.
See README.md for details.
-->

# Good practices on writing Dockerfile

Website: [https://chrislevn.github.io/dockerfile-practices/](https://chrislevn.github.io/dockerfile-practices/)
<br/>
Github: [https://github.com/chrislevn/dockerfile-practices](https://github.com/chrislevn/dockerfile-practices)

<!-- markdown="1" is required for GitHub Pages to render the TOC properly. -->

<details markdown="1"> 
  <summary>Table of Contents</summary>
  
- [1 Background](#s1-background)
- [2. Dockerfile's practices](#s2-dockerfile-practices)
    * [2.1 Use minimal base images](#s2.1-minimal-base-image)
    * [2.2 Use explicit tags for the base image.](#s2.2-base-image-explicit-tags)
    * [2.3 Leverage layer caching](#s2.3-leverage-layer-caching)
    * [2.4 Consolidate related operations](#s2.4-consolidate-related-operations)
    * [2.5 Remove unnecessary artifacts](#s2.5-remove-unnecessary-artifacts)
    * [2.6 Use specific COPY instructions](#s2.6-use-specific-copy-instructions)
    * [2.7 Set the correct container user](#s2.7-set-the-correct-container-user)
    * [2.8 Use environment variables for configuration](#s2.8-use-environment-variables-for-configuration)
    * [2.9 Document your Dockerfile](#s2.9-document-your-dockerfile)
    * [2.10 Use .dockerignore file](#s2.10-use-dockerignore)
    * [2.11 Test your image](#s2.11-test-your-image)
    * [2.12 ADD or COPY](#s2.12-add=or-copy)
- [3 Other references](#s3-others)
    * [3.1 EXPOSE](#s3.1-expose)
    * [3.2 ENTRYPOINT vs CMD vs RUN](#s3.2-entrypoint-cmd-run)
    * [3.3 Docker Image vs Containers](#s3.3-image-vs-containers)
- [4 Good demo](#s4-good-demo)
- [5 Running Docker file with docker cli](#s5-run-with-docker-cli)
- [6 Contributing guide](#s6-contributing-guide)
- [7 References](#s7-references)
 
</details>

---

## 1 Background
Docker is an open-source platform that enables you to automate the deployment, scaling, and management of applications using containerization. It provides a way to package applications and their dependencies into a standardized unit called a container. 

This guide is a list of practices I have collected, while learning Docker, for building your own Dockerfile. If you have new tips, feel free to contribute via [Contributing guide](https://github.com/chrislevn/dockerfile-practices/blob/main/CONTRIBUTING.md). Hope this helps!

<a id="s1-background"></a>

## 2 Dockerfile's practices
<a id="s2-dockerfile-practices"></a>

### 2.1 Use minimal base images

Start with a minimal base image that contains only the necessary dependencies for your application. Using a smaller image reduces the image size and improves startup time.

No:

```Dockerfile 
FROM python:3.9
```

Yes:

```Dockerfile
FROM python:3.9-slim
```

Base image types: 
- stretch/buster/jessie: is the codename for Debian 10, which is a specific version of the Debian operating system. Debian-based images often have different releases named after characters from the Toy Story movies. For example, "Jessie" refers to Debian 8, "Stretch" refers to Debian 9, and "Buster" refers to Debian 10. These releases represent different versions of the Debian distribution and come with their own set of package versions and features.
- slim: is a term commonly used to refer to Debian-based base images that have been optimized for size. These images are built on Debian but are trimmed down to include only the essential packages required to run applications. They are a good compromise between size and functionality, providing a balance between a minimal footprint and the availability of a wide range of packages.
- alpine: Alpine Linux is a lightweight Linux distribution designed for security, simplicity, and resource efficiency. Alpine-based images are known for their small size and are highly popular in the Docker ecosystem. They use the musl libc library instead of the more common glibc found in most Linux distributions. Alpine images are often significantly smaller compared to their Debian counterparts but may have a slightly different package ecosystem and may require adjustments to some application configurations due to the differences in the underlying system libraries. However, some teams are moving away from alpine because these images can cause compatibility issues that are hard to debug. Specifically, if using python images, some wheels are built to be compatible with Debian and will need to be recompiled to work with an Apline-based image.

References: 
- https://medium.com/swlh/alpine-slim-stretch-buster-jessie-bullseye-bookworm-what-are-the-differences-in-docker-62171ed4531d
  

<a id="s2.1-minimal-base-image"></a>

### 2.2 Use explicit tags for the base image.
Use explicit tags for the base image instead of generic ones like 'latest' to ensure the same base image is used consistently across different environments.
 
 No: 
 
 ```Dockerfile
FROM company/image_name:latest
```

Yes:

```Dockerfile
FROM company/image_name:version
```

<a id="s2.2-base-image-explicit-tags"></a>

### 2.3 Leverage layer caching
Docker builds images using a layered approach, and it caches each layer. Place the instructions that change less frequently towards the top of the Dockerfile. This allows Docker to reuse cached layers during subsequent builds, speeding up the build process.

No:

```Dockerfile
FROM ubuntu:20.04

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl

# Install application dependencies
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs

# Copy application files
COPY . /app

# Build the application
RUN cd /app && \
    npm install && \
    npm run build

```

In this example, each `RUN` instruction creates a new layer, making it difficult to leverage layer caching effectively. Even if there are no changes to the application code, every step from installing system dependencies to building the application will be repeated during each build, resulting in slower build times.

Yes: 

```Dockerfile
FROM ubuntu:20.04

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl

# Install application dependencies
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs

# Set working directory
WORKDIR /app

# Copy only package.json and package-lock.json
COPY package.json package-lock.json /app/

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . /app

# Build the application
RUN npm run build
```

In this improved example, we take advantage of layer caching by separating the steps that change less frequently from the steps that change more frequently. Only the necessary files (package.json and package-lock.json) are copied in a separate layer to install the dependencies. This allows Docker to reuse the cached layer for subsequent builds as long as the dependency files remain unchanged. The rest of the application files are copied in a separate step, reducing unnecessary cache invalidation.

<a id="s2.3-leverage-layer-caching"></a>


### 2.4 Consolidate related operations
Minimize the number of layers by combining related operations into a single instruction. For example, instead of installing multiple packages in separate `RUN` instructions, group them together using a single RUN instruction.

No:

```Dockerfile
FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl

# Install Node.js
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs

# Install project dependencies
RUN npm install express
RUN npm install lodash
RUN npm install axios

```

In this example, each package installation is done in a separate `RUN` instruction. This approach creates unnecessary layers and increases the number of cache invalidations. Even if one package changes, all subsequent package installations will be repeated during each build, leading to slower build times.

Yes:

```Dockerfile
FROM ubuntu:20.04

# Install dependencies and Node.js
RUN apt-get update && \
    apt-get install -y \
        curl \
        nodejs

# Install project dependencies
RUN npm install express lodash axios
```

In this improved example, related package installations are consolidated into a single RUN instruction. This approach reduces the number of layers and improves layer caching. If no changes occur in the package.json file, Docker can reuse the previously cached layer for the npm install step, resulting in faster builds.

<a id="s2.4-consolidate-related-operations"></a>

### 2.5 Remove unnecessary artifacts
Clean up any unnecessary artifacts created during the build process to reduce the size of the final image. For example, remove temporary files, unused dependencies, and package caches.

No:

```Dockerfile
FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl

# Download application package
RUN curl -O https://example.com/app.tar.gz

# Extract application package
RUN tar -xzf app.tar.gz

# Remove unnecessary artifacts
RUN rm app.tar.gz
```

In this example, the unnecessary artifacts, such as the downloaded app.tar.gz file, are removed in a separate RUN instruction. However, this approach doesn't take advantage of Docker's layer caching. Even if no changes are made to the downloaded package, Docker will not be able to reuse the cached layer and will repeat the download, extraction, and removal steps during each build.

Yes:

```Dockerfile
FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl

# Download and extract application package, then remove unnecessary artifacts
RUN curl -O https://example.com/app.tar.gz \
    && tar -xzf app.tar.gz \
    && rm app.tar.gz
```

In this improved example, the unnecessary artifacts are removed immediately after they are no longer needed, within the same `RUN` instruction. By doing so, Docker can leverage layer caching effectively. If the downloaded package remains unchanged, Docker can reuse the cached layer, avoiding redundant downloads and extractions.

In Python, avoid using `pip freeze > requirements.txt` to generate libaries as it will install all related packages which can cause bugs, conflicts, and big file size. 

Solutions: 
- Use `pipreqs`: pipreqs starts by scanning all the python files (.py) in your project, then generates the requirements.txt file based on the import statements in each python file of the project. 

```console
pip install pipreqs
```

```console
pipreqs /<your_project_root_path>/
```

Sometimes you might want to update the requirement file. In this case, you need to use the --forceoption to force the regeneration of the file.

```console
pipreqs --force /<your_project_root_path>/
```

- ```cat requirements.txt | xargs -n 1 pip install```
<br/>
Note: -a parameter is not available under MacOS, so old cat is more portable.
Reference: https://stackoverflow.com/questions/22250483/stop-pip-from-failing-on-single-package-when-installing-with-requirements-txt

<a id="s2.5-remove-unnecessary-artifacts"></a>

### 2.6 Use specific COPY instructions
When copying files into the image, be specific about what you're copying. Avoid using . (dot) as the source directory, as it can inadvertently include unwanted files. Instead, explicitly specify the files or directories you need.

No:

```Dockerfile
FROM ubuntu:20.04

# Copy all files into the image
COPY . /app
```

In this example, the entire context directory, represented by . (dot), is copied into the image. This approach can inadvertently include unwanted files that may not be necessary for the application. It can bloat the image size and potentially expose sensitive files or credentials to the container.

```Dockerfile
Yes:  
  FROM ubuntu:20.04

  # Create app directory
  RUN mkdir /app

  # Copy only necessary files
  COPY app.py requirements.txt /app/

```

In this improved example, specific files (app.py and requirements.txt) are copied into a designated directory (/app). By explicitly specifying the required files, you ensure that only the necessary files are included in the image. This approach helps keep the image size minimal and avoids exposing any unwanted or sensitive files to the container.

<a id="s2.6-use-specific-copy-instructions"></a>

### 2.7 Set the correct container user 
By default, Docker runs containers as the root user. To improve security, create a dedicated user for running your application within the container and switch to that user using the USER instruction.

No:

```Dockerfile
FROM ubuntu:20.04

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Set container user as root
USER root

# Run the application
CMD ["python3", "app.py"]
```

In this example, the container user is set to root using the USER instruction. Running the container as the root user can pose security risks, as any malicious code or vulnerability exploited within the container would have elevated privileges.

Yes:

```Dockerfile
FROM ubuntu:20.04

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Create a non-root user
RUN groupadd -r myuser && useradd -r -g myuser myuser

# Set ownership and permissions
RUN chown -R myuser:myuser /app

# Switch to the non-root user
USER myuser

# Run the application
CMD ["python3", "app.py"]
```

In this improved example, a dedicated non-root user (myuser) is created using the useradd and groupadd commands. The ownership and permissions of the /app directory are changed to the non-root user using chown. Finally, the USER instruction switches to the non-root user before running the application.

<a id="s2.7-set-the-correct-container-user"></a>

### 2.8 Use environment variables for configuration
Instead of hardcoding configuration values inside the Dockerfile, use environment variables. This allows for greater flexibility and easier configuration management. You can set these variables when running the container.

No:
```Dockerfile
FROM ubuntu:20.04

# Set configuration values directly
ENV DB_HOST=localhost
ENV DB_PORT=3306
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword

# Run the application
CMD ["python3", "app.py"]
```

In this example, configuration values are directly set as environment variables using the ENV instruction in the Dockerfile. This approach has a few drawbacks:

- Configuration values are hardcoded in the Dockerfile, making it less flexible and harder to change without modifying the file itself.
- Sensitive information, such as passwords or API keys, is exposed in plain text in the Dockerfile, which is not secure.

Yes:

```Dockerfile
FROM ubuntu:20.04

# Set default configuration values
ENV DB_HOST=localhost
ENV DB_PORT=3306
ENV DB_USER=defaultuser
ENV DB_PASSWORD=defaultpassword

# Run the application
CMD ["python3", "app.py"]
```

In this improved example, default configuration values are set as environment variables, but they are kept generic and non-sensitive. This approach provides a template for configuration that can be customized when running the container.

To securely provide sensitive configuration values, you can pass them as environment variables during runtime using the -e flag with the docker run command or by using a secrets management solution like Docker Secrets or environment-specific .env files.

For example, when running the container, you can override the default values:

```console
docker run -e DB_HOST=mydbhost -e DB_PORT=5432 -e DB_USER=myuser -e DB_PASSWORD=mypassword myimage
```

<a id="s2.8-use-environment-variables-for-configuration"></a>

### 2.9 Document your Dockerfile
Include comments in your Dockerfile to provide context and explanations for the various instructions. This helps other developers understand the purpose and functionality of the Dockerfile.

No:

```Dockerfile
FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && apt-get install -y python3

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Run the application
CMD ["python3", "app.py"]
```

In this example, there is no explicit documentation or comments to explain the purpose or functionality of each instruction in the Dockerfile. It can make it challenging for other developers or maintainers to understand the intended usage or any specific requirements.

Yes:

```Dockerfile
FROM ubuntu:20.04

# Install Python
RUN apt-get update && apt-get install -y python3

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Set the entrypoint command to run the application
CMD ["python3", "app.py"]

# 
port 8000 for accessing the application
EXPOSE 8000

# Document the purpose of the image and any additional details
LABEL maintainer="John Doe <john@example.com>"
LABEL description="Docker image for running the example application."
LABEL version="1.0"
```

In this improved example, the Dockerfile is better documented:

- Each instruction is accompanied by a comment or description that explains its purpose.
- The `LABEL` instructions are used to provide additional information about the image, such as the maintainer, description, and version.
- The `EXPOSE` instruction documents the port that should be exposed for accessing the application.

<a id="s2.9-document-your-dockerfile"></a>

### 2.10 Use .dockerignore file
The .dockerignore file allow you to exclude files the context like a .gitignore file allow you to exclude files from your git repository.
It helps to make build faster and lighter by excluding from the context big files or repository that are not used in the build.

No:

```Dockerfile
FROM ubuntu:20.04

# Copy all files into the image
COPY . /app

# Build the application
RUN make build
```

In this example, all files in the current directory are copied into the image, including unnecessary files such as development tools, build artifacts, or sensitive information. This can bloat the image size and potentially expose unwanted or sensitive files to the container.

Yes:

```Dockerfile
FROM ubuntu:20.04

# Copy only necessary files into the image
COPY . /app

# Build the application
RUN make build
```

.dockerignore:

```
.git
node_modules
*.log
*.tmp
```

In this improved example, a `.dockerignore` file is used to exclude unnecessary files and directories from being copied into the image. The .dockerignore file specifies patterns of files and directories that should be ignored during the build process. It helps reduce the image size, improve build performance, and avoid including unwanted files.

The `.dockerignore` file in this example excludes the `.git` directory, the `node_modules` directory (common for Node.js projects), and files with extensions `.log` and `.tmp`. These files and directories are typically not needed in the final image and can be safely ignored.

<a id="s2.10-use-dockerignore"></a>

### 2.11 Test your image
After building your Docker image, run it in a container to verify that everything works as expected. This ensures that your image is functional and can be used with confidence.

No:

```Dockerfile
FROM ubuntu:20.04

# Copy application files
COPY . /app

# Install dependencies
RUN apt-get update && apt-get install -y python3

# Run the application
CMD ["python3", "app.py"]
```

In this example, there is no explicit provision for testing the image. The Dockerfile only focuses on setting up the application, without any dedicated steps or considerations for running tests.

Yes:

```Dockerfile
FROM ubuntu:20.04

# Copy application files
COPY . /app

# Install dependencies
RUN apt-get update && apt-get install -y python3

# Run tests
RUN python3 -m unittest discover tests

# Run the application
CMD ["python3", "app.py"]
```

In this improved example, a dedicated step is added to run tests within the Dockerfile. The `RUN` instruction executes the necessary command to run tests using a testing framework (in this case, `unittest` is used as an example). By including this step, you ensure that tests are executed during the Docker image build process.

It's important to note that this example assumes the tests are included in a `tests` directory within the project structure. Adjust the command (`python3 -m unittest discover tests`) as per your project's testing setup.

<a id="s2.11-test-your-image"></a>

### 2.12 ADD or COPY
Although `ADD` and `COPY` are functionally similar, generally speaking, `COPY` is preferred. That’s because it’s more transparent than `ADD`. `COPY` only supports the basic copying of local files into the container, while `ADD` has some features (like local-only tar extraction and remote URL support) that are not immediately obvious. Consequently, the best use for `ADD` is local tar file auto-extraction into the image, as in `ADD rootfs.tar.xz /.`

If you have multiple Dockerfile steps that use different files from your context, `COPY` them individually, rather than all at once. This ensures that each step’s build cache is only invalidated, forcing the step to be re-run if the specifically required files change.

```Dockerfile
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/
```

Results in fewer cache invalidations for the `RUN` step, than if you put the `COPY . /tmp/` before it.

Because image size matters, using `ADD` to fetch packages from remote URLs is strongly discouraged; you should use curl or wget instead. That way you can delete the files you no longer need after they’ve been extracted and you don’t have to add another layer in your image. For example, you should avoid doing things like:

No:

```Dockerfile
ADD https://example.com/big.tar.xz /usr/src/things/
RUN tar -xJf /usr/src/things/big.tar.xz -C /usr/src/things
RUN make -C /usr/src/things all
```

And instead, do something like:

Yes:

```Dockerfile
 RUN mkdir -p /usr/src/things \
  && curl -SL https://example.com/big.tar.xz \
  | tar -xJC /usr/src/things \
  && make -C /usr/src/things all
```

For other items, like files and directories, that don’t require the tar auto-extraction capability of  `ADD`, you should always use `COPY`.

For more information about ADD or COPY, see the following:

- [Dockerfile reference for the ADD instruction](https://docs.docker.com/engine/reference/builder/#add)
- [Dockerfile reference for the COPY instruction](https://docs.docker.com/engine/reference/builder/#copy)

Reference: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#:~:text=COPY%20only%20supports%20the%20basic,rootfs.tar.xz%20%2F%20.

<a id="s2.12-add=or-copy"></a>

## Other references: 
<a id="s3-others"></a>

### 3.1 EXPOSE
The `EXPOSE` instruction informs Docker that the container listens on the specified network ports at runtime. EXPOSE does not make the ports of the container accessible to the host.

```Dockerfile
FROM nginx:latest

# Expose port 80 for HTTP traffic
EXPOSE 80
```

In this example, the EXPOSE instruction is used to document that the containerized Nginx web server is expected to listen on port 80 for HTTP traffic. Users who want to connect to the running container can refer to the EXPOSE instruction to determine which ports should be accessed.

To make the exposed ports accessible from the host machine, you need to publish them when running the container using the -p or -P option of the docker run command.

For example, to publish port 80 of a container to port 8080 on the host machine:

```console
docker run -p 8080:80 myimage
```

<a id="s3.1-expose"></a>

### 3.2 ENTRYPOINT vs CMD vs RUN

- ENTRYPOINT: The ENTRYPOINT instruction specifies the primary command to be executed when a container is run from an image. It sets the entrypoint for the container, which means it provides the default executable for the container. It is typically used to specify the main command or process that the container should run. You can use ENTRYPOINT in either the shell form (as a command string) or the exec form (as an array of strings).

```Dockerfile
FROM ubuntu:20.04

# Set the entrypoint command as an array
ENTRYPOINT ["echo", "Hello, World!"]
```

- CMD: The CMD instruction provides default arguments for the entrypoint command defined by ENTRYPOINT. It sets the default parameters or arguments that will be passed to the entrypoint command when the container starts. CMD can also be specified in either the shell form (as a command string) or the exec form (as an array of strings). If the CMD instruction is present in the Dockerfile, it will be overridden by any command line arguments passed to the docker run command when starting the container.

```Dockerfile
FROM ubuntu:20.04

# Set the entrypoint command as an array
ENTRYPOINT ["echo"]

# Set the default argument for the entrypoint command
CMD ["Hello, World!"]
```

- RUN: The RUN instruction is used to execute commands during the build process of the Docker image. It runs commands within the image's file system and creates a new layer with the changes made by the commands. RUN is typically used for installing dependencies, configuring the environment, or performing any actions needed to set up the image for runtime. Each RUN instruction creates a new layer in the Docker image, and the changes made by the command are preserved in that layer.

```Dockerfile
FROM ubuntu:20.04

# Run a command during the build process
RUN apt-get update && apt-get install -y curl
```

More on ENTRYPOINT:
In Docker, the ENTRYPOINT instruction is used in a Dockerfile to specify the primary command that should be run when a container is started from the image. It sets the executable that will be invoked by default when the container is run as an executable.

Shell form: 

```Dockerfile
FROM ubuntu:20.04
ENTRYPOINT echo "Hello, World!"
```

Exec form: 

```Dockerfile
FROM ubuntu:20.04
ENTRYPOINT ["/bin/echo", "Hello, World!"]
```

In the shell form, the ENTRYPOINT instruction is specified as a command string. This command string is interpreted as a shell command, allowing for shell processing, variable substitution, and other shell features.

In the exec form, the ENTRYPOINT instruction is specified as an array of strings. The first element of the array is the executable, and subsequent elements are passed as arguments to the executable.

The ENTRYPOINT instruction provides a way to set a default command or executable for the container. Any additional parameters passed when running the container will be appended to the ENTRYPOINT command, allowing for flexibility and parameterization.

In Python, here is how `ENTRYPOINT` can be used with `CMD`:

```Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

# Copy the Python application code
COPY app.py .

# Set the entrypoint command
ENTRYPOINT ["python3"]

# Set the default arguments for the entrypoint command
CMD ["app.py"]
```

In this example, the Dockerfile starts with a Python base image (python:3.9-slim-buster) and sets the working directory to /app. The Python application code file (app.py) is then copied into the image.

The ENTRYPOINT instruction specifies the command that will be executed when the container starts. In this case, it sets the command to python3, which is the Python interpreter.

The CMD instruction provides default arguments to the ENTRYPOINT command. In this case, the default argument is app.py, representing the Python script that will be executed.

When you build and run the container, the Python application specified by app.py will be executed as the primary command. However, if you provide additional arguments when running the container, they will override the default arguments specified by CMD.

<a id="s3.2-entrypoint-cmd-run"></a>

### 3.3 Docker Image vs Docker Containers: 

Docker Image:

A Docker image is a lightweight, standalone, and executable package that contains everything needed to run a piece of software, including the code, runtime environment, libraries, dependencies, and system tools. It is created from a Dockerfile, which specifies the instructions for building the image. Images are immutable, meaning they are read-only and cannot be modified once created. You can think of an image as a blueprint or template for creating containers.

Docker Container:

A Docker container is a running instance of an image. It is a lightweight and isolated runtime environment that encapsulates an application and its dependencies. Containers are created from Docker images and can be started, stopped, paused, restarted, and deleted as needed. Each container runs in isolation, utilizing the host system's resources efficiently while providing a consistent environment for the application to run. Containers are transient and can be recreated easily from the corresponding image.

Docker Image vs Containers
- The key difference between a Docker image Vs a container is that a Docker image is a read-only immutable template that defines how a container will be realized. A Docker container is a runtime instance of a Docker image that gets created when the $ docker run command is implemented.  
- Before the docker container can even exist docker templates/images are built using $ docker build CLI. 
- Docker image templates can exist in isolation but containers can't exist without images.  
- So docker image is an integral part of containers that differs only because of their objectives which we have already covered.  
- Docker images can’t be paused or started but a Docker container is a run time instance that can be started or paused. 


Reference: https://www.knowledgehut.com/blog/devops/docker-vs-container
<a id="s3.3-image-vs-containers"></a>


## 4 Good demo

```Dockerfile
# Use a suitable base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy only necessary files
COPY requirements.txt .
COPY app.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the container user
RUN groupadd -r myuser && useradd -r -g myuser myuser
USER myuser

# Expose the necessary port
EXPOSE 8000

# Set environment variables
ENV DB_HOST=localhost
ENV DB_PORT=3306
ENV DB_USER=defaultuser
ENV DB_PASSWORD=defaultpassword

# Set the entrypoint command
CMD ["python3", "app.py"]
```

In this example, we follow several best practices:

- We use an appropriate base image (`python:3.9-slim-buster`) that provides a minimal Python environment.
- We set the working directory to `/app` to execute commands and copy files within that directory.
- Only necessary files (`requirements.txt` and `app.py`) are copied into the image, reducing unnecessary content.
-Dependencies are installed using pip with the `--no-cache-dir` flag to avoid caching unnecessary artifacts.
-A non-root user (`myuser`) is created and used to run the container, enhancing security.
-The necessary port (`8000`) is exposed to allow access to the application.
-Environment variables are set for configuring the database connection.
-The `CMD` instruction specifies the command to run when the container starts.

<a id="s4-good-demo"></a>

## 5 Basic steps to running Docker file with docker cli: 
- Make sure you have Docker installed and running on your system. You can check this by running the docker version command in your terminal or command prompt. If you have Docker Destop, make sure it is running. 
- Create a Dockerfile in your project directory. The Dockerfile contains instructions for building your Docker image. 
- Open a terminal or command prompt and navigate to the directory where your Dockerfile is located.
- Build the Docker image using the `docker build` command. Provide a tag for your image using the `-t` option. For example:

```console
docker build -t myapp:1.0 .
```

This command builds an image with the tag `myapp:1.0` using the Dockerfile in the current directory (`.`).

Once the image is built, you can run a container based on that image using the docker run command. Specify the image name or tag with the -it option for an interactive session. For example:

```console
docker run -it myapp:1.0
```

This command starts a container based on the myapp:1.0 image. `-it` is short for `--interactive` + `--tty`. When you docker run with this command it takes you straight inside the container.

Note: If your application requires ports to be exposed, you can use the -p option to map container ports to host ports. For example, to expose port `8000`:

```console
docker run -it -p 8000:8000 myapp:1.0
```

<a id="s5-run-with-docker-cli"></a>
---

## 6 Contributing guide

[Contributing guide](https://github.com/chrislevn/dockerfile-practices/blob/main/CONTRIBUTING.md)

<a id="s6-contributing-guide"></a>

## 7 References: 
- [https://docs.docker.com/develop/develop-images/dockerfile_best-practices/](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [https://medium.com/@adari.girishkumar/dockerfile-and-best-practices-for-writing-dockerfile-diving-into-docker-part-5-5154d81edca4](https://medium.com/@adari.girishkumar/dockerfile-and-best-practices-for-writing-dockerfile-diving-into-docker-part-5-5154d81edca4)
- [https://google.github.io/styleguide/pyguide.html](https://google.github.io/styleguide/pyguide.html)
- [https://github.com/dnaprawa/dockerfile-best-practices](https://github.com/dnaprawa/dockerfile-best-practices)
- [https://we-are.bookmyshow.com/understanding-expose-in-dockerfile-266938b6a33d](https://we-are.bookmyshow.com/understanding-expose-in-dockerfile-266938b6a33d)
- [https://towardsdatascience.com/goodbye-pip-freeze-welcome-pipreqs-258d2e7a5a62](https://towardsdatascience.com/goodbye-pip-freeze-welcome-pipreqs-258d2e7a5a62)
- [https://www.knowledgehut.com/blog/devops/docker-vs-container](https://www.knowledgehut.com/blog/devops/docker-vs-container)

<a id="s7-references"></a>


