from util.log import *
from os.path import expanduser


filePath = '~/vt_' + datetime.now().strftime('%Y%m%d') + '.log'
filePath = expanduser(filePath)
print(filePath)
logger = LogEngine()
logger.setLogLevel(LogEngine.LEVEL_DEBUG)
logger.addConsoleHandler(level= LogEngine.LEVEL_INFO)
logger.addFileHandler(filePath=filePath, level=LogEngine.LEVEL_DEBUG)

logger.debug("hello world")

# print("hello")