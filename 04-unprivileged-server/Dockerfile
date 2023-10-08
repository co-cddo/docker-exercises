FROM cddo-simple-webserver


# The standard steps for creating a new user in Linux
RUN mkdir -p /home/runuser && \
    groupadd --gid 1001 runuser && \
    useradd --home-dir /home/runuser --shell /bin/bash --uid 1001 --gid 1001 runuser

# COPY user-init.sh /usr/local/bin
# RUN chmod +x /usr/local/bin/user-init.sh

# This CMD directive replaces the one in the Dockerfile
## we're building on
# CMD ["/usr/local/bin/user-init.sh", "&&", "/app/server.py", "-D", "/www"]

USER runuser

# Note that the container uses the CMD direcive from the Dockerfile it's building on and
## that directives in this Dockerfile come after it. It's conventional to put CMD at the end
## but it doesn't really matter.