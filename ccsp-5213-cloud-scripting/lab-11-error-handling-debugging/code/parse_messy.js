function parseRow(row) {
  const cost = Number(row.cost);
  if (row.cost === '' || Number.isNaN(cost)) {
    console.warn(`${new Date().toISOString()} WARN skipped row: invalid cost "${row.cost}"`);
    return null;
  }
  return { resource: row.resource, cost };
}
