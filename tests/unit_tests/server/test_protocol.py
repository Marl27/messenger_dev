import pytest

from server.protocol import Protocol


class TestProtocol:
    @pytest.fixture
    def protocol_login(self):
        return Protocol.LOGIN

    @pytest.fixture()
    def username(self):
        return "test_username"

    @pytest.fixture()
    def password(self):
        return "test_password"

    @pytest.fixture()
    def login_packet(self, username, password):
        return {"code": "LOGIN",
                "username": username,
                "password": password}

    def test_build_request_login(self, protocol_login, username, password, login_packet):
        actual = Protocol.build_request(protocol_login, username=username, password=password)
        assert actual == login_packet

    def test_build_request_logout(self):
        assert True

    def test_build_request_register(self):
        assert True

    def test_build_request_read(self):
        assert True

    def test_build_request_write(self):
        assert True
