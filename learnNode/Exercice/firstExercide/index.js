const fs = require('fs')
/*
Synchronous read & write file

// Read file
const info = fs.readFileSync('info.txt', 'utf-8')
console.log(info)

// Use backtick (`) to do multi lines
const text = `This is a 
multi lines
textfile`

// Write to file (Will overwrite existing content)
fs.writeFileSync('test.txt', text)
// You don't need to set a variable here
console.log(fs.readFileSync('test.txt', 'utf-8'))
*/

// () => {} = Lambda function in python
/* This is a Asynchronous method to read a file
If you run the script, the console.log function will run before the printing the file content
*/ 
const info = fs.readFile('info.txt', 'utf-8', (err, data) => {
    console.log(data)
})
console.log('File was read')

const loadData = require('./loadData.js')
console.log(loadData())