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

Let's try to access our web server by entering the provided address in the browser (`http://127.0.0.1:8081/`).

Let's try using curl (in another terminal window) to access the server on localhost:

```
curl 127.0.0.1:8081
```

When we want to poke around in a running container, we use `docker exec`. First, find the name Docker generated for the running container then run the following, suitably adapted:

```
docker exec --it container_name /bin/bash
```

We use `run` to start containers and `exec` to start processes in an *already running* container. When containers are giving you trouble there isn't really any substitute for having a look inside. This applies equally to staging and production services where - taking appropriate care - you can use [AWS ECS Exec](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html) or [Azure container exec](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-exec).

With a command prompt, we can now try using curl, but this time from within the container. Use the same command we just tried.

### Making the container's service available on localhost

```
docker run -t -p 8081:8081 cddo-simple-webserver
```

The `-p` switch ('publish') maps the container port on the right to the host port on the left. Try to access the server via the browser again.

You'll often see documentation which says you need this line in the Dockerfile:

```
EXPOSE 8081
```

You don't. If we use the `-P` option with `docker run` it will publish all of the ports exposed in the Dockerfile, but to random ports on the host. It's mostly useful as a statement of intent.

We'll see some examples with `docker compose` where it's important.

### Access the server via Docker's network

The publish command solves our problem by forwarding a port. This tells us we must be dealing with a network.

Let's stop our container and then see what networks are being managed by Docker:

```
docker network ls
```

This isn't much help. Let's try to get more info about the actual container:

```
docker container inspect container_name
```

(`docker inspect container_name` will also work here).

We have an IP address! We can also see which network the container is attached to. We can get more information about this with the following command, though we already have what we need:

```
docker network inspect bridge
```

Now we have the IP address, we can run the container with the original run command (no `-p option`) and try again to access the server via the browser, remembering to specify the port.

### Access the server from another container

Being able to do this is essential to Docker's usefulness. Even when applications follow a monolithic pattern it will almost inevitably involve containers talking to each other.

Let's stop and remove our running containers.

It's occasionally useful to get a container's IP address from within the container itself. We can do this with the `iproute2` package, which is included in the base image. Let's replace the `CMD` directive with:

```
CMD ["sh", "-c", "ip route|awk '/scope/ { print $9 }' && python3 /app/server.py -D /www"]
```

Some additions to the run command. It's common to use `sh` like this for more complex commands but it's a shell, which means we need the `-i` option to close the container with a keyboard interrupt.

`docker run --rm -it cddo-simple-webserver `

Note: be careful not to include `-t` (or `i`) in `docker` commands which are run as part of CI/CD. There's no tty available and the build will fail, in GitHub actions at least.

Now let's get a command prompt in another, temporary container:

`docker run --rm -it cddo-base-image /bin/bash`

We can now curl the webserver in the other container.

So, all of this is doable but a bit fiddly. Remember that each container's IP address is not assigned until runtime. This is where `docker compose` shines.

### Bind mounting

Along with the `docker exec` command and Docker's network, this the other essential way we interact with running containers.