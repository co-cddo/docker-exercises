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

### Access the server via Docker's network (Linux)

The publish command solves our problem by forwarding a port, but it's a convenience which avoids us having to deal directly with the underlying network. 

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

It's sometimes   useful to get a container's IP address from within the container itself. We can do this with the `iproute2` package, which is included in the base image. Let's replace the `CMD` directive with:

```
CMD ["sh", "-c", "ip route|awk '/scope/ { print $9 }' && python3 /app/server.py -D /www"]
```

Some additions to the run command. It's common to use `sh` like this for more complex commands but it's not actually a great idea. It means we're running our command through a shell, which means we need the `-i` option to close the container with a keyboard interrupt.

```
docker run --rm -it cddo-simple-webserver
```

Note: be careful not to include `-t` (or `i`) in `docker` commands which are run as part of CI/CD. There's no tty available and the build will fail, in GitHub actions at least.

Now let's get a command prompt in another, temporary container:

```
docker run --rm -it cddo-base-image /bin/bash
```

We can now curl the webserver in the other container.

So, all of this is doable but a bit fiddly. Remember that each container's IP address is not assigned until runtime. This is where `docker compose` shines.

## Bind mounting

Along with the `docker exec` command and Docker-managed networks, this the other way we typically interact with running containers.

Bind mounting is managed using the command line. Note that we're using the `name` option here which is useful when we know we're just running a single container based on our image. In this case it saves us looking for the container name when we want to run `docker exec`

```
docker run --rm -it -v ./app:/app -v ./www:/www -p 8081:8081 --name sws-container cddo-simple-webserver
```

We can see that the option uses the same format as that for publishing a port.

If we load our page we can now edit the html on the host, reload the page and see the results. We can also change the Python server script but we won't see the results of that until we *stop and restart* the container. This can be anywhere between much and slightly quicker than *rebuilding and running*.

We can also make changes on the container side which are visible in the host:

```
docker exec sws-container touch /app/newfile.txt
```

There's an easy-to-make mistake possible here. Try this, noting the difference between the arguments passed to the two `-v` options:

```
docker run --rm -it -v app:/app -v ./www:/www -p 8081:8081 --name sws-container cddo-simple-webserver
```

Now when we run `docker exec sws-container touch /app/newfile.txt` - what happens?

We've accidentally engaged Docker's other method for enabling persistent storage: volumes.

## Volumes

We can list the volumes being managed by Docker with `docker volume ls`.

We can get information on volume `app` with:

```
docker volume inspect app
```

So it's just a bind-mount really. The main advantage is that we don't have to worry about accidentally changing its contents or otherwise worry about managing it.

We can create anonymous volumes by omitting the first argument to the `-v` option. Try these in turn, noting that the `-d` means we sacrifice output from the server in exchange for not blocking the terminal.

```
docker run -d --rm -it -v /app --name sws-container cddo-simple-webserver
docker exec sws-container touch /app/newfile.txt
docker exec sws-container ls -la /app
docker stop sws-container
```

We'll use the same command to start a container with the same name, using the same image and list the contents of `/app`:

```
docker run -d --rm -it -v /app --name sws-container cddo-simple-webserver
docker exec sws-container ls -la /app
```
Anonymous volumes are not hugely helpful.

### Bind mounts and volumes together

This shows a good use-case for combining volumes and bind mounts. We'll go back to two terminal windows as the keyboard interrupt is usually a quicker way of stopping containers:

```
docker run --rm -it -v sws-root:/root -v app:/app -v ./www:/www -p 8081:8081 --name sws-container cddo-simple-webserver
docker exec -it sws-container /bin/bash
```

Within the container, let's check the working directory and list its contents:

```
pwd
ls -la
```

Exit and stop the container. Run it again and get a command prompt:

```
docker run --rm -it -v sws-root:/root -v app:/app -v ./www:/www -p 8081:8081 --name sws-container cddo-simple-webserver
docker exec -it sws-container /bin/bash
```

Tap the up key. There are many other scenarios where persisting data which you don't really need direct access to is useful.

### Final thoughts on volumes

We can use different 'volume drivers', including third party ones, to mount other types of storage as volumes.

The Docker documentation has a real downer on bind mounts. Ignore this - they have different use cases and that's all that should drive the decision as to which you need.

Volumes can be shared between containers. This can be done, to some extent, dynamically with the `docker run --volumes-from` option, but:
- `docker compose` is probably a better option for this
- unless you're careful it's a recipe for race conditions
- any usage which avoids race conditions is probably better substituted with something like a message broker/AWS SQS

There's a bigger difference between volumes and bind mounts on MacOS: volumes are stored within the VM.

Note that we haven't used the `VOLUME` directive in our Dockerfile to anything here. Like `EXPOSE` it's often referred to in tutorials but isn't really what controls how volumes are managed.

The `VOLUME` directive does have one important effect: changes to the directory it's used with, made within the Dockerfile after it is used have no effect.
