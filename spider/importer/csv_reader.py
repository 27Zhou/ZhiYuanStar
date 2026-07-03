"""
CSV文件读取器
"""
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional

from utils.logger import logger


class CSVReader:
    """CSV文件读取器"""

    def read(self, file_path: str, encoding: str = "utf-8") -> List[Dict[str, Any]]:
        """
        读取CSV文件

        Args:
            file_path: 文件路径
            encoding: 文件编码

        Returns:
            数据列表
        """
        path = Path(file_path)
        if not path.exists():
            logger.error(f"CSV文件不存在: {file_path}")
            return []

        try:
            data = []
            with open(path, "r", encoding=encoding, errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # 过滤空行
                    if any(v.strip() for v in row.values() if v):
                        data.append(dict(row))

            logger.info(f"读取CSV文件: {path.name}，共 {len(data)} 条数据")
            return data

        except Exception as e:
            logger.error(f"读取CSV文件失败: {file_path} - {e}")
            return []

    def read_with_fallback(self, file_path: str) -> List[Dict[str, Any]]:
        """
        读取CSV文件（自动尝试多种编码）

        Args:
            file_path: 文件路径

        Returns:
            数据列表
        """
        encodings = ["utf-8", "utf-8-sig", "gbk", "gb2312", "gb18030", "latin1"]

        for encoding in encodings:
            try:
                data = self.read(file_path, encoding=encoding)
                if data:
                    return data
            except Exception:
                continue

        logger.error(f"无法读取CSV文件（所有编码均失败）: {file_path}")
        return []

    def scan_directory(self, dir_path: str) -> List[str]:
        """
        扫描目录下的所有CSV文件

        Args:
            dir_path: 目录路径

        Returns:
            文件路径列表
        """
        path = Path(dir_path)
        if not path.exists():
            return []

        files = []
        for ext in ["*.csv", "*.CSV"]:
            files.extend(str(f) for f in path.glob(ext))

        logger.info(f"扫描目录 {dir_path}，找到 {len(files)} 个CSV文件")
        return sorted(files)
