-- =====================================================
-- 志愿方案相关表
-- =====================================================

USE gaokao_ai;

-- 志愿方案表
CREATE TABLE IF NOT EXISTS `volunteer_plan` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '方案ID',
    `user_id` BIGINT NOT NULL DEFAULT 1 COMMENT '用户ID',
    `name` VARCHAR(100) COMMENT '方案名称',
    `year` INT COMMENT '年份',
    `province` VARCHAR(50) COMMENT '省份',
    `score` INT COMMENT '分数',
    `ranking` INT COMMENT '排名',
    `subject_type` TINYINT COMMENT '科类：1-文科，2-理科，3-综合改革',
    `status` TINYINT DEFAULT 1 COMMENT '状态：0-草稿，1-已保存，2-已提交',
    `remark` VARCHAR(500) COMMENT '备注',
    `deleted` TINYINT DEFAULT 0 COMMENT '逻辑删除：0-未删除，1-已删除',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='志愿方案表';

-- 志愿明细表
CREATE TABLE IF NOT EXISTS `volunteer_detail` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT 'ID',
    `plan_id` BIGINT NOT NULL COMMENT '方案ID',
    `school_id` BIGINT NOT NULL COMMENT '学校ID',
    `major_id` BIGINT COMMENT '专业ID',
    `priority` INT DEFAULT 0 COMMENT '优先级（排序）',
    `accept_adjust` TINYINT DEFAULT 0 COMMENT '是否接受调剂：0-否，1-是',
    `probability` DECIMAL(5,2) COMMENT '录取概率',
    `remark` VARCHAR(200) COMMENT '备注',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_plan_id` (`plan_id`),
    INDEX `idx_school_id` (`school_id`),
    CONSTRAINT `fk_detail_plan` FOREIGN KEY (`plan_id`) REFERENCES `volunteer_plan` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_detail_school` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='志愿明细表';
