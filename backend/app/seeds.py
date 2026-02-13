"""种子数据：预置程家湾红色地标信息"""
from app import db
from app.models import Site, Media, AudioGuide


def seed_data():
    """插入初始数据"""

    # ── 红色地标 ──
    sites_data = [
        {
            'name': '纪念馆',
            'description': (
                '程家湾红色纪念馆，集中展示了程家湾地区的革命历史与红色文化遗产。'
                '馆内陈列有珍贵的革命文物、图片史料和口述历史资料，'
                '是缅怀先烈、传承红色基因的重要教育基地。'
            ),
            'longitude': 117.88044,
            'latitude': 28.92844,
            'height': 177.12,
            'category': '纪念设施',
            'cover_image': '',
            'sort_order': 1,
        },
    ]

    for data in sites_data:
        site = Site(**data)
        db.session.add(site)

    db.session.flush()  # 获取自增 ID

    # ── 媒体资源（示例占位） ──
    all_sites = Site.query.all()
    for site in all_sites:
        # 每个地标添加一张占位图片记录
        db.session.add(Media(
            site_id=site.id,
            type='image',
            url='',
            title=f'{site.name} - 现场照片',
            description=f'{site.name}的实地拍摄照片',
            sort_order=1,
        ))

    # ── 语音导览（示例占位） ──
    for site in all_sites:
        db.session.add(AudioGuide(
            site_id=site.id,
            title=f'{site.name} - 语音讲解',
            audio_url='',
            transcript=site.description,
            duration=60,
            sort_order=1,
        ))

    db.session.commit()
    print(f'✅ 种子数据插入完成：{len(all_sites)} 个地标')
