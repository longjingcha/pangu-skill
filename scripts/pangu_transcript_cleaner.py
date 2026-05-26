#!/usr/bin/env python3
"""
将 SRT/VTT 字幕文件转写为适合盘古协议提炼的纯文本 transcript。

目标：
- 去除时间戳、序号、HTML 标签、NOTE 块、重复行
- 保留段落与说话节奏
- 为后续人物协议 / 领域协议提炼提供干净材料
- 同时输出元信息，方便来源追溯

用法:
    python3 srt_to_transcript.py input.srt [output.txt]
    python3 srt_to_transcript.py input.vtt [output.txt]

如果不指定输出文件，默认输出到 input_transcript.txt
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple


TIME_RE = re.compile(r"^\d{1,2}:\d{2}:\d{2}[\.,]\d{3}\s+-->\s+\d{1,2}:\d{2}:\d{2}[\.,]\d{3}")
SRT_ALT_TIME_RE = re.compile(r"^\d{2}:\d{2}:\d{2}\s+-->\s+\d{2}:\d{2}:\d{2}")
WEBVTT_HEADER_RE = re.compile(r"^WEBVTT.*?(?:\n\n|\r\n\r\n)", re.DOTALL)
NOTE_BLOCK_RE = re.compile(r"(?ms)^NOTE.*?(?=\n\n|\Z)")
TAG_RE = re.compile(r"<[^>]+>")
POSITION_RE = re.compile(r"(?:align|position|line|vertical|size|region):[^\s]+")
SPEAKER_RE = re.compile(r"^[A-Za-z0-9_\- ]{1,30}:\s*")
INLINE_SPACES_RE = re.compile(r"[ \t]{2,}")
DASH_SPEAKER_RE = re.compile(r"^[-–—]\s+")


def normalize_newlines(content: str) -> str:
    return content.replace("\r\n", "\n").replace("\r", "\n")



def strip_markup(line: str) -> str:
    line = TAG_RE.sub("", line)
    line = POSITION_RE.sub("", line)
    line = line.replace("\u200b", "")
    line = INLINE_SPACES_RE.sub(" ", line)
    return line.strip()



def is_noise_line(line: str) -> bool:
    if not line:
        return True
    if re.match(r"^\d+$", line):
        return True
    if TIME_RE.match(line) or SRT_ALT_TIME_RE.match(line):
        return True
    if line.startswith("WEBVTT"):
        return True
    return False



def remove_headers(content: str) -> str:
    content = WEBVTT_HEADER_RE.sub("", content, count=1)
    content = NOTE_BLOCK_RE.sub("", content)
    return content



def split_lines(content: str) -> List[str]:
    return [line.strip() for line in content.split("\n")]



def collapse_duplicates(lines: List[str]) -> List[str]:
    deduped: List[str] = []
    for line in lines:
        if not deduped or line != deduped[-1]:
            deduped.append(line)
    return deduped



def normalize_line(line: str) -> str:
    line = strip_markup(line)
    line = DASH_SPEAKER_RE.sub("", line)
    line = SPEAKER_RE.sub("", line)
    line = line.replace("\u3000", " ")
    line = INLINE_SPACES_RE.sub(" ", line)
    return line.strip()



def join_to_paragraphs(lines: List[str]) -> str:
    """按句末标点、长度和空行信息重组段落。"""
    paragraphs: List[str] = []
    current: List[str] = []

    def flush() -> None:
        nonlocal current
        if current:
            paragraphs.append(" ".join(current).strip())
            current = []

    for raw in lines:
        line = normalize_line(raw)
        if not line:
            flush()
            continue

        current.append(line)
        joined = " ".join(current)
        if len(joined) >= 220 or re.search(r"[。！？!?\.]$", line):
            flush()

    flush()

    # 合并过短且连续的段落，避免字幕切碎
    merged: List[str] = []
    for para in paragraphs:
        if not merged:
            merged.append(para)
            continue
        if len(merged[-1]) < 80 and len(para) < 80:
            merged[-1] = merged[-1] + " " + para
        else:
            merged.append(para)

    return "\n\n".join(p for p in merged if p)



def clean_srt(content: str) -> str:
    content = normalize_newlines(content)
    content = remove_headers(content)
    lines = split_lines(content)

    texts: List[str] = []
    for line in lines:
        line = strip_markup(line)
        if is_noise_line(line):
            continue
        texts.append(line)

    texts = collapse_duplicates(texts)
    return join_to_paragraphs(texts)



def clean_vtt(content: str) -> str:
    return clean_srt(content)



def detect_output_path(input_path: Path, provided: str | None) -> Path:
    if provided:
        return Path(provided)
    return input_path.parent / f"{input_path.stem}_transcript.txt"



def write_metadata(input_path: Path, output_path: Path, transcript: str) -> Path:
    meta_path = output_path.with_suffix(output_path.suffix + ".meta.json")
    payload = {
        "source_path": str(input_path),
        "transcript_path": str(output_path),
        "source_kind": "vtt" if input_path.suffix.lower() == ".vtt" else "srt",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "char_count": len(transcript),
        "paragraph_count": len([p for p in transcript.split("\n\n") if p.strip()]),
        "line_count": transcript.count("\n") + (1 if transcript else 0),
    }
    meta_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta_path



def main() -> None:
    if len(sys.argv) < 2:
        print("用法: python3 srt_to_transcript.py <input.srt|input.vtt> [output.txt]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"❌ 文件不存在: {input_path}")
        sys.exit(1)

    output_path = detect_output_path(input_path, sys.argv[2] if len(sys.argv) >= 3 else None)
    content = input_path.read_text(encoding="utf-8")

    if input_path.suffix.lower() == ".vtt" or content.lstrip().startswith("WEBVTT"):
        transcript = clean_vtt(content)
    else:
        transcript = clean_srt(content)

    output_path.write_text(transcript, encoding="utf-8")
    meta_path = write_metadata(input_path, output_path, transcript)

    char_count = len(transcript)
    para_count = len([p for p in transcript.split("\n\n") if p.strip()])
    line_count = transcript.count("\n") + (1 if transcript else 0)

    print(f"✅ 转换完成: {output_path}")
    print(f"🧾 元信息: {meta_path}")
    print(f"   字数: {char_count}  段落数: {para_count}  行数: {line_count}")


if __name__ == "__main__":
    main()
