import json

def _try_parse_json(line):
    try:
        return json.loads(line)
    except Exception:
        return None

def load_lines(files, filter_date: str | None = None):
    for file in files:
        with open(file, encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                if filter_date:
                    obj = _try_parse_json(line)
                    if obj is None:
                        continue
                    if obj:
                        ts = obj.get("@timestamp")
                        if ts and ts.split("T")[0] != filter_date:
                            continue
                yield line
