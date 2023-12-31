# CDDO Graduate Developer Programme - Docker Exercises

A set of short, practical exercises to support learning about Docker. The focus is on using containers for local development and some of the underlying mechanics which aren't necessarily well explained in the innumerable Docker tutorials available online.

The Dockerfiles are based on Ubuntu rather than Alpine or another small-footprint distribution, reflecting the focus on prototyping.

The images which rely on code use Python.

## Exercises

There are several sets of Dockerfiles/READMEs to work through, each which introduces different concepts:

- **01-hello-world** - the most basic Dockerfile and run command possible
- **02-base-image** - running downloaded images directly, installing packages, using images as the basis for other images.

With a couple of stopped containers lurking, it's a good time to cover managing Docker objects (images, containers, volumes, networks) below.

- **03-simple-webserver** - deploying a very basic application in Docker; Docker networking; volumes and bind mounts.
- **04-unprivileged-webserver** - how to avoid running services as root.
- **05-dynamic-user-server** - dynamically setting the container's user to match the host's user.
- **06-docker-compose** - how docker compose can simplify managing a multi-container service.

## Docker on MacOS

There are some peculiarities resulting from the fact that Docker runs in a VM. 

One is that we need Docker Desktop to be running before we can use Docker commands. We should ensure that VirtioFS is enabled in Docker Desktop settings (depending on the the version, this may be the default). Also note that while Docker Desktop is running, the allocated resources are resevred by it. 

The Docker VM is designed to be invisible, but sometimes it's useful to get into it. We can do this with the following command:

```
nc -U ~/Library/Containers/com.docker.docker/Data/debug-shell.sock
```

These exercises rely on some basic OS packages and Python. Everything should run well on arm64 Macs. Famous last words.

## Managing Docker objects

### Containers

First, see what containers are there. Docker doesn't like to tie people down so it has three commands for doing exactly the same thing (listing *running* containers):

```
docker container ps

docker container ls

docker ps

```

But obviously `docker ls` doesn't work. What's wrong with you?

Often we want to see stopped containers as well. Try this:

```
docker run --name stopped-container ubuntu:22.04 echo "I've finished"
docker run --name stopped-container ubuntu:22.04 echo "I won't work"
```

We can see all containers, including stopped containers, by adding `-a` to any of the variations of the list command.

We can then get rid of our container with:

```
docker container rm stopped-container
```

Fairly often when running `docker container ls` (etc) we'll find a graveyard of long-forgotten containers from different projects.

Let's simulate this:

```
docker run --name one ubuntu:22.04 echo "one" && docker run --name two ubuntu:22.04 echo "two" && docker run --name three ubuntu:22.04 echo "three"
```

We can see the stopped containers with `docker container ls -a`.

We can get just the container IDs with `-q` or `--quiet`.

By combining this with the `docker rm` command, we can remove all containers:

```
docker container rm $(docker container ps -a -q)
```

This approach also works for stopping containers and removing other docker objects like images, volumes and containers.

#### Stopping conntainers

It's rare to want to preserve containers (vs. images and volumes) between runs when developing. We typically use the `--rm` option with the `docker run` command so that the container is removed when it exits but we typically forget to add it too.

A running container can be stopped with:

```
docker container stop container_name
```

And restarted with:

```
docker start contianer_name
```

### Images

To list all images:

```
docker image ls
```

Naturally there's another variation: `docker images`.

Note that `-a` does something different here (lists intermediate images).

We can narrow things down by repository:

```
docker image ls ubuntu
```

We can use globbing:

```
docker image ls "ubunt*"
```

Note that zsh needs the double quotes. This works in bash: `docker image ls ubunt*`.

When this isn't enough, the `--filter` switch can be helpful. Docs [here](https://docs.docker.com/engine/reference/commandline/images/)

With the hello-world image built:

```
docker image ls --filter "before=cddo-hello-world"
```

We can combine the `ls` command with the `rm` command as we did with the containers (but let's not):

```
docker image rm $(docker image ls -a -q)
```

#### Intermediate vs. dangling images

There is a helpful explanation [here](https://medium.com/@krishnakummar/dangling-none-none-docker-images-714514627fb#:~:text=Dangling%20%3A%20docker%20images,-Krishna&text=These%20intermediate%20images%20are%20important,a%20wastage%20of%20disk%20space.&text=These%20%3A%20are%20called%20as%20the,images%20needs%20to%20be%20pruned.)

The short version is that some images which appear as `<none>  <none>` when we run `docker image ls -a`
are useful and some aren't. We can get rid of the ones we don't need with:

```
docker image rm $(docker images -f "dangling=true" -q)
```

### Volumes

It's rarer to have to deal with volumes day-to-day but they can build up. Bear in mind though that if you use, for example, a Postgres image, all of its data will be in a volume. So be careful.

List:

```
docker volume ls
```

Remove all:

```
docker volume rm $(docker volume ls -q)
```

### Networks

It's even rarer to have to worry about networks but every now and again `docker compose` will die without
properly cleaning up, then fail to start again.

List:

```
docker network ls
```

Remove *almost* all:

```
docker network rm $(docker network ls -q)
```

### Prune commands

The following `docker` subcommands each have a `prune` command:

- `network` - remove all unused networks
- `container` - remove all stopped containers
- `image` - remove all dangling images (and unused with `-a`)
- `volume` - remove all unused, anonymous volumes

Be careful with the `volume prune` subcommand.

Be careful in general with these because you're relying on Docker to choose what to delete. Other than with volumes, any unwanted deletions are usually easily fixed however.