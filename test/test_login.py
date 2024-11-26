import pytest
import requests


def catch_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            pytest.fail(f"函数{func.__name__}执行失败: {e}")

    return wrapper


# 表示模块级的fixture
@pytest.fixture(scope='module')
def login():
    tenant_id = 44211
    user_name = 'rcz'
    password = 111111
    # 设置移动设备（手机）绕过验证码登录
    header = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    url = 'http://110.185.163.49:22222/stage-api/auth/login'
    response = requests.post(url, json={"tenantId": tenant_id, "username": user_name, "password": password},
                             headers=header)
    if response.status_code != 200:
        pytest.fail('登录失败')
    return response.json()['data']['access_token']


# 测试登录
def test_login(login):
    # 断言 登录成功
    assert login is not None, '登录失败'


# 构建新的请求头，包含登录的token信息
@pytest.fixture(scope='module')
def parse_headers(login):
    headers = {
        'Authorization': 'Bearer ' + login
    }
    return headers


def test_get_user_info(parse_headers):
    url = 'http://110.185.163.49:22222/stage-api/employees/user/getInfo'
    response = requests.get(url, headers=parse_headers)
    assert response.json()['code'] == 200, '获取用户信息失败'


def test_get_routers(parse_headers):
    url = 'http://110.185.163.49:22222/stage-api/employees/menu/getRouters'
    response = requests.get(url, headers=parse_headers)
    assert response.json()['code'] == 200, '获取用户菜单失败'


def test_get_dict_info(parse_headers):
    url = 'http://110.185.163.49:22222/stage-api/employees/dict/data/type/ins_risk_level'
    response = requests.get(url, headers=parse_headers)
    assert response.json()['code'] == 200, '获取字典信息失败'


# 多个接口需要测试，并且请求参数类似,装饰器来参数化测试用例。
@pytest.mark.parametrize(
    'url,excepted_code', [
        ('http://110.185.163.49:22222/stage-api/ins/insConfig/listCommonAll', 200),
        ('http://110.185.163.49:22222/stage-api/ins/insConfig/listCommon', 200)
    ]
)
def test_api(url, excepted_code, parse_headers):
    response = requests.post(url, headers=parse_headers, json={})
    assert response.json()['code'] == excepted_code, f'{url}接口请求失败'
