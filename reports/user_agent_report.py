from collections import Counter
from utils.log_parser import _try_parse_json
from .base import BaseReport

class UserAgentReport(BaseReport):
    def generate(self, lines):
        counter = Counter()
        for line in lines:
            obj = _try_parse_json(line)
            if not obj:
                continue
            ua = obj.get("http_user_agent")
            if ua:
                counter[ua] += 1
        return dict(counter)


