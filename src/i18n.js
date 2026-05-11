import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    greeting: "Hi, User",
    navigate: "Navigate with the buttons on the left",
    nav: {
      home: "Home",
      essayList: "Essay List",
      teacherUpload: "Teacher Upload",
      studentUpload: "Student Upload",
    },
    buttons: {
      setting: "Setting",
      logout: "Log Out",
      lang_en: "English",
      lang_zh: "中文"
    },
    home: {
      recentEssay: "Most Recent Essay",
      uploaded: "Uploaded",
      loadingEssay: "Loading latest essay...",
      recentFeedback: "Most Recent Feedback",
      strengths: "Strengths",
      essayScore: "Essay Score",
      noStrengths: "Loading feedback..."
    },
    essayList: {
        title: "Essay List",
        searchPlaceholder: "Search by title, author or status...",
        table: {
            title: "Title",
            author: "Author",
            submissionDate: "Submission Date"
        },
        prev: "Prev",
        next: "Next",
        page: "Page",
        of: "of",
        back: "Back to List",
        detail: {
            author: "Author",
            submissionDate: "Submission Date",
            content: "Content",
            feedback: "Feedback",
            rubric: "Rubric",
            score: "Score"
        }
    },
    upload: {
        title: "Essay Upload (Teacher)",
        aiBadge: "AI Powered",
        feedbackReceived: "Feedback Received",
        backToUpload: "Back to Upload",
        essayTitle: "Essay Title",
        selectTitle: "-- Select a title --",
        typeNewTitle: "Or type a new title...",
        essayContent: "Essay Content",
        pasteEssay: "Paste your essay here...",
        uploadOCR: "Upload Image for OCR",
        essayHint: "Full essays will receive better feedback results.",
        essayType: "Essay Type",
        argumentative: "Argumentative",
        narrative: "Narrative",
        rubric: "Rubric",
        selectRubric: "-- Select a rubric --",
        typeNewRubric: "Or type a new rubric...",
        model: "AI Model",
        reset: "Reset",
        submit: "Submit for Feedback",
        processingImage: "Processing image..."
    },
    student: {
        label: "Essay Upload (Student)"
    }
  },
  zh: {
    greeting: "你好，用户",
    navigate: "使用左侧的按钮导航",
    nav: {
      home: "首页",
      essayList: "文章列表",
      teacherUpload: "教师上传",
      studentUpload: "学生上传",
    },
    buttons: {
      setting: "设置",
      logout: "退出登录",
      lang_en: "English",
      lang_zh: "中文"
    },
    home: {
      recentEssay: "最新文章",
      uploaded: "上传时间",
      loadingEssay: "正在加载最新文章...",
      recentFeedback: "最新反馈",
      strengths: "作文评语",
      essayScore: "作文评分",
      noStrengths: "正在加载..."
    },
    essayList: {
        title: "作文列表",
        searchPlaceholder: "搜索题目或作者...",
        table: {
            title: "题目",
            author: "作者",
            submissionDate: "提交日期"
        },
        prev: "上一页",
        next: "下一页",
        page: "第",
        of: "共",
        back: "返回列表",
        detail: {
            author: "作者",
            submissionDate: "提交日期",
            content: "内容",
            feedback: "反馈",
            rubric: "评分标准",
            score: "评分"
        }
    },
    upload: {
        title: "文章上传（教师）",
        aiBadge: "AI 驱动",
        feedbackReceived: "收到的反馈",
        backToUpload: "返回上传",
        essayTitle: "文章题目",
        selectTitle: "-- 选择一个题目 --",
        typeNewTitle: "或输入新题目...",
        essayContent: "文章内容",
        pasteEssay: "请粘贴文章内容...",
        uploadOCR: "上传图片进行 OCR",
        essayHint: "完整的文章将获得更好的反馈结果。",
        essayType: "文章类型",
        argumentative: "议论文",
        narrative: "记叙文",
        rubric: "评分标准",
        selectRubric: "-- 选择评分标准 --",
        typeNewRubric: "或输入新的评分标准...",
        model: "AI 模型",
        reset: "重置",
        submit: "提交",
        processingImage: "图像处理中..."
    },
    student: {
        label: "文章上传 (学生)"
    }
  }
}


const i18n = createI18n({
  legacy: false, // Composition API mode
  locale: 'en',
  fallbackLocale: 'en',
  messages
})

export default i18n
