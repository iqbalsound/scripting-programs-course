// Usage: node rename_forensic_files.js <dir> [--apply]   (dry run by default; never overwrites)
const fs = require('fs/promises');
const path = require('path');

const STAMPED = /^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z_/;

async function renameFiles(dir, apply) {
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  let count = 0, skipped = 0;
  for (const file of await fs.readdir(dir)) {
    const oldPath = path.join(dir, file);
    if (!(await fs.stat(oldPath)).isFile()) continue;
    if (STAMPED.test(file)) { skipped++; continue; }              // already has a timestamp prefix
    const newPath = path.join(dir, `${stamp}_${file}`);
    try { await fs.access(newPath); console.error(`refusing to overwrite ${newPath}`); continue; } catch {}
    console.log(`${apply ? 'RENAME' : 'DRY RUN'} ${file} -> ${path.basename(newPath)}`);
    if (apply) await fs.rename(oldPath, newPath);
    count++;
  }
  console.log(`${apply ? 'Renamed' : 'Would rename'} ${count} files, skipped ${skipped}, in ${dir}`);
}

const args = process.argv.slice(2);
renameFiles(args.find(a => !a.startsWith('--')) || '.', args.includes('--apply'))
  .catch(err => { console.error('Error:', err.message); process.exit(1); });
