import unittest
import socket
from bertha2 import chat


class TestChat(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):

        # Not sre if these do anything
        cls.web_socket = None
        cls.channel = None

    def tearDown(self):
        pass

    def test_login(self):

        self.web_socket = socket.socket()
        chat.login(self.web_socket)

    def test_send_privmsg(self):
        web_socket = socket.socket()
        chat.login(web_socket)
        # Send a basic message
        chat.send_privmsg(web_socket, "Test", "berthatwo")

        # Send messages with garbage input
        chat.send_privmsg(web_socket, "Test", "berthatwo")

    def test_parse_privmsg(self):
        # TODO
        pass


unittest.main()