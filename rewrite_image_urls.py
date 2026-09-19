#!/usr/bin/env python3
"""
Callum & Sally サイト移行 — 画像URLをローカルパスに書き換え

使い方:
  download_images.py を実行した後に:
    python rewrite_image_urls.py

  content/ 内のMarkdownファイルにある WordPress画像URLを
  /images/ファイル名 に書き換えます。
  WordPress絵文字SVGはテキスト絵文字に変換します。
"""

import os
import re
import glob

# ─── 設定 ───
HUGO_ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(HUGO_ROOT, "content")
IMAGES_DIR = os.path.join(HUGO_ROOT, "static", "images")

# WordPressの画像URLのベースパス
WP_IMAGE_BASE = "https://callumandsally.littlestar.jp/wordpress/wp-content/uploads/"

# WordPress絵文字SVG → テキスト絵文字 変換マップ
EMOJI_MAP = {
    "https://s.w.org/images/core/emoji/16.0.1/svg/1f33b.svg": "🌻",
    "https://s.w.org/images/core/emoji/17.0.2/svg/1f332.svg": "🌲",
    "https://s.w.org/images/core/emoji/17.0.2/svg/1f4ab.svg": "💫",
    "https://s.w.org/images/core/emoji/17.0.2/svg/2744.svg": "❄️",
}


def rewrite_file(filepath):
    """1つのMarkdownファイル内の画像URLを書き換え"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = 0

    # 1. WordPress絵文字SVGをテキスト絵文字に変換
    #    ![emoji](https://s.w.org/images/core/emoji/...) → 絵文字テキスト
    for svg_url, emoji_char in EMOJI_MAP.items():
        # Markdown image syntax: ![alt](url)
        pattern = re.compile(r'!\[[^\]]*\]\(' + re.escape(svg_url) + r'\)')
        if pattern.search(content):
            content = pattern.sub(emoji_char, content)
            changes += 1
        # Also handle raw img tags that might have survived
        pattern2 = re.compile(r'<img[^>]*src="' + re.escape(svg_url) + r'"[^>]*/?>')
        if pattern2.search(content):
            content = pattern2.sub(emoji_char, content)
            changes += 1

    # 2. WordPress画像URLをローカルパスに変換
    #    front matter: image: "https://callumandsally.../filename.png"
    #    → image: "/images/filename.png"
    #
    #    本文: ![alt](https://callumandsally.../filename.png)
    #    → ![alt](/images/filename.png)
    def replace_wp_url(match):
        full_url = match.group(0)
        filename = full_url.split('/')[-1]
        # ダウンロード済みか確認
        local_path = os.path.join(IMAGES_DIR, filename)
        if os.path.exists(local_path):
            return "/images/" + filename
        else:
            # ファイルが見つからない場合はそのまま残す
            print(f"    ⚠ 未ダウンロード: {filename} （URLをそのまま残します）")
            return full_url

    wp_url_pattern = re.compile(
        re.escape(WP_IMAGE_BASE) + r'[^\s"\)]+\.(png|jpg|jpeg|gif|webp)',
        re.IGNORECASE
    )
    content_new = wp_url_pattern.sub(replace_wp_url, content)
    if content_new != content:
        changes += 1
        content = content_new

    # 3. 内部リンクのURL書き換え（記事間リンク）
    #    https://callumandsally.littlestar.jp/カテゴリ/スラッグ/ → /posts/スラッグ/
    #    これは後で個別対応が必要かもなので、今はスキップ

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    return 0


def main():
    print("=" * 60)
    print("  画像URL書き換えツール")
    print("=" * 60)

    # static/images/ の存在確認
    if not os.path.exists(IMAGES_DIR):
        print(f"\n✗ {IMAGES_DIR} が見つかりません。")
        print("  先に download_images.py を実行してください。")
        return

    downloaded_count = len([
        f for f in os.listdir(IMAGES_DIR)
        if os.path.isfile(os.path.join(IMAGES_DIR, f))
    ])
    print(f"\nダウンロード済み画像: {downloaded_count}点")

    # Markdownファイルを収集
    md_files = []
    for root, dirs, files in os.walk(CONTENT_DIR):
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))

    print(f"対象Markdownファイル: {len(md_files)}本\n")

    modified = 0
    for filepath in sorted(md_files):
        relpath = os.path.relpath(filepath, HUGO_ROOT)
        changes = rewrite_file(filepath)
        if changes > 0:
            print(f"  ✓ {relpath} ({changes}箇所)")
            modified += 1

    print(f"\n書き換え完了: {modified}ファイルを更新しました")


if __name__ == '__main__':
    main()
