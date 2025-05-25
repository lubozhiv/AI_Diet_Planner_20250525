## The ASGI asynchronous function handles requests using scope, receive, and send:
async def asgi_app(scope, receive, send):
    # Check that the request type is HTTP
    assert scope['type'] == 'http'
    # Receive the incoming request
    request = await receive()
    # Send the start of the HTTP response with a 200 status and content-type header
    await send({
        'type': 'http.response.start',
        # Status code for successful request
        'status': 200,
        'headers': [
            # Content type is plain text
            [b'content-type', b'text/plain'],
        ],
    })
    # Send the body of the HTTP response with a simple text message
    await send({
        'type': 'http.response.body',
        # Response message in byte format
        'body': b'Hello, ASGI!',
    })