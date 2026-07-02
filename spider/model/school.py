"""
高校数据模型
"""
from dataclasses import dataclass
from typing import Optional

from model.base import BaseModel


@dataclass
class School(BaseModel):
    """高校数据模型"""

    name: Optional[str] = None
    code: Optional[str] = None
    province_id: Optional[int] = None
    city_id: Optional[int] = None
    address: Optional[str] = None
    type: Optional[int] = None  # 类型：1-综合，2-理工，3-师范...
    level: Optional[int] = None  # 层次：1-本科，2-专科
    nature: Optional[int] = None  # 性质：1-公办，2-民办，3-中外合作
    is_985: Optional[int] = 0
    is_211: Optional[int] = 0
    is_double_first_class: Optional[int] = 0
    website: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    ranking: Optional[int] = None
    student_count: Optional[int] = None
    faculty_count: Optional[int] = None
    status: Optional[int] = 1

    # 爬虫扩展字段（不入库）
    province_name: Optional[str] = None
    city_name: Optional[str] = None
