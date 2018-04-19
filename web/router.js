let express = require('express')

let router = express.Router()
const path = require('path')

const sqlite3 = require('sqlite3').verbose();

router.get('/', function (req, res) {
    res.sendFile(path.join(__dirname + '/public/index.html'));
})

module.exports = router