// Lambda Consumer App for Kinesis Stream
import { propagation, trace, ROOT_CONTEXT } from "@opentelemetry/api";


// Lambda Consumer
const consumer = async( event ) => {
  try{
    for( const record of event.Records ) {
      const payload = record.kinesis;
      const message = Buffer.from(payload.data, 'base64').toString();

      // OpenTelemetry Manual Instrumentation
      const carrier = JSON.parse( message ).tracecontext;
      const parentContext = propagation.extract(ROOT_CONTEXT, carrier);
      const tracer = trace.getTracer(process.env.OTEL_SERVICE_NAME);
      const span = tracer.startSpan("Kinesis.getRecord", undefined, parentContext);

      span.setAttribute("span.kind", "CONSUMER");
      const body = JSON.parse( message ).record;
      if (body.name) {
        span.setAttribute("custom.tag.name", body.name);
      }
      if (body.superpower) {
        span.setAttribute("custom.tag.superpower", body.superpower);
      }
      // ------------------------------------

      console.log(
        `Kinesis Message:
        partition key: ${payload.partitionKey}
        sequence number: ${payload.sequenceNumber}
        kinesis schema version: ${payload.kinesisSchemaVersion}
        data: ${message}`
      );

      // End the manually-created span
      span.end();
      // -----------------------------
    }
  } catch ( error ) {
    console.log(error);
  }
};

export { consumer };
