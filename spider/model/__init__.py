"""
数据模型模块
"""
from model.base import BaseModel
from model.school import School
from model.major import Major
from model.admission import AdmissionScore
from model.enrollment import EnrollmentPlan

__all__ = [
    "BaseModel",
    "School",
    "Major",
    "AdmissionScore",
    "EnrollmentPlan",
]
