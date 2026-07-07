import { router } from '@kit.ArkUI';
import { ApiService } from '../services/ApiService';

interface PlanItem {
  id: number;
  name: string;
  year: number;
  province: string;
  score: number;
  subjectType: number;
  status: number;
  createTime: string;
}

interface DetailItem {
  id: number;
  planId: number;
  schoolId: number;
  schoolName: string;
  schoolCode: string;
  majorId: number;
  priority: number;
  probability: number;
  remark: string;
}

interface PlanListResponse {
  code: number;
  message: string;
  data: PlanItem[] | null;
}

interface PlanDetailData {
  plan: PlanItem;
  details: DetailItem[];
}

interface PlanDetailResponse {
  code: number;
  message: string;
  data: PlanDetailData | null;
}

@Entry
@Component
struct VolunteerPlan {
  @State plans: PlanItem[] = []
  @State currentPlan: PlanItem | null = null
  @State details: DetailItem[] = []
  @State loading: boolean = true
  @State fadeIn: boolean = false
  @State showCreate: boolean = false
  @State newPlanName: string = ''
  @State newPlanScore: string = ''
  @State newPlanProvince: string = ''

  aboutToAppear() {
    setTimeout(() => { this.fadeIn = true; }, 100);
    this.loadPlans();
  }

  async loadPlans() {
    this.loading = true;
    try {
      const httpRequest = await import('@ohos.net.http');
      const http = httpRequest.default.createHttp();
      const response = await http.request(
        `http://10.0.2.2:8080/api/volunteer/plans`,
        { method: httpRequest.default.RequestMethod.GET }
      );
      const parsed = JSON.parse(response.result as string) as PlanListResponse;
      http.destroy();

      if (parsed.code === 200 && parsed.data) {
        this.plans = parsed.data;
      }
    } catch (e) {
      console.error('加载失败');
    }
    this.loading = false;
  }

  async loadPlanDetail(planId: number) {
    try {
      const httpRequest = await import('@ohos.net.http');
      const http = httpRequest.default.createHttp();
      const response = await http.request(
        `http://10.0.2.2:8080/api/volunteer/plan/${planId}`,
        { method: httpRequest.default.RequestMethod.GET }
      );
      const result = JSON.parse(response.result as string) as PlanDetailResponse;
      http.destroy();

      if (result.code === 200 && result.data) {
        this.currentPlan = result.data.plan;
        this.details = result.data.details || [];
      }
    } catch (e) {
      console.error('加载详情失败');
    }
  }

  async createPlan() {
    if (!this.newPlanName || !this.newPlanScore) {
      return;
    }
    try {
      const httpRequest = await import('@ohos.net.http');
      const http = httpRequest.default.createHttp();
      await http.request(
        `http://10.0.2.2:8080/api/volunteer/create`,
        {
          method: httpRequest.default.RequestMethod.POST,
          header: { 'Content-Type': 'application/json' },
          extraData: JSON.stringify({
            name: this.newPlanName,
            score: parseInt(this.newPlanScore),
            year: 2024,
            province: this.newPlanProvince || '未知',
            subjectType: 1
          })
        }
      );
      http.destroy();

      this.showCreate = false;
      this.newPlanName = '';
      this.newPlanScore = '';
      this.newPlanProvince = '';
      this.loadPlans();
    } catch (e) {
      console.error('创建失败');
    }
  }

  async deletePlan(planId: number) {
    try {
      const httpRequest = await import('@ohos.net.http');
      const http = httpRequest.default.createHttp();
      await http.request(
        `http://10.0.2.2:8080/api/volunteer/plan/${planId}`,
        { method: httpRequest.default.RequestMethod.DELETE }
      );
      http.destroy();

      this.currentPlan = null;
      this.details = [];
      this.loadPlans();
    } catch (e) {
      console.error('删除失败');
    }
  }

