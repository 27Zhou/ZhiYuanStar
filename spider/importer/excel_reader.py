"""
Excel文件读取器
"""
from pathlib import Path
from typing import List, Dict, Any, Optional

from utils.logger import logger


class ExcelReader:
    """Excel文件读取器"""

    def read(self, file_path: str, sheet_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        读取Excel文件

        Args:
            file_path: 文件路径
            sheet_name: 工作表名称，None表示读取第一个

        Returns:
            数据列表
        """
        path = Path(file_path)
        if not path.exists():
            logger.error(f"Excel文件不存在: {file_path}")
            return []

        try:
            import pandas as pd

            # 读取Excel
            df = pd.read_excel(
                path,
                sheet_name=sheet_name or 0,
                dtype=str,  # 全部作为字符串读取
                na_values=["", "NA", "N/A", "null", "NULL", "-"],
            )

            # 转换为字典列表
            data = df.to_dict("records")

            # 过滤空行
            data = [
                {k: v for k, v in row.items() if pd.notna(v)}
                for row in data
                if any(pd.notna(v) for v in row.values())
            ]

            logger.info(f"读取Excel文件: {path.name}，共 {len(data)} 条数据")
            return data

        except ImportError:
            logger.error("缺少pandas和openpyxl库，请执行: pip install pandas openpyxl")
            return []
        except Exception as e:
            logger.error(f"读取Excel文件失败: {file_path} - {e}")
            return []

    def read_all_sheets(self, file_path: str) -> List[Dict[str, Any]]:
        """
        读取Excel文件的所有工作表

        Args:
            file_path: 文件路径

        Returns:
            数据列表
        """
        path = Path(file_path)
        if not path.exists():
            return []

        try:
            import pandas as pd

            all_data = []
            xls = pd.ExcelFile(path)

            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)
                data = df.to_dict("records")
                data = [
                    {k: v for k, v in row.items() if pd.notna(v)}
                    for row in data
                    if any(pd.notna(v) for v in row.values())
                ]
                all_data.extend(data)

            logger.info(f"读取Excel所有工作表: {path.name}，共 {len(all_data)} 条数据")
            return all_data

        except Exception as e:
            logger.error(f"读取Excel文件失败: {file_path} - {e}")
            return []

    def scan_directory(self, dir_path: str) -> List[str]:
        """
        扫描目录下的所有Excel文件

        Args:
            dir_path: 目录路径

        Returns:
            文件路径列表
        """
        path = Path(dir_path)
        if not path.exists():
            return []

        files = []
        for ext in ["*.xlsx", "*.xls", "*.XLSX", "*.XLS"]:
            files.extend(str(f) for f in path.glob(ext))

        logger.info(f"扫描目录 {dir_path}，找到 {len(files)} 个Excel文件")
        return sorted(files)
