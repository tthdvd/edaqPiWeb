let express = require('express')
let router = express.Router()
const path = require('path')

const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();

//router.use(bodyParser.urlencoded({ extended: true }));
///router.use(bodyParser.json());

router.get('/tasks', (req, res) => {

    let db = new sqlite3.Database('./edaq530.sql');
    let sql = 'SELECT * FROM tasks'
    db.all(sql, [], (err, rows) => {
        if(err) {
            throw err
        }

         res.send(rows)
    })
    db.close()
})

router.get('/task/measurements/:id', (req, res) => {
    let taskId = req.params.id;

    let db = new sqlite3.Database('./edaq530.sql');

    let sql = `SELECT * FROM data WHERE task_id = ${taskId}`

    db.all(sql, [], (err, rows) => {
        if(err) {
            throw err
        }

        res.send(rows)
    })

    db.close()
})

router.get('/task/info/:id', (req, res) => {
    let taskId = req.params.id;

    let db = new sqlite3.Database('./edaq530.sql');

    let sql = `SELECT * FROM tasks WHERE id = ${taskId}`

    db.get(sql, [], (err, rows) => {
        if(err) {
            throw err
        }

        res.send(rows)
    })

    db.close()
})


module.exports = router