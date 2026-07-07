import { router } from '@kit.ArkUI';
import { ApiService } from '../services/ApiService';

interface Question {
  id: number;
  content: string;
  optionA: string;
  optionB: string;
  optionC: string;
  optionD: string;
  dimension: string;
}

interface AssessmentResult {
  logicScore: number;
  creativityScore: number;
  communicationScore: number;
  leadershipScore: number;
  handsOnScore: number;
  socialScore: number;
  artisticScore: number;
  practicalScore: number;
  empathyScore: number;
  innovationScore: number;
  analysisScore: number;
  executionScore: number;
  personalityType: string;
  recommendedMajors: string;
}

@Entry
@Component
struct Assessment {
  @State questions: Question[] = []
  @State currentIndex: number = 0
  @State answers: Record<number, string> = {}
  @State result: AssessmentResult | null = null
  @State loading: boolean = false
  @State fadeIn: boolean = false

  aboutToAppear() {
    setTimeout(() => { this.fadeIn = true; }, 100);
    this.loadQuestions();
  }

  async loadQuestions() {
    this.loading = true;
    try {
      const result = await ApiService.getAssessmentQuestions();
      if (result.code === 200 && result.data) {
        const parsed = JSON.parse(result.data) as Question[];
        if (Array.isArray(parsed)) {
          this.questions = parsed;
        }
      }
    } catch (e) {
      console.error('加载失败');
    }
    this.loading = false;
  }

  async submitAnswers() {
    this.loading = true;
    try {
      const result = await ApiService.submitAssessment(this.answers);
      if (result.code === 200 && result.data) {
        const parsed = JSON.parse(result.data) as AssessmentResult;
        this.result = parsed;
      }
    } catch (e) {
      console.error('提交失败');
    }
    this.loading = false;
  }

  selectAnswer(questionId: number, option: string) {
    this.answers[questionId] = option;
  }

  getCurrentQuestionId(): number {
    return this.questions[this.currentIndex]?.id || 0;
  }

