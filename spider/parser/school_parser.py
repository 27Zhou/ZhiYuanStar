"""
高校数据解析器
负责清洗和标准化高校数据
"""
import re
from typing import List, Dict, Any, Optional

from parser.base import BaseParser
from utils.data_cleaner import data_cleaner


class SchoolParser(BaseParser):
    """高校数据解析器"""

    # 省份名称到ID的映射（与数据库province表对应）
    PROVINCE_MAP = {
        "北京": 1, "天津": 2, "河北": 3, "山西": 4, "内蒙古": 5,
        "辽宁": 6, "吉林": 7, "黑龙江": 8, "上海": 9, "江苏": 10,
        "浙江": 11, "安徽": 12, "福建": 13, "江西": 14, "山东": 15,
        "河南": 16, "湖北": 17, "湖南": 18, "广东": 19, "广西": 20,
        "海南": 21, "重庆": 22, "四川": 23, "贵州": 24, "云南": 25,
        "西藏": 26, "陕西": 27, "甘肃": 28, "青海": 29, "宁夏": 30,
        "新疆": 31,
        # 全称映射
        "北京市": 1, "天津市": 2, "河北省": 3, "山西省": 4, "内蒙古自治区": 5,
        "辽宁省": 6, "吉林省": 7, "黑龙江省": 8, "上海市": 9, "江苏省": 10,
        "浙江省": 11, "安徽省": 12, "福建省": 13, "江西省": 14, "山东省": 15,
        "河南省": 16, "湖北省": 17, "湖南省": 18, "广东省": 19, "广西壮族自治区": 20,
        "海南省": 21, "重庆市": 22, "四川省": 23, "贵州省": 24, "云南省": 25,
        "西藏自治区": 26, "陕西省": 27, "甘肃省": 28, "青海省": 29, "宁夏回族自治区": 30,
        "新疆维吾尔自治区": 31,
    }

    # 学校类型映射
    TYPE_MAP = {
        "综合": 1, "理工": 2, "师范": 3, "医药": 4, "财经": 5,
        "政法": 6, "农林": 7, "艺术": 8, "体育": 9, "民族": 10, "军事": 11,
        "综合类": 1, "理工类": 2, "师范类": 3, "医药类": 4, "财经类": 5,
        "政法类": 6, "农林类": 7, "艺术类": 8, "体育类": 9, "民族类": 10, "军事类": 11,
    }

    # 办学层次映射
    LEVEL_MAP = {
        "本科": 1, "专科": 2, "高职": 2,
    }

    # 办学性质映射
    NATURE_MAP = {
        "公办": 1, "民办": 2, "中外合作": 3, "中外合作办学": 3,
    }

    # 985高校列表（教育部公布）
    SCHOOLS_985 = {
        "北京大学", "清华大学", "中国人民大学", "北京航空航天大学", "北京理工大学",
        "北京师范大学", "中央民族大学", "中国农业大学", "复旦大学", "上海交通大学",
        "同济大学", "华东师范大学", "南京大学", "东南大学", "浙江大学",
        "中国科学技术大学", "厦门大学", "山东大学", "中国海洋大学", "武汉大学",
        "华中科技大学", "湖南大学", "中南大学", "国防科技大学", "中山大学",
        "华南理工大学", "四川大学", "电子科技大学", "重庆大学", "西安交通大学",
        "西北工业大学", "西北农林科技大学", "兰州大学", "大连理工大学", "东北大学",
        "吉林大学", "哈尔滨工业大学", "天津大学", "南开大学",
    }

    # 211高校列表（部分，完整列表太长，用985作为子集 + 补充）
    SCHOOLS_211_EXTRA = {
        "北京交通大学", "北京工业大学", "北京科技大学", "北京化工大学", "北京邮电大学",
        "北京林业大学", "北京中医药大学", "北京外国语大学", "中国传媒大学", "中央财经大学",
        "对外经济贸易大学", "中国政法大学", "华北电力大学", "中国矿业大学（北京）",
        "中国石油大学（北京）", "中国地质大学（北京", "上海财经大学", "上海大学",
        "上海外国语大学", "华东理工大学", "东华大学", "第二军医大学",
        "南京航空航天大学", "南京理工大学", "河海大学", "南京农业大学", "中国药科大学",
        "南京师范大学", "苏州大学", "江南大学", "南京航空航天大学",
        "合肥工业大学", "安徽大学", "福州大学", "南昌大学",
        "中国石油大学（华东）", "郑州大学", "武汉理工大学", "中国地质大学（武汉）",
        "华中农业大学", "华中师范大学", "中南财经政法大学", "湖南师范大学",
        "暨南大学", "华南师范大学", "广西大学", "海南大学",
        "西南大学", "西南政法大学", "贵州大学", "云南大学",
        "西藏大学", "西北大学", "西安电子科技大学", "长安大学", "第四军医大学",
        "陕西师范大学", "宁夏大学", "青海大学", "新疆大学", "石河子大学",
        "太原理工大学", "内蒙古大学", "辽宁大学", "大连海事大学", "延边大学",
        "东北师范大学", "哈尔滨工程大学", "东北农业大学", "东北林业大学",
        "四川农业大学", "西南交通大学", "西南财经大学", "电子科技大学",
    }

    # 双一流高校（除985/211外的新增）
    SCHOOLS_DOUBLE_FIRST_CLASS_EXTRA = {
        "南方科技大学", "上海科技大学", "中国科学院大学", "宁波大学",
        "河南大学", "湘潭大学", "成都理工大学", "成都中医药大学",
        "西南石油大学", "广州中医药大学", "南京信息工程大学", "南京邮电大学",
        "南京林业大学", "天津工业大学", "天津中医药大学", "上海海洋大学",
        "上海中医药大学", "上海体育学院", "上海音乐学院", "南京医科大学",
        "南京中医药大学", "中国美术学院", "河南大学", "广州医科大学",
        "华南农业大学", "山西大学", "河北工业大学",
    }

    def __init__(self):
        super().__init__(name="school_parser")

    def parse(self, content: str, **kwargs) -> List[Dict[str, Any]]:
        """解析HTML内容（本模块主要处理JSON，此方法备用）"""
        return []

    def parse_single(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        解析单条高校数据

        Args:
            raw_data: 原始数据字典

        Returns:
            清洗后的数据字典，无效数据返回None
        """
        try:
            # 提取学校名称（必填）
            name = self._extract_name(raw_data)
            if not name:
                return None

            # 提取学校代码
            code = self._extract_code(raw_data)

            # 提取省份信息
            province_name = self._extract_province_name(raw_data)
            province_id = self._resolve_province_id(province_name)

            # 提取城市信息
            city_name = self._extract_city_name(raw_data)

            # 提取地址
            address = self._extract_address(raw_data)

            # 提取办学类型
            school_type = self._extract_type(raw_data)

            # 提取办学层次
            level = self._extract_level(raw_data)

            # 提取办学性质
            nature = self._extract_nature(raw_data)

            # 提取官网
            website = self._extract_website(raw_data)

            # 判断985/211/双一流
            is_985 = 1 if name in self.SCHOOLS_985 else 0
            is_211 = 1 if (is_985 or name in self.SCHOOLS_211_EXTRA) else 0
            is_double_first = 1 if (is_211 or name in self.SCHOOLS_DOUBLE_FIRST_CLASS_EXTRA) else 0

            # 提取主管部门
            department = self._extract_department(raw_data)

            # 构建结果
            result = {
                "name": name,
                "code": code,
                "province_id": province_id,
                "address": address,
                "type": school_type,
                "level": level,
                "nature": nature,
                "is_985": is_985,
                "is_211": is_211,
                "is_double_first_class": is_double_first,
                "website": website,
                "status": 1,
            }

            # 附加扩展字段（用于日志和调试）
            result["_province_name"] = province_name
            result["_city_name"] = city_name
            result["_department"] = department

            return result

        except Exception as e:
            self.logger.error(f"解析高校数据失败: {e}")
            return None

    def _extract_name(self, data: Dict) -> Optional[str]:
        """提取学校名称"""
        for key in ["name", "school_name", "name_en", "title", "学校名称", "高校名称"]:
            if key in data and data[key]:
                name = str(data[key]).strip()
                # 清理名称中的特殊字符
                name = re.sub(r'\s+', '', name)
                return name if len(name) >= 2 else None
        return None

    def _extract_code(self, data: Dict) -> Optional[str]:
        """提取学校代码"""
        for key in ["code", "school_code", "code_en", "学校代码", "院校代码"]:
            if key in data and data[key]:
                code = str(data[key]).strip()
                return code if code else None
        return None

    def _extract_province_name(self, data: Dict) -> Optional[str]:
        """提取省份名称"""
        for key in ["province", "province_name", "province_id", "省份", "所在地"]:
            if key in data and data[key]:
                val = str(data[key]).strip()
                # 如果是数字ID，跳过
                if val.isdigit():
                    continue
                return val
        return None

    def _extract_city_name(self, data: Dict) -> Optional[str]:
        """提取城市名称"""
        for key in ["city", "city_name", "城市"]:
            if key in data and data[key]:
                return str(data[key]).strip()
        return None

    def _extract_address(self, data: Dict) -> Optional[str]:
        """提取地址"""
        for key in ["address", "addr", "地址", "详细地址"]:
            if key in data and data[key]:
                return data_cleaner.clean_string(str(data[key]))
        return None

    def _extract_type(self, data: Dict) -> Optional[int]:
        """提取办学类型"""
        for key in ["type", "school_type", "type_name", "类型", "学校类型"]:
            if key in data and data[key]:
                val = str(data[key]).strip()
                # 如果是数字
                if val.isdigit():
                    t = int(val)
                    return t if 1 <= t <= 11 else None
                # 文字映射
                return self.TYPE_MAP.get(val)
        return None

    def _extract_level(self, data: Dict) -> Optional[int]:
        """提取办学层次"""
        for key in ["level", "school_level", "level_name", "层次", "办学层次"]:
            if key in data and data[key]:
                val = str(data[key]).strip()
                if val.isdigit():
                    l = int(val)
                    return l if l in (1, 2) else None
                return self.LEVEL_MAP.get(val)
        return None

    def _extract_nature(self, data: Dict) -> Optional[int]:
        """提取办学性质"""
        for key in ["nature", "school_nature", "nature_name", "性质", "办学性质", "办学类型"]:
            if key in data and data[key]:
                val = str(data[key]).strip()
                if val.isdigit():
                    n = int(val)
                    return n if 1 <= n <= 3 else None
                return self.NATURE_MAP.get(val)
        return None

    def _extract_website(self, data: Dict) -> Optional[str]:
        """提取官网地址"""
        for key in ["website", "url", "home_page", "官网", "学校官网"]:
            if key in data and data[key]:
                url = str(data[key]).strip()
                if not url.startswith("http"):
                    url = "http://" + url
                return data_cleaner.clean_url(url)
        return None

    def _extract_department(self, data: Dict) -> Optional[str]:
        """提取主管部门"""
        for key in ["department", "belong", "主管部门"]:
            if key in data and data[key]:
                return str(data[key]).strip()
        return None

    def _resolve_province_id(self, province_name: Optional[str]) -> Optional[int]:
        """省份名称转ID"""
        if not province_name:
            return None

        # 精确匹配
        if province_name in self.PROVINCE_MAP:
            return self.PROVINCE_MAP[province_name]

        # 模糊匹配
        for key, pid in self.PROVINCE_MAP.items():
            if key in province_name or province_name in key:
                return pid

        return None
