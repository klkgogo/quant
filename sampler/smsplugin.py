from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import time
import socket

class Sms(object):
    appid = 1400122245
    appkey = "0084d3708511c5417f65bec77502ba0f"
    phone_numbers = 18948188140

    START_SAMPLE_ID = 169496        #{1}开始{2}数据采集，{3}
    EXCEPTION_ID = 169500           # {1}采集{2}结束，orderbook:{3}, ticker:{4}，{5}
    END_SAMPLE_ID = 169499          # {1}采集{2}，异常{3}，{4}

    @staticmethod
    def send(template_id, params):
        ssender = SmsSingleSender(Sms.appid, Sms.appkey)
        try:
            result = ssender.send_with_param(86, Sms.phone_numbers,
                                             template_id, params)
        except HTTPError as e:
            print(e)
        except Exception as e:
            print(e)
        print(result)

    @staticmethod
    def send_start_sample():
        params = [socket.gethostname()[:12], "",  time.ctime()[11:20]]
        Sms.send(Sms.START_SAMPLE_ID, params)

    @staticmethod
    def send_end_sample(orderbook_count, ticker_count):
        params = [socket.gethostname()[:12], "", orderbook_count, ticker_count,  time.ctime()[11:20]]
        Sms.send(Sms.END_SAMPLE_ID, params)

    @staticmethod
    def send_exception(e):
        params = [socket.gethostname()[:12], "", e[:12], time.ctime()[11:20]]
        Sms.send(Sms.EXCEPTION_ID, params)


if __name__ == '__main__':
    Sms.send_end_sample(1231232, 2323)
    a = "1323"
    print(time.ctime()[11:20])
    print(socket.gethostname())


