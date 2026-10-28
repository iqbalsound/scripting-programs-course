function parseRow(row) {
  const sev = Number(row.severity);
  if (row.severity === '' || Number.isNaN(sev)) {
    console.warn(`${new Date().toISOString()} WARN skipped row: invalid severity "${row.severity}"`);
    return null;
  }
  return { timestamp: row.timestamp, severity: sev };
}
