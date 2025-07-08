// Lambda Consumer App for Kinesis Stream

// Lambda Consumer
const consumer = async( event ) => {
  try{
	for( const record of event.Records ) {
      const payload = record.kinesis;
      const message = Buffer.from(payload.data, 'base64').toString();

      console.log(
        `Kinesis Message:
        partition key: ${payload.partitionKey}
        sequence number: ${payload.sequenceNumber}
        kinesis schema version: ${payload.kinesisSchemaVersion}
        data: ${message}`
      );
    }
  } catch ( error ) {
    console.log(error);
  }
};

export { consumer };
