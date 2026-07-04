package com.gaokao.ai.service;

import com.gaokao.ai.common.PageResult;
import com.gaokao.ai.vo.SchoolDetailVO;
import com.gaokao.ai.vo.SchoolVO;

import java.util.Map;

/**
 * 学校服务接口
 */
public interface SchoolService {

    /**
     * 多条件模糊分页查询学校
     *
     * @param keyword   关键词（学校名称）
     * @param provinceId 省份ID
     * @param type      学校类型
     * @param level     办学层次
     * @param nature    办学性质
     * @param is985     是否985
     * @param is211     是否211
     * @param isDouble  是否双一流
     * @param pageNum   页码
     * @param pageSize  每页大小
     * @param sortField 排序字段
     * @param sortOrder 排序方向
     * @return 分页结果
     */
    PageResult<SchoolVO> searchSchools(
            String keyword, Integer provinceId, Integer type,
            Integer level, Integer nature, Integer is985,
            Integer is211, Integer isDouble,
            int pageNum, int pageSize,
            String sortField, String sortOrder
    );

    /**
     * 根据ID查询学校详情
     *
     * @param schoolId 学校ID
     * @return 学校详情
     */
    SchoolDetailVO getSchoolDetail(Long schoolId);

    /**
     * 获取学校统计信息
     *
     * @return 统计数据
     */
    Map<String, Object> getStatistics();
}
