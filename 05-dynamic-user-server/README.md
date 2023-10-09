## Unpriviledged web server

## Build

```
docker build . -t cddo-du-webserver
```

## Setting the UID and GID of the runuser dynamically

This seems a bit niche but something I always do when configuring containers for local development that I share with other developers. We don't know the user setup on other people's machines.

Even more than anything else we've looked at, this a local development problem.

This example is a bit contrived, accounting for the fact that you probably are all using a user account with UID/GID. See the comment on generally setting the UID/GID to 1000 in the last example's Dockerfile. This will do the job in most cases. In this case, it's set to 1005. If somehow you're using the sixth user account on your host machine, change the value in the Dockerfile.

We can see our current UID/GID with:

```
echo $UID
echo $GID
id
```

Note that user and group names don't matter when it comes to permissions. They're just labels applied to the UID/GID values.

### Trying it out

Let's start by building the image with the command above.

For our contrived example to work, we need some restrictive permissions on the `app` and `www` directories in the `03-simple-web-server` directory. These should already be set, but let's check and make sure.

Enter the directory and run:

```
sudo chmod -R 700 app www 
```

This disables read, write and execute priviledges for anything other than the user account which owns them on the host (probably ID 1000).

Now, let's try to run our new image. It's the same as the unprivileged container image, with the exception of a different UID/GID and some commented out lines. Unlike in the last example, we'll use the bind mounts this time (so we need to still be in the `03-simple-webserver` directory).

```
docker run --rm -t -v ./app:/app -v ./www:/www -p 8081:8081 --name duws-container cddo-du-webserver
```

Recap of where we are: we're no longer using 'root' to run our Python server. We're using a user account we created in the Dockerfile. However, that user and the host machine user have a different UID/GID. So the container won't run. Note that without the bind mount it's fine.

```
docker run --rm -t -p 8081:8081 --name duws-container cddo-du-webserver
```
 
Now, let's uncomment the COPY, RUN and CMD lines in the Dockerfile and comment out the USER line. This has two effects: the CMD runs as root and the command it runs is an init script rather than the Python server.

First let's return to the `05-dynamic-user-server` directory, rebuild the image with `docker build . -t cddo-du-webserver`, and return
to the `03-simple-webserver` directory. We can then run our updated image with:

```
docker run --rm -t -v ./app:/app -v ./www:/www -p 8081:8081 --name duws-container cddo-du-webserver
```

The init script changes the UID/GID of `runuser` to the same values as those of the user account which executes `docker run`.

Init scripts like this can be used to carry out all sorts of useful one-time jobs. 

You can also carry out one-time jobs with the form:

```
docker run --rm -t 
```
