"""
省级教育考试院数据适配器
数据来源：各省教育考试院官网
"""
from typing import List, Dict, Any, Optional

from adapter.base import BaseAdapter
from config.sources import PROVINCE_SOURCES


class ProvinceAdapter(BaseAdapter):
    """省级教育考试院数据适配器"""

    name = "province"
    priority = 40  # 最低优先级

    # 省份ID到配置key的映射
    PROVINCE_KEY_MAP = {
        1: "beijing", 2: "tianjin", 3: "hebei", 4: "shanxi", 5: "neimenggu",
        6: "liaoning", 7: "jilin", 8: "heilongjiang", 9: "shanghai", 10: "jiangsu",
        11: "zhejiang", 12: "anhui", 13: "fujian", 14: "jiangxi", 15: "shandong",
        16: "henan", 17: "hubei", 18: "hunan", 19: "guangdong", 20: "guangxi",
        21: "hainan", 22: "chongqing", 23: "sichuan", 24: "guizhou", 25: "yunnan",
        26: "xizang", 27: "shaanxi", 28: "gansu", 29: "qinghai", 30: "ningxia",
        31: "xinjiang",
    }

    def fetch_school_list(self, **kwargs) -> List[Dict[str, Any]]:
        """省级考试院不提供全国高校列表"""
        return []

    def fetch_major_list(self, **kwargs) -> List[Dict[str, Any]]:
        """省级考试院不提供全国专业列表"""
        return []

    def fetch_admission_scores(self, year: int, province_id: int, **kwargs) -> List[Dict[str, Any]]:
        """从省级考试院获取录取分数线"""
        province_key = self.PROVINCE_KEY_MAP.get(province_id)
        if not province_key:
            return []

        base_url = PROVINCE_SOURCES.get(province_key)
        if not base_url:
            return []

        # 省级考试院通常需要HTML解析，这里返回基础信息
        # 实际解析需要配合具体的parser
        try:
            html = self.fetch_page(base_url)
            if not html:
                return []

            # 返回原始HTML，由parser处理
            return [{"_html": html, "_province_id": province_id, "_year": year, "_source": "province"}]

        except Exception as e:
            self.logger.warning(f"[{self.name}] 获取省份 {province_id} 数据失败: {e}")
            return []

    def get_province_url(self, province_id: int) -> Optional[str]:
        """获取省份考试院URL"""
        province_key = self.PROVINCE_KEY_MAP.get(province_id)
        if province_key:
            return PROVINCE_SOURCES.get(province_key)
        return None
