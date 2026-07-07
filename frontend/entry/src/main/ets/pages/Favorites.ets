import { router } from '@kit.ArkUI';
import { ApiService } from '../services/ApiService';

interface FavoriteItem {
  id: number;
  targetType: number;
  targetId: number;
  name: string;
  code: string;
  remark: string;
  createTime: string;
}

@Entry
@Component
struct Favorites {
  @State favorites: FavoriteItem[] = []
  @State loading: boolean = true
  @State fadeIn: boolean = false
  @State selectedType: number = 0 // 0=全部, 1=学校, 2=专业

  aboutToAppear() {
    setTimeout(() => { this.fadeIn = true; }, 100);
    this.loadFavorites();
  }

  async loadFavorites() {
    this.loading = true;
    try {
      const result = await ApiService.getFavorites();
      if (result.code === 200 && result.data && result.data !== 'null') {
        const parsed = JSON.parse(result.data) as FavoriteItem[];
        if (Array.isArray(parsed)) {
          this.favorites = parsed;
        }
      }
    } catch (e) {
      console.error('加载失败');
    }
    this.loading = false;
  }

  async removeFavorite(targetType: number, targetId: number) {
    try {
      await ApiService.removeFavorite(targetType, targetId);
      this.loadFavorites();
    } catch (e) {
      console.error('取消收藏失败');
    }
  }

  getFilteredFavorites(): FavoriteItem[] {
    if (!this.favorites || this.favorites.length === 0) return [];
    if (this.selectedType === 0) return this.favorites;
    return this.favorites.filter((f: FavoriteItem) => f.targetType === this.selectedType);
  }

  getTypeName(targetType: number): string {
    if (targetType === 1) return '学校';
    if (targetType === 2) return '专业';
    return '其他';
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

        Text('我的收藏')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor('#182431')
          .fontFamily('HarmonyOS Sans')
          .layoutWeight(1)

        Text('⭐')
          .fontSize(20)
      }
      .width('100%')
      .height(56)
      .padding({ left: 16, right: 16 })
      .backgroundColor('#FFFFFF')
      .border({ width: { bottom: 1 }, color: '#F0F0F0' })
      .shadow({ radius: 8, color: '#00000008', offsetY: 2 })

      // ==================== 筛选标签 ====================
      Row() {
        Text('全部')
          .fontSize(14)
          .fontWeight(this.selectedType === 0 ? FontWeight.Medium : FontWeight.Normal)
          .fontColor(this.selectedType === 0 ? '#007DFF' : '#8A8A8A')
          .fontFamily('HarmonyOS Sans')
          .padding({ left: 16, right: 16, top: 8, bottom: 8 })
          .backgroundColor(this.selectedType === 0 ? '#F0F8FF' : '#F6F6F6')
          .borderRadius(16)
          .onClick(() => { this.selectedType = 0; })
          .animation({ duration: 200, curve: Curve.EaseOut })

        Text('学校')
          .fontSize(14)
          .fontWeight(this.selectedType === 1 ? FontWeight.Medium : FontWeight.Normal)
          .fontColor(this.selectedType === 1 ? '#007DFF' : '#8A8A8A')
          .fontFamily('HarmonyOS Sans')
          .padding({ left: 16, right: 16, top: 8, bottom: 8 })
          .backgroundColor(this.selectedType === 1 ? '#F0F8FF' : '#F6F6F6')
          .borderRadius(16)
          .margin({ left: 8 })
          .onClick(() => { this.selectedType = 1; })
          .animation({ duration: 200, curve: Curve.EaseOut })

        Text('专业')
          .fontSize(14)
          .fontWeight(this.selectedType === 2 ? FontWeight.Medium : FontWeight.Normal)
          .fontColor(this.selectedType === 2 ? '#007DFF' : '#8A8A8A')
          .fontFamily('HarmonyOS Sans')
          .padding({ left: 16, right: 16, top: 8, bottom: 8 })
          .backgroundColor(this.selectedType === 2 ? '#F0F8FF' : '#F6F6F6')
          .borderRadius(16)
          .margin({ left: 8 })
          .onClick(() => { this.selectedType = 2; })
          .animation({ duration: 200, curve: Curve.EaseOut })
      }
      .width('92%')
      .margin({ top: 16, bottom: 16 })

      // ==================== 收藏列表 ====================
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
      } else if (this.getFilteredFavorites().length === 0) {
        Column() {
          Column() {
            Text('⭐')
              .fontSize(48)
              .margin({ bottom: 16 })
            Text('暂无收藏')
              .fontSize(18)
              .fontWeight(FontWeight.Medium)
              .fontColor('#182431')
              .fontFamily('HarmonyOS Sans')
            Text('在院校或专业详情页点击收藏按钮')
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
          ForEach(this.getFilteredFavorites(), (item: FavoriteItem) => {
            ListItem() {
              Row() {
                // 类型图标
                Column() {
                  Text(item.targetType === 1 ? '🏫' : '📚')
                    .fontSize(20)
                }
                .width(48)
                .height(48)
                .backgroundColor(item.targetType === 1 ? '#FFF3E0' : '#E8F5E8')
                .borderRadius(12)
                .justifyContent(FlexAlign.Center)
                .margin({ right: 16 })

                Column() {
                  Text(item.name || '未知')
                    .fontSize(16)
                    .fontWeight(FontWeight.Medium)
                    .fontColor('#182431')
                    .fontFamily('HarmonyOS Sans')
                    .maxLines(1)
                    .textOverflow({ overflow: TextOverflow.Ellipsis })

                  Row() {
                    if (item.code) {
                      Text(item.code)
                        .fontSize(12)
                        .fontColor('#007DFF')
                        .fontFamily('HarmonyOS Sans')
                        .fontWeight(FontWeight.Medium)
                        .margin({ right: 8 })
                    }
                    Text(this.getTypeName(item.targetType))
                      .fontSize(12)
                      .fontColor('#8A8A8A')
                      .fontFamily('HarmonyOS Sans')
                  }
                  .margin({ top: 8 })
                }
                .layoutWeight(1)
                .alignItems(HorizontalAlign.Start)

                // 删除按钮
                Column() {
                  Text('🗑️')
                    .fontSize(16)
                }
                .width(40)
                .height(40)
                .backgroundColor('#FFEBEE')
                .borderRadius(12)
                .justifyContent(FlexAlign.Center)
                .onClick(() => { this.removeFavorite(item.targetType, item.targetId); })
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
