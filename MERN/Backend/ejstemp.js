const express = require('express')
const app = express()
const port = 3000

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
    let sitename = "Adidas"
    let searchText = "Search Now"
    res.render('ejstemp', {sitename: sitename, searchText: searchText})
})

app.get('/blog/:slug', (req, res) => {
  console.log("This is get request")
  res.send('Hello About!')
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
  })