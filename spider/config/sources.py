"""
数据源URL配置
所有外部数据源URL集中管理，便于维护和切换
"""

# =====================================================
# 教育部数据源
# =====================================================
EDUCATION_SOURCES = {
    # 教育部高校名单
    "school_list": "https://www.moe.gov.cn/jyb_xxgk/s5743/s5744/A03/202410/t20241024_1160578.html",
    # 备用：教育部API
    "school_list_api": "https://api.moe.edu.cn/v1/school/list",
}

# =====================================================
# 阳光高考平台数据源
# =====================================================
SUNSHINE_SOURCES = {
    # 高校列表
    "school_list": "https://gaokao.chsi.com.cn/sch/search--ss-985,211,dbl,by,sgy,typ-b0,lf-b1,tl-m0102-p1.html",
    # 专业列表
    "major_list": "https://gaokao.chsi.com.cn/zyk/zybk/zyDetail",
    # 录取分数线
    "admission_score": "https://gaokao.chsi.com.cn/zsgs/zhangcheng/listVerif498--method-index,lb-1,start-0.dhtml",
    # 备用API
    "api_school": "https://api.gaokao.cn/api/school/lists",
    "api_major": "https://api.gaokao.cn/api/major/lists",
    "api_score": "https://api.gaokao.cn/api/school/provinceScore",
}

# =====================================================
# 高校官网数据源模板
# =====================================================
UNIVERSITY_SOURCES = {
    # 高校官网招生网模板（{school_code}会被替换）
    "admission_page": "https://www.{school_domain}/zsb/",
    "enrollment_plan": "https://www.{school_domain}/zsb/zsjh/",
}

# =====================================================
# 省级教育考试院数据源
# =====================================================
PROVINCE_SOURCES = {
    # 各省教育考试院
    "beijing": "https://www.bjeea.cn/",
    "shanghai": "https://www.shmeea.edu.cn/",
    "guangdong": "https://eea.gd.gov.cn/",
    "zhejiang": "https://www.zjzs.net/",
    "jiangsu": "https://www.jseea.cn/",
    "shandong": "https://www.sdzk.cn/",
    "henan": "https://www.haeea.cn/",
    "sichuan": "https://www.sceea.cn/",
    "hubei": "https://www.hbea.edu.cn/",
    "hunan": "https://jyt.hunan.gov.cn/",
    "hebei": "https://www.hebeea.edu.cn/",
    "anhui": "https://www.ahzsks.cn/",
    "fujian": "https://www.eeafj.cn/",
    "jiangxi": "https://www.jxeea.cn/",
    "liaoning": "https://www.lnzsks.com/",
    "heilongjiang": "https://www.lzk.hl.cn/",
    "jilin": "https://www.jleea.com.cn/",
    "shanxi": "https://www.sxkszx.cn/",
    "neimenggu": "https://www.nm.zsks.cn/",
    "chongqing": "https://www.cqksy.cn/",
    "guizhou": "https://www.eaagz.org.cn/",
    "yunnan": "https://www.ynzs.cn/",
    "xizang": "https://zsks.edu.xizang.gov.cn/",
    "shaanxi": "https://www.sneea.cn/",
    "gansu": "https://www.ganseea.cn/",
    "qinghai": "https://www.qhjyks.com/",
    "ningxia": "https://www.nxjyks.cn/",
    "xinjiang": "https://www.xjzk.gov.cn/",
    "hainan": "https://ea.hainan.gov.cn/",
    "tianjin": "https://www.zhaokao.net/",
    "guangxi": "https://www.gxeea.cn/",
}

# =====================================================
# 备用数据源（第三方聚合）
# =====================================================
BACKUP_SOURCES = {
    "school_list_json": "https://static-data.gaokao.cn/www/2.0/school/list.json",
    "major_list_json": "https://static-data.gaokao.cn/www/2.0/major/list.json",
    "score_list_json": "https://static-data.gaokao.cn/www/2.0/school/score_list.json",
}
