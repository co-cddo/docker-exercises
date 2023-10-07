# I prefer to avoid pre-built Python images. Doing it this way provides more granular control.
FROM cddo-base-image:latest

# Copy our HTML over
# The COPY command is a bit fussy. 'COPY www /' will copy the contents of www to the root.
COPY www /www
# We could also use:
# ADD www /www
# The ADD command can - unlike COPY - be used to add files from a remote host or unpack a tar

# Copy our server script
COPY app /app

# File permissions can sometimes get mangled when things are copied, so I'd always do this for scripts
## I want to invoke without calling the interpreter (Python, Bash, etc) directly
RUN chmod +x /app/server.py

# clean - delete downloaded archive files
# autoremove - delete any unused packages
# rm ... - delete the package lists downloaded with apt-get update
# Once we're happy with our Dockerfile we can move all apt commands to a single RUN directive at the
## top
RUN apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists


CMD ["/app/server.py", "-D", "/www"]

# Here are some variations on providing Docker with an initial command
# Each works differently
# ENTRYPOINT ["/app/server.py", "-D", "/www"]

# The difference between the two CMD variations is quite subtle. The first (JSON) doesn't run the command through
## a shell, so no variable substitution takes place. We're passing the literal string "$PORT".
# CMD ["/app/server.py", "-D", "/www", "-P", "$PORT"]
# CMD /app/server.py -D /www -P $PORT
