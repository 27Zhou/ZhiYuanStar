import { router } from '@kit.ArkUI';
import { ApiService } from '../services/ApiService';

interface SchoolInfo {
  id: number;
  name: string;
  code: string;
  provinceName: string;
  address: string;
  typeName: string;
  levelName: string;
  natureName: string;
  is985: boolean;
  is211: boolean;
  isDoubleFirstClass: boolean;
  website: string;
  description: string;
  ranking: number;
  studentCount: number;
  facultyCount: number;
}

interface ScoreItem {
  year: number;
  batch: string;
  minScore: number;
  maxScore: number;
  avgScore: number;
  minRanking: number;
}

interface MajorItem {
  id: number;
  name: string;
  code: string;
  category: string;
  duration: number;
  degree: string;
}

interface SchoolDetailData {
  school: SchoolInfo;
  admissionScores: Record<string, ScoreItem[]>;
  majors: MajorItem[];
}

@Entry
@Component
struct SchoolDetail {
  @State schoolId: number = 0
  @State school: SchoolInfo | null = null
  @State scores: Record<string, ScoreItem[]> = {}
  @State majors: MajorItem[] = []
  @State loading: boolean = true
  @State fadeIn: boolean = false
  @State selectedTab: number = 0

  aboutToAppear() {
    setTimeout(() => { this.fadeIn = true; }, 100);
    const params = router.getParams() as Record<string, string>;
    if (params && params['schoolId']) {
      const schoolIdStr = params['schoolId'];
      this.schoolId = parseInt(schoolIdStr, 10) || 0;
      this.loadDetail(this.schoolId);
    }
  }

