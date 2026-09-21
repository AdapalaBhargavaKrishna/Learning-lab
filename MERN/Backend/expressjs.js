const express = require('express')
const blog = require('./routes/blog')
const shop = require('./routes/shop')
const app = express()
const port = 3000

app.use(express.static('public'))
app.use('/blog', blog)
app.use('/shop', shop)

app.get('/', (req, res) => {
  console.log("This is get request")
  res.send('Hello World!')
})

app.post('/', (req, res) => {
  console.log("This is Post request")
  res.send('This is Post request')
})

app.get('/index', (req, res) => {
  console.log("This is index")
  res.sendFile('templates/index.html', {root: __dirname})
})

app.get('/about', (req, res) => {
    res.send('This is about')
  })

app.get('/contact', (req, res) => {
  res.send('This is contact')
})  

app.get('/blog', (req, res) => {
    res.send('Hello Blog!')
  })

  app.get('/blog/:slug', (req, res) => {
    res.send(`Hello ${req.params.slug}`)
  })

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})