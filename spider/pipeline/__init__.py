"""
数据管道模块
"""
from pipeline.base import BasePipeline
from pipeline.db_pipeline import DatabasePipeline

__all__ = ["BasePipeline", "DatabasePipeline"]
