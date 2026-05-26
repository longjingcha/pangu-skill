#!/usr/bin/env bash
# 从 YouTube 视频下载字幕并优先选择可用于盘古协议提炼的原始材料。
#
# 能力目标：
# - 优先人工字幕，其次自动字幕
# - 优先中文，其次英文，其它语言作为兜底
# - 避免依赖 find/tail 等不稳定的事后扫描
# - 输出稳定的 srt/vtt 文件路径，供后续转写脚本处理
#
# 用法:
#   ./download_subtitles.sh <YouTube_URL> [输出目录]
#
# 输出：
#   成功时打印下载到的字幕文件路径并退出 0
#   失败时打印可读错误并退出非 0

set -euo pipefail

URL="${1:-}"
OUTPUT_DIR="${2:-.}"

if [[ -z "$URL" ]]; then
  echo "用法: ./download_subtitles.sh <YouTube_URL> [输出目录]" >&2
  exit 1
fi

if ! command -v yt-dlp >/dev/null 2>&1; then
  echo "❌ 未找到 yt-dlp，请先安装后再试" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

normalize_title() {
  local title="$1"
  title="${title//\//_}"
  title="${title//:/_}"
  title="${title//\?/_}"
  title="${title//\*/_}"
  title="${title//\"/_}"
  title="${title//\</_}"
  title="${title//\>/_}"
  title="${title//\|/_}"
  printf '%s' "$title"
}

before_snapshot() {
  printf '%s\n' "$OUTPUT_DIR"/*.srt "$OUTPUT_DIR"/*.vtt 2>/dev/null | xargs -n1 basename 2>/dev/null | sort || true
}

after_snapshot() {
  printf '%s\n' "$OUTPUT_DIR"/*.srt "$OUTPUT_DIR"/*.vtt 2>/dev/null | xargs -n1 basename 2>/dev/null | sort || true
}

detect_new_file() {
  local before_file="$1"
  local after_file="$2"
  comm -13 "$before_file" "$after_file" | head -n 1
}

attempt_download() {
  local mode="$1"
  local langs="$2"
  local format="$3"
  local label="$4"

  echo ">>> $label"
  local before_file after_file new_name out_base
  before_file="$(mktemp)"
  after_file="$(mktemp)"
  before_snapshot > "$before_file"

  out_base="$OUTPUT_DIR/%(title).200B.%(ext)s"
  local write_auto_subs=()
  if [[ "$mode" == "auto" ]]; then
    write_auto_subs=(--write-auto-subs)
  fi

  if yt-dlp \
    --skip-download \
    --write-subs "${write_auto_subs[@]}" \
    --sub-langs "$langs" \
    --sub-format "$format" \
    -o "$out_base" \
    "$URL" >/dev/null 2>&1; then
    after_snapshot > "$after_file"
    new_name="$(detect_new_file "$before_file" "$after_file")"

    rm -f "$before_file" "$after_file"

    if [[ -n "$new_name" ]]; then
      printf '%s/%s\n' "$OUTPUT_DIR" "$new_name"
      return 0
    fi
  else
    rm -f "$before_file" "$after_file"
    return 1
  fi

  rm -f "$before_file" "$after_file"
  return 1
}

write_metadata() {
  local subtitle_path="$1"
  local mode="$2"
  local langs="$3"
  local format="$4"
  local metadata_path="$OUTPUT_DIR/$(basename "$subtitle_path").meta.json"

  cat > "$metadata_path" <<EOF
{
  "source_url": "${URL}",
  "subtitle_path": "${subtitle_path}",
  "download_mode": "${mode}",
  "language_priority": "${langs}",
  "subtitle_format": "${format}",
  "downloaded_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

  printf '%s\n' "$metadata_path"
}

echo ">>> 检查可用字幕..."
yt-dlp --list-subs --no-download "$URL" >/dev/null 2>&1 || true

# 说明：yt-dlp 自身会按站点/可用字幕生成字幕文件。
# 我们通过“下载前后目录差异”识别新生成文件，避免依赖临时 marker 或 find -newer。

# 1) 人工中文字幕
if result="$(attempt_download "manual" "zh-Hans,zh-Hant,zh,zh-CN,zh-TW" "srt/vtt" "尝试人工中文字幕（优先）")"; then
  meta_result="$(write_metadata "$result" "manual" "zh-Hans,zh-Hant,zh,zh-CN,zh-TW" "srt/vtt")"
  echo "✅ 下载成功: $result"
  echo "🧾 元信息: $meta_result"
  exit 0
fi

# 2) 人工英文字幕
if result="$(attempt_download "manual" "en,en-US,en-GB" "srt/vtt" "无中文人工字幕，尝试英文人工字幕")"; then
  meta_result="$(write_metadata "$result" "manual" "en,en-US,en-GB" "srt/vtt")"
  echo "✅ 下载成功: $result"
  echo "🧾 元信息: $meta_result"
  exit 0
fi

# 3) 自动生成中文字幕/英文字幕
if result="$(attempt_download "auto" "zh-Hans,zh,zh-CN,en" "srt/vtt" "无人工字幕，尝试自动生成字幕")"; then
  meta_result="$(write_metadata "$result" "auto" "zh-Hans,zh,zh-CN,en" "srt/vtt")"
  echo "✅ 自动字幕下载成功: $result"
  echo "🧾 元信息: $meta_result"
  exit 0
fi

# 4) 更宽松的兜底：任何可用字幕
if result="$(attempt_download "auto" "all" "srt/vtt" "最后兜底：尝试所有可用字幕")"; then
  meta_result="$(write_metadata "$result" "auto" "all" "srt/vtt")"
  echo "✅ 兜底字幕下载成功: $result"
  echo "🧾 元信息: $meta_result"
  exit 0
fi

echo "❌ 未找到任何可用字幕" >&2
echo "提示：" >&2
echo "- 可能该视频确实没有字幕" >&2
echo "- 可能站点限制了字幕下载" >&2
echo "- 可尝试更换视频或稍后重试" >&2
echo "- 你也可以先用原视频 URL 保留到 references/sources/ 里，后续再补抓" >&2
exit 1
