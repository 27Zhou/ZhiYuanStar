-- =====================================================
-- 心理测评题目数据
-- 12个能力维度，每个维度3题，共36题
-- =====================================================

USE gaokao_ai;

-- 创建测评题目表
CREATE TABLE IF NOT EXISTS `assessment_question` (
    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '题目ID',
    `content` VARCHAR(500) NOT NULL COMMENT '题目内容',
    `option_a` VARCHAR(200) NOT NULL COMMENT '选项A',
    `option_b` VARCHAR(200) NOT NULL COMMENT '选项B',
    `option_c` VARCHAR(200) NOT NULL COMMENT '选项C',
    `option_d` VARCHAR(200) NOT NULL COMMENT '选项D',
    `dimension` VARCHAR(20) NOT NULL COMMENT '能力维度',
    `sort_order` INT DEFAULT 0 COMMENT '题目排序',
    `status` TINYINT DEFAULT 1 COMMENT '状态：0-禁用，1-正常',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='测评题目表';

-- 创建测评结果表
CREATE TABLE IF NOT EXISTS `assessment_result` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '结果ID',
    `user_id` BIGINT COMMENT '用户ID',
    `session_id` VARCHAR(50) COMMENT '会话ID',
    `logic_score` INT DEFAULT 0 COMMENT '逻辑思维得分',
    `creativity_score` INT DEFAULT 0 COMMENT '创造能力得分',
    `communication_score` INT DEFAULT 0 COMMENT '沟通能力得分',
    `leadership_score` INT DEFAULT 0 COMMENT '领导能力得分',
    `hands_on_score` INT DEFAULT 0 COMMENT '动手能力得分',
    `social_score` INT DEFAULT 0 COMMENT '社交能力得分',
    `artistic_score` INT DEFAULT 0 COMMENT '艺术感知得分',
    `practical_score` INT DEFAULT 0 COMMENT '实践能力得分',
    `empathy_score` INT DEFAULT 0 COMMENT '共情能力得分',
    `innovation_score` INT DEFAULT 0 COMMENT '创新能力得分',
    `analysis_score` INT DEFAULT 0 COMMENT '分析能力得分',
    `execution_score` INT DEFAULT 0 COMMENT '执行能力得分',
    `recommended_majors` TEXT COMMENT '推荐专业方向',
    `personality_type` VARCHAR(500) COMMENT '性格类型描述',
    `report` TEXT COMMENT '详细分析报告',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='测评结果表';

-- 插入测评题目
-- 维度1：逻辑思维 (logic)
INSERT INTO `assessment_question` (`content`, `option_a`, `option_b`, `option_c`, `option_d`, `dimension`, `sort_order`) VALUES
('面对一个复杂问题时，你通常会？', '先把问题拆解成小部分，逐个分析', '凭直觉快速做出判断', '和别人讨论，听取意见', '参考类似案例的解决方案', 'logic', 1),
('你更喜欢哪种类型的课程？', '数学、物理等理科课程', '语文、历史等文科课程', '音乐、美术等艺术课程', '体育、实践等动手课程', 'logic', 2),
('做决策时，你更依赖？', '数据分析和逻辑推理', '自己的直觉和感觉', '他人的建议和意见', '过去的经验和惯例', 'logic', 3);

-- 维度2：创造能力 (creativity)
INSERT INTO `assessment_question` (`content`, `option_a`, `option_b`, `option_c`, `option_d`, `dimension`, `sort_order`) VALUES
('遇到一个没有标准答案的问题时，你会？', '尝试从不同角度思考，寻找新方案', '参考已有的解决方案进行改进', '和团队一起头脑风暴', '先调研再决定', 'creativity', 4),
('你更喜欢哪种工作方式？', '自由发挥，不受约束', '按照明确的流程执行', '和团队协作完成', '独立完成既定任务', 'creativity', 5),
('如果让你设计一个新产品，你会？', '大胆创新，做别人没做过的', '在现有产品基础上优化', '参考市场上的成功案例', '严格按照需求文档执行', 'creativity', 6);

-- 维度3：沟通能力 (communication)
INSERT INTO `assessment_question` (`content`, `option_a`, `option_b`, `option_c`, `option_d`, `dimension`, `sort_order`) VALUES
('在团队讨论中，你通常扮演什么角色？', '主动发言，引导讨论方向', '认真倾听，适时提出观点', '记录要点，整理大家的意见', '执行分工，完成自己的部分', 'communication', 7),
('向别人解释一个复杂概念时，你会？', '用简单的比喻和例子说明', '用专业术语准确描述', '画图或用数据展示', '让对方先了解再解释', 'communication', 8),
('和别人发生意见分歧时，你会？', '坚持自己的观点并说明理由', '先听对方说完再表达', '寻找双方都能接受的方案', '暂时搁置，避免冲突', 'communication', 9);

-- 维度4：领导能力 (leadership)
INSERT INTO `assessment_question` (`content`, `option_a`, `option_b`, `option_c`, `option_d`, `dimension`, `sort_order`) VALUES
('在团队项目中，你更倾向于？', '主动承担组织和协调工作', '专注于自己的任务', '支持团队 leader 的决策', '提出建议但不做最终决定', 'leadership', 10),
('团队遇到困难时，你会？', '主动站出来寻找解决方案', '做好自己分内的事情', '鼓励大家一起想办法', '等待 leader 给出指示', 'leadership', 11),
('你认为好的 leader 应该具备什么特质？', '果断决策，有远见', '善于倾听，尊重团队', '专业能力强，以身作则', '公平公正，赏罚分明', 'leadership', 12);

-- 维度5：动手能力 (hands_on)
INSERT INTO `assessment_question` (`content`, `option_a`, `option_b`, `option_c`, `option_d`, `dimension`, `sort_order`) VALUES
('你更喜欢哪种活动？', '拆装电子设备、做手工', '阅读、写作、思考', '和朋友聚会聊天', '组织活动、策划项目', 'hands_on', 13),
('学习新技能时，你更倾向于？', '直接动手实践，边做边学', '先看教程和理论', '找人手把手教', '看别人做一遍再自己尝试', 'hands_on', 14),
('如果要完成一个项目，你更愿意负责？', '实际操作和制作部分', '方案设计和规划部分', '对外沟通和协调部分', '数据分析和报告部分', 'hands_on', 15);

-- 维度6：社交能力 (social)
INSERT INTO `assessment_question` (`content`, `option_a`, `option_b`, `option_c`, `option_d`, `dimension`, `sort_order`) VALUES
('在社交场合中，你通常？', '主动和陌生人交流', '等待别人来找你聊天', '只和认识的人交流', '尽量避免社交场合', 'social', 16),
('你更喜欢哪种社交方式？', '大型聚会和活动', '小范围的朋友聚会', '一对一的深入交流', '线上社交和聊天', 'social', 17),
('结交新朋友时，你会？', '很快就能和对方聊起来', '需要一些时间才能熟悉', '通过共同兴趣建立联系', '很少主动结交新朋友', 'social', 18);

-- 维度7：艺术感知 (artistic)
INSERT INTO `assessment_question` (`content`, `option_a`, `option_b`, `option_c`, `option_d`, `dimension`, `sort_order`) VALUES
('你对美的事物有什么反应？', '会仔细欣赏并感受', '觉得不错但不会特别在意', '会拍照分享给朋友', '没什么特别的感觉', 'artistic', 19),
('你更喜欢哪种艺术形式？', '绘画、雕塑等视觉艺术', '音乐、舞蹈等表演艺术', '文学、电影等叙事艺术', '不太关注艺术', 'artistic', 20),
('如果让你布置房间，你会？', '精心设计，注重美感', '实用为主，简单整洁', '参考网上的装修方案', '随便弄弄就行', 'artistic', 21);

-- 维度8：实践能力 (practical)
INSERT INTO `assessment_question` (`content`, `option_a`, `option_b`, `option_c`, `option_d`, `dimension`, `sort_order`) VALUES
('面对一个实际问题时，你会？', '立即动手解决', '先分析再行动', '寻求他人帮助', '等待问题自行解决', 'practical', 22),
('你更擅长？', '把想法变成实际行动', '制定详细的计划', '说服别人一起行动', '分析问题的本质', 'practical', 23),
('在学习中，你更喜欢？', '实验、实习等实践活动', '理论学习和阅读', '小组讨论和交流', '听讲座和看视频', 'practical', 24);

-- 维度9：共情能力 (empathy)
INSERT INTO `assessment_question` (`content`, `option_a`, `option_b`, `option_c`, `option_d`, `dimension`, `sort_order`) VALUES
('朋友向你倾诉烦恼时，你会？', '感同身受，给予情感支持', '理性分析问题并给建议', '安静倾听，不打断', '转移话题，让对方开心', 'empathy', 25),
('看到别人遇到困难时，你会？', '主动伸出援手', '评估自己能否帮上忙', '表示同情但不介入', '觉得这是他们自己的事', 'empathy', 26),
('你更容易被什么打动？', '真实的情感故事', '数据和事实', '逻辑严密的论证', '权威人士的推荐', 'empathy', 27);

-- 维度10：创新能力 (innovation)
INSERT INTO `assessment_question` (`content`, `option_a`, `option_b`, `option_c`, `option_d`, `dimension`, `sort_order`) VALUES
('你对新事物的态度是？', '非常好奇，愿意尝试', '谨慎观察，了解后再决定', '跟随大多数人的选择', '倾向于保持现状', 'innovation', 28),
('工作中遇到瓶颈时，你会？', '尝试全新的方法突破', '优化现有方法', '向他人请教经验', '暂时搁置等待时机', 'innovation', 29),
('你更喜欢哪种工作环境？', '鼓励创新和试错', '稳定有序', '团队协作', '独立自主', 'innovation', 30);

-- 维度11：分析能力 (analysis)
INSERT INTO `assessment_question` (`content`, `option_a`, `option_b`, `option_c`, `option_d`, `dimension`, `sort_order`) VALUES
('阅读一篇文章时，你更关注？', '文章的逻辑结构和论证', '文章的核心观点', '文章的写作风格', '文章的实际应用', 'analysis', 31),
('做研究或写报告时，你会？', '收集大量数据，深入分析', '抓住重点，简明扼要', '参考他人的研究成果', '按照模板填写', 'analysis', 32),
('面对一堆数据时，你会？', '找出数据背后的规律和趋势', '提取关键数据做结论', '用图表可视化展示', '直接使用现成的分析结果', 'analysis', 33);

-- 维度12：执行能力 (execution)
INSERT INTO `assessment_question` (`content`, `option_a`, `option_b`, `option_c`, `option_d`, `dimension`, `sort_order`) VALUES
('接到一个任务后，你会？', '立即开始执行', '先制定详细计划', '先和团队沟通分工', '先了解背景再行动', 'execution', 34),
('你更擅长？', '按时完成任务', '优化任务流程', '分配任务给他人', '评估任务风险', 'execution', 35),
('面对多个任务时，你会？', '按优先级逐一完成', '制定时间表并严格执行', '寻求帮助分担任务', '先做最简单的', 'execution', 36);
