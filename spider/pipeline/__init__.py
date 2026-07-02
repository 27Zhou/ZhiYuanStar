"""
数据管道模块
"""
from pipeline.base import BasePipeline

# 延迟导入，避免在导入时就连接数据库
# 使用时: from pipeline.db_pipeline import DatabasePipeline
__all__ = ["BasePipeline"]
