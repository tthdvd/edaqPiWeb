const { exec } = require('child_process');
exec('node server.js', (err, stdout, stderr) => {

    if (err) {
        // node couldn't execute the command
        return;
    }
    // the *entire* stdout and stderr (buffered)
    console.log(`stdout: ${stdout}`);
    console.log(`stderr: ${stderr}`);
});


exec('node socket.js', (err, stdout, stderr) => {
    if (err) {
        // node couldn't execute the command
        return;
    }
    // the *entire* stdout and stderr (buffered)
    console.log(`stdout: ${stdout}`);
    console.log(`stderr: ${stderr}`);
});


exec('python3 pi/main.py', (err, stdout, stderr) => {

    if (err) {
        // node couldn't execute the command
        return;
    }
    // the *entire* stdout and stderr (buffered)
    console.log(`stdout: ${stdout}`);
    console.log(`stderr: ${stderr}`);
});