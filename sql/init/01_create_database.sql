-- =====================================================
-- 智选未来 - 高考志愿辅助填报系统
-- 数据库初始化脚本
-- =====================================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS gaokao_ai DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE gaokao_ai;

-- =====================================================
-- 1. 用户表
-- =====================================================
CREATE TABLE IF NOT EXISTS `user` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(255) NOT NULL COMMENT '密码',
    `real_name` VARCHAR(50) COMMENT '真实姓名',
    `phone` VARCHAR(20) COMMENT '手机号',
    `email` VARCHAR(100) COMMENT '邮箱',
    `gender` TINYINT DEFAULT 0 COMMENT '性别：0-未知，1-男，2-女',
    `avatar` VARCHAR(255) COMMENT '头像URL',
    `province` VARCHAR(50) COMMENT '省份',
    `score` INT COMMENT '高考分数',
    `rank` INT COMMENT '省排名',
    `subject_type` TINYINT COMMENT '科类：1-文科，2-理科，3-综合改革',
    `graduation_year` INT COMMENT '毕业年份',
    `status` TINYINT DEFAULT 1 COMMENT '状态：0-禁用，1-正常',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted` TINYINT DEFAULT 0 COMMENT '逻辑删除：0-未删除，1-已删除',
    INDEX `idx_phone` (`phone`),
    INDEX `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- =====================================================
-- 2. 大学表
-- =====================================================
CREATE TABLE IF NOT EXISTS `university` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '大学ID',
    `name` VARCHAR(100) NOT NULL COMMENT '大学名称',
    `code` VARCHAR(20) COMMENT '大学代码',
    `province` VARCHAR(50) COMMENT '所在省份',
    `city` VARCHAR(50) COMMENT '所在城市',
    `type` TINYINT COMMENT '类型：1-综合，2-理工，3-师范，4-医药，5-财经，6-政法，7-农林，8-艺术，9-体育，10-民族，11-军事',
    `level` TINYINT COMMENT '层次：1-985，2-211，3-双一流，4-普通本科，5-专科',
    `nature` TINYINT COMMENT '性质：1-公办，2-民办，3-中外合作',
    `website` VARCHAR(255) COMMENT '官网地址',
    `logo` VARCHAR(255) COMMENT '校徽URL',
    `description` TEXT COMMENT '简介',
    `ranking` INT COMMENT '排名',
    `status` TINYINT DEFAULT 1 COMMENT '状态：0-禁用，1-正常',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted` TINYINT DEFAULT 0 COMMENT '逻辑删除：0-未删除，1-已删除',
    INDEX `idx_province` (`province`),
    INDEX `idx_type` (`type`),
    INDEX `idx_level` (`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='大学表';

-- =====================================================
-- 3. 专业表
-- =====================================================
CREATE TABLE IF NOT EXISTS `major` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '专业ID',
    `name` VARCHAR(100) NOT NULL COMMENT '专业名称',
    `code` VARCHAR(20) COMMENT '专业代码',
    `category` VARCHAR(50) COMMENT '专业大类',
    `subject_requirements` VARCHAR(200) COMMENT '选科要求',
    `duration` TINYINT COMMENT '学制：3-三年，4-四年，5-五年',
    `degree` VARCHAR(50) COMMENT '授予学位',
    `description` TEXT COMMENT '专业介绍',
    `employment_direction` TEXT COMMENT '就业方向',
    `salary_range` VARCHAR(50) COMMENT '薪资范围',
    `status` TINYINT DEFAULT 1 COMMENT '状态：0-禁用，1-正常',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted` TINYINT DEFAULT 0 COMMENT '逻辑删除：0-未删除，1-已删除',
    INDEX `idx_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='专业表';

