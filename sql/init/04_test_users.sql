-- =====================================================
-- 测试用户数据
-- 密码: 123456 (BCrypt加密)
-- =====================================================

USE gaokao_ai;

-- 插入测试用户
-- 密码都是 123456 的BCrypt加密值
INSERT IGNORE INTO `user` (`username`, `password`, `real_name`, `phone`, `email`, `gender`, `province_id`, `score`, `ranking`, `subject_type`, `graduation_year`, `status`) VALUES
('zhangsan', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '张三', '13800138001', 'zhangsan@test.com', 1, 1, 620, 5000, 3, 2025, 1),
('lisi', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '李四', '13800138002', 'lisi@test.com', 2, 11, 580, 15000, 3, 2025, 1),
('wangwu', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '王五', '13800138003', 'wangwu@test.com', 1, 19, 650, 2000, 3, 2025, 1),
('zhaoliu', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '赵六', '13800138004', 'zhaoliu@test.com', 2, 3, 500, 50000, 3, 2025, 1),
('sunqi', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '孙七', '13800138005', 'sunqi@test.com', 1, 17, 690, 500, 3, 2025, 1);
