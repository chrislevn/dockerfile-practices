# Good practices on writing Dockerfile
Good practices on writing Dockerfile

1. **Use minimal base images**. 

Start with a minimal base image that contains only the necessary dependencies for your application. Using a smaller image reduces the image size and improves startup time.
```
No: 
  FROM python:3.9
```
```
YES:
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
