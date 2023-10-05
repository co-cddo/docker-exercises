## Hello World

Build:

```
docker build . -t cddo-hello-world
```

The `-t` option gives our image a name (tag)

Run a *container* based on our *image*:

```
docker run cddo-hello-world
```

Note that this leaves us with a stopped container. See main README (2).
