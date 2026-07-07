import { router } from '@kit.ArkUI';
import { ApiService } from '../services/ApiService';

interface HistoryItem {
  id: number;
  targetType: number;
  targetId: number;
  name: string;
  content: string;
  createTime: string;
}

interface ApiResponse {
  code: number;
  message: string;
  data: string | null;
}

@Entry
@Component
struct History {
  @State histories: HistoryItem[] = []
  @State loading: boolean = true
  @State fadeIn: boolean = false

  aboutToAppear() {
    setTimeout(() => { this.fadeIn = true; }, 100);
    this.loadHistory();
  }

  async loadHistory() {
    this.loading = true;
    try {
      const httpRequest = await import('@ohos.net.http');
      const http = httpRequest.default.createHttp();
      const response = await http.request(
        `http://10.0.2.2:8080/api/history/list?limit=50`,
        { method: httpRequest.default.RequestMethod.GET }
      );
      const result = JSON.parse(response.result as string) as ApiResponse;
      http.destroy();

      if (result.code === 200 && result.data) {
        const parsed = JSON.parse(result.data) as HistoryItem[];
        if (Array.isArray(parsed)) {
          this.histories = parsed;
        }
      }
    } catch (e) {
      console.error('加载失败');
    }
    this.loading = false;
  }

  async clearHistory() {
    try {
      const httpRequest = await import('@ohos.net.http');
      const http = httpRequest.default.createHttp();
      await http.request(
        `http://10.0.2.2:8080/api/history/clear`,
        { method: httpRequest.default.RequestMethod.DELETE }
      );
      http.destroy();

      this.histories = [];
    } catch (e) {
      console.error('清空失败');
    }
  }

  getTypeName(targetType: number): string {
    if (targetType === 1) return '学校';
    if (targetType === 2) return '专业';
    if (targetType === 3) return '招生计划';
    if (targetType === 4) return 'AI对话';
    return '其他';
  }

  getTypeIcon(targetType: number): string {
    if (targetType === 1) return '🏫';
    if (targetType === 2) return '📚';
    if (targetType === 3) return '📋';
    if (targetType === 4) return '🤖';
    return '📄';
  }

  getTypeColor(targetType: number): string {
    if (targetType === 1) return '#FF6D00';
    if (targetType === 2) return '#00C853';
    if (targetType === 3) return '#007DFF';
    if (targetType === 4) return '#9C27B0';
    return '#8A8A8A';
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
          .onClick(() => { router.back(); })

        Text('浏览记录')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor('#182431')
          .fontFamily('HarmonyOS Sans')
          .layoutWeight(1)

        Row() {
          Text('🗑️')
            .fontSize(16)
            .margin({ right: 6 })
          Text('清空')
            .fontSize(14)
            .fontColor('#182431')
            .fontFamily('HarmonyOS Sans')
        }
        .padding({ left: 12, right: 12, top: 8, bottom: 8 })
        .backgroundColor('#F6F6F6')
        .borderRadius(16)
        .onClick(() => { this.clearHistory(); })
      }
      .width('100%')
      .height(56)
      .padding({ left: 16, right: 16 })
      .backgroundColor('#FFFFFF')
      .border({ width: { bottom: 1 }, color: '#F0F0F0' })
      .shadow({ radius: 8, color: '#00000008', offsetY: 2 })

      // ==================== 记录列表 ====================
      if (this.loading) {
        Column() {
          Text('⏳')
            .fontSize(40)
            .margin({ bottom: 12 })
          Text('加载中...')
            .fontSize(16)
            .fontColor('#8A8A8A')
            .fontFamily('HarmonyOS Sans')
        }
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else if (this.histories.length === 0) {
        Column() {
          Column() {
            Text('📜')
              .fontSize(48)
              .margin({ bottom: 16 })
            Text('暂无浏览记录')
              .fontSize(18)
              .fontWeight(FontWeight.Medium)
              .fontColor('#182431')
              .fontFamily('HarmonyOS Sans')
            Text('浏览学校或专业后会自动记录')
              .fontSize(14)
              .fontColor('#8A8A8A')
              .fontFamily('HarmonyOS Sans')
              .margin({ top: 8 })
          }
          .padding(32)
          .backgroundColor('#FFFFFF')
          .borderRadius(20)
          .border({ width: 1, color: '#F0F0F0' })
          .shadow({ radius: 8, color: '#00000008', offsetY: 4 })
        }
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else {
        List() {
          ForEach(this.histories, (item: HistoryItem) => {
            ListItem() {
              Row() {
                // 类型图标
                Column() {
                  Text(this.getTypeIcon(item.targetType))
                    .fontSize(20)
                }
                .width(48)
                .height(48)
                .backgroundColor(this.getTypeColor(item.targetType) + '15')
                .borderRadius(12)
                .justifyContent(FlexAlign.Center)
                .margin({ right: 16 })

                Column() {
                  Text(item.name || item.content || '未知')
                    .fontSize(16)
                    .fontWeight(FontWeight.Medium)
                    .fontColor('#182431')
                    .fontFamily('HarmonyOS Sans')
                    .maxLines(1)
                    .textOverflow({ overflow: TextOverflow.Ellipsis })

                  Row() {
                    Text(this.getTypeName(item.targetType))
                      .fontSize(12)
                      .fontColor('#FFFFFF')
                      .fontFamily('HarmonyOS Sans')
                      .backgroundColor(this.getTypeColor(item.targetType))
                      .borderRadius(6)
                      .padding({ left: 8, right: 8, top: 4, bottom: 4 })

                    if (item.createTime) {
                      Text(item.createTime)
                        .fontSize(12)
                        .fontColor('#8A8A8A')
                        .fontFamily('HarmonyOS Sans')
                        .margin({ left: 8 })
                    }
                  }
                  .margin({ top: 8 })
                }
                .layoutWeight(1)
                .alignItems(HorizontalAlign.Start)

                Text('›')
                  .fontSize(24)
                  .fontColor('#8A8A8A')
              }
              .width('100%')
              .padding(16)
              .backgroundColor('#FFFFFF')
              .borderRadius(12)
              .border({ width: 1, color: '#F0F0F0' })
              .margin({ bottom: 8 })
            }
          })
        }
        .width('100%')
        .padding({ left: 16, right: 16 })
        .layoutWeight(1)
        .scrollBar(BarState.Off)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#FFFFFF')
    .opacity(this.fadeIn ? 1 : 0)
    .animation({ duration: 300, curve: Curve.EaseOut })
  }
}
