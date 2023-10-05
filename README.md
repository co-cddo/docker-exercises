# Docker Exercises

A set of short, practical exercises to support learning about Docker. The focus is on using containers for local development.

The Dockerfiles are based on Ubuntu rather than Alpine or another small-footprint distribution, reflecting the focus on prototyping.

Want to cover some of the niggles associated with using Docker on Mac.

The images which rely on code use Python.

# 1 - Selecting a base image

I want to find out whether a particular image comes with a command or which version it uses:

```
docker run --rm ubuntu:22.04 curl --help
```

If I want to check several things, or poke about in the base image more generally:

```
docker run --rm -it ubuntu:22.04 /bin/bash
```

Note that `-it` is the same as `-i -t`, as distinct from `--rm` which is a single option. Hence only one dash for the former.

View process in host top. How to do on Mac?

# 2 - Managing Docker objects

## Containers

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

We can avoid some headaches by using `--rm` with the `docker run` command.

## Images

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
