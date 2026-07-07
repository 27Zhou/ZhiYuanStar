import { router } from '@kit.ArkUI';

@Entry
@Component
struct Profile {
  @State username: string = '未登录'
  @State score: number = 0
  @State province: string = '未设置'
  @State fadeIn: boolean = false

  aboutToAppear() {
    setTimeout(() => { this.fadeIn = true; }, 100);
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
        Text('个人中心')
          .fontSize(22)
          .fontWeight(FontWeight.Bold)
          .fontColor('#FFFFFF')
      }
      .width('100%')
      .height(56)
      .backgroundColor('#1976D2')
      .padding({ left: 16 })
      .justifyContent(FlexAlign.Start)

      // ==================== 用户信息卡片 ====================
      Column() {
        // 头像
        Text('👤')
          .fontSize(60)
          .margin({ bottom: 12 })

        Text(this.username)
          .fontSize(22)
          .fontWeight(FontWeight.Bold)
          .fontColor('#333333')

        Text(`${this.province} | ${this.score}分`)
          .fontSize(14)
          .fontColor('#666666')
          .margin({ top: 4 })
      }
      .width('90%')
      .padding(24)
      .backgroundColor('#FFFFFF')
      .borderRadius(16)
      .alignItems(HorizontalAlign.Center)
      .margin({ top: 16 })
      .shadow({ radius: 4, color: '#0000001A', offsetY: 2 })

      // ==================== 功能列表 ====================
      Column() {
        this.MenuItem('⭐', '我的收藏', '查看收藏的学校和专业', 'pages/Favorites')
        this.MenuItem('📋', '志愿方案', '管理我的志愿填报方案', 'pages/VolunteerPlan')
        this.MenuItem('📊', '浏览记录', '查看浏览历史', 'pages/History')
        this.MenuItem('🧠', '测评记录', '查看心理测评结果', 'pages/Assessment')
        this.MenuItem('🔐', '登录/注册', '登录账号同步数据', 'pages/Login')
        this.MenuItem('❓', '帮助', '使用帮助和反馈', '')
      }
      .width('90%')
      .margin({ top: 16 })
      .backgroundColor('#FFFFFF')
      .borderRadius(16)
      .padding({ top: 8, bottom: 8 })
      .shadow({ radius: 4, color: '#0000001A', offsetY: 2 })

      // ==================== 版本信息 ====================
      Text('智选未来 v1.0.0')
        .fontSize(12)
        .fontColor('#CCCCCC')
        .margin({ top: 20 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
    .opacity(this.fadeIn ? 1 : 0)
    .animation({ duration: 500 })
  }

  @Builder
  MenuItem(icon: string, title: string, subtitle: string, page: string) {
    Row() {
      Text(icon)
        .fontSize(24)
        .width(40)

      Column() {
        Text(title)
          .fontSize(15)
          .fontWeight(FontWeight.Medium)
          .fontColor('#333333')
        Text(subtitle)
          .fontSize(12)
          .fontColor('#999999')
          .margin({ top: 2 })
      }
      .layoutWeight(1)
      .alignItems(HorizontalAlign.Start)

      Text('>')
        .fontSize(16)
        .fontColor('#CCCCCC')
    }
    .width('100%')
    .padding({ left: 16, right: 16, top: 14, bottom: 14 })
    .onClick(() => {
      if (page) {
        router.pushUrl({ url: page });
      }
    })
  }
}
