#!/bin/bash
# Chép public/n3 (trang JLPT N3) sang 3 app Gino rồi commit + push từng repo.
# Dùng: bash src/n3/sync.sh "nội dung commit"
set -e
SRC=$(cd "$(dirname "$0")/../../public/n3" && pwd)
MSG=${1:-"JLPT N3: cập nhật đề / từ vựng"}
for R in /home/claude/gino-app /home/claude/gino-vesinhtoanha /home/claude/gino-cbtp-app; do
  [ -d "$R/.git" ] || { echo "bỏ qua $R"; continue; }
  cd "$R"; git pull -q --rebase || true
  rm -rf public/n3 && cp -r "$SRC" public/n3
  git add -A public/n3
  if ! git diff --cached --quiet; then
    git -c user.name="Vương Trọng Anh" -c user.email=tronganh8a@gmail.com commit -qm "$MSG

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01SJAnqGNP8tJV1MTSHQzNnF"
    git push -q origin main && echo "ok $R $(git rev-parse --short HEAD)"
  else echo "không đổi $R"; fi
done
