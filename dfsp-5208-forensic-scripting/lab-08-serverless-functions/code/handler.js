'use strict'
const IOCS = ['malicious.exe', '203.0.113.99', 'suspicious-domain.test'];   // add two or more of your own

module.exports = async (event, context) => {
  const text = (event.body || '').toString().toLowerCase();
  const hits = IOCS.filter(ioc => text.includes(ioc.toLowerCase()));
  return context.status(200).succeed({ scanned: true, hits, matched: hits.length > 0 });
}
