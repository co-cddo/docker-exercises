## Using Docker Compose to Manage Containers

Docker compose has some real benefits when it comes to working with multiple containers, though it's not without its downsides. It's largely a local development and CI/CD tool. When running a multiple container service in production it's more common to use something like AWS Fargate.

Docker compose uses a YAML file to manage several containers. It can run each with either an image of a Dockerfile as an input. The rest of the config for each service largely repeats options and arguments we'd pass to `docker run` or `docker build` on the command line.

Beyond being - arguably - easier to work with than multiple `docker` commands it has two advantages: we can specify the relationships between containers and it makes inter-container communication easier by automatically assigning hostnames.

Let's start by looking at the `docker-compose.yml` file.

## Using the 'up' subcommand

We can build those images which need building and download any others using the following command:

```
docker compose build
```

...but we don't need to. We can equally just go ahead and start them with:

```
docker compose up
```

We can see that this brings up all of our containers. 

Where we set a `depends_on` option, the specified container is either brought up, or allowed to run and exit, before the container with the `depends_on` option is started.

We get the output of all the containers in the terminal. Note the IP addres of the server container is displayed.

If we run `docker container ls` in another terminal we can see three of the four containers are running. It's intentional that the `cddo-init` container runs and exits.

We can bring down all the services with `Ctrl-C`. Note that it's fairly slow. While this stops all the containers, it doesn't remove them.

## Using the 'run' subcommand

The `docker compose up` and `docker compose run` commands have some subtle differences. They don't share all of the same command line arguments and there are some edge cases where neither is flexible enough and it's better to resort to a series of `docker run` commands either in a shell script or Makefile.

We can see some important differences between `up` and `run` now. We'll clean up beforehand, just to make sure we're starting afresh:

```
docker compose down
docker container rm $(docker container ls -a -q) # This ought not to do anything if the last command cleared everything
docker compose run cddo-command-prompt
```

Note:
- This doesn't bring up the cddo-tail container
- We're automatically attached to the tty of the container we specified
- We don't get the terminal output from any other containers (though we can see this with `docker compose logs`)
- When exit the `cddo-command-prompt` container it doesn't stop all the other containers (we need `docker compose down`)

## Further thoughts

When we bring containers up with `docker compose` it creates a new bridge network and this can sometimes be a bit brittle. E.g. accessing a container - on a published port - from the host can make the container inaccessible from other containers. I was unable to re-produce this problem consistently when preparing this exercise.

The `EXPOSE` and `VOLUME` directives still aren't needed in the Dockerfiles.

It's terrible slow.

It has a tendency to leave containers lingering. On the plus side, it gives them sensible (albeit verbose) names.

