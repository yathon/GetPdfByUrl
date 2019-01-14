
MAX_PAGE = -1  # 需要下载的页数，-1为下载全部(自动获取最大页数)
ONE_PAGE_WAIT = 300  # 每页最大等待下载时间，单位秒
TIME_COST_TYPE = None  # 打印函数执行耗时，None-忽略，'usec'-微秒，'msec'-毫秒，'sec'-秒，'min'-分钟
ESC_TITLE = True  # 标题作为文件名时是否转义非法字符（兼容Windows系统必须开启）
FORBID_CHAR = r' /\:*"<>|?'
RETRY_CNT = 1  # 重试次数
