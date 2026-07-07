import { router } from '@kit.ArkUI';
import { ApiService } from '../services/ApiService';

interface ApiResponse {
  code: number;
  message: string;
  data: string | null;
}

@Entry
@Component
struct Login {
  @State username: string = ''
  @State password: string = ''
  @State isLogin: boolean = true
  @State loading: boolean = false
  @State errorMsg: string = ''
  @State fadeIn: boolean = false

  aboutToAppear() {
    setTimeout(() => { this.fadeIn = true; }, 100);
  }

  async doLogin() {
    if (!this.username || !this.password) {
      this.errorMsg = '请输入用户名和密码';
      return;
    }
    this.loading = true;
    this.errorMsg = '';
    try {
      const httpRequest = await import('@ohos.net.http');
      const http = httpRequest.default.createHttp();
      const response = await http.request(
        `http://10.0.2.2:8080/api/auth/login`,
        {
          method: httpRequest.default.RequestMethod.POST,
          header: { 'Content-Type': 'application/json' },
          extraData: JSON.stringify({ username: this.username, password: this.password }),
        }
      );
      const result = JSON.parse(response.result as string) as ApiResponse;
      http.destroy();

      if (result.code === 200) {
        router.pushUrl({ url: 'pages/Index' });
      } else {
        this.errorMsg = result.message || '登录失败';
      }
    } catch (e) {
      this.errorMsg = '网络错误，请检查后端是否启动';
    }
    this.loading = false;
  }

  async doRegister() {
    if (!this.username || !this.password) {
      this.errorMsg = '请输入用户名和密码';
      return;
    }
    if (this.username.length < 4) {
      this.errorMsg = '用户名至少4位';
      return;
    }
    if (this.password.length < 6) {
      this.errorMsg = '密码至少6位';
      return;
    }
    this.loading = true;
    this.errorMsg = '';
    try {
      const httpRequest = await import('@ohos.net.http');
      const http = httpRequest.default.createHttp();
      const response = await http.request(
        `http://10.0.2.2:8080/api/auth/register`,
        {
          method: httpRequest.default.RequestMethod.POST,
          header: { 'Content-Type': 'application/json' },
          extraData: JSON.stringify({ username: this.username, password: this.password }),
        }
      );
      const result = JSON.parse(response.result as string) as ApiResponse;
      http.destroy();

      if (result.code === 200) {
        this.errorMsg = '';
        this.isLogin = true;
        this.errorMsg = '注册成功，请登录';
      } else {
        this.errorMsg = result.message || '注册失败';
      }
    } catch (e) {
      this.errorMsg = '网络错误，请检查后端是否启动';
    }
    this.loading = false;
  }

  build() {
    Column() {
      // ==================== Logo区域 ====================
      Column() {
        Text('🎓')
          .fontSize(60)
          .margin({ bottom: 16 })
        Text('智选未来')
          .fontSize(28)
          .fontWeight(FontWeight.Bold)
          .fontColor('#182431')
          .fontFamily('HarmonyOS Sans')
        Text('AI高考志愿填报系统')
          .fontSize(14)
          .fontColor('#8A8A8A')
          .fontFamily('HarmonyOS Sans')
          .margin({ top: 8 })
      }
      .margin({ top: 60, bottom: 40 })

      // ==================== 表单卡片 ====================
      Column() {
        // 标签切换
        Row() {
          Text('登录')
            .fontSize(16)
            .fontWeight(this.isLogin ? FontWeight.Bold : FontWeight.Normal)
            .fontColor(this.isLogin ? '#007DFF' : '#8A8A8A')
            .fontFamily('HarmonyOS Sans')
            .padding({ left: 24, right: 24, top: 12, bottom: 12 })
            .borderRadius(20)
            .backgroundColor(this.isLogin ? '#F0F8FF' : 'transparent')
            .onClick(() => { this.isLogin = true; this.errorMsg = ''; })
            .animation({ duration: 200, curve: Curve.EaseOut })

          Text('注册')
            .fontSize(16)
            .fontWeight(!this.isLogin ? FontWeight.Bold : FontWeight.Normal)
            .fontColor(!this.isLogin ? '#007DFF' : '#8A8A8A')
            .fontFamily('HarmonyOS Sans')
            .padding({ left: 24, right: 24, top: 12, bottom: 12 })
            .borderRadius(20)
            .backgroundColor(!this.isLogin ? '#F0F8FF' : 'transparent')
            .onClick(() => { this.isLogin = false; this.errorMsg = ''; })
            .animation({ duration: 200, curve: Curve.EaseOut })
        }
        .margin({ bottom: 32 })

        // 用户名输入框
        Column() {
          Text('用户名')
            .fontSize(14)
            .fontColor('#5A6C82')
            .fontFamily('HarmonyOS Sans')
            .margin({ bottom: 8 })
          TextInput({ placeholder: '请输入用户名', text: this.username })
            .width('100%')
            .height(48)
            .borderRadius(12)
            .backgroundColor('#F6F6F6')
            .placeholderColor('#8A8A8A')
            .placeholderFont({ size: 16, family: 'HarmonyOS Sans' })
            .fontFamily('HarmonyOS Sans')
            .onChange((value: string) => { this.username = value; })
        }
        .margin({ bottom: 24 })

        // 密码输入框
        Column() {
          Text('密码')
            .fontSize(14)
            .fontColor('#5A6C82')
            .fontFamily('HarmonyOS Sans')
            .margin({ bottom: 8 })
          TextInput({ placeholder: '请输入密码', text: this.password })
            .width('100%')
            .height(48)
            .borderRadius(12)
            .backgroundColor('#F6F6F6')
            .placeholderColor('#8A8A8A')
            .placeholderFont({ size: 16, family: 'HarmonyOS Sans' })
            .fontFamily('HarmonyOS Sans')
            .type(InputType.Password)
            .onChange((value: string) => { this.password = value; })
        }
        .margin({ bottom: 32 })

        // 错误提示
        if (this.errorMsg) {
          Row() {
            Text('⚠️')
              .fontSize(14)
              .margin({ right: 8 })
            Text(this.errorMsg)
              .fontSize(14)
              .fontColor('#FF3B30')
              .fontFamily('HarmonyOS Sans')
          }
          .width('100%')
          .margin({ bottom: 16 })
        }

        // 登录/注册按钮
        Button(this.loading ? '处理中...' : (this.isLogin ? '登录' : '注册'))
          .width('100%')
          .height(52)
          .borderRadius(26)
          .backgroundColor('#007DFF')
          .fontColor('#FFFFFF')
          .fontSize(16)
          .fontWeight(FontWeight.Medium)
          .fontFamily('HarmonyOS Sans')
          .onClick(() => {
            if (this.isLogin) {
              this.doLogin();
            } else {
              this.doRegister();
            }
          })
          .margin({ bottom: 20 })

        // 跳过登录
        Text('跳过，直接使用 →')
          .fontSize(14)
          .fontColor('#007DFF')
          .fontFamily('HarmonyOS Sans')
          .onClick(() => { router.pushUrl({ url: 'pages/Index' }); })
      }
      .width('84%')
      .padding(32)
      .backgroundColor('#FFFFFF')
      .borderRadius(24)
      .border({ width: 1, color: '#F0F0F0' })
      .shadow({ radius: 16, color: '#00000008', offsetY: 8 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#FFFFFF')
    .opacity(this.fadeIn ? 1 : 0)
    .animation({ duration: 300, curve: Curve.EaseOut })
  }
}
