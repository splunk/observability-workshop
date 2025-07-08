// Lambda Producer App for Kinesis Stream
import { KinesisClient, PutRecordCommand } from "@aws-sdk/client-kinesis";
import { context, propagation, trace, } from "@opentelemetry/api";


const tracer = trace.getTracer(process.env.OTEL_SERVICE_NAME);

// Lambda Producer
const producer = async( event ) => {
  const kinesis = new KinesisClient({});

  let statusCode = 200;
  let message;

  if (!event.body) {
    return {
      statusCode: 400,
      body: JSON.stringify({
        message: "No message body found",
      }),
    };
  }

  const streamName = process.env.KINESIS_STREAM;

  // OpenTelemetry Manual Instrumentation
  return tracer.startActiveSpan('Kinesis.PutRecord', async(span) => {
    span.setAttribute('span.kind', 'PRODUCER');
    span.setAttribute('messaging.system', 'Kinesis');
    let carrier = {};
    propagation.inject(context.active(), carrier);
    const eventBody = Buffer.from(event.body, 'base64').toString();
    const data = "{\"tracecontext\": " + JSON.stringify(carrier) + ", \"record\": " + eventBody + "}";
    console.log(
      `Record with Trace Context added:
      ${data}`
    );

    try {
      await kinesis.send(
        new PutRecordCommand({
          StreamName: streamName,
          PartitionKey: "1234",
          Data: data,
		}),
	
        message = `Message placed in the Event Stream: ${streamName}`
      )
    } catch ( error ) {
      console.log(error);
      message = error;
      statusCode = 500;
    }

    span.end();

    return {
      statusCode,
      body: JSON.stringify({
        message,
      }),
    };
  });
};

export { producer };
