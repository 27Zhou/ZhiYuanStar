"""
JSON文件读取器
"""
import json
from pathlib import Path
from typing import List, Dict, Any

from utils.logger import logger


class JSONReader:
    """JSON文件读取器"""

    def read(self, file_path: str) -> List[Dict[str, Any]]:
        """
        读取JSON文件

        Args:
            file_path: 文件路径

        Returns:
            数据列表
        """
        path = Path(file_path)
        if not path.exists():
            logger.error(f"JSON文件不存在: {file_path}")
            return []

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 如果是字典，尝试提取data字段
            if isinstance(data, dict):
                data = data.get("data", data.get("list", [data]))

            # 确保是列表
            if not isinstance(data, list):
                data = [data]

            logger.info(f"读取JSON文件: {path.name}，共 {len(data)} 条数据")
            return data

        except Exception as e:
            logger.error(f"读取JSON文件失败: {file_path} - {e}")
            return []

    def scan_directory(self, dir_path: str) -> List[str]:
        """
        扫描目录下的所有JSON文件

        Args:
            dir_path: 目录路径

        Returns:
            文件路径列表
        """
        path = Path(dir_path)
        if not path.exists():
            return []

        files = []
        for ext in ["*.json", "*.JSON"]:
            files.extend(str(f) for f in path.glob(ext))

        logger.info(f"扫描目录 {dir_path}，找到 {len(files)} 个JSON文件")
        return sorted(files)
