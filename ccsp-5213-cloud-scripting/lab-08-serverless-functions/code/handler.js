'use strict'
const THRESHOLD_USD = Number(process.env.THRESHOLD_USD || 75);   // set to the instructor's value

module.exports = async (event, context) => {
  let payload;
  try { payload = JSON.parse(event.body || '{}'); }
  catch (e) { return context.status(400).succeed({ error: 'body must be JSON' }); }
  const cost = Number(payload.costUsd);
  if (!payload.resource || Number.isNaN(cost)) {
    return context.status(400).succeed({ error: 'resource and numeric costUsd are required' });
  }
  return context.status(200).succeed({ resource: payload.resource, costUsd: cost, overBudget: cost > THRESHOLD_USD });
}