  build() {
    Column() {
      // ==================== 顶部导航栏 ====================
      Row() {
        Text('‹')
          .fontSize(24)
          .fontColor('#182431')
          .fontFamily('HarmonyOS Sans')
          .fontWeight(FontWeight.Bold)
          .margin({ right: 16 })
          .onClick(() => {
            if (this.currentPlan) {
              this.currentPlan = null;
              this.details = [];
            } else {
              router.back();
            }
          })

        Text('志愿方案')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor('#182431')
          .fontFamily('HarmonyOS Sans')
          .layoutWeight(1)

        if (!this.currentPlan) {
          Row() {
            Text('➕')
              .fontSize(16)
              .margin({ right: 6 })
            Text('新建')
              .fontSize(14)
              .fontColor('#182431')
              .fontFamily('HarmonyOS Sans')
          }
          .padding({ left: 12, right: 12, top: 8, bottom: 8 })
          .backgroundColor('#F6F6F6')
          .borderRadius(16)
          .onClick(() => { this.showCreate = !this.showCreate; })
        }
      }
      .width('100%')
      .height(56)
      .padding({ left: 16, right: 16 })
      .backgroundColor('#FFFFFF')
      .border({ width: { bottom: 1 }, color: '#F0F0F0' })
      .shadow({ radius: 8, color: '#00000008', offsetY: 2 })

      // ==================== 内容区域 ====================
      if (this.currentPlan) {
        this.PlanDetailView()
      } else {
        this.PlanListView()
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#FFFFFF')
    .opacity(this.fadeIn ? 1 : 0)
    .animation({ duration: 300, curve: Curve.EaseOut })
  }

  @Builder
  PlanListView() {
    Column() {
      // 创建表单
      if (this.showCreate) {
        Column() {
          Text('创建新方案')
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
            .fontColor('#333333')
            .margin({ bottom: 16 })

          TextInput({ placeholder: '方案名称', text: this.newPlanName })
            .width('100%')
            .height(48)
            .borderRadius(12)
            .backgroundColor('#F8F9FA')
            .border({ width: 1, color: '#E8E8E8' })
            .onChange((value: string) => { this.newPlanName = value; })
            .margin({ bottom: 12 })

          TextInput({ placeholder: '高考分数', text: this.newPlanScore })
            .width('100%')
            .height(48)
            .borderRadius(12)
            .backgroundColor('#F8F9FA')
            .border({ width: 1, color: '#E8E8E8' })
            .onChange((value: string) => { this.newPlanScore = value; })
            .margin({ bottom: 12 })

          TextInput({ placeholder: '省份（可选）', text: this.newPlanProvince })
            .width('100%')
            .height(48)
            .borderRadius(12)
            .backgroundColor('#F8F9FA')
            .border({ width: 1, color: '#E8E8E8' })
            .onChange((value: string) => { this.newPlanProvince = value; })
            .margin({ bottom: 20 })

          Row() {
            Button('取消')
              .width('45%')
              .height(48)
              .borderRadius(24)
              .backgroundColor('#F0F0F0')
              .fontColor('#666666')
              .onClick(() => { this.showCreate = false; })

            Button('创建')
              .width('45%')
              .height(48)
              .borderRadius(24)
              .linearGradient({
                angle: 90,
                colors: [['#667eea', 0], ['#764ba2', 1]]
              })
              .fontColor('#FFFFFF')
              .onClick(() => { this.createPlan(); })
          }
          .width('100%')
          .justifyContent(FlexAlign.SpaceBetween)
        }
        .width('92%')
        .padding(24)
        .backgroundColor('#FFFFFF')
        .borderRadius(20)
        .margin({ top: 16, bottom: 16 })
        .shadow({ radius: 12, color: '#00000015', offsetY: 6 })
      }

      // 方案列表
      if (this.loading) {
        Column() {
          Text('🔄')
            .fontSize(48)
            .margin({ bottom: 12 })
          Text('加载中...')
            .fontSize(16)
            .fontColor('#999999')
        }
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else if (this.plans.length === 0) {
        Column() {
          Column() {
            Text('📋')
              .fontSize(64)
              .margin({ bottom: 16 })
            Text('暂无志愿方案')
              .fontSize(20)
              .fontWeight(FontWeight.Bold)
              .fontColor('#333333')
            Text('点击上方按钮创建')
              .fontSize(14)
              .fontColor('#999999')
              .margin({ top: 8 })
          }
          .padding(32)
          .backgroundColor('#FFFFFF')
          .borderRadius(24)
          .shadow({ radius: 12, color: '#00000012', offsetY: 6 })
        }
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else {
        List() {
          ForEach(this.plans, (plan: PlanItem) => {
            ListItem() {
              Row() {
                Column() {
                  Text(plan.name)
                    .fontSize(17)
                    .fontWeight(FontWeight.Medium)
                    .fontColor('#333333')

                  Row() {
                    Text(`${plan.year}年`)
                      .fontSize(13)
                      .fontColor('#999999')
                    if (plan.score) {
                      Text(` | ${plan.score}分`)
                        .fontSize(13)
                        .fontColor('#667eea')
                        .fontWeight(FontWeight.Bold)
                    }
                  }
                  .margin({ top: 6 })
                }
                .layoutWeight(1)
                .alignItems(HorizontalAlign.Start)

                Text('›')
                  .fontSize(24)
                  .fontColor('#CCCCCC')
              }
              .width('100%')
              .padding(16)
              .backgroundColor('#FFFFFF')
              .borderRadius(16)
              .margin({ bottom: 12 })
              .shadow({ radius: 6, color: '#00000012', offsetY: 3 })
              .onClick(() => { this.loadPlanDetail(plan.id); })
            }
          })
        }
        .width('92%')
        .layoutWeight(1)
        .margin({ top: 8 })
        .scrollBar(BarState.Off)
      }
    }
  }

  @Builder
  PlanDetailView() {
    Column() {
      // 方案信息
      if (this.currentPlan) {
        Column() {
          Row() {
            Text('📊')
              .fontSize(28)
              .margin({ right: 12 })

            Column() {
              Text(this.currentPlan.name)
                .fontSize(18)
                .fontWeight(FontWeight.Bold)
                .fontColor('#333333')

              Row() {
                Text(`${this.currentPlan.year}年`)
                  .fontSize(13)
                  .fontColor('#999999')
                if (this.currentPlan.score) {
                  Text(` | ${this.currentPlan.score}分`)
                    .fontSize(13)
                    .fontColor('#667eea')
                    .fontWeight(FontWeight.Bold)
                }
              }
              .margin({ top: 4 })
            }
            .layoutWeight(1)
            .alignItems(HorizontalAlign.Start)
          }
          .width('100%')
        }
        .width('92%')
        .padding(20)
        .backgroundColor('#FFFFFF')
        .borderRadius(20)
        .margin({ top: 16, bottom: 16 })
        .shadow({ radius: 8, color: '#00000012', offsetY: 4 })
      }

      // 志愿列表
      if (this.details.length === 0) {
        Column() {
          Column() {
            Text('📝')
              .fontSize(64)
              .margin({ bottom: 16 })
            Text('暂无志愿')
              .fontSize(20)
              .fontWeight(FontWeight.Bold)
              .fontColor('#333333')
            Text('从院校详情页添加学校到方案')
              .fontSize(14)
              .fontColor('#999999')
              .margin({ top: 8 })
          }
          .padding(32)
          .backgroundColor('#FFFFFF')
          .borderRadius(24)
          .shadow({ radius: 12, color: '#00000012', offsetY: 6 })
        }
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else {
        List() {
          ForEach(this.details, (item: DetailItem, index: number) => {
            ListItem() {
              Row() {
                // 排名徽章
                Column() {
                  Text(`${index + 1}`)
                    .fontSize(16)
                    .fontWeight(FontWeight.Bold)
                    .fontColor('#FFFFFF')
                }
                .width(36)
                .height(36)
                .borderRadius(18)
                .linearGradient({
                  angle: 135,
                  colors: [['#667eea', 0], ['#764ba2', 1]]
                })
                .justifyContent(FlexAlign.Center)
                .margin({ right: 14 })

                Column() {
                  Text(item.schoolName || '未知学校')
                    .fontSize(16)
                    .fontWeight(FontWeight.Medium)
                    .fontColor('#333333')

                  if (item.probability) {
                    Row() {
                      Text('录取概率:')
                        .fontSize(12)
                        .fontColor('#999999')
                      Text(`${item.probability}%`)
                        .fontSize(12)
                        .fontColor('#4ECDC4')
                        .fontWeight(FontWeight.Bold)
                    }
                    .margin({ top: 4 })
                  }
                }
                .layoutWeight(1)
                .alignItems(HorizontalAlign.Start)
              }
              .width('100%')
              .padding(16)
              .backgroundColor('#FFFFFF')
              .borderRadius(16)
              .margin({ bottom: 12 })
              .shadow({ radius: 6, color: '#00000012', offsetY: 3 })
            }
          })
        }
        .width('92%')
        .layoutWeight(1)
        .scrollBar(BarState.Off)
      }

      // 删除方案按钮
      Button('删除此方案')
        .width('92%')
        .height(52)
        .borderRadius(26)
        .backgroundColor('#FF6B6B')
        .fontColor('#FFFFFF')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .shadow({ radius: 12, color: '#FF6B6B40', offsetY: 6 })
        .margin({ top: 16, bottom: 20 })
        .onClick(() => {
          if (this.currentPlan) {
            this.deletePlan(this.currentPlan.id);
          }
        })
    }
  }
}
