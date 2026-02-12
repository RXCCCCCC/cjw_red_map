"""种子数据：预置程家湾红色遗址信息"""
from app import db
from app.models import Site, Media, AudioGuide


def seed_data():
    """插入初始数据"""

    # ── 遗址 ──
    sites_data = [
        {
            'name': '红军医院旧址',
            'description': (
                '程家湾红军医院旧址，始建于土地革命战争时期。'
                '当年红军在此设立战地医院，救治伤病员，是闽浙赣革命根据地重要的后勤保障设施。'
                '建筑为典型赣东北民居风格，青砖黛瓦，至今保存较为完好。'
            ),
            'longitude': 117.8960,
            'latitude': 28.8150,
            'category': '医院',
            'cover_image': '',
            'sort_order': 1,
        },
        {
            'name': '红军炮台',
            'description': (
                '红军炮台位于程家湾村东侧高地，扼守交通要道。'
                '土地革命时期，红军在此修筑防御工事，居高临下，有效阻击了敌军多次进攻。'
                '炮台遗迹至今可见夯土基座与射击掩体，是研究红军防御战术的珍贵实物。'
            ),
            'longitude': 117.8975,
            'latitude': 28.8140,
            'category': '军事设施',
            'cover_image': '',
            'sort_order': 2,
        },
        {
            'name': '红军路',
            'description': (
                '红军路是当年红军行军、运输物资的主要通道，蜿蜒穿过程家湾村落。'
                '路面由青石板铺就，两侧山林茂密。沿途可见多处红军标语石刻，'
                '见证了那段烽火岁月。如今已成为红色研学的重要徒步线路。'
            ),
            'longitude': 117.8950,
            'latitude': 28.8165,
            'category': '道路',
            'cover_image': '',
            'sort_order': 3,
        },
        {
            'name': '程家湾村口',
            'description': (
                '程家湾村口是进入红色遗址群的起点，设有村庄标识牌。'
                '村口古樟树下曾是红军集合、宣传的场所。'
                '如今这里是游客集散中心，从此处可步行前往各处红色遗址。'
            ),
            'longitude': 117.8940,
            'latitude': 28.8155,
            'category': '地标',
            'cover_image': '',
            'sort_order': 4,
        },
    ]

    for data in sites_data:
        site = Site(**data)
        db.session.add(site)

    db.session.flush()  # 获取自增 ID

    # ── 媒体资源（示例占位） ──
    all_sites = Site.query.all()
    for site in all_sites:
        # 每个遗址添加一张占位图片记录
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
    print(f'✅ 种子数据插入完成：{len(all_sites)} 个遗址')
