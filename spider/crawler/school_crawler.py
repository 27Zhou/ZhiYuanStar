"""
高校数据采集模块（重构版）
采用Adapter架构，Crawler只负责调度
"""
import json
from pathlib import Path
from typing import List, Dict, Any

from crawler.base import BaseCrawler
from parser.school_parser import SchoolParser
from pipeline.school_pipeline import SchoolPipeline
from adapter.registry import adapter_registry
from adapter.education import EducationAdapter
from adapter.sunshine import SunshineAdapter


class SchoolCrawler(BaseCrawler):
    """高校数据采集器（调度器）"""

    CHECKPOINT_FILE = "data/school_checkpoint.json"

    def __init__(self):
        super().__init__(name="school_crawler")
        self.parser = SchoolParser()
        self.pipeline = SchoolPipeline()
        self.checkpoint_path = Path(self.config.project_root) / self.CHECKPOINT_FILE

        # 注册数据源适配器
        adapter_registry.register("school", EducationAdapter())
        adapter_registry.register("school", SunshineAdapter())

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
        return {"completed": 0, "school_ids": []}

    def _save_checkpoint(self, checkpoint: Dict[str, Any]):
        """保存断点信息"""
        try:
            self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.checkpoint_path, "w", encoding="utf-8") as f:
                json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.warning(f"保存断点失败: {e}")

    def crawl(self, **kwargs) -> List[Dict[str, Any]]:
        """执行高校数据采集（调度Adapter）"""
        checkpoint = self._load_checkpoint()
        completed_ids = set(checkpoint.get("school_ids", []))

        # 通过Adapter注册表获取数据（自动切换数据源）
        all_schools = adapter_registry.execute("school", "fetch_school_list")

        if not all_schools:
            self.logger.warning("所有数据源均未获取到高校数据")
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
                cleaned = self.parser.parse_single(school_data)
                if not cleaned:
                    continue

                if self.pipeline.save_school(cleaned):
                    saved_count += 1
                    completed_ids.add(school_data.get("code", ""))
                    checkpoint["school_ids"] = list(completed_ids)
                    checkpoint["completed"] = len(completed_ids)

                    if saved_count % 50 == 0:
                        self._save_checkpoint(checkpoint)
                        self.logger.info(f"进度: {saved_count}/{len(new_schools)}")

            except Exception as e:
                self.logger.error(f"处理高校数据失败: {school_data.get('name', '未知')} - {e}")

        self._save_checkpoint(checkpoint)
        self.pipeline.flush()

        self.logger.info(f"高校数据采集完成，成功保存 {saved_count} 所高校")
        return all_schools

    def parse(self, content: str, **kwargs) -> List[Dict[str, Any]]:
        """解析内容（由parser处理）"""
        return self.parser.parse(content, **kwargs)

    def cleanup(self):
        """清理资源"""
        self.pipeline.close()
        self.logger.info("高校数据采集器已清理")
