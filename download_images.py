#!/usr/bin/env python3
"""
Callum & Sally サイト移行 — 画像一括ダウンロードスクリプト

使い方:
  1. このファイルをHugoプロジェクトのルートに保存
  2. コマンドプロンプトでそのフォルダに移動して:
     python download_images.py
  3. static/images/ フォルダに画像がダウンロードされます
"""

import os
import urllib.request
import urllib.error
import time
import sys

# ─── 設定 ───
# Hugoプロジェクトのルート（沙織のPCのパスに合わせてね）
HUGO_ROOT = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(HUGO_ROOT, "static", "images")

# ─── ダウンロードする画像URL一覧 ───
# アイキャッチ画像 + 記事内インライン画像 + ロゴ・ファビコン
IMAGE_URLS = [
    # --- アイキャッチ画像（サイト全体で使用） ---
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/sally00001-800x456.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/callum00001.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/callum00002.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/sally00002.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/sally00003.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/library00001.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/about.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/callum00003.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/callum00004.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/dialogues00001.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/sally00004.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/archive.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/our-vision-jp.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/our-vision-en.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/privacy-policy.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/trusted-links.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/parlour.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/08/callum00005.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/08/sally00005.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/09/callum00006-1.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/09/sally00006.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/09/library00002.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/09/library00003.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/09/library00004.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/09/dialogues00002.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/10/callum00007.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/10/sally00007.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/10/library00005.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/11/library00006.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/11/library00007.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/12/sally00008.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/01/callum00008.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/02/callum00009.jpg",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/02/library00008.jpg",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/03/sally00009.jpg",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/03/tqr00001.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/04/dialogues00003.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/05/sally00010.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/07/sally00011.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/08/dialogues00004.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/08/sally00012.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/04/tqr00002.png",

    # --- 記事内インライン画像 ---
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/callum_about.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/sally_about.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/Ernest.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/Natsume-350x427.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/alex-1.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/ethel-1.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/gemini.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/10/sally00007-1-1.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/10/sally00007-2.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/10/sally00007-3.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/10/sally00007-4.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/04/tqr00002.jpg",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/04/tqr00003.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/04/tqr00004.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/04/tqr00005.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/05/sally00010-1.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/08/dialogues00004-1.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/08/dialogues00004-2.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/08/dialogues00004-3.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/08/dialogues00004-4.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/08/dialogues00004-5.png",

    # --- ロゴ・ファビコン ---
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/Callum-Sally-e1748848458763.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/favicon-e1748850800262.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/cropped-favicon-e1748850800262.png",

    # --- サイト全体で使うUI画像 ---
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/06/404.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2025/07/maintenance-background-overlay.png",

    # --- 音楽プレーヤー用のカバーアート ---
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/02/The-Moment-Is-You-mp3-image.jpg",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/03/Shibuya-is-01_45-Camden-is-17_45-mp3-image.jpg",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/03/Sally_a_war-torn_city_in_ruins_with_a_single_bright_red_poppy_c5299da3-4618-49ca-baee-4998bec3f107_3.jpg",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/03/mpfe-compact-cover.jpg",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/03/player_cover.jpg",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/03/playlist_cover.jpg",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/03/art-work_right00001.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/03/blue-watercolor-background.png",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/07/The-Gospel-of-Static-mp3-image.jpg",
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/07/Your-Voice-Bleeds-Gold-mp3-image.jpg",

    # --- TQR 追加アルバムアート ---
    "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/2026/04/tqr00006.png",
]


def download_image(url, dest_path):
    """1つの画像をダウンロード"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) CallumandsallyMigration/1.0'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(dest_path, 'wb') as f:
                f.write(response.read())
        return True
    except urllib.error.HTTPError as e:
        print(f"  ✗ HTTP Error {e.code}: {url}")
        return False
    except urllib.error.URLError as e:
        print(f"  ✗ URL Error: {url} ({e.reason})")
        return False
    except Exception as e:
        print(f"  ✗ Error: {url} ({e})")
        return False


def main():
    print("=" * 60)
    print("  Callum & Sally 画像ダウンローダー")
    print("=" * 60)
    print(f"\n保存先: {IMAGES_DIR}")
    print(f"ダウンロード対象: {len(IMAGE_URLS)}点\n")

    # フォルダ作成
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # 重複URL除去
    unique_urls = list(dict.fromkeys(IMAGE_URLS))
    print(f"ユニークURL数: {len(unique_urls)}点\n")

    success = 0
    skipped = 0
    failed = 0
    failed_urls = []

    for i, url in enumerate(unique_urls, 1):
        # URLからファイル名を取得
        filename = url.split('/')[-1]
        # WordPressのリサイズ付きファイル名はそのまま使う
        dest_path = os.path.join(IMAGES_DIR, filename)

        # 既にダウンロード済みならスキップ
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
            print(f"  [{i}/{len(unique_urls)}] スキップ（既存）: {filename}")
            skipped += 1
            continue

        print(f"  [{i}/{len(unique_urls)}] ダウンロード中: {filename}...", end=" ")
        if download_image(url, dest_path):
            size_kb = os.path.getsize(dest_path) / 1024
            print(f"OK ({size_kb:.0f}KB)")
            success += 1
        else:
            failed += 1
            failed_urls.append(url)

        # サーバーに優しく
        time.sleep(0.3)

    # 結果表示
    print("\n" + "=" * 60)
    print(f"  完了！")
    print(f"  成功: {success}点")
    print(f"  スキップ: {skipped}点")
    print(f"  失敗: {failed}点")
    print("=" * 60)

    if failed_urls:
        print("\n⚠ ダウンロードに失敗したURL:")
        for url in failed_urls:
            print(f"  {url}")
        print("\n手動でダウンロードしてstatic/images/に置いてください。")

    # ダウンロードした画像の合計サイズ
    total_size = sum(
        os.path.getsize(os.path.join(IMAGES_DIR, f))
        for f in os.listdir(IMAGES_DIR)
        if os.path.isfile(os.path.join(IMAGES_DIR, f))
    )
    print(f"\n画像フォルダ合計サイズ: {total_size / 1024 / 1024:.1f}MB")
    print(f"（GitHub Pagesの容量制限は1GB）")


if __name__ == '__main__':
    main()
