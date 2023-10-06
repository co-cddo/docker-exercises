# Docker Exercises

A set of short, practical exercises to support learning about Docker. The focus is on using containers for local development.

The Dockerfiles are based on Ubuntu rather than Alpine or another small-footprint distribution, reflecting the focus on prototyping.

Want to cover some of the niggles associated with using Docker on Mac.

The images which rely on code use Python.

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

We can avoid some headaches by using `--rm` with the `docker run` command.

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
