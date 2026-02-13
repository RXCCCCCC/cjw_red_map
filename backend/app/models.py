from datetime import datetime
from app import db


class Site(db.Model):
    """红色遗址"""
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment='遗址名称')
    description = db.Column(db.Text, comment='遗址简介')
    longitude = db.Column(db.Numeric(12, 8), nullable=False, comment='经度 WGS84')
    latitude = db.Column(db.Numeric(12, 8), nullable=False, comment='纬度 WGS84')
    height = db.Column(db.Numeric(10, 4), default=0, comment='高度(米) 用于3D标注')
    category = db.Column(db.String(50), comment='分类')
    icon = db.Column(db.String(200), default='', comment='地图图标URL')
    cover_image = db.Column(db.String(200), default='', comment='封面图URL')
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    media = db.relationship('Media', backref='site', lazy='dynamic', cascade='all, delete-orphan')
    audio_guides = db.relationship('AudioGuide', backref='site', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'longitude': float(self.longitude) if self.longitude is not None else None,
            'latitude': float(self.latitude) if self.latitude is not None else None,
            'height': float(self.height) if self.height else 0,
            'category': self.category,
            'icon': self.icon,
            'cover_image': self.cover_image,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Media(db.Model):
    """媒体资源 (图片/音频/视频)"""
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False, comment='关联遗址')
    type = db.Column(db.Enum('image', 'audio', 'video'), nullable=False, comment='媒体类型')
    url = db.Column(db.String(300), nullable=False, comment='资源路径')
    title = db.Column(db.String(200), default='', comment='标题')
    description = db.Column(db.Text, comment='描述')
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'site_id': self.site_id,
            'type': self.type,
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class AudioGuide(db.Model):
    """语音导览"""
    __tablename__ = 'audio_guides'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False, comment='关联遗址')
    title = db.Column(db.String(200), nullable=False, comment='导览标题')
    audio_url = db.Column(db.String(300), nullable=False, comment='音频路径')
    transcript = db.Column(db.Text, comment='文字稿')
    duration = db.Column(db.Integer, default=0, comment='时长(秒)')
    sort_order = db.Column(db.Integer, default=0, comment='排序')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'site_id': self.site_id,
            'title': self.title,
            'audio_url': self.audio_url,
            'transcript': self.transcript,
            'duration': self.duration,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
