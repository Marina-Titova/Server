import asyncio


def form_string_from_one_key(d, key):
    str = ''
    for k in d[key]:
        str += key + ' ' + k + '\n'
    return str

def form_string_from_all_keys(d):
    str = ''
    for key in d:
        str += form_string_from_one_key(d, key)
    return str

def process_data(data):
    data = data.split()
    if len(data) >= 2:
        cmd, key = data[0:2]
        val = data[2:]

        if cmd == 'put':
            if val:
                if key not in d:
                    d[key] = []
                if ' '.join(val) not in d[key]:
                    d[key].append(' '.join(val))
                str = 'ok\n\n'
            else:
                str = 'error\nempty key\n\n'

        elif cmd == 'get':
            if key == '*':
                str = 'ok\n' + form_string_from_all_keys(d) + '\n'
            elif key in d:
                str = 'ok\n' + form_string_from_one_key(d, key) + '\n'
            else:
                str = 'ok\n\n'
        else:
            str = 'error\nwrong command\n\n'
        return str

    else:
        return 'error\nto short request\n\n'


class ClientServerProtocol(asyncio.Protocol):

    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport


    def data_received(self, data):
        response = process_data(data.decode())
        self.transport.write(response.encode('utf8'))


if __name__== '__main__':

    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, '127.0.0.1', 8888)
    server = loop.run_until_complete(coro)

    d = {}
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
