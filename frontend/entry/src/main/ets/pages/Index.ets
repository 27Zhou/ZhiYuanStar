import { router } from '@kit.ArkUI';
import { ApiService } from '../services/ApiService';

interface SchoolItem {
  id: number;
  name: string;
  typeName: string;
  levelName: string;
  is985: boolean;
  is211: boolean;
  ranking: number;
}

@Entry
@Component
struct Index {
  @State title: string = '智选未来'
  @State searchKeyword: string = ''
  @State schools: SchoolItem[] = []
  @State fadeIn: boolean = false

  aboutToAppear() {
    this.loadHotSchools();
    setTimeout(() => { this.fadeIn = true; }, 100);
  }

  async loadHotSchools() {
    try {
      const result = await ApiService.searchSchools('', 1, 5);
      if (result.code === 200 && result.data && result.data !== 'null') {
        const parsed = JSON.parse(result.data) as Record<string, object>;
        const records = parsed['records'];
        if (records && Array.isArray(records)) {
          this.schools = records as SchoolItem[];
        }
      }
    } catch (e) {
      console.error('load failed');
    }
  }

  build() {
    Column() {
      // ==================== 标题栏 ====================
      Row() {
        Text(this.title)
          .fontSize(22)
          .fontWeight(FontWeight.Bold)
          .fontColor('#FFFFFF')
      }
      .width('100%')
      .height(56)
      .backgroundColor('#1976D2')
      .justifyContent(FlexAlign.Center)

      // ==================== 搜索框 ====================
      TextInput({ placeholder: '搜索学校或专业...', text: this.searchKeyword })
        .width('90%')
        .height(44)
        .margin({ top: 16, bottom: 16 })
        .borderRadius(22)
        .backgroundColor('#FFFFFF')
        .shadow({ radius: 4, color: '#0000001A', offsetY: 2 })
        .onChange((value: string) => { this.searchKeyword = value; })

      // ==================== 功能入口 ====================
      Row() {
        this.FunctionItem('院校查询', 'pages/SchoolList')
        this.FunctionItem('AI推荐', 'pages/Recommend')
        this.FunctionItem('心理测评', 'pages/Assessment')
        this.FunctionItem('个人中心', 'pages/Profile')
      }
      .width('90%')
      .margin({ bottom: 20 })

      // ==================== 热门院校 ====================
      Row() {
        Text('热门院校')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
        Text('查看全部 >')
          .fontSize(12)
          .fontColor('#1976D2')
          .onClick(() => { router.pushUrl({ url: 'pages/SchoolList' }); })
      }
      .width('90%')
      .justifyContent(FlexAlign.SpaceBetween)
      .margin({ bottom: 10 })

      // ==================== 学校列表 ====================
      List() {
        ForEach(this.schools, (school: SchoolItem, index: number) => {
          ListItem() {
            Row() {
              // 排名
              if (school.ranking && school.ranking <= 10) {
                Text(`${school.ranking}`)
                  .fontSize(14)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#FFFFFF')
                  .backgroundColor('#FF6B6B')
                  .borderRadius(12)
                  .width(28)
                  .height(28)
                  .textAlign(TextAlign.Center)
                  .margin({ right: 12 })
              } else if (school.ranking) {
                Text(`${school.ranking}`)
                  .fontSize(12)
                  .fontColor('#999999')
                  .width(28)
                  .height(28)
                  .textAlign(TextAlign.Center)
                  .margin({ right: 12 })
              }

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
                }

                Text(school.typeName || '')
                  .fontSize(12)
                  .fontColor('#999999')
                  .margin({ top: 4 })
              }
              .layoutWeight(1)
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

      // ==================== 底部导航栏 ====================
      Row() {
        this.NavItem('首页', true)
        this.NavItem('搜索', false, 'pages/SchoolList')
        this.NavItem('推荐', false, 'pages/Recommend')
        this.NavItem('我的', false, 'pages/Profile')
      }
      .width('100%')
      .height(60)
      .backgroundColor('#FFFFFF')
      .border({ width: { top: 1 }, color: '#F0F0F0' })
      .shadow({ radius: 8, color: '#0000001A', offsetY: -2 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
    .opacity(this.fadeIn ? 1 : 0)
    .animation({ duration: 500 })
  }

  @Builder
  FunctionItem(title: string, page: string) {
    Column() {
      Text(title)
        .fontSize(14)
        .fontColor('#333333')
    }
    .width('25%')
    .height(60)
    .backgroundColor('#FFFFFF')
    .borderRadius(10)
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
    .shadow({ radius: 2, color: '#0000000D', offsetY: 1 })
    .onClick(() => { router.pushUrl({ url: page }); })
  }

  @Builder
  NavItem(title: string, isActive: boolean, page?: string) {
    Column() {
      Text(title)
        .fontSize(14)
        .fontColor(isActive ? '#1976D2' : '#999999')
        .fontWeight(isActive ? FontWeight.Bold : FontWeight.Normal)
    }
    .width('25%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .onClick(() => {
      if (page) {
        router.pushUrl({ url: page });
      }
    })
  }
}
