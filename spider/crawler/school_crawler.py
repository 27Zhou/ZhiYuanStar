"""
高校数据采集模块
数据来源：教育部高校名单、高校信息公开
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from crawler.base import BaseCrawler
from parser.school_parser import SchoolParser
from pipeline.school_pipeline import SchoolPipeline
from utils.exceptions import SpiderException


class SchoolCrawler(BaseCrawler):
    """高校数据采集器"""

    # 教育部高校名单API（阳光高考平台公开数据）
    API_URL = "https://api.gaokao.cn/api/school/lists"
    # 备用：高校名单JSON数据源
    BACKUP_URL = "https://static-data.gaokao.cn/www/2.0/school/list.json"

    # 断点续爬文件
    CHECKPOINT_FILE = "data/school_checkpoint.json"

    def __init__(self):
        super().__init__(name="school_crawler")
        self.parser = SchoolParser()
        self.pipeline = SchoolPipeline()
        self.checkpoint_path = Path(self.config.project_root) / self.CHECKPOINT_FILE

    def _load_checkpoint(self) -> Dict[str, Any]:
        """加载断点信息"""
        if self.checkpoint_path.exists():
            try:
                with open(self.checkpoint_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.logger.info(f"加载断点：已完成 {data.get('completed', 0)} 所高校")
                    return data
            except Exception as e:
                self.logger.warning(f"加载断点失败: {e}")
        return {"completed": 0, "school_ids": [], "last_page": 0}

    def _save_checkpoint(self, checkpoint: Dict[str, Any]):
        """保存断点信息"""
        try:
            self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.checkpoint_path, "w", encoding="utf-8") as f:
                json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.warning(f"保存断点失败: {e}")

    def crawl(self, **kwargs) -> List[Dict[str, Any]]:
        """
        执行高校数据采集

        Returns:
            高校数据列表
        """
        all_schools = []
        checkpoint = self._load_checkpoint()
        completed_ids = set(checkpoint.get("school_ids", []))

        # 方式1：尝试从API获取
        schools = self._crawl_from_api()
        if schools:
            self.logger.info(f"从API获取到 {len(schools)} 所高校数据")
            all_schools = schools
        else:
            # 方式2：尝试从JSON数据源获取
            self.logger.info("API获取失败，尝试备用数据源...")
            schools = self._crawl_from_backup()
            if schools:
                self.logger.info(f"从备用源获取到 {len(schools)} 所高校数据")
                all_schools = schools

        if not all_schools:
            self.logger.warning("未获取到任何高校数据")
            return []

        # 过滤已处理的数据（断点续爬）
        new_schools = []
        for school in all_schools:
            school_code = school.get("code", "")
            if school_code and school_code not in completed_ids:
                new_schools.append(school)

        self.logger.info(f"总计 {len(all_schools)} 所高校，新增待处理 {len(new_schools)} 所")

        # 逐条处理并保存
        saved_count = 0
        for i, school_data in enumerate(new_schools):
            try:
                # 解析并清洗数据
                cleaned = self.parser.parse_single(school_data)
                if not cleaned:
                    continue

                # 保存到数据库
                if self.pipeline.save_school(cleaned):
                    saved_count += 1
                    # 更新断点
                    completed_ids.add(school_data.get("code", ""))
                    checkpoint["school_ids"] = list(completed_ids)
                    checkpoint["completed"] = len(completed_ids)

                    # 每50条保存一次断点
                    if saved_count % 50 == 0:
                        self._save_checkpoint(checkpoint)
                        self.logger.info(f"进度: {saved_count}/{len(new_schools)}")

            except Exception as e:
                self.logger.error(f"处理高校数据失败: {school_data.get('name', '未知')} - {e}")

        # 最终保存断点
        self._save_checkpoint(checkpoint)

        # 刷新管道
        self.pipeline.flush()

        self.logger.info(f"高校数据采集完成，成功保存 {saved_count} 所高校")
        return all_schools

    def _crawl_from_api(self) -> List[Dict[str, Any]]:
        """从API获取高校数据"""
        all_schools = []

        for page in range(1, 200):
            try:
                params = {
                    "page": page,
                    "size": 50,
                    "school_type": 0,  # 0-全部
                }

                data = self.fetch_json(self.API_URL, params=params)

                if not data:
                    break

                # 解析API返回数据
                school_list = data.get("data", {}).get("list", [])
                if not school_list:
                    break

                all_schools.extend(school_list)
                self.logger.debug(f"API第 {page} 页: {len(school_list)} 所高校")

                # 如果本页数据少于每页数量，说明已是最后一页
                if len(school_list) < params["size"]:
                    break

            except Exception as e:
                self.logger.warning(f"API第 {page} 页获取失败: {e}")
                break

        return all_schools

    def _crawl_from_backup(self) -> List[Dict[str, Any]]:
        """从备用JSON数据源获取高校数据"""
        try:
            content = self.fetch_page(self.BACKUP_URL, encoding="utf-8")
            if not content:
                return []

            # 解析JSON
            data = json.loads(content)
            school_list = data.get("data", data) if isinstance(data, dict) else data

            if isinstance(school_list, list):
                return school_list

            return []

        except Exception as e:
            self.logger.error(f"备用数据源获取失败: {e}")
            return []

    def parse(self, content: str, **kwargs) -> List[Dict[str, Any]]:
        """解析内容（由parser处理）"""
        return self.parser.parse(content, **kwargs)

    def cleanup(self):
        """清理资源"""
        self.pipeline.close()
        self.logger.info("高校数据采集器已清理")
