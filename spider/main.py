"""
智选未来 - 爬虫主入口
"""
import sys
from pathlib import Path

# 将项目根目录加入Python路径
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import logger
from config.config import config


def check_environment():
    """检查运行环境"""
    logger.info("=" * 50)
    logger.info("智选未来 - 高考数据爬虫系统")
    logger.info("=" * 50)
    logger.info(f"项目根目录: {config.project_root}")
    logger.info(f"数据库: {config.database.host}:{config.database.port}/{config.database.database}")
    logger.info(f"日志目录: {config.log_dir}")
    logger.info(f"数据目录: {config.data_dir}")
    logger.info("=" * 50)


def main():
    """主函数"""
    check_environment()

    # TODO: 在此注册和启动爬虫任务
    #
    # 示例:
    # from crawler.school_crawler import SchoolCrawler
    # from pipeline.db_pipeline import db_pipeline
    #
    # crawler = SchoolCrawler()
    # data = crawler.start()
    # for item in data:
    #     db_pipeline.process(item, table="school")
    # db_pipeline.flush()

    logger.info("爬虫框架初始化完成，等待注册具体爬虫任务...")
    logger.info("提示: 请在 crawler/ 目录下创建具体爬虫类，继承 BaseCrawler")


if __name__ == "__main__":
    main()
