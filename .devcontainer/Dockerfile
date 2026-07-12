FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm

# The Yarn repository GPG key is currently broken in Microsoft's devcontainer images,
# which causes apt-get update to fail when the docker-in-docker feature is installing.
# We remove the yarn list so apt-get update succeeds.
RUN rm -f /etc/apt/sources.list.d/yarn.list || true