  getOptionText(option: string): string {
    const question = this.questions[this.currentIndex];
    if (!question) return '';
    switch (option) {
      case 'A': return question.optionA;
      case 'B': return question.optionB;
      case 'C': return question.optionC;
      case 'D': return question.optionD;
      default: return '';
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
          .onClick(() => { router.back(); })
        Text('心理测评')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor('#182431')
          .fontFamily('HarmonyOS Sans')
          .layoutWeight(1)
      }
      .width('100%')
      .height(56)
      .padding({ left: 16, right: 16 })
      .backgroundColor('#FFFFFF')
      .border({ width: { bottom: 1 }, color: '#F0F0F0' })
      .shadow({ radius: 8, color: '#00000008', offsetY: 2 })

      if (this.result) {
        this.ResultView()
      } else if (this.questions.length > 0) {
        // ==================== 答题界面 ====================
        Column() {
          // 进度条
          Column() {
            Row() {
              Text(`题目 ${this.currentIndex + 1}`)
                .fontSize(14)
                .fontWeight(FontWeight.Medium)
                .fontColor('#007DFF')
                .fontFamily('HarmonyOS Sans')
              Text(` / ${this.questions.length}`)
                .fontSize(14)
                .fontColor('#8A8A8A')
                .fontFamily('HarmonyOS Sans')
            }
            .width('100%')
            .margin({ bottom: 8 })

            Row() {
              Row()
                .width(`${((this.currentIndex + 1) / this.questions.length) * 100}%`)
                .height(6)
                .backgroundColor('#007DFF')
                .borderRadius(3)
                .animation({ duration: 300, curve: Curve.EaseOut })
            }
            .width('100%')
            .height(6)
            .backgroundColor('#F0F0F0')
            .borderRadius(3)
          }
          .width('92%')
          .margin({ top: 24, bottom: 24 })

          // 题目卡片
          Column() {
            Text(this.questions[this.currentIndex]?.content || '')
              .fontSize(18)
              .fontWeight(FontWeight.Medium)
              .fontColor('#182431')
              .fontFamily('HarmonyOS Sans')
              .lineHeight(26)
          }
          .width('92%')
          .padding(20)
          .backgroundColor('#FFFFFF')
          .borderRadius(16)
          .border({ width: 1, color: '#F0F0F0' })
          .shadow({ radius: 8, color: '#00000008', offsetY: 4 })
          .margin({ bottom: 24 })

          // 选项
          Column() {
            ForEach(['A', 'B', 'C', 'D'], (option: string) => {
              Row() {
                Column() {
                  Text(option)
                    .fontSize(16)
                    .fontWeight(FontWeight.Medium)
                    .fontColor(this.answers[this.getCurrentQuestionId()] === option ? '#FFFFFF' : '#007DFF')
                    .fontFamily('HarmonyOS Sans')
                }
                .width(32)
                .height(32)
                .borderRadius(16)
                .backgroundColor(this.answers[this.getCurrentQuestionId()] === option ? '#007DFF' : '#F0F0F0')
                .justifyContent(FlexAlign.Center)
                .margin({ right: 16 })

                Text(this.getOptionText(option))
                  .fontSize(16)
                  .fontColor(this.answers[this.getCurrentQuestionId()] === option ? '#007DFF' : '#5A6C82')
                  .fontFamily('HarmonyOS Sans')
                  .lineHeight(22)
                  .layoutWeight(1)
              }
              .width('100%')
              .padding(16)
              .backgroundColor(this.answers[this.getCurrentQuestionId()] === option ? '#F0F8FF' : '#FFFFFF')
              .borderRadius(12)
              .border({ width: 1, color: this.answers[this.getCurrentQuestionId()] === option ? '#007DFF' : '#F0F0F0' })
              .margin({ bottom: 12 })
              .onClick(() => { this.selectAnswer(this.getCurrentQuestionId(), option); })
            })
          }
          .width('92%')
          .margin({ bottom: 32 })

          // 导航按钮
          Row() {
            if (this.currentIndex > 0) {
              Button('上一题')
                .width('45%')
                .height(48)
                .borderRadius(24)
                .backgroundColor('#F6F6F6')
                .fontColor('#182431')
                .fontFamily('HarmonyOS Sans')
                .fontWeight(FontWeight.Medium)
                .onClick(() => { this.currentIndex--; })
            }

            if (this.currentIndex < this.questions.length - 1) {
              Button('下一题')
                .width('45%')
                .height(48)
                .borderRadius(24)
                .backgroundColor('#007DFF')
                .fontColor('#FFFFFF')
                .fontFamily('HarmonyOS Sans')
                .fontWeight(FontWeight.Medium)
                .margin({ left: '10%' })
                .onClick(() => { this.currentIndex++; })
            } else {
              Button(this.loading ? '提交中...' : '提交测评')
                .width('45%')
                .height(48)
                .borderRadius(24)
                .backgroundColor('#007DFF')
                .fontColor('#FFFFFF')
                .fontFamily('HarmonyOS Sans')
                .fontWeight(FontWeight.Medium)
                .margin({ left: '10%' })
                .onClick(() => { this.submitAnswers(); })
            }
          }
          .width('92%')
        }
        .width('100%')
        .layoutWeight(1)
        .alignItems(HorizontalAlign.Center)
      } else {
        // ==================== 加载状态 ====================
        Column() {
          Text('⏳')
            .fontSize(48)
            .margin({ bottom: 16 })
          Text('加载题目中...')
            .fontSize(16)
            .fontColor('#8A8A8A')
            .fontFamily('HarmonyOS Sans')
        }
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#FFFFFF')
    .opacity(this.fadeIn ? 1 : 0)
    .animation({ duration: 300, curve: Curve.EaseOut })
  }

  @Builder
  ResultView() {
    Column() {
      // 结果标题
      Column() {
        Text('📊')
          .fontSize(48)
          .margin({ bottom: 16 })
        Text('你的能力图谱')
          .fontSize(22)
          .fontWeight(FontWeight.Bold)
          .fontColor('#182431')
          .fontFamily('HarmonyOS Sans')
        Text('基于测评结果的专业推荐')
          .fontSize(14)
          .fontColor('#8A8A8A')
          .fontFamily('HarmonyOS Sans')
          .margin({ top: 4 })
      }
      .alignItems(HorizontalAlign.Center)
      .margin({ bottom: 32 })

      if (this.result) {
        // 能力维度
        Column() {
          this.ScoreRow('逻辑思维', this.result.logicScore, '#007DFF')
          this.ScoreRow('创造能力', this.result.creativityScore, '#00C853')
          this.ScoreRow('沟通能力', this.result.communicationScore, '#FF6D00')
          this.ScoreRow('领导能力', this.result.leadershipScore, '#9C27B0')
          this.ScoreRow('动手能力', this.result.handsOnScore, '#FF4081')
          this.ScoreRow('社交能力', this.result.socialScore, '#3F51B5')
          this.ScoreRow('艺术能力', this.result.artisticScore, '#4CAF50')
          this.ScoreRow('实践能力', this.result.practicalScore, '#FF9800')
        }
        .width('92%')
        .margin({ bottom: 32 })

        // 人格类型
        Column() {
          Text('人格类型')
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
            .fontColor('#182431')
            .fontFamily('HarmonyOS Sans')
            .margin({ bottom: 12 })
          Text(this.result.personalityType || '未检测到')
            .fontSize(16)
            .fontColor('#5A6C82')
            .fontFamily('HarmonyOS Sans')
            .lineHeight(24)
        }
        .width('92%')
        .padding(20)
        .backgroundColor('#F9F9F9')
        .borderRadius(16)
        .margin({ bottom: 20 })

        // 推荐专业
        Column() {
          Text('推荐专业')
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
            .fontColor('#182431')
            .fontFamily('HarmonyOS Sans')
            .margin({ bottom: 12 })
          Text(this.result.recommendedMajors || '暂无推荐')
            .fontSize(16)
            .fontColor('#5A6C82')
            .fontFamily('HarmonyOS Sans')
            .lineHeight(24)
        }
        .width('92%')
        .padding(20)
        .backgroundColor('#F9F9F9')
        .borderRadius(16)
        .margin({ bottom: 32 })

        // 重新测试按钮
        Button('重新测试')
          .width('92%')
          .height(48)
          .borderRadius(24)
          .backgroundColor('#F6F6F6')
          .fontColor('#182431')
          .fontFamily('HarmonyOS Sans')
          .fontWeight(FontWeight.Medium)
          .onClick(() => {
            this.result = null;
            this.currentIndex = 0;
            this.answers = {};
          })
      }
    }
    .width('100%')
    .height('100%')
    .alignItems(HorizontalAlign.Center)
    .padding({ top: 24 })
  }

  @Builder
  ScoreRow(label: string, score: number, color: string) {
    Row() {
      Text(label)
        .fontSize(16)
        .fontColor('#5A6C82')
        .fontFamily('HarmonyOS Sans')
        .width(80)
      
      Row() {
        Row()
          .width(`${score}%`)
          .height(8)
          .backgroundColor(color)
          .borderRadius(4)
      }
      .layoutWeight(1)
      .height(8)
      .backgroundColor('#F0F0F0')
      .borderRadius(4)
      .margin({ left: 16, right: 16 })

      Text(`${score}分`)
        .fontSize(16)
        .fontWeight(FontWeight.Medium)
        .fontColor('#182431')
        .fontFamily('HarmonyOS Sans')
        .width(50)
    }
    .width('100%')
    .margin({ bottom: 12 })
  }
}
