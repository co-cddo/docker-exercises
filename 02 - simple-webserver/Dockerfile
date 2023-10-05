# I prefer to avoid pre-built Python images. Doing it this way provides more granular control.
FROM ubuntu:22.04

# Update the OS's list of packages. We don't use 'apt subcommand' in scripts
# Add an env var and some options to stop it asking us questions and installing things which it
## thinks are helpful but aren't strictly needed

# Start by installing some text editors and basic tools.
# If you think I'm lame for using Nano, I don't care
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nano vim emacs \
    curl wget

# See the main README (1) for help on working out what other packages we need
# If we specify python3-pip we don't need to specify python3, because it's a dependency. It's
## a good idea to do so anyway
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip

# This is an Ubuntu-specific thing.
# If we don't do this then sometimes our build will stop to ask us to specify a time zone, so I
## put it in all my base images.

ENV TZ=Europe/London
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# clean - delete downloaded archive files
# autoremove - delete any unused packages
# rm ... - delete the package lists downloaded with apt-get update
# Once we're happy with our Dockerfile we can move all apt commands to a single RUN directive at the
## top

RUN apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists


CMD
