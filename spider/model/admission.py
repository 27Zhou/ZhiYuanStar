"""
录取分数线数据模型
"""
from dataclasses import dataclass
from typing import Optional

from model.base import BaseModel


@dataclass
class AdmissionScore(BaseModel):
    """录取分数线数据模型"""

    school_id: Optional[int] = None
    major_id: Optional[int] = None
    year: Optional[int] = None
    province_id: Optional[int] = None
    subject_type: Optional[int] = None  # 科类：1-文科，2-理科，3-综合改革
    batch: Optional[str] = None  # 批次
    min_score: Optional[int] = None
    max_score: Optional[int] = None
    avg_score: Optional[float] = None
    min_ranking: Optional[int] = None
    plan_count: Optional[int] = None
    enroll_count: Optional[int] = None

    # 爬虫扩展字段（不入库）
    school_name: Optional[str] = None
    major_name: Optional[str] = None
    province_name: Optional[str] = None