  async loadDetail(id: number) {
    this.loading = true;
    try {
      const result = await ApiService.getSchoolDetail(id);
      if (result.code === 200 && result.data && result.data !== 'null') {
        const data = JSON.parse(result.data) as Record<string, object>;
        // API返回的SchoolDetailVO直接包含学校字段
        this.school = data['school'] as SchoolInfo;
        this.scores = (data['admissionScores'] as Record<string, ScoreItem[]>) || {};
        this.majors = (data['majors'] as MajorItem[]) || [];
      }
    } catch (e) {
      console.error('加载失败');
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
        Text(this.school?.name || '学校详情')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor('#FFFFFF')
      }
      .width('100%')
      .height(56)
      .backgroundColor('#1976D2')
      .padding({ left: 16 })
      .justifyContent(FlexAlign.Start)

      if (this.loading) {
        Column() {
          Text('🔄')
            .fontSize(40)
            .margin({ bottom: 8 })
          Text('加载中...')
            .fontSize(16)
            .fontColor('#999999')
        }
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else if (this.school) {
        // ==================== 学校信息卡片 ====================
        Column() {
          // 学校名称和标签
          Row() {
            Text(this.school.name)
              .fontSize(22)
              .fontWeight(FontWeight.Bold)
              .fontColor('#333333')

            if (this.school.is985) {
              Text('985')
                .fontSize(11)
                .fontColor('#FFFFFF')
                .backgroundColor('#FF6B6B')
                .borderRadius(4)
                .padding({ left: 6, right: 6, top: 2, bottom: 2 })
                .margin({ left: 8 })
            }
            if (this.school.is211) {
              Text('211')
                .fontSize(11)
                .fontColor('#FFFFFF')
                .backgroundColor('#4ECDC4')
                .borderRadius(4)
                .padding({ left: 6, right: 6, top: 2, bottom: 2 })
                .margin({ left: 4 })
            }
            if (this.school.isDoubleFirstClass) {
              Text('双一流')
                .fontSize(11)
                .fontColor('#FFFFFF')
                .backgroundColor('#45B7D1')
                .borderRadius(4)
                .padding({ left: 6, right: 6, top: 2, bottom: 2 })
                .margin({ left: 4 })
            }
          }

          // 基本信息
          Column() {
            this.InfoRow('代码', this.school.code)
            this.InfoRow('类型', `${this.school.typeName} | ${this.school.levelName} | ${this.school.natureName}`)
            this.InfoRow('省份', this.school.provinceName || '未知')
            this.InfoRow('地址', this.school.address || '暂无')
            if (this.school.ranking) {
              this.InfoRow('排名', `全国第 ${this.school.ranking} 名`)
            }
            if (this.school.website) {
              this.InfoRow('官网', this.school.website)
            }
          }
          .width('100%')
          .margin({ top: 12 })

          // 简介
          if (this.school.description) {
            Column() {
              Text('学校简介')
                .fontSize(14)
                .fontWeight(FontWeight.Bold)
                .margin({ bottom: 6 })
              Text(this.school.description)
                .fontSize(13)
                .fontColor('#666666')
                .lineHeight(20)
            }
            .width('100%')
            .margin({ top: 12 })
            .padding(12)
            .backgroundColor('#F8F9FA')
            .borderRadius(8)
          }
        }
        .width('90%')
        .padding(16)
        .backgroundColor('#FFFFFF')
        .borderRadius(12)
        .margin({ top: 12 })
        .shadow({ radius: 4, color: '#0000001A', offsetY: 2 })

        // ==================== 标签页 ====================
        Row() {
          Text('录取分数')
            .fontSize(14)
            .padding({ left: 16, right: 16, top: 8, bottom: 8 })
            .fontColor(this.selectedTab === 0 ? '#1976D2' : '#666666')
            .fontWeight(this.selectedTab === 0 ? FontWeight.Bold : FontWeight.Normal)
            .border({ width: { bottom: this.selectedTab === 0 ? 2 : 0 }, color: '#1976D2' })
            .onClick(() => { this.selectedTab = 0; })

          Text('开设专业')
            .fontSize(14)
            .padding({ left: 16, right: 16, top: 8, bottom: 8 })
            .fontColor(this.selectedTab === 1 ? '#1976D2' : '#666666')
            .fontWeight(this.selectedTab === 1 ? FontWeight.Bold : FontWeight.Normal)
            .border({ width: { bottom: this.selectedTab === 1 ? 2 : 0 }, color: '#1976D2' })
            .onClick(() => { this.selectedTab = 1; })
        }
        .width('90%')
        .margin({ top: 12 })
        .border({ width: { bottom: 1 }, color: '#EEEEEE' })

        // ==================== 内容区域 ====================
        if (this.selectedTab === 0) {
          this.ScoreTab()
        } else {
          this.MajorTab()
        }
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
    .opacity(this.fadeIn ? 1 : 0)
    .animation({ duration: 500 })
  }

  @Builder
  InfoRow(label: string, value: string) {
    Row() {
      Text(label)
        .fontSize(13)
        .fontColor('#999999')
        .width(60)
      Text(value)
        .fontSize(13)
        .fontColor('#333333')
        .layoutWeight(1)
    }
    .width('100%')
    .margin({ bottom: 6 })
  }

  @Builder
  ScoreTab() {
    Column() {
      if (Object.keys(this.scores).length === 0) {
        Column() {
          Text('📊')
            .fontSize(40)
            .margin({ bottom: 8 })
          Text('暂无录取分数数据')
            .fontSize(14)
            .fontColor('#999999')
        }
        .margin({ top: 30 })
      } else {
        List() {
          ForEach(Object.keys(this.scores).sort().reverse(), (year: string) => {
            ListItem() {
              Column() {
                Text(`${year} 年`)
                  .fontSize(16)
                  .fontWeight(FontWeight.Bold)
                  .margin({ bottom: 8 })

                ForEach(this.scores[year], (item: ScoreItem) => {
                  Row() {
                    Text(item.batch || '本科批')
                      .fontSize(12)
                      .fontColor('#666666')
                      .width(60)

                    Text(`最低 ${item.minScore} 分`)
                      .fontSize(13)
                      .fontWeight(FontWeight.Medium)
                      .fontColor('#1976D2')

                    if (item.minRanking) {
                      Text(` | 位次 ${item.minRanking}`)
                        .fontSize(12)
                        .fontColor('#999999')
                    }
                  }
                  .width('100%')
                  .padding(8)
                  .backgroundColor('#F8F9FA')
                  .borderRadius(6)
                  .margin({ bottom: 4 })
                })
              }
              .width('100%')
              .padding(12)
              .backgroundColor('#FFFFFF')
              .borderRadius(8)
              .margin({ bottom: 8 })
            }
          })
        }
        .width('90%')
      }
    }
    .width('100%')
    .layoutWeight(1)
    .padding({ top: 12 })
  }

  @Builder
  MajorTab() {
    Column() {
      if (this.majors.length === 0) {
        Column() {
          Text('📚')
            .fontSize(40)
            .margin({ bottom: 8 })
          Text('暂无专业数据')
            .fontSize(14)
            .fontColor('#999999')
        }
        .margin({ top: 30 })
      } else {
        List() {
          ForEach(this.majors, (major: MajorItem) => {
            ListItem() {
              Row() {
                Column() {
                  Text(major.name)
                    .fontSize(14)
                    .fontWeight(FontWeight.Medium)
                    .fontColor('#333333')
                  Row() {
                    if (major.code) {
                      Text(major.code)
                        .fontSize(11)
                        .fontColor('#999999')
                    }
                    if (major.category) {
                      Text(` | ${major.category}`)
                        .fontSize(11)
                        .fontColor('#999999')
                    }
                    if (major.duration) {
                      Text(` | ${major.duration}年制`)
                        .fontSize(11)
                        .fontColor('#999999')
                    }
                    if (major.degree) {
                      Text(` | ${major.degree}`)
                        .fontSize(11)
                        .fontColor('#999999')
                    }
                  }
                  .margin({ top: 2 })
                }
                .layoutWeight(1)
              }
              .width('100%')
              .padding(12)
              .backgroundColor('#FFFFFF')
              .borderRadius(8)
              .margin({ bottom: 6 })
            }
          })
        }
        .width('90%')
      }
    }
    .width('100%')
    .layoutWeight(1)
    .padding({ top: 12 })
  }
}