-- =====================================================
-- 4. 大学专业关联表
-- =====================================================
CREATE TABLE IF NOT EXISTS `university_major` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `university_id` BIGINT NOT NULL COMMENT '大学ID',
    `major_id` BIGINT NOT NULL COMMENT '专业ID',
    `ranking` INT COMMENT '专业排名',
    `is_key` TINYINT DEFAULT 0 COMMENT '是否重点学科：0-否，1-是',
    `tuition` DECIMAL(10,2) COMMENT '学费',
    `remark` VARCHAR(500) COMMENT '备注',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY `uk_university_major` (`university_id`, `major_id`),
    INDEX `idx_university_id` (`university_id`),
    INDEX `idx_major_id` (`major_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='大学专业关联表';

-- =====================================================
-- 5. 录取分数线表
-- =====================================================
CREATE TABLE IF NOT EXISTS `admission_score` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `university_id` BIGINT NOT NULL COMMENT '大学ID',
    `major_id` BIGINT COMMENT '专业ID（为空表示院校分数线）',
    `year` INT NOT NULL COMMENT '年份',
    `province` VARCHAR(50) NOT NULL COMMENT '招生省份',
    `subject_type` TINYINT NOT NULL COMMENT '科类：1-文科，2-理科，3-综合改革',
    `batch` VARCHAR(50) COMMENT '批次：本科一批，本科二批，专科批',
    `min_score` INT COMMENT '最低分',
    `max_score` INT COMMENT '最高分',
    `avg_score` DECIMAL(5,1) COMMENT '平均分',
    `min_rank` INT COMMENT '最低位次',
    `plan_count` INT COMMENT '计划招生数',
    `enroll_count` INT COMMENT '实际录取数',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY `uk_university_year_province` (`university_id`, `major_id`, `year`, `province`, `subject_type`),
    INDEX `idx_university_id` (`university_id`),
    INDEX `idx_year` (`year`),
    INDEX `idx_province` (`province`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='录取分数线表';

-- =====================================================
-- 6. 用户收藏表
-- =====================================================
CREATE TABLE IF NOT EXISTS `user_favorite` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `user_id` BIGINT NOT NULL COMMENT '用户ID',
    `target_type` TINYINT NOT NULL COMMENT '收藏类型：1-大学，2-专业',
    `target_id` BIGINT NOT NULL COMMENT '目标ID',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY `uk_user_target` (`user_id`, `target_type`, `target_id`),
    INDEX `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏表';

-- =====================================================
-- 7. 志愿填报方案表
-- =====================================================
CREATE TABLE IF NOT EXISTS `volunteer_plan` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '方案ID',
    `user_id` BIGINT NOT NULL COMMENT '用户ID',
    `name` VARCHAR(100) COMMENT '方案名称',
    `year` INT COMMENT '年份',
    `province` VARCHAR(50) COMMENT '省份',
    `score` INT COMMENT '分数',
    `rank` INT COMMENT '排名',
    `subject_type` TINYINT COMMENT '科类',
    `status` TINYINT DEFAULT 1 COMMENT '状态：0-草稿，1-已保存，2-已提交',
    `remark` VARCHAR(500) COMMENT '备注',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `deleted` TINYINT DEFAULT 0 COMMENT '逻辑删除：0-未删除，1-已删除',
    INDEX `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='志愿填报方案表';

-- =====================================================
-- 8. 志愿明细表
-- =====================================================
CREATE TABLE IF NOT EXISTS `volunteer_detail` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `plan_id` BIGINT NOT NULL COMMENT '方案ID',
    `university_id` BIGINT NOT NULL COMMENT '大学ID',
    `major_id` BIGINT COMMENT '专业ID',
    `priority` INT COMMENT '优先级',
    `accept调剂` TINYINT DEFAULT 0 COMMENT '是否接受调剂：0-否，1-是',
    `probability` DECIMAL(5,2) COMMENT '录取概率',
    `remark` VARCHAR(200) COMMENT '备注',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_plan_id` (`plan_id`),
    INDEX `idx_university_id` (`university_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='志愿明细表';

-- =====================================================
-- 9. AI对话记录表
-- =====================================================
CREATE TABLE IF NOT EXISTS `ai_chat` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `user_id` BIGINT NOT NULL COMMENT '用户ID',
    `session_id` VARCHAR(50) NOT NULL COMMENT '会话ID',
    `role` TINYINT NOT NULL COMMENT '角色：1-用户，2-AI',
    `content` TEXT NOT NULL COMMENT '消息内容',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_session_id` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI对话记录表';

-- =====================================================
-- 10. 系统配置表
-- =====================================================
CREATE TABLE IF NOT EXISTS `system_config` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `config_key` VARCHAR(100) NOT NULL UNIQUE COMMENT '配置键',
    `config_value` TEXT COMMENT '配置值',
    `description` VARCHAR(200) COMMENT '描述',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';
