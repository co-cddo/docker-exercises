## Unpriviledged web server

## Build

```
docker build . -t cddo-up-webserver
```

## Run

```
docker run -t --rm -p 8081:8081 --name upws-container cddo-up-webserver
```

## Running processes without root

You often see advice that we shouldn't run container processes as root. It's probably a bit overdone. There are two main reasons not to:
- When we're providing access to the host filesytem (permissions headaches and security)
- When we're using software which is glitchy when run as root

### Trying it out

We're not going to worry about volumes and bind mounts for now:

```
docker run -t --rm -p 8081:8081 --name upws-container cddo-up-webserver
```

In another terminal window, run:

```
docker exec -it upws-container /bin/bash
```

What do we see that's different from previous command prompts in our containers?

Run the following, in the container:

```
ps aux
```

The `USER` directive applies to any process we start unless/until we say otherwise.

Quit the command prompt opened with `docker exec` and run:

```
docker exec -u root -it upws-container /bin/bash
```

Then, just for good measure, in the container run `ps aux` again.
