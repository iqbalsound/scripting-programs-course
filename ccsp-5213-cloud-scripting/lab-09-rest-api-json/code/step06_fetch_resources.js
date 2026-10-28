const url = (process.env.API_URL || 'https://jsonplaceholder.typicode.com') + '/todos';
const axios = require('axios');
axios.get(url, { timeout: 10000, validateStatus: () => true })
  .then(res => {
    if (res.status !== 200) throw new Error(`HTTP ${res.status}`);
    console.table(res.data.slice(0, 5).map(p => ({ id: p.id, title: p.title })));
  })
  .catch(err => { console.error('API error:', err.message); process.exitCode = 1; });
