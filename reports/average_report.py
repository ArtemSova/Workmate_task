from collections import defaultdict
from utils.log_parser import _try_parse_json
from .base import BaseReport


class AverageReport(BaseReport):
    def generate(self, lines):
        stats = defaultdict(lambda: {"count": 0, "total_time": 0.0})

        for line in lines:
            obj = _try_parse_json(line)
            if not obj:
                continue
            url = obj.get("url")
            rt = obj.get("response_time")
            if url and rt is not None:
                try:
                    rt = float(rt)
                    stats[url]["count"] += 1
                    stats[url]["total_time"] += rt
                except ValueError:
                    continue

        result = {}
        for url, data in stats.items():
            result[url] = {
                "count": data["count"],
                "avg_time": data["total_time"] / data["count"]
            }
        return result