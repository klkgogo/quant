from util.log import *
from os.path import expanduser


filePath = '~/vt_' + datetime.now().strftime('%Y%m%d') + '.log'
filePath = expanduser(filePath)
print(filePath)
logger = LogEngine()
logger.setLogLevel(LogEngine.LEVEL_DEBUG)
logger.addConsoleHandler()
logger.addFileHandler(filePath=filePath)

logger.debug("hello world")

# print("hello")