"""
专业数据采集模块（重构版）
采用Adapter架构，Crawler只负责调度
"""
import json
from pathlib import Path
from typing import List, Dict, Any

from crawler.base import BaseCrawler
from parser.major_parser import MajorParser
from pipeline.major_pipeline import MajorPipeline
from adapter.registry import adapter_registry
from adapter.sunshine import SunshineAdapter


class MajorCrawler(BaseCrawler):
    """专业数据采集器（调度器）"""

    CHECKPOINT_FILE = "data/major_checkpoint.json"

    def __init__(self):
        super().__init__(name="major_crawler")
        self.parser = MajorParser()
        self.pipeline = MajorPipeline()
        self.checkpoint_path = Path(self.config.project_root) / self.CHECKPOINT_FILE

        # 注册数据源适配器
        adapter_registry.register("major", SunshineAdapter())

    def _load_checkpoint(self) -> Dict[str, Any]:
        """加载断点信息"""
        if self.checkpoint_path.exists():
            try:
                with open(self.checkpoint_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.logger.info(f"加载断点：已完成 {data.get('completed', 0)} 个专业")
                    return data
            except Exception as e:
                self.logger.warning(f"加载断点失败: {e}")
        return {"completed": 0, "major_codes": []}

    def _save_checkpoint(self, checkpoint: Dict[str, Any]):
        """保存断点信息"""
        try:
            self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.checkpoint_path, "w", encoding="utf-8") as f:
                json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.warning(f"保存断点失败: {e}")

    def crawl(self, **kwargs) -> List[Dict[str, Any]]:
        """执行专业数据采集（调度Adapter）"""
        checkpoint = self._load_checkpoint()
        completed_codes = set(checkpoint.get("major_codes", []))

        # 通过Adapter注册表获取数据（自动切换数据源）
        all_majors = adapter_registry.execute("major", "fetch_major_list")

        if not all_majors:
            self.logger.warning("所有数据源均未获取到专业数据")
            return []

        # 过滤已处理的数据（断点续爬）
        new_majors = []
        for major in all_majors:
            code = major.get("code", major.get("major_code", ""))
            if code and code not in completed_codes:
                new_majors.append(major)

        self.logger.info(f"总计 {len(all_majors)} 个专业，新增待处理 {len(new_majors)} 个")

        # 逐条处理并保存
        saved_count = 0
        for i, major_data in enumerate(new_majors):
            try:
                cleaned = self.parser.parse_single(major_data)
                if not cleaned:
                    continue

                if self.pipeline.save_major(cleaned):
                    saved_count += 1
                    code = major_data.get("code", major_data.get("major_code", ""))
                    completed_codes.add(code)
                    checkpoint["major_codes"] = list(completed_codes)
                    checkpoint["completed"] = len(completed_codes)

                    if saved_count % 50 == 0:
                        self._save_checkpoint(checkpoint)
                        self.logger.info(f"进度: {saved_count}/{len(new_majors)}")

            except Exception as e:
                self.logger.error(f"处理专业数据失败: {major_data.get('name', '未知')} - {e}")

        self._save_checkpoint(checkpoint)
        self.pipeline.flush()

        self.logger.info(f"专业数据采集完成，成功保存 {saved_count} 个专业")
        return all_majors

    def parse(self, content: str, **kwargs) -> List[Dict[str, Any]]:
        """解析内容（由parser处理）"""
        return self.parser.parse(content, **kwargs)

    def cleanup(self):
        """清理资源"""
        self.pipeline.close()
        self.logger.info("专业数据采集器已清理")
