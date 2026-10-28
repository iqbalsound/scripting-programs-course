const fs = require('fs');
const [, ...lines] = fs.readFileSync('messy_billing.csv', 'utf8').trim().split('\n');
const rows = lines.map(l => { const [resource, cost] = l.split(','); return { resource, cost }; });
const parsed = rows.map(parseRow).filter(Boolean); console.log(`Successfully parsed ${parsed.length} rows`);
