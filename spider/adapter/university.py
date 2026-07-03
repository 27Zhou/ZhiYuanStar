"""
高校官网数据适配器
数据来源：各高校官方网站
"""
import re
from typing import List, Dict, Any, Optional

from adapter.base import BaseAdapter
from config.sources import UNIVERSITY_SOURCES


class UniversityAdapter(BaseAdapter):
    """高校官网数据适配器"""

    name = "university"
    priority = 30  # 较低优先级

    # 常见高校官网域名
    UNIVERSITY_DOMAINS = {
        "北京大学": "pku.edu.cn",
        "清华大学": "tsinghua.edu.cn",
        "复旦大学": "fudan.edu.cn",
        "上海交通大学": "sjtu.edu.cn",
        "浙江大学": "zju.edu.cn",
        "南京大学": "nju.edu.cn",
        "武汉大学": "whu.edu.cn",
        "华中科技大学": "hust.edu.cn",
        "中山大学": "sysu.edu.cn",
        "四川大学": "scu.edu.cn",
        "西安交通大学": "xjtu.edu.cn",
        "哈尔滨工业大学": "hit.edu.cn",
        "中国科学技术大学": "ustc.edu.cn",
        "吉林大学": "jlu.edu.cn",
        "山东大学": "sdu.edu.cn",
        "厦门大学": "xmu.edu.cn",
        "同济大学": "tongji.edu.cn",
        "中南大学": "csu.edu.cn",
        "东南大学": "seu.edu.cn",
        "北京航空航天大学": "buaa.edu.cn",
        "北京理工大学": "bit.edu.cn",
        "北京师范大学": "bnu.edu.cn",
        "天津大学": "tju.edu.cn",
        "南开大学": "nankai.edu.cn",
        "大连理工大学": "dlut.edu.cn",
        "东北大学": "neu.edu.cn",
        "华南理工大学": "scut.edu.cn",
        "重庆大学": "cqu.edu.cn",
        "电子科技大学": "uestc.edu.cn",
        "兰州大学": "lzu.edu.cn",
        "西北工业大学": "nwpu.edu.cn",
        "中国农业大学": "cau.edu.cn",
        "北京交通大学": "bjtu.edu.cn",
        "北京科技大学": "ustb.edu.cn",
        "北京邮电大学": "bupt.edu.cn",
        "华东师范大学": "ecnu.edu.cn",
        "华东理工大学": "ecust.edu.cn",
        "上海财经大学": "shufe.edu.cn",
        "南京航空航天大学": "nuaa.edu.cn",
        "南京理工大学": "njust.edu.cn",
        "河海大学": "hhu.edu.cn",
        "南京农业大学": "njau.edu.cn",
        "南京师范大学": "njnu.edu.cn",
        "苏州大学": "suda.edu.cn",
        "江南大学": "jiangnan.edu.cn",
        "合肥工业大学": "hfut.edu.cn",
        "安徽大学": "ahu.edu.cn",
        "福州大学": "fzu.edu.cn",
        "南昌大学": "ncu.edu.cn",
        "郑州大学": "zzu.edu.cn",
        "武汉理工大学": "whut.edu.cn",
        "华中农业大学": "hzau.edu.cn",
        "华中师范大学": "ccnu.edu.cn",
        "中南财经政法大学": "zuel.edu.cn",
        "湖南大学": "hnu.edu.cn",
        "湖南师范大学": "hunnu.edu.cn",
        "暨南大学": "jnu.edu.cn",
        "华南师范大学": "scnu.edu.cn",
        "广西大学": "gxu.edu.cn",
        "海南大学": "hainanu.edu.cn",
        "西南大学": "swu.edu.cn",
        "西南交通大学": "swjtu.edu.cn",
        "西南财经大学": "swufe.edu.cn",
        "贵州大学": "gzu.edu.cn",
        "云南大学": "ynu.edu.cn",
        "西藏大学": "utibet.edu.cn",
        "西北大学": "nwu.edu.cn",
        "西安电子科技大学": "xidian.edu.cn",
        "长安大学": "chd.edu.cn",
        "陕西师范大学": "snnu.edu.cn",
        "宁夏大学": "nxu.edu.cn",
        "青海大学": "qhu.edu.cn",
        "新疆大学": "xju.edu.cn",
        "石河子大学": "shzu.edu.cn",
        "太原理工大学": "tyut.edu.cn",
        "内蒙古大学": "imu.edu.cn",
        "辽宁大学": "lnu.edu.cn",
        "大连海事大学": "dlmu.edu.cn",
        "延边大学": "ybu.edu.cn",
        "东北师范大学": "nenu.edu.cn",
        "哈尔滨工程大学": "hrbeu.edu.cn",
        "东北农业大学": "neau.edu.cn",
        "东北林业大学": "nefu.edu.cn",
        "四川农业大学": "sicau.edu.cn",
    }

    def fetch_school_list(self, **kwargs) -> List[Dict[str, Any]]:
        """高校官网不提供批量列表"""
        return []

    def fetch_major_list(self, **kwargs) -> List[Dict[str, Any]]:
        """高校官网不提供批量专业列表"""
        return []

    def fetch_admission_scores(self, year: int, province_id: int, **kwargs) -> List[Dict[str, Any]]:
        """从高校招生网获取录取分数线"""
        school_name = kwargs.get("school_name")
        if not school_name:
            return []

        domain = self.UNIVERSITY_DOMAINS.get(school_name)
        if not domain:
            return []

        url = UNIVERSITY_SOURCES.get("admission_page", "").format(school_domain=domain)
        if not url:
            return []

        try:
            html = self.fetch_page(url)
            if not html:
                return []

            # 解析录取数据（需要配合parser）
            return [{"_html": html, "_school_name": school_name, "_year": year, "_province_id": province_id}]

        except Exception as e:
            self.logger.warning(f"[{self.name}] 获取 {school_name} 录取数据失败: {e}")
            return []

    def get_school_domain(self, school_name: str) -> Optional[str]:
        """获取高校官网域名"""
        return self.UNIVERSITY_DOMAINS.get(school_name)
