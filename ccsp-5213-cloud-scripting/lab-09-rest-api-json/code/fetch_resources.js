const BASE = process.env.API_URL || 'https://jsonplaceholder.typicode.com';

async function main() {
  try {
    const res = await fetch(`${BASE}/todos`, { signal: AbortSignal.timeout(10000) });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);          // non-200 handled explicitly
    const data = await res.json();
    console.table(data.slice(0, 5).map(p => ({ id: p.id, title: p.title })));
  } catch (err) {
    console.error('API error:', err.message);
    process.exitCode = 1;
  }
}
main();
