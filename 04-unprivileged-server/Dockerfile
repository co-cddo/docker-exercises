FROM cddo-simple-webserver


# The standard steps for creating a new user in Linux
# The first user created in any *nix OS will usually be UID/GID 1000 but we're setting
## it explicitly here
RUN mkdir -p /home/runuser && \
    groupadd --gid 1000 runuser && \
    useradd --home-dir /home/runuser --shell /bin/bash --uid 1000 --gid 1000 runuser

USER runuser

# Note that the container uses the CMD direcive from the Dockerfile it's building on and
## that directives in this Dockerfile come after it. It's conventional to put CMD at the end
## but it doesn't really matter.