const kafka = require('./kafka')

const consumer = kafka.consumer({
  groupId: 'group-id'
})

const main = async () => {
  await consumer.connect()

  await consumer.subscribe({
    topic: 'loan-events',
    fromBeginning: true
  })

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      console.log('Received message', {
        topic,
        partition,
        value: message.value.toString()
      })
    }
  })
}

main().catch(async error => {
  console.error(error)
  try {
    await consumer.disconnect()
  } catch (e) {
    console.error('Failed to gracefully disconnect consumer', e)
  }
  process.exit(1)
})
