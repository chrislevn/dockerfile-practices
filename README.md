# Good practices on writing Dockerfile

1. Use minimal base images

Start with a minimal base image that contains only the necessary dependencies for your application. Using a smaller image reduces the image size and improves startup time.
```
No: 
  FROM python:3.9
```
```
Yes:
  FROM python:3.9-slim
```
<details>
<summary>Base image types: </summary>
  
  + stretch/buster/jessie: is the codename for Debian 10, which is a specific version of the Debian operating system. Debian-based images often have different releases named after characters from the Toy Story movies. For example, "Jessie" refers to Debian 8, "Stretch" refers to Debian 9, and "Buster" refers to Debian 10. These releases represent different versions of the Debian distribution and come with their own set of package versions and features.
  
  + slim: is a term commonly used to refer to Debian-based base images that have been optimized for size. These images are built on Debian but are trimmed down to include only the essential packages required to run applications. They are a good compromise between size and functionality, providing a balance between a minimal footprint and the availability of a wide range of packages.
  
  + alpine: Alpine Linux is a lightweight Linux distribution designed for security, simplicity, and resource efficiency. Alpine-based images are known for their small size and are highly popular in the Docker ecosystem. They use the musl libc library instead of the more common glibc found in most Linux distributions. Alpine images are often significantly smaller compared to their Debian counterparts but may have a slightly different package ecosystem and may require adjustments to some application configurations due to the differences in the underlying system libraries. However, some teams are moving away from alpine because these images can cause compatibility issues that are hard to debug. Specifically, if using python images, some wheels are built to be compatible with Debian and will need to be recompiled to work with an Apline-based image.

References: 
- https://medium.com/swlh/alpine-slim-stretch-buster-jessie-bullseye-bookworm-what-are-the-differences-in-docker-62171ed4531d
  
</details>

2. Use explicit tags for the base image. 
 Use explicit tags for the base image instead of generic ones like 'latest' to ensure the same base image is used consistently across different environments.
 
 ```
No: 
  FROM company/image_name:latest
```
```
Yes:
  FROM company/image_name:version
```

3. Leverage layer caching
Docker builds images using a layered approach, and it caches each layer. Place the instructions that change less frequently towards the top of the Dockerfile. This allows Docker to reuse cached layers during subsequent builds, speeding up the build process.

```
No:
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
In this bad example, each RUN instruction creates a new layer, making it difficult to leverage layer caching effectively. Even if there are no changes to the application code, every step from installing system dependencies to building the application will be repeated during each build, resulting in slower build times.

```
Yes:
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


4. Consolidate related operations
Minimize the number of layers by combining related operations into a single instruction. For example, instead of installing multiple packages in separate RUN instructions, group them together using a single RUN instruction.

```
No:
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
In this bad example, each package installation is done in a separate RUN instruction. This approach creates unnecessary layers and increases the number of cache invalidations. Even if one package changes, all subsequent package installations will be repeated during each build, leading to slower build times.

```
Yes: 
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


5. 
