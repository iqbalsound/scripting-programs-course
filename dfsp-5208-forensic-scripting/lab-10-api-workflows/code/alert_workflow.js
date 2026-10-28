const nodemailer = require('nodemailer');
const IOCS = ['malicious.exe', '203.0.113.99'];
const LINES = ['user admin logged in', 'outbound connection to 203.0.113.99 flagged', 'process malicious.exe started', 'backup done', 'dns query'];

async function main() {
  const findings = LINES.map((l, i) => ({ n: i + 1, l, hits: IOCS.filter(x => l.includes(x)) })).filter(f => f.hits.length);
  if (!findings.length) return console.log('No IOC matches, no alert sent');
  const transporter = nodemailer.createTransport({ host: 'localhost', port: 1025, secure: false });
  await transporter.sendMail({
    from: 'soc-automation@lab.local', to: 'analyst@lab.local',
    subject: `Forensic Alert: ${findings.length} IOC match(es)`,
    text: findings.map(f => `- line ${f.n}: ${f.hits.join(', ')} -> ${f.l}`).join('\n'),
  });
  console.log(`Consolidated alert sent: ${findings.length} matches`); }
main().catch(e => { console.error('Alert failed:', e.message); process.exit(1); });
