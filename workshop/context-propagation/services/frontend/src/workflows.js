import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('cosmic-shop-ui');

/**
 * RUM custom workflow for a full purchase (distinct from the Purchase button click).
 * Requires Splunk RUM to be initialized first — uses the agent's TraceProvider.
 */
export function startPurchaseWorkflow(product) {
  return tracer.startSpan('purchase.checkout', {
    attributes: {
      'workflow.name': 'purchase.checkout',
      'purchase.product_id': product?.id ?? '',
      'purchase.product_name': product?.name ?? '',
    },
  });
}
