const fs = require("fs/promises");
const path = require("path");
async function main(dir) {
  const names = await fs.readdir(dir);
  for (const [i, name] of names.entries()) {
    const ext = path.extname(name);
    const next = `file_${String(i + 1).padStart(4, "0")}${ext}`;
    console.log(`DRY RUN ${name} -> ${next}`);
  }
}
main(process.argv[2]).catch(e => { console.error(e.message); process.exit(1); });
