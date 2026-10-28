// Local harness that mimics the OpenFaaS node template, so the function can be tested without faasd.
const file = process.argv[2];
const handler = require(require('path').resolve(file));
const body = process.argv[3] ?? '';
const ctx = { status(code) { return { succeed: b => ({ status: code, body: b }) }; } };
handler({ body }, ctx).then(r => console.log(JSON.stringify(r)));
