import time as dt
from futuquant.examples.emailplugin import EmailNotification
import socket

hostName = socket.gethostname()
print(hostName)

ts = dt.localtime()
print(ts)

EmailNotification.set_enable(True)
EmailNotification.send_email('49072565@qq.com', 'test', 'hahahaha')