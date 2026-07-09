import { start } from '@splunk/otel';

start({
  serviceName: process.env.OTEL_SERVICE_NAME || 'frontend-api',
});
