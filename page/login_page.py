from po.login import Login_Object as lo
from utils.feishu_bot import FeishuBot as fb
from utils.api_listen import listen_for_graphql_response as grpc



class Login_Page:
    def __init__(self, page):
        self.page = page

    def navigate_to_login_page(self):

        # Fill [placeholder="请输入账号"]
        self.page.fill(lo.login_phone_input, "aaa")

        self.page.fill(lo.login_password_input, "bbb")
        self.page.click(lo.login_checkbox)
        self.page.click(lo.login_button)
        resp = grpc(self.page, "graphql", "refreshUserData")
        token = resp["data"]["refreshUserData"]["token"]
        try:
            assert 'login' not in self.page.url
        except AssertionError as e:
            fb(webhook="https://open.feishu.cn/open-apis/bot/v2/hook/example_webhook_token").send_text("登录失败")
            print(e)
