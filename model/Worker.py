class Worker(object):
    def __init__(self, address=None, port=None):
        self.address = address
        self.port = port

    def set_address(self, address):
        self.address = address

    def set_port(self, port):
        self.port = port
