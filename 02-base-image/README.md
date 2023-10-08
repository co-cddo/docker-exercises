## Base Image

## What packackes do we need?

Ubuntu distributions come with Python 3, so perhaps the Docker image does too. We can find out easily (we're going to be using Ubuntu 22 from now on):

```
docker run --rm ubuntu:22.04 python3 -V
```

If there are several things to check, or we want to poke around in a container based on the base image more generally:

```
docker run --rm -it ubuntu:22.04 /bin/bash
```

Note that `-it` is the same as `-i -t`, as distinct from `--rm` which is a single option. Hence only one dash for the former.

From within the container, we can check whether `curl` and/or `wget` are installed. We can also double check `python3` isn't masquerading as `python`.

Note something important: we're running as `root`. Making a user account on your host a member of the `docker` group means that account can carry out most operations as `root`, even if it's not a member of the `sudoers` group.

## Build

```
docker build . -t cddo-base-image
```

The `-t` option gives our image a name (tag)

## Run

```
docker run cddo-base-image
```

Note that this leaves us with a stopped container. If we also ran the hello world container, we now have two.
