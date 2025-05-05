import logging

# 配置基础日志
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d]  - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # 输出到文件
        logging.StreamHandler()          # 输出到控制台
    ]
)

logger = logging.getLogger(__name__)