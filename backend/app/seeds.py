"""种子数据：预置程家湾红色地标信息"""
from app import db
from app.models import Site, Media, AudioGuide


def seed_data():
    """插入初始数据"""

    # ── 红色地标（程家湾核心景点）──
    sites_data = [
        {
            'name': '纪念馆',
            'description': (
                '程家湾红色纪念馆，集中展示了程家湾地区的革命历史与红色文化遗产。'
                '馆内陈列有珍贵的革命文物、图片史料和口述历史资料，'
                '是缅怀先烈、传承红色基因的重要教育基地。'
            ),
            'longitude': 117.88045,
            'latitude': 28.92844,
            'height': 175.0,
            'category': '纪念设施',
            'cover_image': '',
            'sort_order': 1,
        },
        {
            'name': '程家湾老人们的家',
            'description': (
                '赣东北传统民居建筑，青砖黛瓦马头墙，至今保存完好。'
                '革命年代曾为红军伤员提供掩护和治疗，村中老人世代守护红色记忆，'
                '讲述当年军民鱼水情深的感人故事。'
            ),
            'longitude': 117.88210,
            'latitude': 28.92944,
            'height': 171.4,
            'category': '居民生活',
            'cover_image': '',
            'sort_order': 2,
        },
        {
            'name': '碉堡',
            'description': (
                '建于制高点的防御工事，石头和泥土混合堆砌，开有扣眼朗朵（射击孔）。'
                '是程家湾突围战中的重要军事据点，至今仍可见当年战斗留下的弹痕。'
            ),
            'longitude': 117.88235,
            'latitude': 28.92964,
            'height': 174.9,
            'category': '军事遗址',
            'cover_image': '',
            'sort_order': 3,
        },
        {
            'name': '炮台',
            'description': (
                '位于村子东南侧山顶的火炮阵地，与碉堡遥相呼应形成交叉火力网。'
                '可俯瞰周边数公里范围，是当年红军控制要道、掩护撤退的关键制高点。'
            ),
            'longitude': 117.88170,
            'latitude': 28.92695,
            'height': 219.5,
            'category': '军事遗址',
            'cover_image': '',
            'sort_order': 4,
        },
        {
            'name': '程家湾突围指挥部',
            'description': (
                '闽浙赣省委在程家湾设立的临时指挥中心，方志敏等领导人曾在此制定突围计划。'
                '现建筑为原址复建，室内还原了当年指挥部的陈设和作战地图，'
                '是了解程家湾突围战全过程的核心展馆。'
            ),
            'longitude': 117.88075,
            'latitude': 28.92838,
            'height': 215.4,
            'category': '革命旧址',
            'cover_image': '',
            'sort_order': 5,
        },
        {
            'name': '胜利之门',
            'description': (
                '为纪念程家湾突围战胜利而建的标志性建筑，红色拱门气势恢宏。'
                '门楣镌刻"胜利之门"四个大字，两侧浮雕展现红军将士英勇作战的场景，'
                '是游客进入红色教育基地的第一站。'
            ),
            'longitude': 117.88045,
            'latitude': 28.92801,
            'height': 171.4,
            'category': '纪念设施',
            'cover_image': '',
            'sort_order': 6,
        },
        {
            'name': '程家湾广场',
            'description': (
                '村中心的开阔集会区，铺设红色广场砖，中央矗立革命烈士纪念碑。'
                '是举办红色教育活动、重温入党誓词的主要场所，周边配套有休息廊亭和宣传栏。'
            ),
            'longitude': 117.68216,
            'latitude': 28.92739,
            'height': 229.8,
            'category': '公共设施',
            'cover_image': '',
            'sort_order': 7,
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
