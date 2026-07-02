"""
基础数据模型
"""
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class BaseModel:
    """基础数据模型类"""

    id: Optional[int] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, datetime):
                    result[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    result[key] = value
        return result

    def to_insert_dict(self) -> Dict[str, Any]:
        """转换为插入字典（排除id和时间字段）"""
        exclude_fields = {'id', 'create_time', 'update_time'}
        result = {}
        for key, value in self.__dict__.items():
            if key not in exclude_fields and value is not None:
                result[key] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """从字典创建实例"""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def __str__(self) -> str:
        fields = ', '.join(f"{k}={v}" for k, v in self.__dict__.items() if v is not None)
        return f"{self.__class__.__name__}({fields})"
