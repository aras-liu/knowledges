ORDER_BUY = 1
ORDER_SELL = 0

TRADETP_BUY = 1
TRADETP_SELL = 0

ACC = "affc7f63-0c04-438f-884e-e1e709f01182"
SEC = "4975b909-0628-4136-8598-942a2bd13067"

STATUS_ORDER_CONCEL = 1
STATUS_ORDER_DONE = 2
STATUS_ORDER_DOING = 3

ENV = 'test'

# 当前购买和卖出限额
XIANE = 2000

# 比较比例
BILI = 0.003


standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]' #其中name为getlogger指定的名字
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'
# diy_format = '%d{yyyy-MM-dd} [%thread] %-5level %logger{50} -%msg%n'
diy_format = '[%(asctime)s %(levelname)s] [%(filename)s:%(lineno)d] : %(message)s'

LOGGING_DIC = {
    'version': 1,  # 版本号
    'disable_existing_loggers': False,  #　固定写法
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': diy_format
        },
    },
    'filters': {},
    'handlers': {
        #打印到终端的日志
        'sh': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        # #打印到文件的日志,收集info及以上的日志
        # 'fh': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
        #     'formatter': 'standard',
        #     'filename': 'log1.log',  # 日志文件
        #     'maxBytes': 300,  # 日志大小 300字节
        #     'backupCount': 5,  # 轮转文件的个数
        #     'encoding': 'utf-8',  # 日志文件的编码
        # },
    },
    'loggers': {
        #logging.getLogger(__name__)拿到的logger配置
        '': {
            # 'handlers': ['sh', 'fh'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'handlers': ['sh'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'INFO',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}
