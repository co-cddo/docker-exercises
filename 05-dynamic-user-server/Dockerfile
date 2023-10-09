FROM cddo-simple-webserver

# This time we're setting the GID/UID to something unlikely to be the same as your
## user account on the host. Note that this is effectively the reverse of the 
## problem we're trying to solve: if we set the UID/GID as 1000 (typical) what
## happens if another dev has UID/GID 1002 because their machine has two accounts?
RUN mkdir -p /home/runuser && \
    groupadd --gid 1005 runuser && \
    useradd --home-dir /home/runuser --shell /bin/bash --uid 1005 --gid 1005 runuser

# Note that the container uses the CMD direcive from the Dockerfile it's building on and
## that directives in this Dockerfile come after it. It's conventional to put CMD at the end
## but it doesn't really matter.

# COPY user-init.sh /usr/local/bin
# RUN chmod +x /usr/local/bin/user-init.sh

USER runuser

# With the CMD line below commented out, we use the same one from the simple-webserver image
# CMD ["/usr/local/bin/user-init.sh"]
