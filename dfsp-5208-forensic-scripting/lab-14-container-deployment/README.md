# Lab 14: Automating Container Deployment

**Course:** DFSP-5208  |  **Lecture week:** 14 (2nd half) or 15  |  **Part of:** [Part I – DFSP-5208](../README.md)

## Objectives

- Run a free, self-hosted Docker Registry (open source, Apache-2.0) instead of a paid Docker Hub plan.
- Tag and push the Lab 13 image to the local registry.
- Pull and run the image from the registry on a second (simulated) host.

## Short theory

Docker Hub's free tier has pull-rate limits and a limited number of private repositories (check the current terms). The official `registry:2` image is fully open source and can be self-hosted at zero cost, which is what many organisations do internally for sensitive forensic tool images that must never leave a controlled network. This lab stands up a local registry and treats it as the deployment target. The lab registry has no TLS and no authentication, so use it only on your own machine or a closed lab network.

## Prerequisites

- Lab 13 completed (forensic-log-filter:1.0 image built).

## Step-by-step solution


### Step 1: Run a local open-source registry


```bash
docker run -d -p 5000:5000 --restart=always --name local-registry registry:2
```


### Step 2: Tag the image for the local registry


```bash
docker tag forensic-log-filter:1.0 localhost:5000/forensic-log-filter:1.0
```


### Step 3: Push the image


```bash
docker push localhost:5000/forensic-log-filter:1.0
```


### Step 4: Verify it is stored in the registry


```bash
curl http://localhost:5000/v2/_catalog
#   {"repositories":["forensic-log-filter"]}
curl http://localhost:5000/v2/forensic-log-filter/tags/list
#   {"name":"forensic-log-filter","tags":["1.0"]}
```


### Step 5: Simulate a second host: remove the local image, then pull it back and run it

The run mounts only a new out2 sub-folder, never /app.

```bash
docker rmi forensic-log-filter:1.0 localhost:5000/forensic-log-filter:1.0
docker pull localhost:5000/forensic-log-filter:1.0
mkdir -p out2
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD/out2:/app/out" localhost:5000/forensic-log-filter:1.0
```


## Required outcomes / tasks

- [ ] Output of `curl http://localhost:5000/v2/_catalog` showing the pushed image (system clock visible).
- [ ] Screenshot of the pull-then-run sequence proving the image was retrieved fresh from the registry, and the file out2/output.csv.
- [ ] Short note on one advantage and one limitation of self-hosting a registry versus using Docker Hub's free tier.
