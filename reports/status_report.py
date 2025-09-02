from collections import Counter
from utils.log_parser import _try_parse_json
from .base import BaseReport

class StatusReport(BaseReport):
    def generate(self, lines):
        counter = Counter()
        for line in lines:
            obj = _try_parse_json(line)
            if not obj:
                continue
            code = obj.get("status")
            if code is not None:
                counter[str(code)] += 1
        return dict(counter)



