import { router } from '@kit.ArkUI';
import { ApiService } from '../services/ApiService';

interface SchoolItem {
  id: number;
  name: string;
  code: string;
  provinceName: string;
  typeName: string;
  levelName: string;
  natureName: string;
  is985: boolean;
  is211: boolean;
  isDoubleFirstClass: boolean;
  ranking: number;
}

@Entry
@Component
struct SchoolList {
  @State schools: SchoolItem[] = []
  @State keyword: string = ''
  @State loading: boolean = false
  @State fadeIn: boolean = false

  aboutToAppear() {
    this.loadSchools();
    setTimeout(() => { this.fadeIn = true; }, 100);
  }

  async loadSchools() {
    this.loading = true;
    try {
      const result = await ApiService.searchSchools(this.keyword, 1, 50);
      if (result.code === 200 && result.data) {
        const parsed = JSON.parse(result.data) as Record<string, object>;
        const records = parsed['records'] as SchoolItem[];
        if (records) {
          this.schools = records;
        }
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
        Text('院校库')
          .fontSize(22)
          .fontWeight(FontWeight.Bold)
          .fontColor('#FFFFFF')
      }
      .width('100%')
      .height(56)
      .backgroundColor('#1976D2')
      .padding({ left: 16 })
      .justifyContent(FlexAlign.Start)

      // ==================== 搜索框 ====================
      Row() {
        TextInput({ placeholder: '搜索学校名称...', text: this.keyword })
          .layoutWeight(1)
          .height(42)
          .borderRadius(21)
          .backgroundColor('#F5F5F5')
          .onChange((value: string) => { this.keyword = value; })

        Button('搜索')
          .height(42)
          .margin({ left: 8 })
          .borderRadius(21)
          .backgroundColor('#1976D2')
          .onClick(() => { this.loadSchools(); })
      }
      .width('90%')
      .margin({ top: 12, bottom: 12 })

      // ==================== 学校列表 ====================
      if (this.loading) {
        Column() {
          Text('🔄')
            .fontSize(40)
            .margin({ bottom: 8 })
          Text('加载中...')
            .fontSize(16)
            .fontColor('#999999')
        }
        .margin({ top: 50 })
      } else if (this.schools.length === 0) {
        Column() {
          Text('📭')
            .fontSize(40)
            .margin({ bottom: 8 })
          Text('暂无数据')
            .fontSize(16)
            .fontColor('#999999')
        }
        .margin({ top: 50 })
      } else {
        List() {
          ForEach(this.schools, (school: SchoolItem) => {
            ListItem() {
              Row() {
                Column() {
                  Row() {
                    Text(school.name)
                      .fontSize(16)
                      .fontWeight(FontWeight.Medium)
                      .fontColor('#333333')

                    if (school.is985) {
                      Text('985')
                        .fontSize(10)
                        .fontColor('#FFFFFF')
                        .backgroundColor('#FF6B6B')
                        .borderRadius(4)
                        .padding({ left: 4, right: 4, top: 1, bottom: 1 })
                        .margin({ left: 6 })
                    }
                    if (school.is211) {
                      Text('211')
                        .fontSize(10)
                        .fontColor('#FFFFFF')
                        .backgroundColor('#4ECDC4')
                        .borderRadius(4)
                        .padding({ left: 4, right: 4, top: 1, bottom: 1 })
                        .margin({ left: 4 })
                    }
                    if (school.isDoubleFirstClass) {
                      Text('双一流')
                        .fontSize(10)
                        .fontColor('#FFFFFF')
                        .backgroundColor('#45B7D1')
                        .borderRadius(4)
                        .padding({ left: 4, right: 4, top: 1, bottom: 1 })
                        .margin({ left: 4 })
                    }
                  }

                  Text(`${school.typeName || ''} | ${school.levelName || ''} | ${school.natureName || ''}`)
                    .fontSize(12)
                    .fontColor('#999999')
                    .margin({ top: 4 })

                  if (school.provinceName) {
                    Text(school.provinceName)
                      .fontSize(12)
                      .fontColor('#666666')
                      .margin({ top: 2 })
                  }
                }
                .layoutWeight(1)

                if (school.ranking) {
                  Column() {
                    Text('排名')
                      .fontSize(10)
                      .fontColor('#999999')
                    Text(`#${school.ranking}`)
                      .fontSize(18)
                      .fontWeight(FontWeight.Bold)
                      .fontColor('#1976D2')
                  }
                  .alignItems(HorizontalAlign.Center)
                }
              }
              .width('100%')
              .padding(14)
              .backgroundColor('#FFFFFF')
              .borderRadius(10)
              .margin({ bottom: 8 })
              .shadow({ radius: 2, color: '#0000000D', offsetY: 1 })
              .onClick(() => {
                router.pushUrl({ url: 'pages/SchoolDetail', params: { schoolId: school.id } });
              })
            }
          })
        }
        .width('90%')
        .layoutWeight(1)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
    .opacity(this.fadeIn ? 1 : 0)
    .animation({ duration: 500 })
  }
}
