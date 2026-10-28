exports.handler = async (event) => {
  const text = event.text ?? "";
  const words = text.split(/\s+/).filter(Boolean).length;
  return { statusCode: 200, body: JSON.stringify({ words }) };
};
