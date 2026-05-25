#!/usr/bin/env bash
set -euo pipefail

INPUT_FILE="${1:-research/raw/source_links.txt}"
OUTPUT_DIR="${2:-research/raw/subtitles}"

mkdir -p "$OUTPUT_DIR"

if [ ! -f "$INPUT_FILE" ]; then
  echo "Input file not found: $INPUT_FILE"
  exit 1
fi

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

sanitize_name() {
  local s="$1"
  s="${s//[^a-zA-Z0-9._-]/_}"
  echo "$s"
}

record() {
  local file="$1"
  local line="$2"
  echo "$line" >> "$file"
}

download_with_ytdlp() {
  local url="$1"
  local platform="$2"
  local outdir="$3"

  if ! command_exists yt-dlp; then
    echo "yt-dlp not found. Please install yt-dlp first."
    return 1
  fi

  local safe_platform
  safe_platform="$(sanitize_name "$platform")"

  yt-dlp \
    --write-auto-subs \
    --write-subs \
    --sub-langs "zh,zh-Hans,zh-Hant,en,en-US,en-GB" \
    --skip-download \
    --output "$outdir/${safe_platform}_%(title)s.%(ext)s" \
    "$url"
}

detect_platform() {
  local url="$1"
  if [[ "$url" == *"youtube.com"* || "$url" == *"youtu.be"* ]]; then
    echo "youtube"
  elif [[ "$url" == *"bilibili.com"* || "$url" == *"b23.tv"* ]]; then
    echo "bilibili"
  elif [[ "$url" == *"douyin.com"* || "$url" == *"iesdouyin.com"* ]]; then
    echo "douyin"
  else
    echo "unknown"
  fi
}

log_ok() {
  local platform="$1"
  local url="$2"
  echo "[$platform] OK: $url" | tee -a "$OUTPUT_DIR/download.log"
  record "$OUTPUT_DIR/downloaded_urls.txt" "$url"
}

log_fail() {
  local platform="$1"
  local url="$2"
  local reason="$3"
  echo "[$platform] FAIL: $url | $reason" | tee -a "$OUTPUT_DIR/download.log"
  record "$OUTPUT_DIR/failed_urls.txt" "$platform | $url | $reason"
}

download_youtube() {
  local url="$1"
  echo "[YouTube] $url" | tee -a "$OUTPUT_DIR/download.log"
  if download_with_ytdlp "$url" "youtube" "$OUTPUT_DIR"; then
    log_ok "YouTube" "$url"
  else
    log_fail "YouTube" "$url" "yt-dlp download failed"
  fi
}

download_bilibili() {
  local url="$1"
  echo "[Bilibili] $url" | tee -a "$OUTPUT_DIR/download.log"
  if download_with_ytdlp "$url" "bilibili" "$OUTPUT_DIR"; then
    log_ok "Bilibili" "$url"
  else
    log_fail "Bilibili" "$url" "yt-dlp download failed"
  fi
}

download_douyin() {
  local url="$1"
  echo "[Douyin] $url" | tee -a "$OUTPUT_DIR/download.log"
  if download_with_ytdlp "$url" "douyin" "$OUTPUT_DIR"; then
    log_ok "Douyin" "$url"
  else
    log_fail "Douyin" "$url" "yt-dlp download failed or subtitles unavailable"
  fi
}

download_unknown() {
  local url="$1"
  echo "[Unknown] $url" | tee -a "$OUTPUT_DIR/download.log"
  record "$OUTPUT_DIR/unknown_urls.txt" "$url"
  log_fail "Unknown" "$url" "unsupported platform"
}

: > "$OUTPUT_DIR/download.log"
: > "$OUTPUT_DIR/downloaded_urls.txt"
: > "$OUTPUT_DIR/failed_urls.txt"
: > "$OUTPUT_DIR/unknown_urls.txt"

while IFS= read -r url; do
  [ -z "$url" ] && continue
  [[ "$url" =~ ^# ]] && continue

  platform="$(detect_platform "$url")"

  case "$platform" in
    youtube) download_youtube "$url" ;;
    bilibili) download_bilibili "$url" ;;
    douyin) download_douyin "$url" ;;
    *) download_unknown "$url" ;;
  esac

done < "$INPUT_FILE"

echo "Done. Subtitle download stage finished."
echo "Output dir: $OUTPUT_DIR"
echo "Log: $OUTPUT_DIR/download.log"
echo "Downloaded: $OUTPUT_DIR/downloaded_urls.txt"
echo "Failed: $OUTPUT_DIR/failed_urls.txt"
echo "Unknown: $OUTPUT_DIR/unknown_urls.txt"
