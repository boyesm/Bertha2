import time
import unittest
import socket
import src.input.chat


class TestChat(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.web_socket = socket.socket()
        src.input.chat.login(cls.web_socket)
        cls.channel = "bertha2"

        print("Running")

    def tearDown(self):
        pass




    def test_send_privmsg(self):

        # Send a basic message
        src.input.chat.send_privmsg(self.web_socket, "Test", self.channel)

        # Send messages with garbage input
        src.input.chat.send_privmsg(self.web_socket, "Test", self.channel)

    def test_parse_privmsg(self):
        # TODO
        pass

    def test_

if __name__ == '__main__':
    unittest.main()