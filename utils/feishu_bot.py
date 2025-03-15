import requests
import json
import logging
import time
import urllib
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def is_not_null_and_blank(s):
    """
    Check if a string is not null and not blank
    :param s:
    :return:
    """
    if s or s.strip():
        return True
    else:
        return False


class FeishuBot:
    def __init__(self, webhook, secret=None, pc_slide=False, fail_notice=False):
        super().__init__()
        self.webhook = webhook
        self.secret = secret
        self.pc_slide = pc_slide
        self.fail_notice = fail_notice
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}

    def send_text(self, msg, at_mobiles=None, at_all=False):
        data = {
            "msg_type": "text",
            "at": {
                "atMobiles": at_mobiles,
                "isAtAll": at_all
            }
        }
        if is_not_null_and_blank(msg):
            data["content"] = {"text": msg}
        else:
            logging.warning("Message is empty, not sending.")
            raise ValueError("Message is empty, not sending.")
        logging.debug('text data: %s' % data)
        return self.post(data)

    def post(self, data):
        """

        :param data: dict
        :return: the result of requests.post
        """
        try:
            post_data = json.dumps(data)
            resp = requests.post(self.webhook, data=post_data, headers=self.headers, verify=False)
        except requests.exceptions.HTTPError as e:
            logging.error("HTTP Error: %d,Reason: %s" % (e.response.status_code, e.response.reason))
            raise
        except requests.exceptions.ConnectionError as e:
            logging.error("Error Connecting: %s" % e)
            raise
        except requests.exceptions.Timeout as e:
            logging.error("Timeout Error")
            raise
        except requests.exceptions.RequestException as e:
            logging.error("Something went wrong")
            raise
        else:
            try:
                result = resp.json()
            except json.JSONDecodeError:
                logging.error("Invalid JSON response: %s" % resp.text)
                return {'errorCode': 500, 'errMsg': 'server error'}
            else:
                logging.debug("Feishu Bot Response: %s" % result)
                if self.fail_notice and result.get('errorCode', True):
                    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    error_data = {
                        "msg_type": "text",
                        "text": {
                            "content": f"Feishu Bot Error: {result['errMsg'] if result.get('errMsg', False) else 'unknown error'}\nTime: {time_now}"
                        },
                        "at": {
                            "isAtAll": False
                        }
                    }
                    logging.error("Feishu Bot Error: %s" % result['errMsg'])
                    requests.post(self.webhook, headers=self.headers, data=json.dumps(error_data), verify=False)
                return result


if __name__ == '__main__':
    webhook = 'https://open.feishu.cn/open-apis/bot/v2/hook/example'
    bot = FeishuBot(webhook)
    bot.send_text('Hello, Feishu Bot!')
