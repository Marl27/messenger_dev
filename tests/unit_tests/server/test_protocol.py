import pytest

from server.protocol import Protocol
from employee import Employee


class TestProtocol:
    @pytest.fixture
    def protocol_login(self):
        return Protocol.LOGIN

    @pytest.fixture
    def protocol_logout(self):
        return Protocol.LOGOUT

    @pytest.fixture
    def protocol_register(self):
        return Protocol.REGISTER

    @pytest.fixture
    def protocol_read(self):
        return Protocol.READ

    @pytest.fixture
    def protocol_write(self):
        return Protocol.WRITE

    @pytest.fixture
    def protocol_request(self):
        # Do we want request or request.value?
        return Protocol.REQUEST.value

    @pytest.fixture
    def protocol_response(self):
        # Do we want request or request.value?
        return Protocol.RESPONSE.value

    @pytest.fixture
    def username(self):
        return "test_username"

    @pytest.fixture
    def password(self):
        return "test_password"

    @pytest.fixture
    def employee(self, username, password):
        return Employee(
            first_name="test_first_name",
            middle_name="test_middle_name",
            last_name="test_last_name",
            username=username,
            password=password,
            start_date="01/01/2022",
            leaving_date="01/01/2023")

    @pytest.fixture
    def login_packet(self, username, password):
        return {"code": "LOGIN",
                "direction": Protocol.REQUEST.value,
                "username": username,
                "password": password}

    @pytest.fixture
    def logout_packet(self, username):
        return {"code": "LOGOUT",
                "direction": Protocol.REQUEST.value,
                "username": username}

    @pytest.fixture
    def register_packet(self, employee):
        return {"code": "REGISTER",
                "direction": Protocol.REQUEST.value,
                "username": employee.username,
                "password": employee.password,
                "first_name": employee.first_name,
                "middle_name": employee.middle_name,
                "last_name": employee.last_name,
                "start_date": employee.start_date,
                "leaving_date": employee.leaving_date}

    def test_build_request_login(self, protocol_login, username, password, login_packet):
        actual = Protocol.build_request(protocol_login, username=username, password=password)
        assert actual == login_packet

    def test_build_request_logout(self, protocol_logout, username, logout_packet):
        actual = Protocol.build_request(protocol_logout, username=username)
        assert actual == logout_packet

    def test_build_request_register(self, employee, protocol_register, register_packet):
        actual = Protocol.build_request(protocol_register, employee=employee)
        assert actual == register_packet

    def test_build_request_read(self):
        assert True

    def test_build_request_write(self):
        assert True
