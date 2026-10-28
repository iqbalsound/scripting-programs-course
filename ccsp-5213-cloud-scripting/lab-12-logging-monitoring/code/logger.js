const winston = require('winston');
const logger = winston.createLogger({
  level: 'debug',
  format: winston.format.combine(winston.format.timestamp(), winston.format.json()),
  transports: [
    new winston.transports.File({ filename: 'pipeline.json.log', maxsize: 1_000_000, maxFiles: 3 }),
    new winston.transports.Console(),
  ],
});
logger.info('Deployment pipeline started', { resource: 'vm-01', region: 'us-east-1' });
logger.warn('Resource vm-01 approaching budget limit'); logger.error('Failed to provision resource: quota exceeded');
