const winston = require('winston');
const logger = winston.createLogger({
  level: 'debug',
  format: winston.format.combine(winston.format.timestamp(), winston.format.json()),
  transports: [
    new winston.transports.File({ filename: 'pipeline.json.log', maxsize: 1_000_000, maxFiles: 3 }),
    new winston.transports.Console(),
  ],
});
logger.info('Pipeline started');
logger.warn('Suspicious file skipped: corrupt_evidence.dat'); logger.error('Failed to hash file: permission denied');
