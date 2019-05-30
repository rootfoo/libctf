import socket
import select
import sys
from data import hexdump
import ansi 

class Sock(object):

    """
    wrapper for a socket that's smart
    functions for pretty printing the dialog
    read_until_string
    read_all (for slow connections)
    """
    def __init__(self, host, port, verbose=True, timeout=.1, newline='', color=True):
        socket.setdefaulttimeout(timeout)
	# supports ipv4 and ipv6
        self.socket = socket.create_connection((host,port))
        self._timeout = timeout
        self._host = host
        self._port = port
        self._tail = ""
        self._recv_color = ansi.ANSI_F_CYAN if color else ''
        self._send_color = ansi.ANSI_F_MAGENTA if color else ''
        self.history = []
        self.verbose = verbose
        self.newline = newline


    def recv(self, count=None, timeout=None):
        """Alias for read()"""
        return self.read(count)


    def read(self, count=None, timeout=None):
        """read up to count bytes, if specified, otherwise read all data available"""
        if timeout:
            # set timeout for this request
            self.socket.settimeout(timeout)
        data = self._tail
        if count:
            data = self._read(count)
        else:
            data = self._readall()
        if self.verbose:
            sys.stdout.write(self._recv_color + data + ansi.ANSI_ENDC)
            #print hexdump(data)

        # reset timeout, append to history, truncate tail
        self.socket.settimeout(self._timeout)
        self.history.append(('>',data))
        self._tail = ''
        
        return data


    def _read(self, count=4096):
        data = ''
        try:
            data = self.socket.recv(count)

        except socket.timeout:
            # timeout doesn't necesarily mean the connection is closed
            pass

        return data

    def _readall(self):
        # read all data from sock
        data = ""
        chunk = ""
        flag = True
        while flag:
            try:
                chunk = self.socket.recv(1024)
            except socket.timeout:
                chunk = ""
            finally:
                if len(chunk) > 0:
                    data += chunk
                    chunk = ""
                else:
                    flag = False

        return data


    def recvuntil(self, premark, postmark="\n"):
        """
        Read until premark in mesg. Return string between premark and postmark.
        TODO: add support for regex
        """
        # self._tail caches data read but not yet returned. May be part of next read
        while not premark in self._tail:
            self._tail += self._readall()

        start = self._tail.find(premark) + len(premark)
        end = self._tail.find(postmark, start)
        sub = self._tail[start:end]
        self._tail = self._tail[end:]

        return sub


    def send(self, data):
        """alias for write()"""
        self.write(data)


    def sendline(self, data):
        """write(data + "\n")"""
        self.write(data, newline="\n")


    def sr(self, data=''):
        """send(data) && return recv()"""
        if data:
            self.write(data)
        return self.read()


    def write(self, data, newline=''):
        newline = newline or self.newline
        try:
            data += newline
            self.socket.send(data)
            self.history.append(('<',data))

            if self.verbose:
                sys.stdout.write(self._send_color + data + ansi.ANSI_ENDC)
                #print hexdump(data)

            return data

        except Exception as e:
            self.socket.close()
            self._closed = True


    def close(self):
        self.socket.close()

    def reconnect(self):
        self.socket.close()
        self.socket = socket.socket(self._family, self._stype)
        self.socket.settimeout(2)
        self.socket.connect((self._host,self._port))


    def interact(self, newline="\n"):

        while True:
            try:
                # It would be nice to have a prompt, but it's tricky to add
                #sys.stdout.write('$> ')
                #sys.stdout.flush()

                # Wait for input from stdin & socket
                input_ready,output_ready,except_ready = select.select([sys.stdin, self.socket], [],[])

                # loop over the file handles with input
                for i in input_ready:
                    if i == sys.stdin:
                        data = sys.stdin.readline()
                        # patch up newlines
                        if not data.endswith(newline):
                            data = data.strip('\n') + newline

                        if data:
                            self.history.append(('<', data))
                            self.socket.send(data)
                    elif i == self.socket:
                        data = self.socket.recv(1024)
                        if data:
                            self.history.append(('>', data))
                            sys.stdout.write(data)
                            sys.stdout.flush()

            except KeyboardInterrupt:
                break

            except socket.error as msg:
                print msg
                break





