"""최적화기가 한 점을 평가할 때 부르는 감싸기 스크립트 (뼈대).

사용: python optim/evaluate.py --max_iter 30 --llr_scale 1.0
하는 일: 기준 실험(workspace/base_run/config.json)을 읽어 인자대로 고친 설정을 optim/_work/ 에 쓰고,
`python -m src.run <설정>` 을 돌린 뒤 결과 폴더의 summary.txt 에서 FER 줄을 찾아 `FER = 값` 한 줄로 출력한다.
최적화기(optim/config.json 의 metric_regex)는 이 줄에서 값을 읽는다.
첫 실행에서는 summary.txt 의 FER 표기가 아래 정규식과 맞는지 확인한다.
"""
import argparse
import glob
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_CONFIG = os.path.join(ROOT, "workspace", "base_run", "config.json")
WORK = os.path.join(ROOT, "optim", "_work")
FER_LINE = re.compile(r"FER[^0-9]*([0-9]*\.?[0-9]+(?:[eE][+-]?[0-9]+)?)")


def scaled(values, factor):
    if isinstance(values, list):
        return [scaled(v, factor) for v in values]
    if isinstance(values, (int, float)) and not isinstance(values, bool):
        return round(values * factor, 4)
    return values


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--max_iter", type=int, required=True)
    ap.add_argument("--llr_scale", type=float, default=1.0)
    args = ap.parse_args(argv)
    config = json.load(io.open(BASE_CONFIG, encoding="utf-8"))
    config["decoder"]["max_iter"] = args.max_iter
    for key in list(config["decoder"]):
        if key.startswith("channel_llr_"):
            config["decoder"][key] = scaled(config["decoder"][key], args.llr_scale)
    tag = f"iter{args.max_iter}_scale{args.llr_scale:.2f}"
    out_dir = os.path.join(WORK, tag)
    os.makedirs(out_dir, exist_ok=True)
    config.setdefault("output", {})["dir"] = out_dir
    config["output"]["label"] = tag
    cfg_path = os.path.join(out_dir, "config.json")
    io.open(cfg_path, "w", encoding="utf-8").write(json.dumps(config, ensure_ascii=False, indent=2))
    result = subprocess.run([sys.executable, "-m", "src.run", cfg_path], cwd=ROOT, capture_output=True, text=True)
    summaries = sorted(glob.glob(os.path.join(out_dir, "**", "summary.txt"), recursive=True), key=os.path.getmtime)
    text = io.open(summaries[-1], encoding="utf-8", errors="replace").read() if summaries else result.stdout
    m = FER_LINE.search(text)
    if not m:
        sys.stderr.write(result.stderr[-2000:])
        print("FER = nan  (summary.txt 에서 FER 줄을 찾지 못함)")
        return 1
    print(f"FER = {m.group(1)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
