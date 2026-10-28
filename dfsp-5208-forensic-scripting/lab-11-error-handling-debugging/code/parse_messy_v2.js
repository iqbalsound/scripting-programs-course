const fs = require('fs');
const [, ...lines] = fs.readFileSync('messy_log.csv', 'utf8').trim().split('\n');
const rows = lines.map(l => { const [timestamp, severity] = l.split(','); return { timestamp, severity }; });
const parsed = rows.map(parseRow).filter(Boolean); console.log(`Successfully parsed ${parsed.length} rows`);
