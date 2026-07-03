"""
专业数据采集模块
数据来源：教育部专业目录、阳光高考平台
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from crawler.base import BaseCrawler
from parser.major_parser import MajorParser
from pipeline.major_pipeline import MajorPipeline


class MajorCrawler(BaseCrawler):
    """专业数据采集器"""

    # 阳光高考专业目录API
    API_URL = "https://api.gaokao.cn/api/major/lists"
    # 备用：专业目录JSON数据源
    BACKUP_URL = "https://static-data.gaokao.cn/www/2.0/major/list.json"

    # 断点续爬文件
    CHECKPOINT_FILE = "data/major_checkpoint.json"

    def __init__(self):
        super().__init__(name="major_crawler")
        self.parser = MajorParser()
        self.pipeline = MajorPipeline()
        self.checkpoint_path = Path(self.config.project_root) / self.CHECKPOINT_FILE

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
        return {"completed": 0, "major_codes": [], "last_page": 0}

    def _save_checkpoint(self, checkpoint: Dict[str, Any]):
        """保存断点信息"""
        try:
            self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.checkpoint_path, "w", encoding="utf-8") as f:
                json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.warning(f"保存断点失败: {e}")

    def crawl(self, **kwargs) -> List[Dict[str, Any]]:
        """执行专业数据采集"""
        all_majors = []
        checkpoint = self._load_checkpoint()
        completed_codes = set(checkpoint.get("major_codes", []))

        # 方式1：尝试从API获取
        majors = self._crawl_from_api()
        if majors:
            self.logger.info(f"从API获取到 {len(majors)} 个专业数据")
            all_majors = majors
        else:
            # 方式2：尝试从备用JSON数据源获取
            self.logger.info("API获取失败，尝试备用数据源...")
            majors = self._crawl_from_backup()
            if majors:
                self.logger.info(f"从备用源获取到 {len(majors)} 个专业数据")
                all_majors = majors

        if not all_majors:
            self.logger.warning("未获取到任何专业数据")
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

    def _crawl_from_api(self) -> List[Dict[str, Any]]:
        """从API获取专业数据"""
        all_majors = []

        for page in range(1, 100):
            try:
                params = {"page": page, "size": 50}
                data = self.fetch_json(self.API_URL, params=params)

                if not data:
                    break

                major_list = data.get("data", {}).get("list", [])
                if not major_list:
                    break

                all_majors.extend(major_list)
                self.logger.debug(f"API第 {page} 页: {len(major_list)} 个专业")

                if len(major_list) < params["size"]:
                    break

            except Exception as e:
                self.logger.warning(f"API第 {page} 页获取失败: {e}")
                break

        return all_majors

    def _crawl_from_backup(self) -> List[Dict[str, Any]]:
        """从备用JSON数据源获取专业数据"""
        try:
            content = self.fetch_page(self.BACKUP_URL, encoding="utf-8")
            if not content:
                return []

            data = json.loads(content)
            major_list = data.get("data", data) if isinstance(data, dict) else data

            if isinstance(major_list, list):
                return major_list

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
        self.logger.info("专业数据采集器已清理")
