"""
智选未来 - 爬虫主入口
"""
import sys
import io
import argparse
from pathlib import Path

# Windows终端UTF-8支持
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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


def run_school():
    """运行高校数据采集"""
    from crawler.school_crawler import SchoolCrawler

    logger.info("启动高校数据采集任务...")
    crawler = SchoolCrawler()

    try:
        data = crawler.start()
        logger.info(f"高校数据采集完成，共获取 {len(data)} 所高校")
    except Exception as e:
        logger.error(f"高校数据采集失败: {e}")
    finally:
        crawler.cleanup()


def run_major():
    """运行专业数据采集"""
    from crawler.major_crawler import MajorCrawler

    logger.info("启动专业数据采集任务...")
    crawler = MajorCrawler()

    try:
        data = crawler.start()
        logger.info(f"专业数据采集完成，共获取 {len(data)} 个专业")
    except Exception as e:
        logger.error(f"专业数据采集失败: {e}")
    finally:
        crawler.cleanup()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="智选未来 - 高考数据爬虫系统")
    parser.add_argument(
        "task",
        choices=["school", "major", "score", "all"],
        help="采集任务: school=高校, major=专业, score=录取分数, all=全部",
    )
    parser.add_argument(
        "--check-env",
        action="store_true",
        help="仅检查环境，不执行采集",
    )

    args = parser.parse_args()

    check_environment()

    if args.check_env:
        logger.info("环境检查完成")
        return

    if args.task == "school":
        run_school()
    elif args.task == "major":
        run_major()
    elif args.task == "score":
        logger.info("录取分数采集模块待开发...")
    elif args.task == "all":
        run_school()
        run_major()
        logger.info("录取分数采集模块待开发...")


if __name__ == "__main__":
    main()
