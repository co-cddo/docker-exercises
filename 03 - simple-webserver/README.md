## Simple web server

## Build

This time, let's set the following environment variable, because we don't like new things:

```
export BUILDKIT_PROGRESS=plain
```

Note that prepending `export` causes the env var to be passed to sub-processes.

```
docker build . -t cddo-simple-webserver
```

## Run

```
docker run -t --rm cddo-simple-webserver
```

We've used `-t` before but only with `-i` which isn't needed here because we're not interacting with the running container.

## Try the server out

### Access the server on localhost

Let's try to access our web server by entering the provided address in the browser (`http://0.0.0.0:8081/`).

Let's try using curl (in another terminal window) to access the server on localhost:

```
curl 127.0.0.1:8081
```

When we want to poke around in a running container, we use `docker exec`. First, find the name Docker generated for the running container then run the following, suitably adapted:

```
docker exec --it tiresome_couplet /bin/bash
```

We use `run` to start containers and `exec` to start processes in an *already running* container. When containers are giving you trouble there isn't really any substitute for having a look inside. This applies equally to staging and production services where - taking appropriate care - you can use [AWS ECS Exec](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html) or [Azure container exec](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-exec).

With a command prompt, we can now try using curl, but this time from within the container. Use the same command we just tried.

### Access the container via Docker's network

Let's see what networks are being managed by Docker:

```
docker network ls
```

This isn't much help. Let's try to get more info about the actual container:

```
docker container inspect tedious_phraseme
```

(`docker inspect tedious_phraseme` will also work here).

We have an IP address! We can also see which network the container is attached to. We can get more information about this with the following command, though we already have what we need:

```
docker network inspect bridge
```

Now we have the IP address, we can try accessing the server via the browser, remembering to specify the port.

### An easier way

Let's add the following line to the simple-webserver Dockerfile, immediately above the `CMD` directive:

```
EXPOSE 8081
```