const http = require('http')

const friends = [
    {id: 1, name: 'André Paolo Leitao', age: 22},
    {id: 2, name: 'Illona Lefevre', age: 21},
]

const mylove = [
    {id: 1, name: 'Laura Goncalves', age: 19, nickName: 'Chouwtouille', dogName: 'Tintin'},
]
const myloveJson = JSON.stringify(mylove)

const server = http.createServer((req, res) => {
    const pathName = req.url
    const [, , entity, id] = pathName.split('/') 
    // ['127.0.0.1', 'api', 'friends', '1']

    if (pathName === '/friends'){
        res.writeHead(200, {'Content-Type': 'text/html'})
        res.end('<h1>This is my friends page</h1>')
    }else if (pathName === '/api/friends/') {
        const friend = friends.find((friend) => friend.id === Number(id))
        const friendJson = JSON.stringify(friend) 
        res.writeHead(200, {'Content-Type': 'text/json'})
        res.end(friendJson)
    }else if (pathName === '/mylove'){
        res.writeHead(200, {'Content-Type': 'text/html'})
        res.end('<h1>This is my Chouwtouille page <3</h1>')
    }else if (pathName === '/api/mylove') {
        res.writeHead(200, {'Content-Type': 'text/json'})
        res.end(myloveJson)
    } else if (pathName === '/') {
        res.writeHead(200, {'Content-Type': 'text/html'})
        res.end('<h1>This is the server root page</h1>')
    } else {
        res.writeHead(404, {'Content-type': 'text/html'})
        res.end('<h1>Page not found</h1>')
    }
    // Send response to the client
})



// Convert JS array to JSON

// Setup the port and the host
const port = 8000;
const host = '127.0.0.1';
server.listen(port, host, () => {
    console.log(`Server listening on port ${port} on host ${host}`);
});