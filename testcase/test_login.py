from page.login_page import Login_Page




def test_01_login(page, base_url):
    """
        名称：登录功能
        步骤：
        1、打开网页
        2、输入 账号密码
        3、点击登录
        检查点：
        * 登录后url不含login
    """
    login = Login_Page(page).navigate_to_login_page()
    print(f"{base_url}")
    page.goto(base_url)
    if 'login' in page.url:
        login(page)
