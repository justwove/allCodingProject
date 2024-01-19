const friends = [
    {id: 1, name: 'Andre Paulo Leitao', age: 22},
    {id: 2, name: 'Illona Lefevre', age: 21},
]

let page = `<h1>Hello {%name%}<h2>
<p>Your age are {%age%}<p>`

page = page.replace('{%name%}', friends[0].name)
page = page.replace('{%age%}', friends[0].age)

const http = require('http')
const server = http.createServer((req, res) => {
    res.writeHead(200, {'Content-type': 'text/html'})
    res.end(page)
})

// Setup the port and the host
const port = 8000;
const host = '127.0.0.1';
server.listen(port, host, () => {
    console.log(`Server listening on port ${port} on host ${host}`);
});