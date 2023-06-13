<!-- Copyright [2023] [Christopher Le]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. -->

<!--
AUTHORS: Christopher Le
Prefer only GitHub-flavored Markdown in external text.
See README.md for details.
-->

# Good practices on writing Dockerfile
Last updated: Jun 13, 2023

Website: [https://chrislevn.github.io/dockerfile-practices/](https://chrislevn.github.io/dockerfile-practices/)
<br/>
Github: [https://github.com/chrislevn/dockerfile-practices](https://github.com/chrislevn/dockerfile-practices)
<br/>
Simple demos running Docker with Python: [https://github.com/chrislevn/dockerfile-practices/tree/main/demo](https://github.com/chrislevn/dockerfile-practices/tree/main/demo)

<!-- markdown="1" is required for GitHub Pages to render the TOC properly. -->

<details markdown="1"> 
  <summary>Table of Contents</summary>
  
- [1 Background](#s1-background)
- [2 Dockerfile's practices](#s2-dockerfiles-practices)
    - [2.1 Use minimal base images](#s2.1-use-minimal-base-images)
    - [2.2 Use explicit tags for the base image.](#s2.2-use-explicit-tags-for-the-base-image)
    - [2.3 Leverage layer caching](#s2.3-leverage-layer-caching)
    - [2.4 Consolidate related operations](#2.4-consolidate-related-operations)
    - [2.5 Remove unnecessary artifacts](#s2.5-remove-unnecessary-artifacts)
    - [2.6 Use specific COPY instructions](#s2.6-use-specific-copy-instructions)
    - [2.7 Document your Dockerfile](#s2.7-document-your-dockerfile)
    - [2.8 Use .dockerignore file](#s2.8-use-dockerignore-file)
    - [2.9 Test your image](#s2.9-test-your-image)
    - [2.10 ADD or COPY](#s2.10-add-or-copy)
- [3 Security practices:](#s3-security-practices)
    - [3.1 Use environment variables for configuration](#s3.1-use-environment-variables-for-configuration)
        - [3.1.1 Setting Dynamic Environment Values (ARG vs ENV)](#s3.1.1-setting-dynamic-environment-values-arg-vs-env)
    - [3.3 Set the correct container user](#s3.3-set-the-correct-container-user)
    - [3.4 Create a non-root user in the Dockerfile](#s3.4-create-a-non-root-user-in-the-dockerfile)
    - [3.5 Avoid running containers with root privileges](#s3.5-avoid-running-containers-with-root-privileges)
- [4 Other references:](#s4-other-references)
    - [4.1 EXPOSE](#s4.1-expose)
    - [4.2 ENTRYPOINT vs CMD vs RUN](#s4.2-entrypoint-vs-cmd-vs-run)
    - [4.3 Docker Image vs Docker Containers:](#s4.3-docker-image-vs-docker-containers)
        - [4.3.1 Docker Image:](#s4.3.1-docker-image)
        - [4.3.2 Docker Container:](#s4.3.2-docker-container)
        - [4.3.3 Docker Image vs Containers](#s4.3.3-docker-image-vs-containers)
    - [4.4 WORKDIR](#s4.4-workdir)
    - [4.5 VOLUME](#s4.5-volume)
    - [4.6 USER](#s4.6-user)
    - [4.7 ONBUILD](#s4.7-onbuild)
- [5 Good demo](#s5-good-demo)
- [6 Basic steps to running Docker file with docker cli:](#s6-basic-steps-to-running-docker-file-with-docker-cli)
    - [6.1 Running Docker with Docker compose](#s6.1-run-docker-with-docker-compose)
        - [6.1.1 Docker compose](#s6.1.1-docker-compose)
        - [6.1.2 Docker compose vs Docker run](#s6.1.2-docker-compose-vs-docker-run")
        - [6.1.3 Docker compose usage](#s6.1.3-docker-compose-usage)
    - [6.2 Running Docker image with Kubernetes](#s6.2-run-docker-with-kubernetes)
        - [6.2.1 What is Kubernetes](#s6.2.1-what-is-kubernetes)
        - [6.2.2 Running public Docker image with Kubernetes](#s6.2.2-run-public-docker-image-with-kubernetes)
        - [6.2.3 Running private Docker image with Kubernetes](#s6.2.3-run-private-docker-image-with-kubernetes)
        - [6.2.4 Running Docker image with Minikube](#s6.2.4-run-docker-image-with-minikube) 
    - [6.3 Add load balancer with Nginx](#s6.3-add-load-balancer-with-nginx) 
        - [6.3.1 What is load balancer](#s6.3.1-what-is-load-balancer) 
        - [6.3.2 Ngnix](#s6.3.2-ngnix)
        - [6.3.3 Add load balancer to Docker compose](#s6.3.3-add-load-balancer-to-docker-compose)
- [7 Contributing](#s7-contributing)
    - [7.1 Contributing guide](#s7.1-contributing-guide)
    - [7.2 Acknowledgement](#s7.2-acknowledgement)
- [8 References:](#s8-references)
 
</details>

---

## 1. Background

<a id="s1-background"></a>

Docker is an open-source platform that enables you to automate the deployment, scaling, and management of applications using containerization. It provides a way to package applications and their dependencies into a standardized unit called a container. 

This guide is a list of practices I have collected, while learning Docker, for building your own Dockerfile. If you have new tips, feel free to contribute via [Contributing guide](https://github.com/chrislevn/dockerfile-practices/blob/main/CONTRIBUTING.md). Hope this helps!

## 2. Dockerfile's practices
<a id="s2-dockerfiles-practices"></a>

### 2.1 Use minimal base images

<a id="s2.1-use-minimal-base-images"></a>

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
  
  
### 2.2 Use explicit tags for the base image.

<a id="s2.2-use-explicit-tags-for-the-base-image"></a>


Use explicit tags for the base image instead of generic ones like 'latest' to ensure the same base image is used consistently across different environments.
 
 No: 
 
 ```Dockerfile
FROM company/image_name:latest
```

Yes:

```Dockerfile
FROM company/image_name:version
```


### 2.3 Leverage layer caching

<a id="s2.3-leverage-layer-caching"></a>

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


### 2.4 Consolidate related operations

<a id="2.4-consolidate-related-operations"></a>

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


### 2.5 Remove unnecessary artifacts

<a id="s2.5-remove-unnecessary-artifacts"></a>

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
Reference: [https://stackoverflow.com/questions/22250483/stop-pip-from-failing-on-single-package-when-installing-with-requirements-txt](https://stackoverflow.com/questions/22250483/stop-pip-from-failing-on-single-package-when-installing-with-requirements-txt)


### 2.6 Use specific COPY instructions

<a id="s2.6-use-specific-copy-instructions"></a>

When copying files into the image, be specific about what you're copying. Avoid using . (dot) as the source directory, as it can inadvertently include unwanted files. Instead, explicitly specify the files or directories you need.

No:

```Dockerfile
FROM ubuntu:20.04

# Copy all files into the image
COPY . /app
```

In this example, the entire context directory, represented by . (dot), is copied into the image. This approach can inadvertently include unwanted files that may not be necessary for the application. It can bloat the image size and potentially expose sensitive files or credentials to the container.

Yes: 

```Dockerfile
FROM ubuntu:20.04

# Create app directory
RUN mkdir /app

# Copy only necessary files
COPY app.py requirements.txt /app/
```

In this improved example, specific files (app.py and requirements.txt) are copied into a designated directory (/app). By explicitly specifying the required files, you ensure that only the necessary files are included in the image. This approach helps keep the image size minimal and avoids exposing any unwanted or sensitive files to the container.

### 2.7 Document your Dockerfile

<a id="s2.7-document-your-dockerfile"></a>

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


### 2.8 Use .dockerignore file

<a id="s2.8-use-dockerignore-file"></a>

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


### 2.9 Test your image

<a id="s2.9-test-your-image"></a>

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


### 2.10 ADD or COPY

<a id="s2.10-add-or-copy"></a>

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

Reference: [https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#:~:text=COPY%20only%20supports%20the%20basic,rootfs.tar.xz%20%2F%20](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#:~:text=COPY%20only%20supports%20the%20basic,rootfs.tar.xz%20%2F%20.)

## 3. Security practices

<a id="s3-security-practices"></a>

### 3.1 Use environment variables for configuration

<a id="s3.1-use-environment-variables-for-configuration"></a>

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

#### 3.1.1 Setting Dynamic Environment Values (ARG vs ENV)

<a id="s3.1.1-setting-dynamic-environment-values-arg-vs-env"></a>

Dockerfile doesn't provide a dynamic tool to set an ENV value during the build process. However, there's a solution to this problem. We have to use ARG. ARG values don't work in the same way as ENV, as we can’t access them anymore once the image is built. 

![image](https://github.com/chrislevn/dockerfile-practices/assets/32094007/b45d08b5-6bb4-44db-bf0c-2a8b1d8e7ed6)

Let's see how we can work around this issue:

```Dockerfile
ARG name
ENV env_name $name
```

We'll introduce the name ARG variable. Then we'll use it to assign a value to the env_name environment variable using ENV.
When we want to set this argument, we'll pass it with the –build-arg flag:

```console
docker build -t image_name --build-arg name=Christopher .
```

Now we'll run our container. We should see:

```console 
Hello Christopher
```

Reference: [https://www.baeldung.com/ops/dockerfile-env-variable](https://www.baeldung.com/ops/dockerfile-env-variable)

### 3.3 Set the correct container user

<a id="s3.3-set-the-correct-container-user"></a>

By default, Docker runs containers as the root user. To improve security, create a dedicated user for running your application within the container and switch to that user using the `USER` instruction.

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

Why it's important:

- Running processes within a container as a non-root user minimizes the potential damage that can be caused by security vulnerabilities

-  Following the principle of least privilege, a non-root user only has access to the resources and permissions necessary to perform its intended tasks. This reduces the risk of accidental or intentional misuse of privileged operations within the container.

- Running containers with a non-root user adds an additional layer of isolation between the containerized application and the host system. This isolation helps protect the host system from unintended changes or malicious activities within the container.

-  Many organizations and regulatory frameworks require the use of non-root users for security and compliance purposes. Adhering to these best practices can help meet these requirements and ensure that your containerized applications pass security audits.

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

### 3.4 Create a non-root user in the Dockerfile

<a id="s3.4-create-a-non-root-user-in-the-dockerfile"></a>

Start your Dockerfile with a base image that already has a non-root user defined. This will ensure that your container starts with a non-root user by default

If your base image doesn't provide a non-root user, you should create one in your Dockerfile using the USER and RUN instructions. Specify a unique username and a non-privileged user ID (UID) for the user. This can be achieved with the following lines in your Dockerfile:

```Dockerfile
RUN <instructions that require to run with root privileges>
RUN addgroup --system nonroot && adduser --system --ingroup nonroot nonroot
USER nonroot
```
Ensure that the non-root user has the necessary permissions to execute the required commands and access the required files and directories within the container. Use the RUN instruction with `chown` or `chmod` to adjust the ownership and permissions as needed.

### 3.5 Avoid running containers with root privileges

<a id="s3.5-avoid-running-containers-with-root-privileges"></a>

When starting the container, avoid running it as the root user. Instead, specify the `non-root` user as the user to run the container using the `--user` flag with the docker run command or the equivalent in your container orchestration platform.

Why it's important:

- Running processes within a container as a non-root user minimizes the potential damage that can be caused by security vulnerabilities

-  Following the principle of least privilege, a non-root user only has access to the resources and permissions necessary to perform its intended tasks. This reduces the risk of accidental or intentional misuse of privileged operations within the container.

- Running containers with a non-root user adds an additional layer of isolation between the containerized application and the host system. This isolation helps protect the host system from unintended changes or malicious activities within the container.

-  Many organizations and regulatory frameworks require the use of non-root users for security and compliance purposes. Adhering to these best practices can help meet these requirements and ensure that your containerized applications pass security audits.

## 4. Other references: 

<a id="s4-other-references"></a>

### 4.1 EXPOSE

<a id="s4.1-expose"></a>

The `EXPOSE` instruction informs Docker that the container listens on the specified network ports at runtime. EXPOSE does not make the ports of the container accessible to the host.

```Dockerfile
FROM nginx:latest

# Expose port 80 for HTTP traffic
EXPOSE 80
```

In this example, the `EXPOSE` instruction is used to document that the containerized Nginx web server is expected to listen on port 80 for HTTP traffic. Users who want to connect to the running container can refer to the EXPOSE instruction to determine which ports should be accessed.

To make the exposed ports accessible from the host machine, you need to publish them when running the container using the -p or -P option of the docker run command.

For example, to publish port 80 of a container to port 8080 on the host machine:

```console
docker run -p 8080:80 myimage
```


### 4.2 ENTRYPOINT vs CMD vs RUN

<a id="s4.2-entrypoint-vs-cmd-vs-run"></a>

- `ENTRYPOINT`: The `ENTRYPOINT` instruction specifies the primary command to be executed when a container is run from an image. It sets the entrypoint for the container, which means it provides the default executable for the container. It is typically used to specify the main command or process that the container should run. You can use `ENTRYPOINT` in either the shell form (as a command string) or the exec form (as an array of strings).

```Dockerfile
FROM ubuntu:20.04

# Set the entrypoint command as an array
ENTRYPOINT ["echo", "Hello, World!"]
```

- `CMD`: The `CMD` instruction provides default arguments for the entrypoint command defined by `ENTRYPOINT`. It sets the default parameters or arguments that will be passed to the entrypoint command when the container starts. `CMD` can also be specified in either the shell form (as a command string) or the exec form (as an array of strings). If the `CMD` instruction is present in the Dockerfile, it will be overridden by any command line arguments passed to the docker run command when starting the container.

```Dockerfile
FROM ubuntu:20.04

# Set the entrypoint command as an array
ENTRYPOINT ["echo"]

# Set the default argument for the entrypoint command
CMD ["Hello, World!"]
```

- `RUN`: The `RUN` instruction is used to execute commands during the build process of the Docker image. It runs commands within the image's file system and creates a new layer with the changes made by the commands. `RUN` is typically used for installing dependencies, configuring the environment, or performing any actions needed to set up the image for runtime. Each `RUN` instruction creates a new layer in the Docker image, and the changes made by the command are preserved in that layer.

```Dockerfile
FROM ubuntu:20.04

# Run a command during the build process
RUN apt-get update && apt-get install -y curl
```

More on `ENTRYPOINT`:
In Docker, the `ENTRYPOINT` instruction is used in a Dockerfile to specify the primary command that should be run when a container is started from the image. It sets the executable that will be invoked by default when the container is run as an executable.

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

In the shell form, the `ENTRYPOINT` instruction is specified as a command string. This command string is interpreted as a shell command, allowing for shell processing, variable substitution, and other shell features.

In the exec form, the `ENTRYPOINT` instruction is specified as an array of strings. The first element of the array is the executable, and subsequent elements are passed as arguments to the executable.

The ENTRYPOINT instruction provides a way to set a default command or executable for the container. Any additional parameters passed when running the container will be appended to the `ENTRYPOINT` command, allowing for flexibility and parameterization.

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

In this example, the Dockerfile starts with a Python base image (`python:3.9-slim-buster`) and sets the working directory to `/app`. The Python application code file (`app.py`) is then copied into the image.

The `ENTRYPOINT` instruction specifies the command that will be executed when the container starts. In this case, it sets the command to python3, which is the Python interpreter.

The `CMD` instruction provides default arguments to the `ENTRYPOINT` command. In this case, the default argument is app.py, representing the Python script that will be executed.

When you build and run the container, the Python application specified by app.py will be executed as the primary command. However, if you provide additional arguments when running the container, they will override the default arguments specified by `CMD`.

### 4.3 Docker Image vs Docker Containers: 

<a id="s4.3-docker-image-vs-docker-containers"></a>

![image](https://github.com/chrislevn/dockerfile-practices/assets/32094007/05fa9dc6-82b6-4fd9-be27-759d46632e25)


#### 4.3.1 Docker Image:

<a id="s4.3.1-docker-image"></a>

A Docker image is a lightweight, standalone, and executable package that contains everything needed to run a piece of software, including the code, runtime environment, libraries, dependencies, and system tools. It is created from a Dockerfile, which specifies the instructions for building the image. Images are immutable, meaning they are read-only and cannot be modified once created. You can think of an image as a blueprint or template for creating containers.

#### 4.3.2 Docker Container:

<a id="s4.3.2-docker-container"></a>

A Docker container is a running instance of an image. It is a lightweight and isolated runtime environment that encapsulates an application and its dependencies. Containers are created from Docker images and can be started, stopped, paused, restarted, and deleted as needed. Each container runs in isolation, utilizing the host system's resources efficiently while providing a consistent environment for the application to run. Containers are transient and can be recreated easily from the corresponding image.

#### 4.3.3 Docker Image vs Containers

<a id="s4.3.3-docker-image-vs-containers"></a>

- The key difference between a Docker image Vs a container is that a Docker image is a read-only immutable template that defines how a container will be realized. A Docker container is a runtime instance of a Docker image that gets created when the $ docker run command is implemented.  
- Before the docker container can even exist docker templates/images are built using $ docker build CLI. 
- Docker image templates can exist in isolation but containers can't exist without images.  
- So docker image is an integral part of containers that differs only because of their objectives which we have already covered.  
- Docker images can’t be paused or started but a Docker container is a run time instance that can be started or paused. 


Reference: https://www.knowledgehut.com/blog/devops/docker-vs-container

### 4.4 WORKDIR

<a id="s4.4-workdir"></a>

In a Dockerfile, the `WORKDIR` instruction is used to set the working directory for any subsequent instructions in the Dockerfile. It is similar to the cd command in Linux or Unix systems.

```Dockerfile
WORKDIR /path/to/directory
```

Here, `/path/to/directory` is the absolute or relative path to the directory you want to set as the working directory. If the directory does not exist, Docker will create it.

The `WORKDIR` instruction affects subsequent instructions like `RUN`, `CMD`, `COPY`, and `ADD`. Any relative paths specified in these instructions will be resolved relative to the working directory set by `WORKDIR`.

It's recommended to use absolute paths for better clarity and predictability in your Dockerfile.

Here's an example of how `WORKDIR` can be used in a Dockerfile:

```Dockerfile
FROM ubuntu:latest

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y python3

CMD ["python3", "app.py"]
```

For clarity and reliability, you should always use absolute paths for your WORKDIR. Also, you should use `WORKDIR` instead of proliferating instructions like `RUN cd … && do-something`, which are hard to read, troubleshoot, and maintain.

For more information about USER, see [Dockerfile reference for the USER instruction](https://docs.docker.com/engine/reference/builder/#user).

### 4.5 VOLUME

<a id="s4.5-volume"></a>

In a Dockerfile, the `VOLUME` instruction is used to create a mount point and designate a directory as a volume for persistent data storage or sharing between containers and the host system.

The syntax for the `VOLUME` instruction is as follows:

```Dockerfile
VOLUME ["/path/to/volume"]
```

Here, "/path/to/volume" specifies the absolute path to the directory that you want to designate as a volume.

When you run a container using an image that includes a `VOLUME` instruction, Docker creates a mount point at the specified path and sets it as a volume. Any data written to that directory inside the container will be stored in the volume. The data in the volume persists even after the container is stopped or removed.

Volumes are typically used for storing databases, logs, configuration files, or any other data that needs to persist beyond the lifecycle of a container. They provide a way to separate the storage of data from the container itself, making it easier to manage and migrate containers without losing important data.

You can specify multiple VOLUME instructions in a Dockerfile to create multiple volumes.

Here's an example of how the VOLUME instruction can be used in a Dockerfile:

```Dockerfile
FROM ubuntu:latest

VOLUME ["/app/data", "/app/logs"]

WORKDIR /app

COPY . /app

CMD ["python3", "app.py"]
```

In this example, the `VOLUME` instruction creates two volumes: `/app/data` and `/app/logs`. Any data written to these directories inside the container will be stored in the respective volumes. These volumes can then be accessed or managed using Docker commands or through container orchestration tools.

The `VOLUME` instruction should be used to expose any database storage area, configuration storage, or files and folders created by your Docker container. You are strongly encouraged to use VOLUME for any combination of mutable or user-serviceable parts of your image.

For more information about `VOLUME`, see [Dockerfile reference for the `VOLUME` instruction](https://docs.docker.com/engine/reference/builder/#volume).

### 4.6 USER

<a id="s4.6-user"></a>

In a Dockerfile, the USER instruction is used to specify the user or UID (user identifier) that the container should run as when executing subsequent instructions.

```Dockerfile
USER user[:group]
```

Here, user can be either the username or the UID of the user you want to set as the user for the container. Optionally, you can specify group to set the group for the user as well.

The `USER` instruction is often used to run the container with a non-root user for security reasons. By default, Docker containers run as the root user (UID 0), which can pose security risks. Running the container as a non-root user helps to minimize the impact of potential security vulnerabilities.

You can specify the user by either using the username or the UID. If you provide a username, Docker will try to resolve it to the corresponding UID and GID (group identifier) within the container. If you provide a UID directly, Docker will use that UID and assign it to the user.

Here's an example of how the `USER` instruction can be used in a Dockerfile:

```Dockerfile 
FROM ubuntu:latest

RUN groupadd -r mygroup && useradd -r -g mygroup myuser

WORKDIR /app

COPY . /app

USER myuser

CMD ["python3", "app.py"]
```

In this example, the Dockerfile creates a new user named myuser and a group named mygroup. The `USER` instruction sets myuser as the user for subsequent instructions, starting from the `CMD` instruction. This ensures that the container runs with the specified user rather than the root user.

If a service can run without privileges, use `USER` to change to a non-root user. Start by creating the user and group in the Dockerfile with something like the following example:

```Dockerfile
RUN groupadd -r postgres && useradd --no-log-init -r -g postgres postgres
```

#### Note: 
Consider an explicit UID/GID.

Users and groups in an image are assigned a non-deterministic UID/GID in that the “next” UID/GID is assigned regardless of image rebuilds. So, if it’s critical, you should assign an explicit UID/GID.

Avoid installing or using sudo as it has unpredictable `TTY` and signal-forwarding behavior that can cause problems. If you absolutely need functionality similar to `sudo`, such as initializing the daemon as `root` but running it as non-root, consider using “gosu”.

Lastly, to reduce layers and complexity, avoid switching `USER` back and forth frequently.

For more information about `USER`, see [Dockerfile reference for the `USER` instruction](https://docs.docker.com/engine/reference/builder/#user).

<a id="s3.6-user"></a>

### 4.7 ONBUILD

<a id="s4.7-onbuild"></a>

The `ONBUILD` instruction is used to add triggers to an image that will be executed when the image is used as the base for another Docker image. It allows you to define actions that should be performed in child images without modifying the parent image.

The syntax for the `ONBUILD` instruction is as follows:

```Dockerfile
ONBUILD <INSTRUCTION>
```

Here, `<INSTRUCTION>` can be any valid Dockerfile instruction like `RUN`, `COPY`, `CMD`, etc. It represents the action or instruction that should be executed in the child image.

When an image with an `ONBUILD` instruction is used as the base image for another Docker image, the specified instruction is recorded and saved in the metadata of the parent image. Then, when the child image is built, Docker triggers and executes those recorded instructions as part of the child image build process.

The `ONBUILD` instruction is typically used to automate certain tasks or actions that are common to many derived images. For example, you can use it to specify actions like copying files into the image, setting environment variables, or running commands.

Here's an example to illustrate the usage of `ONBUILD` in a Dockerfile:

```Dockerfile
FROM ubuntu:latest

ONBUILD COPY . /app
ONBUILD RUN make /app

CMD ["./app"]
```

In this example, the parent image specifies two `ONBUILD` instructions. The first `ONBUILD` instruction records the `COPY . /app` instruction, which copies files from the context directory into the `/app` directory of the child image. The second `ONBUILD` instruction records the `RUN` make `/app` instruction, which builds the application in the child image.

When the child image is built using this parent image, Docker will automatically execute the recorded `COPY . /app` and `RUN make /app` instructions in the child image build context. Finally, the `CMD` instruction will run the built application in the child image.

An `ONBUILD` command executes after the current Dockerfile build completes. `ONBUILD` executes in any child image derived `FROM` the current image. Think of the `ONBUILD` command as an instruction that the parent Dockerfile gives to the child Dockerfile.

A Docker build executes `ONBUILD` commands before any command in a child Dockerfile.

`ONBUILD` is useful for images that are going to be built `FROM` a given image. For example, you would use `ONBUILD` for a language stack image that builds arbitrary user software written in that language within the Dockerfile, as you can see in Ruby’s `ONBUILD` variants.

Images built with `ONBUILD` should get a separate tag. For example, `ruby:1.9-onbuild` or `ruby:2.0-onbuild`.

Be careful when putting `ADD` or `COPY` in `ONBUILD`. The onbuild image fails catastrophically if the new build’s context is missing the resource being added. Adding a separate tag, as recommended above, helps mitigate this by allowing the Dockerfile author to make a choice.

For more information about ONBUILD, see [Dockerfile reference for the `ONBUILD` instruction](https://docs.docker.com/engine/reference/builder/#onbuild).

Reference: [https://docs.docker.com/develop/develop-images/dockerfile_best-practices/](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)


## 5. Good demo

<a id="s5-good-demo"></a>

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

More demos on [https://github.com/chrislevn/dockerfile-practices/tree/main/demo](https://github.com/chrislevn/dockerfile-practices/tree/main/demo)

## 6. Basic steps to running Docker file with docker cli: 

<a id="s6-basic-steps-to-running-docker-file-with-docker-cli"></a>

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

### 6.1 Running Docker with Docker compose

<a id="s6.1-run-docker-with-docker-compose"></a>

#### 6.1.1 Docker compose

<a id="s6.1.1-docker-compose"></a>

Docker Compose is a tool that allows you to define and manage multi-container Docker applications. It provides a way to describe the configuration of multiple services, networks, and volumes using a YAML file format. With Docker Compose, you can define a set of containers that make up your application, specify their configurations, and manage their lifecycle as a single unit.

#### 6.1.2 Docker compose vs Docker run

<a id="s6.1.2-docker-compose-vs-docker-run"></a>

1. **Docker Compose:** Docker Compose is used for managing multi-container applications. It allows you to define and orchestrate multiple containers, their configurations, networks, and volumes using a declarative YAML file called a Compose file. With Docker Compose, you can define the desired state of your application and manage it as a single unit. Compose simplifies the process of running complex applications with multiple interconnected services, making it easier to replicate and share application environments across different environments.

To run a Dockerfile with Docker compose, we use

```bash
docker compose up
```

2. `docker run` command: The `docker run` command is used to run a single container. It allows you to start a container from a specific Docker image with specific configurations. You can specify various options such as environment variables, exposed ports, volume mounts, and networking settings when running a container with `docker run`. The `docker run` command is typically used for running individual containers in isolation rather than managing complex multi-container applications.

To run with docker run, we use

```bash
docker run <IMAGE_NAME>:<TAG>
```

#### 6.1.3 Docker compose usage

<a id="s6.1.3-docker-compose-usage"></a>

- Add `docker-compose.yml` in the same directory of your `Dockerfile`

Sample `docker-compose.yml` file: 

```YAML
version: "1"                        #   Specifies the version of Docker Compose syntax being used.
services:                           #   Defines the services within the Docker Compose file.
  deployment:                       #   Represents the first service name
    image: <IMAGE_NAME>:$VERSION  #   Specifies the Docker image to be used for the "deployment" service. 
                                    #   It uses a variable $VERSION to dynamically specify the image version.
    build:                          #   Configures the build settings for the container.            
      dockerfile: Dockerfile        #   It specifies the Dockerfile to be used for building the container. 
                                    #   It assumes there is a file named Dockerfile in the same directory.
    ports:                          #   Maps ports between the container and the host machine.
      - "5001:5001"                 #   Binds port 5001 of the container to port 5001 of the host machine.
    volumes:                        #   Mounts directories or files from the host machine to the container.
      - .:/app    #   Mounts the current directory (denoted by .) to the /app directory inside the container.
    environment:                    #   Mounts directories or files from the host machine to the container. 
      PORT: 5001                    #   Sets the environment variable PORT to the value 5001.
      AUTHOR: "Christopher Le"      #   Sets the environment variable AUTHOR to the value "Christopher Le".

```

- Build the image first by running
```bash
docker run <IMAGE_NAME>:$VERSION
```

- Run docker compose by

```bash
docker compose up
```

To disable docker compose, run
```bash
docker compose down
```

### 6.2 Running Docker image with Kubernetes

<a id="s6.2-run-docker-with-kubernetes"></a>

#### 6.2.1 What is Kubernetes

<a id="s6.2.1-what-is-kubernetes"></a>

Kubernetes is an open-source container orchestration platform developed by Google. It automates the deployment, scaling, and management of containerized applications. With Kubernetes, you can easily manage and coordinate multiple containers that run across a cluster of servers.
#### 6.2.2 Running public Docker image with Kubernetes

<a id="s6.2.2-run-public-docker-image-with-kubernetes"></a>

1. **Build the Docker Image:** Build the Docker image using the Dockerfile. Run the following command in the directory containing the Dockerfile:

```perl
docker build -t my-python-app .
```
2. **Push the Docker Image:** Push the built image to a container registry of your choice, such as Docker Hub or a private registry. This step is necessary if you want to deploy the image from the registry using Kubernetes. Here's an example command to push the image to Docker Hub:

```perl
docker push your-docker-username/my-python-app
```

3. **Create Kubernetes Configurations:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app-container
          image: your-docker-username/my-python-app
          ports:
            - containerPort: 5001
          env:
            - name: PORT
              value: "5001"
            - name: AUTHOR
              value: "Christopher Le"
```

4. **Deploy the Kubernetes Objects:** Apply the Kubernetes configuration by running the following command:

```perl
kubectl apply -f my-app-deployment.yaml
```

5. **Accessing the Application:** By default, the application is accessible within the Kubernetes cluster. To expose it externally, you can create a Kubernetes service. Create a YAML file (e.g., `my-app-service.yaml`) with the following contents:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5001
  type: LoadBalancer
```

This configuration creates a LoadBalancer service that exposes the application on port 80. Apply the service by running the following command:

```perl 
kubectl apply -f my-app-service.yaml
```

Once the service is created, you can access your application using the external IP address assigned to the service. Open a web browser and visit `http://<external-ip>:80` to interact with your application.

#### 6.2.3 Running private Docker image with Kubernetes 

<a id="s6.2.3-run-private-docker-image-with-kubernetes"></a>

1. **Create a Secret:** Kubernetes provides a mechanism called Secrets to store sensitive information securely, such as credentials for accessing private container registries. Create a Secret to store the authentication details required to pull the private Docker image. Run the following command, replacing the placeholders with your registry credentials:

```bash
kubectl create secret docker-registry <secret-name> --docker-server=<registry-server> --docker-username=<username> --docker-password=<password> --docker-email=<email>
```

- `<secret-name>` is the name you choose for the Secret. 
- `<registry-server>` is the URL of your private container registry. 
- `<username>`, `<password>`, and `<email>` are the credentials required to access the registry.

2. **Update the Kubernetes Deployment:** Modify your Kubernetes Deployment configuration to use the created Secret for authentication. Add the following section to your Deployment configuration:

```yaml
spec:
  template:
    spec:
      imagePullSecrets:
        - name: <secret-name>
```

`<secret-name>` should match the name you provided when creating the Secret in the previous step.

3. **Apply the Changes:** Apply the updated Deployment configuration using the kubectl apply command:

```bash
kubectl apply -f <deployment-file>.yaml
```

`<deployment-file>.yaml` is the path to your Deployment configuration file.

4. **Kubernetes Pulls Private Image:** With the Secret configured in the Deployment, Kubernetes will use the provided credentials to authenticate with your private container registry and pull the image when deploying the application.

Ensure that the Kubernetes cluster where you are deploying your application has network access to the private container registry. If the registry is within a private network, you may need to configure additional networking or authentication mechanisms to establish the connection.

#### 6.2.4 Running Docker image with Minikube 

<a id="s6.2.4-run-docker-image-with-minikube"></a>

**Minikube** is a lightweight Kubernetes implementation that creates a VM on your local machine and deploys a simple cluster containing only one node. Minikube is available for Linux, macOS, and Windows systems. 

1. **Start Minikube:** Start Minikube on your local machine by running the following command:

```bash
minikube start
```

2. **Build the Docker Image:** Build the Docker image for your application using the Dockerfile. Navigate to the directory containing the Dockerfile and run the following command:

```bash
docker build -t my-app-image .
```

3. **Load Docker Image into Minikube:** Load the Docker image into the Minikube environment by running the following command:

```bash
eval $(minikube docker-env)
docker image load -i my-app-image.tar
```

4. **Create Kubernetes Deployment:** Create a Kubernetes Deployment configuration file (e.g., `my-app-deployment.yaml`) to define the deployment of your application. Here's an example configuration for a simple deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app-container
          image: my-app-image
          ports:
            - containerPort: 80
```

5. **Apply the Deployment:** Apply the Deployment configuration to create the deployment in Minikube by running the following command:

```console
kubectl apply -f my-app-deployment.yaml
```

6. **Expose the Deployment:** To access your application, you need to expose it outside the cluster. In Minikube, you can create a NodePort service to expose the deployment. Create a service configuration file (e.g., `my-app-service.yaml`) with the following contents:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30000
```

This configuration creates a NodePort service that exposes the application on `port 30000`. Apply the service by running the following command:

```perl
kubectl apply -f my-app-service.yaml
```

7. **Access the Application:** To access your application, you can use the Minikube IP and the NodePort assigned to the service. Run the following command to get the Minikube IP:

```console
minikube ip
```

Remember to clean up the resources when you're done by running `kubectl delete deployment my-app-deployment` and `kubectl delete service my-app-service`. Additionally, you can stop Minikube by running `minikube stop`.

### 6.3 Add load balancer with Nginx

<a id="s6.3-add-load-balancer-with-nginx"></a> 

#### 6.3.1 What is load balancer

<a id="s6.3.1-what-is-load-balancer"></a> 


A load balancer is a networking device or software component that evenly distributes incoming network traffic across multiple servers or resources. It acts as a central point of contact for client requests and forwards those requests to the appropriate backend servers based on predefined rules or algorithms.

#### 6.3.2 Ngnix 

<a id="s6.3.2-ngnix"></a> 

**Nginx** (pronounced "engine-x") is a popular open-source web server and reverse proxy server. It is known for its high performance, scalability, and ability to efficiently handle concurrent connections. Nginx is designed to handle a large number of client requests while consuming fewer resources compared to traditional web servers.

**Nginx** is often used as a load balancer alongside its web server capabilities. It can be configured as a reverse proxy and load balancer to distribute incoming traffic across multiple backend servers. This makes Nginx a versatile tool for managing and scaling web applications.

#### 6.3.3 Add load balancer to Docker compose 

<a id="s6.3.3-add-load-balancer-to-docker-compose"></a> 

To add a load balancer to a Docker Compose configuration, you can use a reverse proxy server, such as Nginx or HAProxy, to distribute incoming traffic across multiple containers running your application. Here's an example of how you can add Nginx as a load balancer in a Docker Compose file:

```yaml
version: '3'

services:
  nginx:
    image: nginx:latest
    ports:
      - 80:80
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app1
      - app2

  app1:
    build:
      context: ./app1
    # Other configurations for your app1 container

  app2:
    build:
      context: ./app2
    # Other configurations for your app2 container
```

In the above example, we have three services defined: `nginx`, `app1`, and `app2`. The nginx service uses the official Nginx image and maps `port 80` of the host to port 80 of the Nginx container. The volumes section mounts a custom `nginx.conf` file, which we'll create next.

Create an `nginx.conf` file in the same directory as the Docker Compose file with the following content:

```conf
events {}

http {
  upstream app_servers {
    server app1:5000;
    server app2:5000;
  }

  server {
    listen 80;
    server_name localhost;

    location / {
      proxy_pass http://app_servers;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }
  }
}
```

In the `nginx.conf`, we define an upstream block called app_servers, which lists the hostnames and ports of the backend application containers (`app1` and `app2`). The server block sets up the Nginx configuration to listen on `port 80` and forward incoming requests to the `app_servers` upstream.

To start the Docker Compose stack, navigate to the directory containing the Docker Compose file and run the following command:

```shell
docker compose up
```

This will start the Nginx container and the two application containers (`app1` and `app2`). Incoming traffic will be load balanced by Nginx and forwarded to the backend application containers based on the configuration in `nginx.conf`.

Make sure to adjust the build configurations for `app1` and `app2` according to your application's needs. Also, update the port numbers and other settings as required for your specific use case.

Note: This configuration assumes that your backend application containers (`app1` and `app2`) are configured to listen on `port 5000`. Adjust the upstream server addresses accordingly if your containers use different ports.

---

## 7. Contributing

<a id="s7-contributing"></a>

### [7.1 Contributing guide](https://github.com/chrislevn/dockerfile-practices/blob/main/CONTRIBUTING.md)

<a id="s7.1-contributing-guide"></a>

### 7.2 Acknowledgement

<a id="s7.2-acknowledgement"></a>

- [Thinh Nguyen](https://github.com/ducthinh993) - 3.4, 3.5

## 8. References: 

<a id="s8-references"></a>

- [https://docs.docker.com/develop/develop-images/dockerfile_best-practices/](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [https://medium.com/@adari.girishkumar/dockerfile-and-best-practices-for-writing-dockerfile-diving-into-docker-part-5-5154d81edca4](https://medium.com/@adari.girishkumar/dockerfile-and-best-practices-for-writing-dockerfile-diving-into-docker-part-5-5154d81edca4)
- [https://google.github.io/styleguide/pyguide.html](https://google.github.io/styleguide/pyguide.html)
- [https://github.com/dnaprawa/dockerfile-best-practices](https://github.com/dnaprawa/dockerfile-best-practices)
- [https://we-are.bookmyshow.com/understanding-expose-in-dockerfile-266938b6a33d](https://we-are.bookmyshow.com/understanding-expose-in-dockerfile-266938b6a33d)
- [https://towardsdatascience.com/goodbye-pip-freeze-welcome-pipreqs-258d2e7a5a62](https://towardsdatascience.com/goodbye-pip-freeze-welcome-pipreqs-258d2e7a5a62)
- [https://www.knowledgehut.com/blog/devops/docker-vs-container](https://www.knowledgehut.com/blog/devops/docker-vs-container)
- [https://refine.dev/blog/docker-build-args-and-env-vars/#how-to-pass-arg-variables](https://refine.dev/blog/docker-build-args-and-env-vars/#how-to-pass-arg-variables)



