CREATE TABLE IF NOT EXISTS `routes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '路径名称',
  `description` text DEFAULT NULL COMMENT '路径描述',
  `points` json NOT NULL COMMENT '路径坐标点数组例如 [[lon, lat, height], ...]',
  `line_color` varchar(20) DEFAULT '#FF0000' COMMENT '线条颜色 hex',
  `width` int(11) DEFAULT 5 COMMENT '线条宽度',
  `is_visible` tinyint(1) DEFAULT 1 COMMENT '是否默认显示',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户自定义3D漫游路径';
