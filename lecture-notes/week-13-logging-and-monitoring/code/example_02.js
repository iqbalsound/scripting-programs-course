const winston = require("winston");
const logger = winston.createLogger({
  level: "info",
  format: winston.format.combine(winston.format.timestamp(), winston.format.json()),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: "workflow.log" }),
  ],
});
logger.error("fetch failed", { url, err: err.message });
