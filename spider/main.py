"""
智选未来 - ETL数据导入系统
支持从CSV/Excel/JSON文件批量导入数据到MySQL
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
from importer.csv_reader import CSVReader
from importer.excel_reader import ExcelReader
from importer.json_reader import JSONReader
from importer.batch_import import batch_importer, ImportResult


def scan_files(data_dir: str) -> list:
    """
    扫描目录下的所有数据文件

    Args:
        data_dir: 数据目录

    Returns:
        文件路径列表
    """
    csv_reader = CSVReader()
    excel_reader = ExcelReader()
    json_reader = JSONReader()

    files = []
    files.extend(csv_reader.scan_directory(data_dir))
    files.extend(excel_reader.scan_directory(data_dir))
    files.extend(json_reader.scan_directory(data_dir))

    return files


def read_file(file_path: str) -> list:
    """
    读取单个文件

    Args:
        file_path: 文件路径

    Returns:
        数据列表
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        csv_reader = CSVReader()
        return csv_reader.read_with_fallback(file_path)
    elif suffix in (".xlsx", ".xls"):
        excel_reader = ExcelReader()
        return excel_reader.read(file_path)
    elif suffix == ".json":
        json_reader = JSONReader()
        return json_reader.read(file_path)
    else:
        logger.warning(f"不支持的文件格式: {suffix}")
        return []


def print_result(task: str, result: ImportResult):
    """
    打印导入结果

    Args:
        task: 任务名称
        result: 导入结果
    """
    print()
    print("=" * 50)
    print(f"📊 {task} 数据导入结果")
    print("=" * 50)
    print(f"📂 读取文件数量: {result.files_read}")
    print(f"✅ 解析成功数量: {result.parsed}")
    print(f"💾 插入数据库数量: {result.inserted}")
    print(f"🔁 重复数量: {result.duplicated}")
    print(f"❌ 失败数量: {result.failed}")
    print("=" * 50)

    if result.errors:
        print(f"\n⚠️ 前10条错误信息:")
        for error in result.errors[:10]:
            print(f"   - {error}")


def run_import(task: str, data_dir: str, table: str):
    """
    执行数据导入

    Args:
        task: 任务名称
        data_dir: 数据目录
        table: 目标表名
    """
    result = ImportResult()

    # 扫描文件
    files = scan_files(data_dir)
    result.files_read = len(files)

    if not files:
        logger.warning(f"未找到数据文件: {data_dir}")
        print_result(task, result)
        return

    logger.info(f"找到 {len(files)} 个数据文件")

    # 读取所有文件数据
    all_data = []
    for file_path in files:
        try:
            data = read_file(file_path)
            all_data.extend(data)
            logger.info(f"读取文件: {Path(file_path).name} -> {len(data)} 条")
        except Exception as e:
            logger.error(f"读取文件失败: {file_path} - {e}")
            result.errors.append(f"读取失败: {Path(file_path).name}")

    result.parsed = len(all_data)

    if not all_data:
        logger.warning("未读取到任何数据")
        print_result(task, result)
        return

    logger.info(f"共读取 {len(all_data)} 条数据，开始导入...")

    # 执行导入
    import_result = batch_importer.import_data(all_data, table)

    # 合并结果
    result.inserted = import_result.inserted
    result.duplicated = import_result.duplicated
    result.failed = import_result.failed
    result.errors.extend(import_result.errors)

    # 打印结果
    print_result(task, result)


def run_school():
    """导入学校数据"""
    data_dir = str(config.project_root / "data" / "school")
    run_import("学校", data_dir, "school")


def run_major():
    """导入专业数据"""
    data_dir = str(config.project_root / "data" / "major")
    run_import("专业", data_dir, "major")


def run_admission():
    """导入录取数据"""
    data_dir = str(config.project_root / "data" / "admission")
    run_import("录取", data_dir, "admission_score")


def run_plan():
    """导入招生计划数据"""
    data_dir = str(config.project_root / "data" / "plan")
    run_import("招生计划", data_dir, "enrollment_plan")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="智选未来 - ETL数据导入系统")
    parser.add_argument(
        "task",
        choices=["school", "major", "admission", "plan"],
        help="导入任务: school=学校, major=专业, admission=录取, plan=招生计划",
    )
    parser.add_argument(
        "--check-env",
        action="store_true",
        help="仅检查环境，不执行导入",
    )

    args = parser.parse_args()

    if args.check_env:
        print(f"数据库: {config.database.host}:{config.database.port}/{config.database.database}")
        print(f"数据目录: {config.data_dir}")
        return

    if args.task == "school":
        run_school()
    elif args.task == "major":
        run_major()
    elif args.task == "admission":
        run_admission()
    elif args.task == "plan":
        run_plan()


if __name__ == "__main__":
    main()
