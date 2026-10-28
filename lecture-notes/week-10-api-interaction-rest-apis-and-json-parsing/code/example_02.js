const fs = require("fs/promises");
require("dotenv").config();

async function main() {
  try {
    const res = await fetch(process.env.API_URL, {
      headers: { Key: process.env.API_KEY, Accept: "application/json" },
      signal: AbortSignal.timeout(10000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const ts = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15);
    await fs.writeFile(`evidence_${ts}.json`, JSON.stringify(data, null, 2));
    console.log("saved", ts);
  } catch (err) {
    console.error("Fetch failed:", err.message);
    process.exitCode = 1;
  }
}
main();
