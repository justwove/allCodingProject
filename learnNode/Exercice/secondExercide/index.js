// Import the http module
const http = require('http');

// Create the server instance 
// req : incoming Request
// res : outgoing Response

const server = http.createServer((req, res) => {
    // send a response to the client
    // res.end('Hello world from the street');
    const pathName = req.url;
    if (pathName === '/friends') {
        res.end('This is my friends page')
    } else if (pathName === '/') {
        res.end('This is the server root page')
    } else {
        res.writeHead(404, {
            'Content-Type': 'text/html'
        });
        res.end('<h1>Page not found</h1>');
    }
});

// Setup the port and the host
const port = 8000;
const host = '127.0.0.1';
server.listen(port, host, () => {
    console.log(`Server listening on port ${port} on host ${host}`);
});