##############################################################################
# Copyright (c) 2009-2013 Hajime Nakagami<nakagami@gmail.com>
# All rights reserved.
# Licensed under the New BSD License
# (http://www.freebsd.org/copyright/freebsd-license.html)
#
# Python DB-API 2.0 module for Firebird. 
##############################################################################
import os
import socket
import select

try:
    import fcntl
except ImportError:
    def setcloexec(sock):
        pass
else:
    def setcloexec(sock):
        """Set FD_CLOEXEC property on a file descriptors
        """
        fd = sock.fileno()
        flags = fcntl.fcntl(fd, fcntl.F_GETFD)
        fcntl.fcntl(fd, fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)

class SocketStream(object):
    def __init__(self, host, port, timeout=None, cloexec=False):
        self.timeout = timeout
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if cloexec:
            setcloexec(self._sock)
        self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._sock.connect((host, port))

    def recv(self, nbytes):
        return self._sock.recv(nbytes)

    def send(self, b):
        n = 0
        while (n < len(b)):
            n += self._sock.send(b[n:])

    def close(self):
        self._sock.close()