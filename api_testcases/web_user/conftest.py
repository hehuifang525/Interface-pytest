import pytest

from .login.Login.test_cases import common_login
from .login.Logout.test_cases import common_logout


@pytest.fixture(scope="module", autouse=True)
def user_login_logout_fixture():
    """
    web-user常规登录接口
    """
    common_login()  # 登录
    yield
    common_logout()  # 登出
