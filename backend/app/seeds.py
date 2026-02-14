"""种子数据：预置程家湾红色地标信息（由 sync_seeds.py 自动生成）"""
from app import db
from app.models import Site, Media, AudioGuide


def seed_data():
    """插入初始数据"""

    # ── 红色地标（程家湾核心景点）──
    # 由 sync_seeds.py 从数据库自动导出，请勿手动修改
    sites_data = [
        {
            'name': '程家湾老人们的家',
            'description': (
                '程家湾村中老人们的聚居地，这里依山而建的民居保留着赣东北传统建筑风格。'
                '革命年代，村民们曾在此掩护红军伤员、传递情报，为闽浙赣革命根据地的巩固发展作出了重要贡献。如今仍有部分老人在此居住，守护着这片红色土地上的记忆。'
            ),
            'longitude': 117.88209415,
            'latitude': 28.92901258,
            'height': 171.4256,
            'category': '居民生活',
            'cover_image': '/uploads/20260213161822_d2d934d3.png',
            'sort_order': 0,
        },
        {
            'name': '碉堡',
            'description': (
                '程家湾碉堡位于村子制高点，是闽浙赣革命根据地时期红军为抵御外敌侵犯而修建的防御工事。'
                '碉堡以石头和泥土堆砖而成，扣眼朗朵清晰可见，充分利用了山地地形优势，是程家湾作为红军战略要地的重要物证。'
            ),
            'longitude': 117.88216000,
            'latitude': 28.92739000,
            'height': 229.8000,
            'category': '军事遗址',
            'cover_image': '',
            'sort_order': 0,
        },
        {
            'name': '炮台',
            'description': (
                '红军炮台遗址位于程家湾山顶附近，居高临下视野开阔。当年红军在此架设火炮阵地，扮演着保卫根据地、掩护部队转移的关键角色。'
                '炮台遗址与碜堡遥相呼应，共同构成了程家湾的红军防御体系。'
            ),
            'longitude': 117.88170000,
            'latitude': 28.92695000,
            'height': 219.5000,
            'category': '军事遗址',
            'cover_image': '',
            'sort_order': 0,
        },
        {
            'name': '程家湾突围指挥部',
            'description': (
                '程家湾突围指挥部是闽浙赣省委和红军在程家湾战斗期间的核心指挥中心。当年红军将领在此制定突围作战计划，组织部队实施战略转移。'
                '作为重要的军事指挥地点，它见证了红军在困境中英勇不屈的革命精神。'
            ),
            'longitude': 117.88210821,
            'latitude': 28.92943888,
            'height': 174.8743,
            'category': '革命旧址',
            'cover_image': '/uploads/20260213161238_1b35346e.png',
            'sort_order': 0,
        },
        {
            'name': '胜利之门',
            'description': (
                '胜利之门是为纪念程家湾突围战胜利而建造的标志性建筑，位于进入村庄的主通道口。'
                '门楼巨大庄严，象征着革命先烈为民族解放事业所取得的伟大胜利，是进入程家湾红色教育基地的第一站。'
            ),
            'longitude': 117.88075000,
            'latitude': 28.92838000,
            'height': 168.4000,
            'category': '纪念设施',
            'cover_image': '/uploads/20260213160138_b2f8ac0a.png',
            'sort_order': 0,
        },
        {
            'name': '程家湾广场',
            'description': (
                '程家湾广场是村中的中心集会区，也是红色教育活动的主要场所。广场周围布局有红色文化展示标识，是参观者集合出发、了解程家湾革命历史的起点。'
            ),
            'longitude': 117.88225000,
            'latitude': 28.92964000,
            'height': 171.0000,
            'category': '公共设施',
            'cover_image': '',
            'sort_order': 0,
        },
        {
            'name': '程家湾广场',
            'description': (
                '程家湾广场是村中的中心集会区，也是红色教育活动的主要场所。广场周围布局有红色文化展示标识。'
            ),
            'longitude': 117.88225000,
            'latitude': 28.92964000,
            'height': 171.0000,
            'category': '公共设施',
            'cover_image': '/uploads/20260213162055_28d96087.jpg',
            'sort_order': 0,
        },
        {
            'name': '程家湾红色纪念馆',
            'description': (
                '程家湾红色纪念馆，集中展示了程家湾地区的革命历史与红色文化遗产。'
                '馆内陈列有珍贵的革命文物、图片史料和口述历史资料，是缅怀先烈、传承红色基因的重要教育基地。'
            ),
            'longitude': 117.88044967,
            'latitude': 28.92843615,
            'height': 175.0251,
            'category': '纪念设施',
            'cover_image': '/uploads/20260213133748_50216999.jpg',
            'sort_order': 1,
        },
    ]

    for data in sites_data:
        site = Site(**data)
        db.session.add(site)

    db.session.flush()  # 获取自增 ID

    # ── 媒体资源（从数据库导出） ──
    media_data = [
        {
            'site_id': 1,
            'type': 'image',
            'url': '/uploads/20260213155616_75ff592c.png',
            'title': '大厅.png',
            'description': '',
            'sort_order': 0,
        },
        {
            'site_id': 1,
            'type': 'image',
            'url': '/uploads/20260213155622_ca773d63.png',
            'title': '字牌.png',
            'description': '',
            'sort_order': 1,
        },
        {
            'site_id': 1,
            'type': 'image',
            'url': '/uploads/20260213155627_3f397bbc.png',
            'title': '中间.png',
            'description': '',
            'sort_order': 2,
        },
        {
            'site_id': 1,
            'type': 'image',
            'url': '/uploads/20260213155632_8b452af6.jpg',
            'title': '结束.jpg',
            'description': '',
            'sort_order': 3,
        },
        {
            'site_id': 2,
            'type': 'image',
            'url': '/uploads/20260213161828_b6f13dea.png',
            'title': '门牌.png',
            'description': '',
            'sort_order': 0,
        },
        {
            'site_id': 2,
            'type': 'image',
            'url': '/uploads/20260213161833_c651a8eb.jpg',
            'title': '老人.jpg',
            'description': '',
            'sort_order': 1,
        },
        {
            'site_id': 5,
            'type': 'image',
            'url': '/uploads/20260213161249_722aecff.png',
            'title': '旗子.png',
            'description': '',
            'sort_order': 0,
        },
        {
            'site_id': 5,
            'type': 'image',
            'url': '/uploads/20260213161255_99b06208.png',
            'title': '大厅.png',
            'description': '',
            'sort_order': 1,
        },
        {
            'site_id': 5,
            'type': 'image',
            'url': '/uploads/20260213161300_14fa8c6f.png',
            'title': '名字.png',
            'description': '',
            'sort_order': 2,
        },
        {
            'site_id': 5,
            'type': 'image',
            'url': '/uploads/20260213161305_8841f9d8.png',
            'title': '卧室.png',
            'description': '',
            'sort_order': 3,
        },
    ]

    for data in media_data:
        db.session.add(Media(**data))

    # ── 语音导览（暂无实际文件） ──

    db.session.commit()
    print(f'✅ 种子数据插入完成：{len(sites_data)} 个地标')

