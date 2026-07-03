"""
历年录取数据采集模块
数据来源：阳光高考平台、各省教育考试院
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from crawler.base import BaseCrawler
from parser.admission_parser import AdmissionParser
from pipeline.admission_pipeline import AdmissionPipeline


class AdmissionCrawler(BaseCrawler):
    """历年录取数据采集器"""

    # 阳光高考录取数据API
    API_URL = "https://api.gaokao.cn/api/school/provinceScore"
    # 备用数据源
    BACKUP_URL = "https://static-data.gaokao.cn/www/2.0/school/score_list.json"

    # 采集年份范围
    YEAR_RANGE = [2020, 2021, 2022, 2023, 2024, 2025]

    # 31个省份ID
    PROVINCE_IDS = list(range(1, 32))

    # 断点续爬文件
    CHECKPOINT_FILE = "data/admission_checkpoint.json"

    def __init__(self):
        super().__init__(name="admission_crawler")
        self.parser = AdmissionParser()
        self.pipeline = AdmissionPipeline()
        self.checkpoint_path = Path(self.config.project_root) / self.CHECKPOINT_FILE

    def _load_checkpoint(self) -> Dict[str, Any]:
        """加载断点信息"""
        if self.checkpoint_path.exists():
            try:
                with open(self.checkpoint_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.logger.info(
                        f"加载断点：已完成 {data.get('completed', 0)} 条，"
                        f"当前年份 {data.get('current_year', '无')}，"
                        f"当前省份 {data.get('current_province', '无')}"
                    )
                    return data
            except Exception as e:
                self.logger.warning(f"加载断点失败: {e}")
        return {
            "completed": 0,
            "current_year": None,
            "current_province": None,
            "finished_keys": [],
        }

    def _save_checkpoint(self, checkpoint: Dict[str, Any]):
        """保存断点信息"""
        try:
            self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.checkpoint_path, "w", encoding="utf-8") as f:
                json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.warning(f"保存断点失败: {e}")

    def crawl(self, **kwargs) -> List[Dict[str, Any]]:
        """执行历年录取数据采集"""
        all_scores = []
        checkpoint = self._load_checkpoint()
        finished_keys = set(checkpoint.get("finished_keys", []))
        saved_count = checkpoint.get("completed", 0)

        # 按年份 → 省份 逐个采集
        for year in self.YEAR_RANGE:
            for province_id in self.PROVINCE_IDS:
                key = f"{year}_{province_id}"

                # 断点续爬：跳过已完成的
                if key in finished_keys:
                    continue

                self.logger.info(f"采集 {year} 年 省份ID={province_id} 录取数据...")

                scores = self._crawl_by_year_province(year, province_id)

                if scores:
                    # 解析并保存
                    for score_data in scores:
                        try:
                            cleaned = self.parser.parse_single(score_data)
                            if not cleaned:
                                continue

                            if self.pipeline.save_score(cleaned):
                                saved_count += 1
                        except Exception as e:
                            self.logger.error(f"处理录取数据失败: {e}")

                    all_scores.extend(scores)
                    self.logger.info(f"  {year}年 省份ID={province_id}: 获取 {len(scores)} 条")
                else:
                    self.logger.debug(f"  {year}年 省份ID={province_id}: 无数据")

                # 标记完成
                finished_keys.add(key)
                checkpoint["finished_keys"] = list(finished_keys)
                checkpoint["current_year"] = year
                checkpoint["current_province"] = province_id
                checkpoint["completed"] = saved_count

                # 每完成一个省份保存一次断点
                self._save_checkpoint(checkpoint)

                # 刷新缓冲区
                self.pipeline.flush()

        self.logger.info(f"录取数据采集完成，共获取 {len(all_scores)} 条，成功保存 {saved_count} 条")
        return all_scores

    def _crawl_by_year_province(self, year: int, province_id: int) -> List[Dict[str, Any]]:
        """按年份和省份采集录取数据"""
        all_scores = []

        for page in range(1, 200):
            try:
                params = {
                    "year": year,
                    "province_id": province_id,
                    "page": page,
                    "size": 50,
                }

                data = self.fetch_json(self.API_URL, params=params)

                if not data:
                    break

                score_list = data.get("data", {}).get("list", [])
                if not score_list:
                    break

                # 给每条数据附加年份和省份信息
                for item in score_list:
                    item["_year"] = year
                    item["_province_id"] = province_id

                all_scores.extend(score_list)

                if len(score_list) < params["size"]:
                    break

            except Exception as e:
                self.logger.warning(f"API第 {page} 页获取失败: {e}")
                break

        return all_scores

    def _crawl_from_backup(self, year: int, province_id: int) -> List[Dict[str, Any]]:
        """从备用数据源获取录取数据"""
        try:
            params = {"year": year, "province_id": province_id}
            content = self.fetch_page(self.BACKUP_URL, params=params, encoding="utf-8")
            if not content:
                return []

            data = json.loads(content)
            score_list = data.get("data", data) if isinstance(data, dict) else data

            if isinstance(score_list, list):
                for item in score_list:
                    item["_year"] = year
                    item["_province_id"] = province_id
                return score_list

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
        self.logger.info("录取数据采集器已清理")
