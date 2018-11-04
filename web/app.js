let express = require('express');
let app = express();
const router = require('./router.js')
const path = require('path')
const api = require('./api.js')

app.use('/', router);
app.use(express.static(path.join(__dirname, 'public')))
app.use('/api/',api )

module.exports = app;