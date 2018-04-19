let app = require('./web/app.js')
let port = '8080'

let server = app.listen(port, function () {
    console.log('The server is running on port' + port)
})