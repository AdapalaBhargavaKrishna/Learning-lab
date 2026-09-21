const express = require('express')
const app = express()
const port = 3000

app.use(express.static('public'))

app.use((req, res, next) =>{
    console.log("m1")
    next()
})

app.use((req, res, next) =>{
    console.log("m2")
    next()
})

app.get('/', (req, res) => {
  console.log("This is get request")
  res.send('Hello World!')
})

app.get('/about', (req, res) => {
  console.log("This is get request")
  res.send('Hello About!')
})

app.get('/contact', (req, res) => {
  console.log("This is get request")
  res.send('Hello Contact!')
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
  })