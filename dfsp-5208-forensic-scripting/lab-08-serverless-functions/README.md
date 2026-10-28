# Lab 8: Deploying Node.js Scripts as Serverless Functions

**Course:** DFSP-5208  |  **Lecture week:** 8  |  **Part of:** [Part I – DFSP-5208](../README.md)

## Objectives

- Understand the serverless/Functions-as-a-Service (FaaS) model without needing a paid cloud account.
- Write and test a Node.js forensic-alert function locally with a small harness that mimics the OpenFaaS Node template (Tier 1, required).
- Optionally deploy the same function with OpenFaaS on faasd, invoke it over HTTP and inspect its logs (Tier 2, optional).

## Short theory

Serverless computing lets a function run on demand without managing a server. Rather than requiring a paid AWS/Azure subscription, this lab first writes and tests the function locally with a small harness (Tier 1, required and graded) and then, optionally, deploys it with OpenFaaS on faasd (Tier 2). faasd is a lightweight FaaS engine that needs only Linux with systemd and containerd, with no Kubernetes cluster. Check the License before installing it: the faasd Community Edition is licensed for non-commercial, personal use under the faasd CE EULA, so confirm with your department that classroom use is covered. The local harness has no such restriction. This mirrors how a forensic alerting function (for example, “flag any log entry containing a known IOC”) is built and tested before it is deployed.

## Prerequisites

- Lab 7 completed (Node.js basics).
- Tier 1 needs only Node.js. Tier 2 (optional) also needs Docker (installed in Lab 1, Step 7), Linux with systemd, and faas-cli.

## Step-by-step solution


### Step 1: Create the lab folder and the local harness (Tier 1, required)

The harness loads a handler file and calls it the same way the OpenFaaS Node template does, so the function can be tested without faasd.

```bash
mkdir -p ~/forensic-scripting/lab08 && cd ~/forensic-scripting/lab08
```


```javascript
// Local harness that mimics the OpenFaaS node template, so the function can be tested without faasd.
const file = process.argv[2];
const handler = require(require('path').resolve(file));
const body = process.argv[3] ?? '';
const ctx = { status(code) { return { succeed: b => ({ status: code, body: b }) }; } };
handler({ body }, ctx).then(r => console.log(JSON.stringify(r)));
```

> 📁 Saved as [`code/harness.js`](code/harness.js)


### Step 2: Write the function logic

Create handler.js. It is the same file you would later place in ioc-alert/handler.js for faasd.

```javascript
'use strict'
const IOCS = ['malicious.exe', '203.0.113.99', 'suspicious-domain.test'];   // add two or more of your own

module.exports = async (event, context) => {
  const text = (event.body || '').toString().toLowerCase();
  const hits = IOCS.filter(ioc => text.includes(ioc.toLowerCase()));
  return context.status(200).succeed({ scanned: true, hits, matched: hits.length > 0 });
}
```

> 📁 Saved as [`code/handler.js`](code/handler.js)


### Step 3: Test the function


```bash
node harness.js handler.js 'beacon to 203.0.113.99 seen'
node harness.js handler.js 'all quiet'
```

Expected: the first command prints {"status":200,"body":{"scanned":true,"hits":["203.0.113.99"],"matched":true}} and the second prints a body with "hits":[] and "matched":false.

### Step 4: Understand “stateless”

A serverless function keeps nothing between calls: every invocation starts fresh, so anything that must persist (alerts already sent, counters) has to live in a database or file outside the function. Lab 10 returns to this idea.

### Step 5: Check the License and prerequisites (Tier 2, optional)

Only continue if your department confirmed that the faasd CE EULA covers classroom use, and your machine runs Linux with systemd (not plain Windows; use WSL2 with systemd enabled). Everything above this step is enough for full marks.

### Step 6: Install faasd and faas-cli (Tier 2)

Follow the faasd handbook for your faasd version; the commands below are the ones used when this manual was revised. The faas-cli installer is downloaded and read before it is run.

```bash
git clone https://github.com/openfaas/faasd --depth=1
cd faasd
sudo ./hack/install.sh
sudo systemctl status faasd   # should show active (running)
cd ..

curl -sSLo get-faas-cli.sh https://cli.openfaas.com
less get-faas-cli.sh          # read it before running it
sudo sh get-faas-cli.sh
faas-cli version
```


### Step 7: Start a local registry and scaffold the function (Tier 2)

faasd has no built-in registry, and faas-cli up builds and pushes the image, so run a local registry first. List the available Node templates and use the newest one (the node20 template is the oldest you should use: Node 20 reached end of life in April 2026).

```bash
docker run -d -p 5000:5000 --name registry registry:2
export OPENFAAS_URL=http://127.0.0.1:8080
sudo cat /var/lib/faasd/secrets/basic-auth-password | faas-cli login --username admin --password-stdin
faas-cli template store list
faas-cli template store pull <newest-node-template>
faas-cli new ioc-alert --lang <newest-node-template>
```


### Step 8: Deploy, invoke and inspect logs (Tier 2)

Copy handler.js into ioc-alert/handler.js and open ioc-alert.yml. Change the image line to 127.0.0.1:5000/ioc-alert:latest, then build, deploy and invoke. Check the faasd handbook for the registry and pull-policy settings of your faasd version if the pull fails.

```bash
cp handler.js ioc-alert/handler.js
faas-cli up -f ioc-alert.yml
curl -X POST http://127.0.0.1:8080/function/ioc-alert -d 'connection from 203.0.113.99 detected'   # expect "matched":true
faas-cli list
faas-cli logs ioc-alert
```


## Required outcomes / tasks

- [ ] Harness output showing a successful IOC match (matched: true) and a clean case (matched: false), system clock visible.
- [ ] Add at least two additional IOC strings relevant to a sample scenario provided by the instructor, and resubmit handler.js with new test output.
- [ ] Short answer: what does “stateless” mean for a function, and why does it matter?
- [ ] Optional (Tier 2): screenshot of `faas-cli list` showing the deployed ioc-alert function and the curl output.

## Code files in this lab

- [`code/handler.js`](code/handler.js)
- [`code/harness.js`](code/harness.js)
