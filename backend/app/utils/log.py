import logging
from logging.handlers import RotatingFileHandler
import sys

# 配置日志
def setup_logging():
    # 创建日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # 文件处理器（自动轮换）
    file_handler = RotatingFileHandler(
        "app.log", maxBytes=1024*1024*5, backupCount=3  # 5MB per file, 3 backups
    )
    file_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

t=setup_logging()
t.logger