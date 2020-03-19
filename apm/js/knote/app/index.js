const tracer = require('signalfx-tracing').init({
  // Service name also configurable via SIGNALFX_SERVICE_NAME environment variable
  service: process.env.SIGNALFX_SERVICE_NAME || 'knote-js',
  url: `http://${process.env.SIGNALFX_AGENT_HOST}:9080/v1/trace`,
  debug: true
})
const path = require('path')
const express = require('express')
const MongoClient = require('mongodb').MongoClient
const multer = require('multer')
const marked = require('marked')
const minio = require('minio')

const app = express()
const port = process.env.PORT || 3000
const mongoURL = process.env.MONGO_URL || 'mongodb://localhost:27017/dev'
const minioHost = process.env.MINIO_HOST || 'localhost'
const minioBucket = 'image-storage'

async function initMongo() {
  console.log('Initialising MongoDB...')
  let success = false
  while (!success) {
    try {
      client = await MongoClient.connect(mongoURL, { useNewUrlParser: true })
      success = true
    } catch {
      console.log('Error connecting to MongoDB, retrying in 1 second')
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
  }
  console.log('MongoDB initialised')
  return client.db(client.s.options.dbName).collection('notes')
}

async function initMinIO() {
  console.log('Initialising MinIO...')
  const client = new minio.Client({
    endPoint: minioHost,
    port: 9000,
    useSSL: false,
    accessKey: process.env.MINIO_ACCESS_KEY,
    secretKey: process.env.MINIO_SECRET_KEY,
  })
  let success = false
  while (!success) {
    try {
      if (!(await client.bucketExists(minioBucket))) {
        await client.makeBucket(minioBucket)
      }
      success = true
    } catch {
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
  }
  console.log('MinIO initialised')
  return client
}

async function start() {
  const db = await initMongo()
  const minio = await initMinIO()

  app.set('view engine', 'pug')
  app.set('views', path.join(__dirname, 'views'))
  app.use(express.static(path.join(__dirname, 'public')))

  app.get('/', async (req, res) => {
    res.render('index', { notes: await retrieveNotes(db) })
  })

  app.post(
    '/note',
    multer({ storage: multer.memoryStorage() }).single('image'),
    async (req, res) => {
      if (!req.body.upload && req.body.description) {
        await saveNote(db, { description: req.body.description })
        res.redirect('/')
      } else if (req.body.upload && req.file) {
        await minio.putObject(
          minioBucket,
          req.file.originalname,
          req.file.buffer
        )
        const link = `/img/${encodeURIComponent(req.file.originalname)}`
        res.render('index', {
          content: `${req.body.description} ![](${link})`,
          notes: await retrieveNotes(db),
        })
      }
    }
  )

  app.get('/img/:name', async (req, res) => {
    const stream = await minio.getObject(
      minioBucket,
      decodeURIComponent(req.params.name),
    )
    stream.pipe(res)
  })

  app.listen(port, () => {
    console.log(`App listening on http://localhost:${port}`)
  })
}

async function saveNote(db, note) {
  await db.insertOne(note)
}

async function retrieveNotes(db) {
  const notes = (await db.find().toArray()).reverse()
  return notes.map(it => {
    return { ...it, description: marked(it.description) }
  })
}

start()
