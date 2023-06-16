# Getting started with Docker

You can run all of the code in this repository by creating a Docker container. You will need to have installed Docker on your computer and then:

1. Run the Docker application
2. Create directory and place the DockerFile inside it
3. cd into directory and use the command: docker build -t hsma2023 ./
4. Start the container using the comamnd: docker run -p 8080:80 hsma2023