import { router } from '@kit.ArkUI';
import { ApiService } from '../services/ApiService';

interface RecommendSchool {
  id: number;
  name: string;
  typeName: string;
  is985: boolean;
  is211: boolean;
  minScore: number;
  probability: number;
  reason: string;
}

interface RecommendResult {
  score: number;
  algorithm: string;
  rush: RecommendSchool[];
  stable: RecommendSchool[];
  safe: RecommendSchool[];
}

@Entry
@Component
struct Recommend {
  @State score: string = ''
  @State provinceId: number = 1
  @State result: RecommendResult | null = null
  @State loading: boolean = false
  @State fadeIn: boolean = false
  @State provinces: string[] = [
    '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江',
    '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南',
    '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州',
    '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆'
  ]

  aboutToAppear() {
    setTimeout(() => { this.fadeIn = true; }, 100);
  }

  async doRecommend() {
    if (!this.score) return;
    this.loading = true;
    this.result = null;
    try {
      const res = await ApiService.getRecommendation(parseInt(this.score), this.provinceId, 3);
      if (res.code === 200 && res.data) {
        this.result = JSON.parse(res.data) as RecommendResult;
      }
    } catch (e) {
      console.error('推荐失败');
    }
    this.loading = false;
  }

  build() {
    Column() {
      // ==================== 顶部 ====================
      Row() {
        Text('<')
          .fontSize(24)
          .fontColor('#FFFFFF')
          .margin({ right: 16 })
          .onClick(() => { router.back(); })
        Text('AI智能推荐')
          .fontSize(22)
          .fontWeight(FontWeight.Bold)
          .fontColor('#FFFFFF')
      }
      .width('100%')
      .height(56)
      .backgroundColor('#1976D2')
      .padding({ left: 16 })
      .justifyContent(FlexAlign.Start)

      // ==================== 输入区域 ====================
      Column() {
        Text('请输入你的高考信息')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .margin({ bottom: 16 })

        TextInput({ placeholder: '请输入高考分数', text: this.score })
          .width('100%')
          .height(44)
          .borderRadius(8)
          .backgroundColor('#F5F5F5')
          .onChange((value: string) => { this.score = value; })
          .margin({ bottom: 12 })

        Text('选择省份')
          .fontSize(14)
          .fontColor('#666666')
          .margin({ bottom: 8 })

        Flex({ wrap: FlexWrap.Wrap }) {
          ForEach(this.provinces, (province: string, index: number) => {
            Text(province)
              .fontSize(12)
              .padding({ left: 12, right: 12, top: 6, bottom: 6 })
              .backgroundColor(this.provinceId === index + 1 ? '#1976D2' : '#F0F0F0')
              .fontColor(this.provinceId === index + 1 ? '#FFFFFF' : '#333333')
              .borderRadius(16)
              .margin({ right: 6, bottom: 6 })
              .onClick(() => { this.provinceId = index + 1; })
          })
        }
        .margin({ bottom: 16 })

        Button(this.loading ? '推荐中...' : '开始推荐')
          .width('100%')
          .height(48)
          .borderRadius(24)
          .backgroundColor('#1976D2')
          .fontColor('#FFFFFF')
          .onClick(() => { this.doRecommend(); })
      }
      .width('90%')
      .padding(16)
      .backgroundColor('#FFFFFF')
      .borderRadius(12)
      .margin({ top: 16 })
      .shadow({ radius: 4, color: '#0000001A', offsetY: 2 })

      // ==================== 推荐结果 ====================
      if (this.result) {
        Column() {
          // 算法说明
          Row() {
            Text(`📊 算法: ${this.result.algorithm === 'ranking' ? '位次法' : '线差法'}`)
              .fontSize(14)
              .fontColor('#1976D2')
              .fontWeight(FontWeight.Medium)
          }
          .width('100%')
          .padding(12)
          .backgroundColor('#E3F2FD')
          .borderRadius(8)
          .margin({ bottom: 16 })

          // 冲刺院校
          if (this.result.rush && this.result.rush.length > 0) {
            this.Section('🚀 冲刺院校', this.result.rush, '#FF6B6B', '录取概率较低，但有机会')
          }

          // 稳妥院校
          if (this.result.stable && this.result.stable.length > 0) {
            this.Section('✅ 稳妥院校', this.result.stable, '#4ECDC4', '录取概率较大，推荐填报')
          }

          // 保底院校
          if (this.result.safe && this.result.safe.length > 0) {
            this.Section('🛡️ 保底院校', this.result.safe, '#45B7D1', '录取概率很高，建议填报')
          }
        }
        .width('90%')
        .margin({ top: 16 })
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
    .opacity(this.fadeIn ? 1 : 0)
    .animation({ duration: 500 })
  }

  @Builder
  Section(title: string, schools: RecommendSchool[], color: string, desc: string) {
    Column() {
      Row() {
        Text(title)
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
          .fontColor(color)
        Text(desc)
          .fontSize(12)
          .fontColor('#999999')
          .margin({ left: 8 })
      }
      .width('100%')
      .margin({ bottom: 8 })

      ForEach(schools, (school: RecommendSchool) => {
        Row() {
          Column() {
            Text(school.name)
              .fontSize(14)
              .fontWeight(FontWeight.Medium)
              .fontColor('#333333')
            Row() {
              if (school.typeName) {
                Text(school.typeName)
                  .fontSize(11)
                  .fontColor('#666666')
              }
              if (school.probability) {
                Text(` | 录取概率: ${school.probability}%`)
                  .fontSize(11)
                  .fontColor('#1976D2')
                  .fontWeight(FontWeight.Medium)
              }
            }
            .margin({ top: 2 })
          }
          .layoutWeight(1)

          if (school.reason) {
            Text(school.reason)
              .fontSize(11)
              .fontColor('#666666')
              .maxLines(2)
              .textOverflow({ overflow: TextOverflow.Ellipsis })
              .width(120)
          }
        }
        .width('100%')
        .padding(12)
        .backgroundColor('#FFFFFF')
        .borderRadius(8)
        .margin({ bottom: 6 })
        .shadow({ radius: 1, color: '#0000000A', offsetY: 1 })
      })
    }
    .width('100%')
    .margin({ bottom: 16 })
  }
}
