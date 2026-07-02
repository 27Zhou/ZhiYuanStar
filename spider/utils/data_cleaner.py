"""
数据清洗模块
提供数据清洗和转换功能
"""
import re
from typing import Any, Optional
from datetime import datetime

from utils.logger import logger


class DataCleaner:
    """数据清洗器"""

    @staticmethod
    def clean_string(value: Any) -> Optional[str]:
        """清洗字符串"""
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        value = value.strip()
        value = re.sub(r'\s+', ' ', value)
        value = value.replace('\n', '').replace('\r', '').replace('\t', '')
        return value if value else None

    @staticmethod
    def clean_integer(value: Any) -> Optional[int]:
        """清洗整数"""
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str):
            value = value.replace(',', '').replace(' ', '')
            match = re.search(r'-?\d+', value)
            if match:
                return int(match.group())
        return None

    @staticmethod
    def clean_float(value: Any) -> Optional[float]:
        """清洗浮点数"""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            value = value.replace(',', '').replace(' ', '')
            match = re.search(r'-?\d+\.?\d*', value)
            if match:
                return float(match.group())
        return None

    @staticmethod
    def clean_phone(value: Any) -> Optional[str]:
        """清洗手机号"""
        if value is None:
            return None
        value = str(value).strip()
        match = re.search(r'1[3-9]\d{9}', value)
        if match:
            return match.group()
        return None

    @staticmethod
    def clean_email(value: Any) -> Optional[str]:
        """清洗邮箱"""
        if value is None:
            return None
        value = str(value).strip().lower()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, value):
            return value
        return None

    @staticmethod
    def clean_date(value: Any, fmt: str = '%Y-%m-%d') -> Optional[datetime]:
        """清洗日期"""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            value = value.strip()
            formats = [
                '%Y-%m-%d', '%Y/%m/%d', '%Y年%m月%d日',
                '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S',
            ]
            for f in formats:
                try:
                    return datetime.strptime(value, f)
                except ValueError:
                    continue
        return None

    @staticmethod
    def clean_score(value: Any) -> Optional[int]:
        """清洗高考分数（0-750）"""
        score = DataCleaner.clean_integer(value)
        if score is not None and 0 <= score <= 750:
            return score
        return None

    @staticmethod
    def clean_ranking(value: Any) -> Optional[int]:
        """清洗排名/位次"""
        ranking = DataCleaner.clean_integer(value)
        if ranking is not None and ranking > 0:
            return ranking
        return None

    @staticmethod
    def clean_year(value: Any) -> Optional[int]:
        """清洗年份"""
        year = DataCleaner.clean_integer(value)
        if year is not None and 1900 <= year <= 2100:
            return year
        return None

    @staticmethod
    def clean_url(value: Any) -> Optional[str]:
        """清洗URL"""
        if value is None:
            return None
        value = str(value).strip()
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if re.match(pattern, value, re.IGNORECASE):
            return value
        return None

    @staticmethod
    def clean_province(value: Any) -> Optional[str]:
        """清洗省份名称（标准化）"""
        if value is None:
            return None
        value = str(value).strip()

        province_mapping = {
            '京': '北京市', '津': '天津市', '冀': '河北省', '晋': '山西省',
            '蒙': '内蒙古自治区', '辽': '辽宁省', '吉': '吉林省', '黑': '黑龙江省',
            '沪': '上海市', '苏': '江苏省', '浙': '浙江省', '皖': '安徽省',
            '闽': '福建省', '赣': '江西省', '鲁': '山东省', '豫': '河南省',
            '鄂': '湖北省', '湘': '湖南省', '粤': '广东省', '桂': '广西壮族自治区',
            '琼': '海南省', '渝': '重庆市', '川': '四川省', '黔': '贵州省',
            '滇': '云南省', '藏': '西藏自治区', '陕': '陕西省', '甘': '甘肃省',
            '青': '青海省', '宁': '宁夏回族自治区', '疆': '新疆维吾尔自治区',
        }

        if value in province_mapping:
            return province_mapping[value]

        for short, full in province_mapping.items():
            if short in value or full in value:
                return full

        return value


# 全局实例
data_cleaner = DataCleaner()
