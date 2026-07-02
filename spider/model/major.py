"""
专业数据模型
"""
from dataclasses import dataclass
from typing import Optional

from model.base import BaseModel


@dataclass
class Major(BaseModel):
    """专业数据模型"""

    name: Optional[str] = None
    code: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    subject_requirements: Optional[str] = None
    duration: Optional[int] = None  # 学制：3-三年，4-四年，5-五年
    degree: Optional[str] = None
    description: Optional[str] = None
    employment_direction: Optional[str] = None
    salary_range: Optional[str] = None
    is_special: Optional[int] = 0
    status: Optional[int] = 1
