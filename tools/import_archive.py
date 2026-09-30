"""논문 분석 아카이브(형제 저장소 LDPC_Paper_Analysis)의 탐색기 자료를 이 프로젝트의 papers/ 로 들여온다.

사용: python tools/import_archive.py [--archive ../LDPC_Paper_Analysis] [--plugin ../AI_Assisted_Dev/plugin/scripts] [--limit N]
들여오는 것: docs/papers.json 의 항목(탐색기에 보이는 논문) 전부. 논문마다 papers 표에 한 줄, analysis 표에 분류 JSON,
papers/analysis/{id 안전화}.md 에 분석 문서 사본. 초록은 아카이브의 data/papers.db 에서 id 로 찾아 붙인다.
다시 돌리면 이미 있는 논문은 건너뛴다 (중복은 셈만 한다).
"""
import argparse
import io
import json
import os
import re
import shutil
import sqlite3
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

META_KEYS = {"id", "sid", "title", "venue", "year", "month", "vtype", "md"}
MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def fix_outside_links(analysis_dir):
    """분석 md 사본에서 이 저장소 안에 없는 파일을 가리키는 상대 링크(아카이브의 다른 문서를 가리키던 것)를 글자만 남기고 지운다.
    바깥 주소(http, https, mailto)와 같은 문서 안 링크(#)는 그대로 둔다. 고친 파일 수를 돌려준다."""
    fixed = 0
    for name in sorted(os.listdir(analysis_dir)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(analysis_dir, name)
        text = io.open(path, encoding="utf-8", errors="replace").read()

        def keep_or_strip(m):
            target = m.group(2).split("#")[0]
            if not target or re.match(r"[a-z]+:", m.group(2)) or m.group(2).startswith("#"):
                return m.group(0)
            if os.path.exists(os.path.normpath(os.path.join(analysis_dir, target))):
                return m.group(0)
            return m.group(1)

        new = MD_LINK.sub(keep_or_strip, text)
        if new != text:
            io.open(path, "w", encoding="utf-8", newline="\n").write(new)
            fixed += 1
    return fixed


def source_and_ids(pid):
    """아카이브 id('arxiv:2601.05340v1', 'ieee:9496601')를 플러그인 insert_paper 가 받는 칸으로.
    arXiv 의 판 접미사(v1)는 뗀다 (플러그인 paper_search 도 떼므로 같은 논문이 같은 id 가 된다)."""
    src, _sep, rest = pid.partition(":")
    if src == "arxiv":
        rest = re.sub(r"v\d+$", "", rest)
        return {"source": "arxiv", "arxiv_id": rest, "url": f"https://arxiv.org/abs/{rest}"}
    if src == "ieee":
        return {"source": "ieee", "native_id": rest, "url": f"https://ieeexplore.ieee.org/document/{rest}"}
    return {"source": src or "other", "native_id": rest or pid, "url": ""}


def migrate_versioned_arxiv_ids(conn, analysis_dir, safe_name):
    """지난 반입이 남긴 'arxiv:xxxxv1' 꼴 id 를 판 접미사 없는 id 로 옮긴다 (papers, analysis 표와 md 파일 이름). 옮긴 수를 돌려준다."""
    moved = 0
    rows = conn.execute("SELECT id FROM papers WHERE id LIKE 'arxiv:%' AND id GLOB 'arxiv:*v[0-9]*'").fetchall()
    for (old,) in rows:
        new = re.sub(r"v\d+$", "", old)
        if new == old or conn.execute("SELECT 1 FROM papers WHERE id=?", (new,)).fetchone():
            continue
        old_md = os.path.join(analysis_dir, safe_name(old) + ".md")
        new_md = os.path.join(analysis_dir, safe_name(new) + ".md")
        if os.path.isfile(old_md) and not os.path.exists(new_md):
            os.rename(old_md, new_md)
        conn.execute("UPDATE papers SET id=?, url=? WHERE id=?", (new, f"https://arxiv.org/abs/{new[6:]}", old))
        conn.execute("UPDATE analysis SET id=?, md_path=? WHERE id=?",
                     (new, "papers/analysis/" + safe_name(new) + ".md", old))
        conn.execute("UPDATE judgments SET id=? WHERE id=?", (new, old))
        moved += 1
    conn.commit()
    return moved


def prune_orphan_analysis(conn, analysis_dir, safe_name):
    """지난 반입이 papers 표에 없는 id 로 남긴 analysis 행과 그 md 사본을 지운다 (이 스크립트가 만든 것만). 지운 수를 돌려준다."""
    orphans = [r[0] for r in conn.execute("SELECT a.id FROM analysis a LEFT JOIN papers p ON p.id = a.id WHERE p.id IS NULL")]
    for pid in orphans:
        md = os.path.join(analysis_dir, safe_name(pid) + ".md")
        if os.path.isfile(md):
            os.remove(md)
        conn.execute("DELETE FROM analysis WHERE id=?", (pid,))
    conn.commit()
    return len(orphans)


def load_abstracts(archive):
    path = os.path.join(archive, "data", "papers.db")
    if not os.path.isfile(path):
        return {}
    conn = sqlite3.connect(path)
    try:
        return {r[0]: (r[1] or "") for r in conn.execute("SELECT id, abstract FROM papers")}
    finally:
        conn.close()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", default=os.path.join("..", "LDPC_Paper_Analysis"))
    ap.add_argument("--plugin", default=os.path.join("..", "AI_Assisted_Dev", "plugin", "scripts"))
    ap.add_argument("--root", default=".")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--fix-links", action="store_true", help="반입 없이 papers/analysis/*.md 의 바깥 링크만 글자로 바꾼다")
    args = ap.parse_args(argv)
    if args.fix_links:
        n = fix_outside_links(os.path.join(os.path.abspath(args.root), "papers", "analysis"))
        print(f"바깥 링크를 글자로 바꾼 파일 {n}개")
        return 0
    sys.path.insert(0, os.path.abspath(args.plugin))
    import paper_analyze  # noqa: E402
    import papers_db  # noqa: E402

    root = os.path.abspath(args.root)
    archive = os.path.abspath(args.archive)
    items = json.load(io.open(os.path.join(archive, "docs", "papers.json"), encoding="utf-8"))
    if not isinstance(items, list):
        items = next(v for v in items.values() if isinstance(v, list))
    if args.limit:
        items = items[:args.limit]
    abstracts = load_abstracts(archive)
    analysis_dir = os.path.join(root, "papers", "analysis")
    os.makedirs(analysis_dir, exist_ok=True)
    conn = papers_db.connect(papers_db.default_db_path(root))
    moved = migrate_versioned_arxiv_ids(conn, analysis_dir, paper_analyze.safe_name)
    if moved:
        print(f"옛 arXiv id {moved}건을 판 접미사 없는 id 로 옮김")
    pruned = prune_orphan_analysis(conn, analysis_dir, paper_analyze.safe_name)
    if pruned:
        print(f"papers 표에 없는 분석 행 {pruned}건과 그 md 사본을 지움")
    known = {r[0] for r in conn.execute("SELECT id FROM analysis")}
    inserted = skipped = copied = missing_md = 0
    started = time.time()
    for n, it in enumerate(items, start=1):
        archive_id = it["id"]
        row = dict(source_and_ids(archive_id), title=it.get("title") or archive_id, year=it.get("year"), venue=it.get("venue") or "",
                   abstract=abstracts.get(archive_id, ""))
        pid = papers_db.make_id(row)
        if papers_db.insert_paper(conn, row):
            inserted += 1
        else:  # 같은 DOI 나 같은 제목이 이미 있으면 그 논문의 id 아래에 분석을 붙인다
            skipped += 1
            found = conn.execute("SELECT id FROM papers WHERE id=? OR title_key=?",
                                 (pid, papers_db.normalize_title(row["title"]))).fetchone()
            if not found:
                continue
            pid = found[0]
        if pid in known:
            continue
        known.add(pid)
        data = {k: v for k, v in it.items() if k not in META_KEYS and v not in (None, "")}
        md_src = os.path.join(archive, it.get("md") or "")
        md_dst = os.path.join(analysis_dir, paper_analyze.safe_name(pid) + ".md")
        md_rel = None
        if it.get("md") and os.path.isfile(md_src):
            if not os.path.isfile(md_dst):
                shutil.copyfile(md_src, md_dst)
                copied += 1
            md_rel = os.path.relpath(md_dst, root).replace(os.sep, "/")
        else:
            missing_md += 1
        paper_analyze.record(conn, pid, data, md_rel)
        if n % 500 == 0:
            conn.commit()
            print(f"{n}/{len(items)} 처리, 새로 넣음 {inserted}, 사본 {copied}, {int(time.time() - started)}초", flush=True)
    conn.commit()
    conn.close()
    print(f"끝: 항목 {len(items)}, 새로 넣음 {inserted}, 이미 있음 {skipped}, 분석 md 사본 {copied}, md 없음 {missing_md}, {int(time.time() - started)}초")
    return 0


if __name__ == "__main__":
    sys.exit(main())
