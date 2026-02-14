"""
一键同步脚本：将当前 MySQL 数据库中的数据自动写入 seeds.py
────────────────────────────────────────────────────────
用法：
    cd backend
    python sync_seeds.py

效果：
    1. 读取数据库中所有 Site、Media、AudioGuide 数据
    2. 自动重写 backend/app/seeds.py 文件（保留原有格式）
    3. 打印变更摘要

之后只需：
    git add app/seeds.py
    git commit -m "同步最新地标数据"
    git push
────────────────────────────────────────────────────────
"""
import os
import textwrap
from app import create_app, db
from app.models import Site, Media, AudioGuide


def generate_seeds_py(sites, media_list, audio_list):
    """根据数据库记录，生成完整的 seeds.py 文件内容"""

    lines = []
    lines.append('"""种子数据：预置程家湾红色地标信息（由 sync_seeds.py 自动生成）"""')
    lines.append('from app import db')
    lines.append('from app.models import Site, Media, AudioGuide')
    lines.append('')
    lines.append('')
    lines.append('def seed_data():')
    lines.append('    """插入初始数据"""')
    lines.append('')

    # ── Sites ──
    lines.append('    # ── 红色地标（程家湾核心景点）──')
    lines.append('    # 由 sync_seeds.py 从数据库自动导出，请勿手动修改')
    lines.append('    sites_data = [')

    for site in sites:
        lines.append('        {')
        lines.append(f"            'name': {repr(site.name)},")

        # 描述：格式化为多行
        desc = site.description or ''
        if desc:
            lines.append(f"            'description': (")
            # 按句号拆分为多行，每行不超过 76 字符
            chunks = _split_description(desc, max_len=72)
            for chunk in chunks:
                lines.append(f"                {repr(chunk)}")
            lines.append(f"            ),")
        else:
            lines.append(f"            'description': '',")

        lines.append(f"            'longitude': {_fmt_coord(site.longitude)},")
        lines.append(f"            'latitude': {_fmt_coord(site.latitude)},")
        lines.append(f"            'height': {_fmt_height(site.height)},")
        lines.append(f"            'category': {repr(site.category or '')},")
        lines.append(f"            'cover_image': {repr(site.cover_image or '')},")
        lines.append(f"            'sort_order': {site.sort_order or 0},")
        lines.append('        },')

    lines.append('    ]')
    lines.append('')
    lines.append('    for data in sites_data:')
    lines.append('        site = Site(**data)')
    lines.append('        db.session.add(site)')
    lines.append('')
    lines.append('    db.session.flush()  # 获取自增 ID')
    lines.append('')

    # ── Media ──
    # 按 site_id 分组，只导出有实际 url 的媒体记录
    real_media = [m for m in media_list if m.url and m.url.strip()]
    if real_media:
        lines.append('    # ── 媒体资源（从数据库导出） ──')
        lines.append('    media_data = [')
        for m in real_media:
            lines.append('        {')
            lines.append(f"            'site_id': {m.site_id},")
            lines.append(f"            'type': {repr(m.type)},")
            lines.append(f"            'url': {repr(m.url)},")
            lines.append(f"            'title': {repr(m.title or '')},")
            lines.append(f"            'description': {repr(m.description or '')},")
            lines.append(f"            'sort_order': {m.sort_order or 0},")
            lines.append('        },')
        lines.append('    ]')
        lines.append('')
        lines.append('    for data in media_data:')
        lines.append('        db.session.add(Media(**data))')
        lines.append('')
    else:
        lines.append('    # ── 媒体资源（暂无实际文件） ──')
        lines.append('')

    # ── AudioGuide ──
    real_audio = [a for a in audio_list if a.audio_url and a.audio_url.strip()]
    if real_audio:
        lines.append('    # ── 语音导览（从数据库导出） ──')
        lines.append('    audio_data = [')
        for a in real_audio:
            lines.append('        {')
            lines.append(f"            'site_id': {a.site_id},")
            lines.append(f"            'title': {repr(a.title or '')},")
            lines.append(f"            'audio_url': {repr(a.audio_url)},")
            lines.append(f"            'transcript': {repr(a.transcript or '')},")
            lines.append(f"            'duration': {a.duration or 0},")
            lines.append(f"            'sort_order': {a.sort_order or 0},")
            lines.append('        },')
        lines.append('    ]')
        lines.append('')
        lines.append('    for data in audio_data:')
        lines.append('        db.session.add(AudioGuide(**data))')
        lines.append('')
    else:
        lines.append('    # ── 语音导览（暂无实际文件） ──')
        lines.append('')

    lines.append('    db.session.commit()')
    lines.append(f"    print(f'✅ 种子数据插入完成：{{len(sites_data)}} 个地标')")
    lines.append('')

    return '\n'.join(lines) + '\n'


def _split_description(text, max_len=72):
    """将描述文本按句号/句末拆分为多行"""
    chunks = []
    while len(text) > max_len:
        # 优先在句号处断行
        split_at = text.rfind('。', 0, max_len)
        if split_at == -1:
            split_at = text.rfind('，', 0, max_len)
        if split_at == -1:
            split_at = max_len
        else:
            split_at += 1  # 包含标点
        chunks.append(text[:split_at])
        text = text[split_at:]
    if text:
        chunks.append(text)
    return chunks


def _fmt_coord(val):
    """格式化经纬度，保留 8 位小数"""
    if val is None:
        return '0.0'
    return f'{float(val):.8f}'


def _fmt_height(val):
    """格式化高度，保留 4 位小数"""
    if val is None:
        return '0.0'
    return f'{float(val):.4f}'


def main():
    app = create_app()
    with app.app_context():
        # 读取所有数据
        sites = Site.query.order_by(Site.sort_order, Site.id).all()
        media_list = Media.query.order_by(Media.site_id, Media.sort_order).all()
        audio_list = AudioGuide.query.order_by(AudioGuide.site_id, AudioGuide.sort_order).all()

        print(f'📊 数据库概览：')
        print(f'   地标: {len(sites)} 个')
        print(f'   媒体: {len(media_list)} 条（有文件: {sum(1 for m in media_list if m.url and m.url.strip())} 条）')
        print(f'   导览: {len(audio_list)} 条（有文件: {sum(1 for a in audio_list if a.audio_url and a.audio_url.strip())} 条）')
        print()

        # 生成 seeds.py 内容
        content = generate_seeds_py(sites, media_list, audio_list)

        # 写入文件
        seeds_path = os.path.join(os.path.dirname(__file__), 'app', 'seeds.py')
        
        # 读取旧文件用于对比
        old_content = ''
        if os.path.exists(seeds_path):
            with open(seeds_path, 'r', encoding='utf-8') as f:
                old_content = f.read()

        if content == old_content:
            print('✅ seeds.py 已经是最新的，无需更新。')
            return

        with open(seeds_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f'✅ seeds.py 已更新！({seeds_path})')
        print()
        print('📋 下一步操作：')
        print('   cd backend')
        print('   git add app/seeds.py ../backend/uploads/')
        print('   git commit -m "同步最新地标数据和图片"')
        print('   git push')


if __name__ == '__main__':
    main()
