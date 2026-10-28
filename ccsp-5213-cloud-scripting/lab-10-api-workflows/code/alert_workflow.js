const nodemailer = require('nodemailer');
const BUDGET_USD = 50;
const RESOURCES = [['vm-01', 72.5], ['db-02', 20.0], ['vm-03', 130.0], ['cache-04', 49.99], ['vm-05', 51.0]];
async function main() {
  const over = RESOURCES.filter(([, cost]) => cost > BUDGET_USD);
  if (!over.length) return console.log('Within budget, no alert sent');
  const transporter = nodemailer.createTransport({ host: 'localhost', port: 1025, secure: false });
  await transporter.sendMail({
    from: 'cost-automation@lab.local', to: 'ops@lab.local',
    subject: `Cloud Cost Alert: ${over.length} resources over budget`,
    text: over.map(([name, cost]) => `- ${name}: $${cost.toFixed(2)} (limit $${BUDGET_USD})`).join('\n'),
  });
  console.log(`Consolidated alert sent: ${over.length} resources over budget`);
}
main().catch(e => { console.error('Alert failed:', e.message); process.exit(1); });
