-- =====================================================
-- 智选未来 - 高考志愿辅助填报系统
-- 数据库初始化脚本
-- =====================================================

-- 创建数据库
DROP DATABASE IF EXISTS gaokao_ai;
CREATE DATABASE gaokao_ai DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE gaokao_ai;

-- =====================================================
-- 1. 省份表 (Province)
-- =====================================================
CREATE TABLE `province` (
    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '省份ID',
    `name` VARCHAR(50) NOT NULL COMMENT '省份名称',
    `code` VARCHAR(10) NOT NULL COMMENT '省份代码',
    `region` VARCHAR(20) COMMENT '所属区域：华北、东北、华东、华中、华南、西南、西北',
    `is_new_gaokao` TINYINT DEFAULT 0 COMMENT '是否新高考省份：0-否，1-是',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `uk_code` (`code`),
    UNIQUE KEY `uk_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='省份表';

-- =====================================================
-- 2. 城市表 (City)
-- =====================================================
CREATE TABLE `city` (
    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '城市ID',
    `name` VARCHAR(50) NOT NULL COMMENT '城市名称',
    `code` VARCHAR(10) NOT NULL COMMENT '城市代码',
    `province_id` INT NOT NULL COMMENT '所属省份ID',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `uk_code` (`code`),
    INDEX `idx_province_id` (`province_id`),
    CONSTRAINT `fk_city_province` FOREIGN KEY (`province_id`) REFERENCES `province` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='城市表';

-- =====================================================
-- 3. 用户表 (User)
-- =====================================================
CREATE TABLE `user` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(50) NOT NULL COMMENT '用户名',
    `password` VARCHAR(255) NOT NULL COMMENT '密码(BCrypt加密)',
    `real_name` VARCHAR(50) COMMENT '真实姓名',
    `phone` VARCHAR(20) COMMENT '手机号',
    `email` VARCHAR(100) COMMENT '邮箱',
    `gender` TINYINT DEFAULT 0 COMMENT '性别：0-未知，1-男，2-女',
    `avatar` VARCHAR(500) COMMENT '头像URL',
    `province_id` INT COMMENT '所在省份ID',
    `city_id` INT COMMENT '所在城市ID',
    `score` INT COMMENT '高考分数',
    `ranking` INT COMMENT '省排名/位次',
    `subject_type` TINYINT COMMENT '科类：1-文科，2-理科，3-综合改革',
    `graduation_year` INT COMMENT '毕业年份',
    `status` TINYINT DEFAULT 1 COMMENT '状态：0-禁用，1-正常',
    `last_login_time` DATETIME COMMENT '最后登录时间',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted` TINYINT DEFAULT 0 COMMENT '逻辑删除：0-未删除，1-已删除',
    UNIQUE KEY `uk_username` (`username`),
    UNIQUE KEY `uk_phone` (`phone`),
    UNIQUE KEY `uk_email` (`email`),
    INDEX `idx_province_id` (`province_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_graduation_year` (`graduation_year`),
    CONSTRAINT `fk_user_province` FOREIGN KEY (`province_id`) REFERENCES `province` (`id`),
    CONSTRAINT `fk_user_city` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- =====================================================
-- 4. 管理员表 (Admin)
-- =====================================================
CREATE TABLE `admin` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '管理员ID',
    `username` VARCHAR(50) NOT NULL COMMENT '用户名',
    `password` VARCHAR(255) NOT NULL COMMENT '密码(BCrypt加密)',
    `real_name` VARCHAR(50) COMMENT '真实姓名',
    `phone` VARCHAR(20) COMMENT '手机号',
    `email` VARCHAR(100) COMMENT '邮箱',
    `role` TINYINT DEFAULT 1 COMMENT '角色：1-普通管理员，2-超级管理员',
    `avatar` VARCHAR(500) COMMENT '头像URL',
    `status` TINYINT DEFAULT 1 COMMENT '状态：0-禁用，1-正常',
    `last_login_time` DATETIME COMMENT '最后登录时间',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted` TINYINT DEFAULT 0 COMMENT '逻辑删除：0-未删除，1-已删除',
    UNIQUE KEY `uk_username` (`username`),
    UNIQUE KEY `uk_phone` (`phone`),
    INDEX `idx_role` (`role`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管理员表';

-- =====================================================
-- 5. 高校表 (School)
-- =====================================================
CREATE TABLE `school` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '高校ID',
    `name` VARCHAR(100) NOT NULL COMMENT '高校名称',
    `code` VARCHAR(20) COMMENT '高校代码(教育部编码)',
    `province_id` INT COMMENT '所在省份ID',
    `city_id` INT COMMENT '所在城市ID',
    `address` VARCHAR(255) COMMENT '详细地址',
    `type` TINYINT COMMENT '类型：1-综合，2-理工，3-师范，4-医药，5-财经，6-政法，7-农林，8-艺术，9-体育，10-民族，11-军事',
    `level` TINYINT COMMENT '层次：1-本科，2-专科',
    `nature` TINYINT COMMENT '性质：1-公办，2-民办，3-中外合作',
    `is_985` TINYINT DEFAULT 0 COMMENT '是否985：0-否，1-是',
    `is_211` TINYINT DEFAULT 0 COMMENT '是否211：0-否，1-是',
    `is_double_first_class` TINYINT DEFAULT 0 COMMENT '是否双一流：0-否，1-是',
    `website` VARCHAR(255) COMMENT '官网地址',
    `logo` VARCHAR(500) COMMENT '校徽URL',
    `description` TEXT COMMENT '学校简介',
    `ranking` INT COMMENT '综合排名',
    `student_count` INT COMMENT '在校生人数',
    `faculty_count` INT COMMENT '教职工人数',
    `status` TINYINT DEFAULT 1 COMMENT '状态：0-禁用，1-正常',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted` TINYINT DEFAULT 0 COMMENT '逻辑删除：0-未删除，1-已删除',
    UNIQUE KEY `uk_code` (`code`),
    INDEX `idx_province_id` (`province_id`),
    INDEX `idx_city_id` (`city_id`),
    INDEX `idx_type` (`type`),
    INDEX `idx_level` (`level`),
    INDEX `idx_is_985` (`is_985`),
    INDEX `idx_is_211` (`is_211`),
    INDEX `idx_is_double_first_class` (`is_double_first_class`),
    INDEX `idx_ranking` (`ranking`),
    CONSTRAINT `fk_school_province` FOREIGN KEY (`province_id`) REFERENCES `province` (`id`),
    CONSTRAINT `fk_school_city` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='高校表';

-- =====================================================
-- 6. 专业表 (Major)
-- =====================================================
CREATE TABLE `major` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '专业ID',
    `name` VARCHAR(100) NOT NULL COMMENT '专业名称',
    `code` VARCHAR(20) COMMENT '专业代码',
    `category` VARCHAR(50) COMMENT '专业大类',
    `sub_category` VARCHAR(50) COMMENT '专业小类',
    `subject_requirements` VARCHAR(200) COMMENT '选科要求(新高考)',
    `duration` TINYINT COMMENT '学制：3-三年，4-四年，5-五年',
    `degree` VARCHAR(50) COMMENT '授予学位',
    `description` TEXT COMMENT '专业介绍',
    `employment_direction` TEXT COMMENT '就业方向',
    `salary_range` VARCHAR(50) COMMENT '薪资范围',
    `is_special` TINYINT DEFAULT 0 COMMENT '是否特色专业：0-否，1-是',
    `status` TINYINT DEFAULT 1 COMMENT '状态：0-禁用，1-正常',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted` TINYINT DEFAULT 0 COMMENT '逻辑删除：0-未删除，1-已删除',
    INDEX `idx_code` (`code`),
    INDEX `idx_category` (`category`),
    INDEX `idx_sub_category` (`sub_category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='专业表';

-- =====================================================
-- 7. 高校专业关联表 (SchoolMajor)
-- =====================================================
CREATE TABLE `school_major` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `school_id` BIGINT NOT NULL COMMENT '高校ID',
    `major_id` BIGINT NOT NULL COMMENT '专业ID',
    `ranking` INT COMMENT '专业排名',
    `is_key` TINYINT DEFAULT 0 COMMENT '是否重点学科：0-否，1-是',
    `is_national_key` TINYINT DEFAULT 0 COMMENT '是否国家重点学科：0-否，1-是',
    `tuition` DECIMAL(10,2) COMMENT '学费(元/年)',
    `remark` VARCHAR(500) COMMENT '备注',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `uk_school_major` (`school_id`, `major_id`),
    INDEX `idx_school_id` (`school_id`),
    INDEX `idx_major_id` (`major_id`),
    CONSTRAINT `fk_school_major_school` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`),
    CONSTRAINT `fk_school_major_major` FOREIGN KEY (`major_id`) REFERENCES `major` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='高校专业关联表';

-- =====================================================
-- 8. 历年录取数据表 (AdmissionScore)
-- =====================================================
CREATE TABLE `admission_score` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `school_id` BIGINT NOT NULL COMMENT '高校ID',
    `major_id` BIGINT COMMENT '专业ID(为空表示院校分数线)',
    `year` INT NOT NULL COMMENT '年份',
    `province_id` INT NOT NULL COMMENT '招生省份ID',
    `subject_type` TINYINT NOT NULL COMMENT '科类：1-文科，2-理科，3-综合改革',
    `batch` VARCHAR(50) COMMENT '批次：本科一批/本科提前批/本科批/专科批',
    `min_score` INT COMMENT '最低分',
    `max_score` INT COMMENT '最高分',
    `avg_score` DECIMAL(5,1) COMMENT '平均分',
    `min_ranking` INT COMMENT '最低位次',
    `plan_count` INT COMMENT '计划招生数',
    `enroll_count` INT COMMENT '实际录取数',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `uk_score_unique` (`school_id`, `major_id`, `year`, `province_id`, `subject_type`, `batch`),
    INDEX `idx_school_id` (`school_id`),
    INDEX `idx_major_id` (`major_id`),
    INDEX `idx_year` (`year`),
    INDEX `idx_province_id` (`province_id`),
    INDEX `idx_subject_type` (`subject_type`),
    CONSTRAINT `fk_admission_school` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`),
    CONSTRAINT `fk_admission_major` FOREIGN KEY (`major_id`) REFERENCES `major` (`id`),
    CONSTRAINT `fk_admission_province` FOREIGN KEY (`province_id`) REFERENCES `province` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='历年录取数据表';

-- =====================================================
-- 9. 招生计划表 (EnrollmentPlan)
-- =====================================================
CREATE TABLE `enrollment_plan` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `school_id` BIGINT NOT NULL COMMENT '高校ID',
    `major_id` BIGINT COMMENT '专业ID',
    `year` INT NOT NULL COMMENT '年份',
    `province_id` INT NOT NULL COMMENT '招生省份ID',
    `subject_type` TINYINT NOT NULL COMMENT '科类：1-文科，2-理科，3-综合改革',
    `batch` VARCHAR(50) COMMENT '批次',
    `plan_count` INT COMMENT '计划招生人数',
    `duration` TINYINT COMMENT '学制',
    `tuition` DECIMAL(10,2) COMMENT '学费(元/年)',
    `remark` VARCHAR(500) COMMENT '备注',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `uk_plan_unique` (`school_id`, `major_id`, `year`, `province_id`, `subject_type`),
    INDEX `idx_school_id` (`school_id`),
    INDEX `idx_major_id` (`major_id`),
    INDEX `idx_year` (`year`),
    INDEX `idx_province_id` (`province_id`),
    CONSTRAINT `fk_plan_school` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`),
    CONSTRAINT `fk_plan_major` FOREIGN KEY (`major_id`) REFERENCES `major` (`id`),
    CONSTRAINT `fk_plan_province` FOREIGN KEY (`province_id`) REFERENCES `province` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='招生计划表';

-- =====================================================
-- 10. 收藏表 (Favorite)
-- =====================================================
CREATE TABLE `favorite` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `user_id` BIGINT NOT NULL COMMENT '用户ID',
    `target_type` TINYINT NOT NULL COMMENT '收藏类型：1-高校，2-专业，3-招生计划',
    `target_id` BIGINT NOT NULL COMMENT '目标ID',
    `remark` VARCHAR(200) COMMENT '备注',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY `uk_user_target` (`user_id`, `target_type`, `target_id`),
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_target_type` (`target_type`),
    CONSTRAINT `fk_favorite_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='收藏表';

-- =====================================================
-- 11. 浏览记录表 (History)
-- =====================================================
CREATE TABLE `history` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `user_id` BIGINT NOT NULL COMMENT '用户ID',
    `target_type` TINYINT NOT NULL COMMENT '浏览类型：1-高校，2-专业，3-招生计划，4-AI对话',
    `target_id` BIGINT COMMENT '目标ID',
    `content` VARCHAR(500) COMMENT '浏览内容摘要',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_target_type` (`target_type`),
    INDEX `idx_create_time` (`create_time`),
    CONSTRAINT `fk_history_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='浏览记录表';

-- =====================================================
-- 12. AI聊天记录表 (ChatRecord)
-- =====================================================
CREATE TABLE `chat_record` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `user_id` BIGINT NOT NULL COMMENT '用户ID',
    `session_id` VARCHAR(50) NOT NULL COMMENT '会话ID',
    `role` TINYINT NOT NULL COMMENT '角色：1-用户，2-AI助手',
    `content` TEXT NOT NULL COMMENT '消息内容',
    `tokens` INT COMMENT '消耗Token数',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_session_id` (`session_id`),
    INDEX `idx_create_time` (`create_time`),
    CONSTRAINT `fk_chat_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI聊天记录表';

-- =====================================================
-- 13. 系统配置表 (SystemConfig)
-- =====================================================
CREATE TABLE `system_config` (
    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `config_key` VARCHAR(100) NOT NULL COMMENT '配置键',
    `config_value` TEXT COMMENT '配置值',
    `description` VARCHAR(200) COMMENT '描述',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `uk_config_key` (`config_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- =====================================================
-- 初始化省份数据
-- =====================================================
INSERT INTO `province` (`name`, `code`, `region`, `is_new_gaokao`) VALUES
('北京市', '11', '华北', 1),
('天津市', '12', '华北', 1),
('河北省', '13', '华北', 1),
('山西省', '14', '华北', 0),
('内蒙古自治区', '15', '华北', 0),
('辽宁省', '21', '东北', 1),
('吉林省', '22', '东北', 1),
('黑龙江省', '23', '东北', 1),
('上海市', '31', '华东', 1),
('江苏省', '32', '华东', 1),
('浙江省', '33', '华东', 1),
('安徽省', '34', '华东', 1),
('福建省', '35', '华东', 1),
('江西省', '36', '华东', 0),
('山东省', '37', '华东', 1),
('河南省', '41', '华中', 0),
('湖北省', '42', '华中', 1),
('湖南省', '43', '华中', 1),
('广东省', '44', '华南', 1),
('广西壮族自治区', '45', '华南', 0),
('海南省', '46', '华南', 1),
('重庆市', '50', '西南', 1),
('四川省', '51', '西南', 1),
('贵州省', '52', '西南', 0),
('云南省', '53', '西南', 0),
('西藏自治区', '54', '西南', 0),
('陕西省', '61', '西北', 0),
('甘肃省', '62', '西北', 0),
('青海省', '63', '西北', 0),
('宁夏回族自治区', '64', '西北', 0),
('新疆维吾尔自治区', '65', '西北', 0);

-- =====================================================
-- 完成
-- =====================================================
