#!/usr/bin/env bash
# Сборка финального ролика: рендер кадров → сведение звука → MP4 1080×1920, 30 fps, -14 LUFS
set -euo pipefail
H="$(cd "$(dirname "$0")" && pwd)"; W="${WORK:-$H/_build}"; mkdir -p "$W"
python3 "$H/timeline.py" >/dev/null
node "$H/../art/render.js" "$H/words_short.json" "$W" 30 4
python3 "$H/mix.py" "$W/mix.wav"
ffmpeg -loglevel error -y -i "$W/mix.wav" -af alimiter=limit=0.85:level=false "$W/mix_lim.wav"
M=$(ffmpeg -hide_banner -i "$W/mix_lim.wav" -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$M" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -loglevel error -y -i "$W/video_only.mp4" -i "$W/mix_lim.wav" -map 0:v -map 1:a -c:v copy \
  -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" \
  -ar 48000 -c:a aac -b:a 192k -movflags +faststart -shortest "$H/POTOP_s01.mp4"
echo "готово: $H/POTOP_s01.mp4"
