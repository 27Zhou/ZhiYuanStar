import http from '@ohos.net.http';

const BASE_URL = 'http://10.0.2.2:8080/api';

export interface ApiResponse {
  code: number;
  message: string;
  data: string;
}

export class ApiService {

  private static async doGet(url: string): Promise<ApiResponse> {
    const httpRequest = http.createHttp();
    try {
      const response = await httpRequest.request(url, { method: http.RequestMethod.GET });
      const result = JSON.parse(response.result as string) as Record<string, object>;
      return {
        code: result['code'] as unknown as number,
        message: result['message'] as unknown as string,
        data: JSON.stringify(result['data']),
      };
    } catch (e) {
      return { code: 500, message: '请求失败', data: '' };
    } finally {
      httpRequest.destroy();
    }
  }

  private static async doPost(url: string, body: string): Promise<ApiResponse> {
    const httpRequest = http.createHttp();
    try {
      const response = await httpRequest.request(url, {
        method: http.RequestMethod.POST,
        header: { 'Content-Type': 'application/json' },
        extraData: body,
      });
      const result = JSON.parse(response.result as string) as Record<string, object>;
      return {
        code: result['code'] as unknown as number,
        message: result['message'] as unknown as string,
        data: JSON.stringify(result['data']),
      };
    } catch (e) {
      return { code: 500, message: '请求失败', data: '' };
    } finally {
      httpRequest.destroy();
    }
  }

  private static async doDelete(url: string): Promise<ApiResponse> {
    const httpRequest = http.createHttp();
    try {
      const response = await httpRequest.request(url, { method: http.RequestMethod.DELETE });
      const result = JSON.parse(response.result as string) as Record<string, object>;
      return {
        code: result['code'] as unknown as number,
        message: result['message'] as unknown as string,
        data: JSON.stringify(result['data']),
      };
    } catch (e) {
      return { code: 500, message: '请求失败', data: '' };
    } finally {
      httpRequest.destroy();
    }
  }

  static async searchSchools(keyword: string, pageNum: number, pageSize: number): Promise<ApiResponse> {
    let url = `${BASE_URL}/school/search?pageNum=${pageNum}&pageSize=${pageSize}`;
    if (keyword) {
      url += `&keyword=${encodeURIComponent(keyword)}`;
    }
    return this.doGet(url);
  }

  static async getSchoolDetail(schoolId: number): Promise<ApiResponse> {
    return this.doGet(`${BASE_URL}/school/detail/${schoolId}`);
  }

  static async getSchoolStatistics(): Promise<ApiResponse> {
    return this.doGet(`${BASE_URL}/school/statistics`);
  }

  static async getRecommendation(score: number, provinceId: number, subjectType: number): Promise<ApiResponse> {
    return this.doGet(`${BASE_URL}/recommend/school?score=${score}&provinceId=${provinceId}&subjectType=${subjectType}`);
  }

  static async getAssessmentQuestions(): Promise<ApiResponse> {
    return this.doGet(`${BASE_URL}/assessment/questions`);
  }

  static async submitAssessment(answers: Record<number, string>): Promise<ApiResponse> {
    return this.doPost(`${BASE_URL}/assessment/submit`, JSON.stringify(answers));
  }

  static async addFavorite(targetType: number, targetId: number): Promise<ApiResponse> {
    return this.doPost(`${BASE_URL}/favorite/add?targetType=${targetType}&targetId=${targetId}`, '');
  }

  static async getFavorites(): Promise<ApiResponse> {
    return this.doGet(`${BASE_URL}/favorite/list`);
  }

  static async removeFavorite(targetType: number, targetId: number): Promise<ApiResponse> {
    return this.doDelete(`${BASE_URL}/favorite/remove?targetType=${targetType}&targetId=${targetId}`);
  }
}
