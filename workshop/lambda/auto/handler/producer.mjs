// Lambda Producer App for Kinesis Stream
import { KinesisClient, PutRecordCommand } from "@aws-sdk/client-kinesis";


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

  try {
    await kinesis.send(
      new PutRecordCommand({
        StreamName: streamName,
        PartitionKey: "1234",
        Data: event.body,
      }),

      message = `Message placed in the Event Stream: ${streamName}`
	)
  } catch ( error ) {
    console.log(error);
    message = error;
    statusCode = 500;
  }

  return {
    statusCode,
    body: JSON.stringify({
      message,
    }),
  };
};

export { producer };
