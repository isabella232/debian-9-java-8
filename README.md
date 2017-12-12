# Debian 9 (Stretch) Java 8 Docker Image

## Description

This image provides a [Debian](https://www.debian.org/) 9 image plus java 8. Jar files placed under /var/www should automatically get run. This is created specifically to be run under [OpenShift Origin](https://www.openshift.org/) and [Kubernetes](https://kubernetes.io/), as well as any other standard Docker environment.

**Ensure you specify a user id (UID) other than zero. Running as root is not a supported configuration.**

## Current Status: Work In Progress

This image is currently an experimental work in progress.
