# Lab 14: Automating Container Deployment

**Course:** CCSP-5213  |  **Lecture week:** 14 (2nd half) or 15  |  **Part of:** [Part II – CCSP-5213](../README.md)

## Objectives

- Run a free, self-hosted Docker Registry (open source) instead of a paid Docker Hub plan.
- Run Moto (free, open-source S3 emulator) to simulate cloud object storage without an AWS account.
- Tag, push, and pull the Lab 13 image, and upload and download an artefact to and from the emulated bucket.

## Short theory

This lab pairs two free, open-source stand-ins for paid cloud services: the official `registry:2` image (Apache-2.0) for container images, and Moto, an S3 emulator that speaks the same API as AWS S3, so any boto3/AWS-SDK code written against it also works against real S3 later, with zero cost during coursework. (MinIO, used in earlier editions, no longer publishes community images and its repository is in maintenance mode.) The lab registry has no TLS and no authentication, so use it only on your own machine or a closed lab network.

## Prerequisites

- Lab 13 completed (cloud-log-filter:1.0 image built).
- Docker running.

## Step-by-step solution


### Step 1: Run a local open-source registry


```bash
docker run -d -p 5000:5000 --restart=always --name local-registry registry:2
```


### Step 2: Tag and push the image


```bash
docker tag cloud-log-filter:1.0 localhost:5000/cloud-log-filter:1.0
docker push localhost:5000/cloud-log-filter:1.0
```


### Step 3: Verify the push


```bash
curl http://localhost:5000/v2/_catalog
#   {"repositories":["cloud-log-filter"]}
curl http://localhost:5000/v2/cloud-log-filter/tags/list
#   {"name":"cloud-log-filter","tags":["1.0"]}
```


### Step 4: Make sure the artefact exists

Lab 13 should have produced out/output.csv. If it is missing, run the container again.

```bash
cd ~/cloud-scripting/lab13
ls out/output.csv || docker run --rm --user "$(id -u):$(id -g)" -v "$PWD/out:/app/out" cloud-log-filter:1.0
```


### Step 5: Run Moto and upload and download the artefact

Start the emulator, upload out/output.csv to a bucket, list the bucket, then download the file again and compare it with the original.

```bash
pip install "moto[server]" boto3
moto_server -p 5000 &
python3 - <<'PY'
import boto3
s3 = boto3.client("s3", endpoint_url="http://localhost:5000", region_name="us-east-1",
                  aws_access_key_id="test", aws_secret_access_key="test")
s3.create_bucket(Bucket="pipeline-artifacts")
s3.upload_file("out/output.csv", "pipeline-artifacts", "output.csv")
print([o["Key"] for o in s3.list_objects_v2(Bucket="pipeline-artifacts")["Contents"]])
s3.download_file("pipeline-artifacts", "output.csv", "downloaded.csv")
# the step the manual never does
PY
cmp out/output.csv downloaded.csv && echo "identical"
```


### Step 6: Simulate a second host: pull the image and run it


```bash
docker rmi cloud-log-filter:1.0 localhost:5000/cloud-log-filter:1.0
docker pull localhost:5000/cloud-log-filter:1.0
mkdir -p out2
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD/out2:/app/out" localhost:5000/cloud-log-filter:1.0
```


## Required outcomes / tasks

- [ ] Output of `curl http://localhost:5000/v2/_catalog` showing the pushed image (system clock visible).
- [ ] The list_objects_v2 output showing output.csv in the pipeline-artifacts bucket, and `identical` from the cmp command.
- [ ] Screenshot of the pull-then-run sequence proving the image was retrieved fresh from the registry.
- [ ] Short note comparing a self-hosted S3 emulator with a managed cloud storage free tier (durability, scaling, IAM, limits, account and billing).
