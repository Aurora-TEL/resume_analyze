import { computed } from "vue";

import { useLocaleStore } from "@/stores/locale";

type UserMessages = {
  layout: {
    brandCopy: string;
    defaultUserName: string;
    loggedOut: string;
    logout: string;
    newAnalysis: string;
    uploadResume: string;
    languageLabel: string;
    languageChinese: string;
    languageEnglish: string;
    navDashboard: string;
    navDashboardHint: string;
    navResumes: string;
    navResumesHint: string;
    navJobs: string;
    navJobsHint: string;
    navAnalysis: string;
    navAnalysisHint: string;
    navReports: string;
    navReportsHint: string;
    navProfile: string;
    navProfileHint: string;
    titleDashboard: string;
    titleResumes: string;
    titleResumeUpload: string;
    titleResumeDetail: string;
    titleJobs: string;
    titleJobCreate: string;
    titleJobDetail: string;
    titleAnalysisCreate: string;
    titleAnalysisTask: string;
    titleReports: string;
    titleReportDetail: string;
    titleProfile: string;
    titleFallback: string;
  };
  auth: {
    login: {
      heroTitle: string;
      heroCopy: string;
      pointResume: string;
      pointStructure: string;
      pointReport: string;
      panelTitle: string;
      panelCopy: string;
      email: string;
      password: string;
      passwordPlaceholder: string;
      submit: string;
      noAccount: string;
      registerNow: string;
      validationEmailRequired: string;
      validationEmailInvalid: string;
      validationPasswordRequired: string;
      success: string;
    };
    register: {
      panelTitle: string;
      panelCopy: string;
      nickname: string;
      nicknamePlaceholder: string;
      email: string;
      password: string;
      passwordPlaceholder: string;
      confirmPassword: string;
      confirmPasswordPlaceholder: string;
      submit: string;
      hasAccount: string;
      toLogin: string;
      heroTitle: string;
      heroCopy: string;
      validationNicknameRequired: string;
      validationEmailRequired: string;
      validationEmailInvalid: string;
      validationPasswordRequired: string;
      validationPasswordMin: string;
      validationConfirmRequired: string;
      validationConfirmMismatch: string;
      success: string;
    };
  };
  dashboard: {
    heroTitle: string;
    heroCopy: string;
    actionUpload: string;
    actionCreateJob: string;
    actionStartAnalysis: string;
    metricResumes: string;
    metricResumesNote: string;
    metricJobs: string;
    metricJobsNote: string;
    metricTasks: string;
    metricTasksNote: string;
    metricReports: string;
    metricReportsNote: string;
    recentReportsTitle: string;
    recentReportsCopy: string;
    recentReportsAll: string;
    recentReportsEmpty: string;
    tableResume: string;
    tableJob: string;
    tableTotalScore: string;
    tableMatchScore: string;
    tableCreatedAt: string;
    tableAction: string;
    tableView: string;
    nextStepsTitle: string;
    nextStepsCopy: string;
    stepUploadTitle: string;
    stepUploadDesc: string;
    stepJobTitle: string;
    stepJobDesc: string;
    stepReportTitle: string;
    stepReportDesc: string;
  };
  resumes: {
    list: {
      heroTitle: string;
      heroCopy: string;
      actionUpload: string;
      actionRefresh: string;
      sectionTitle: string;
      sectionCopy: string;
      searchPlaceholder: string;
      empty: string;
      tableTitle: string;
      tableFileName: string;
      tableType: string;
      tableSize: string;
      tableStatus: string;
      tableDefault: string;
      tableCreatedAt: string;
      tableAction: string;
      defaultYes: string;
      actionDetail: string;
      actionParse: string;
      actionSetDefault: string;
      actionAnalyze: string;
      actionDelete: string;
      parseSuccess: string;
      defaultUpdated: string;
      deleteConfirmTitle: string;
      deleteConfirmMessage: string;
      deleteSuccess: string;
    };
  };
  jobs: {
    list: {
      heroTitle: string;
      heroCopy: string;
      actionCreate: string;
      actionRefresh: string;
      sectionTitle: string;
      sectionCopy: string;
      searchPlaceholder: string;
      empty: string;
      tableTitle: string;
      tableCompany: string;
      tableIndustry: string;
      tableLocation: string;
      tableStatus: string;
      tableCreatedAt: string;
      tableAction: string;
      actionDetail: string;
      actionParse: string;
      actionAnalyze: string;
      actionDelete: string;
      parseSuccess: string;
      deleteConfirmTitle: string;
      deleteConfirmMessage: string;
      deleteSuccess: string;
    };
  };
  analysis: {
    create: {
      heroTitle: string;
      heroCopy: string;
      sectionTitle: string;
      sectionCopy: string;
      labelResume: string;
      labelJob: string;
      labelTaskType: string;
      placeholderResume: string;
      placeholderJob: string;
      taskTypeValue: string;
      actionSubmit: string;
      actionViewReports: string;
      resumeSectionTitle: string;
      resumeSectionCopy: string;
      resumeEmpty: string;
      jobSectionTitle: string;
      jobSectionCopy: string;
      jobEmpty: string;
      companyFallback: string;
      validationResumeRequired: string;
      validationJobRequired: string;
      success: string;
    };
  };
  reports: {
    list: {
      heroTitle: string;
      heroCopy: string;
      actionCreate: string;
      actionRefresh: string;
      sectionTitle: string;
      sectionCopy: string;
      empty: string;
      tableResume: string;
      tableJob: string;
      tableTotalScore: string;
      tableMatchScore: string;
      tableSummary: string;
      tableCreatedAt: string;
      tableAction: string;
      actionDetail: string;
    };
  };
};

const userMessages: Record<"zh-CN" | "en-US", UserMessages> = {
  "zh-CN": {
    layout: {
      brandCopy: "\u628a\u7b80\u5386\u3001\u5c97\u4f4d\u548c\u5206\u6790\u62a5\u544a\u653e\u8fdb\u4e00\u6761\u987a\u6ed1\u4e3b\u94fe\u8def\u91cc\u3002",
      defaultUserName: "\u672a\u547d\u540d\u7528\u6237",
      loggedOut: "\u672a\u767b\u5f55",
      logout: "\u9000\u51fa\u767b\u5f55",
      newAnalysis: "\u65b0\u5efa\u5206\u6790",
      uploadResume: "\u4e0a\u4f20\u7b80\u5386",
      languageLabel: "\u8bed\u8a00",
      languageChinese: "\u4e2d\u6587",
      languageEnglish: "English",
      navDashboard: "\u6982\u89c8",
      navDashboardHint: "\u603b\u89c8\u5f53\u524d\u8fdb\u5ea6",
      navResumes: "\u7b80\u5386",
      navResumesHint: "\u4e0a\u4f20\u4e0e\u89e3\u6790",
      navJobs: "\u5c97\u4f4d",
      navJobsHint: "\u6574\u7406 JD \u9700\u6c42",
      navAnalysis: "\u5206\u6790",
      navAnalysisHint: "\u53d1\u8d77\u5339\u914d\u5206\u6790",
      navReports: "\u62a5\u544a",
      navReportsHint: "\u67e5\u770b\u7ed3\u679c\u6c89\u6dc0",
      navProfile: "\u6211\u7684",
      navProfileHint: "\u7ef4\u62a4\u4e2a\u4eba\u4fe1\u606f",
      titleDashboard: "\u5de5\u4f5c\u53f0",
      titleResumes: "\u7b80\u5386\u4e2d\u5fc3",
      titleResumeUpload: "\u4e0a\u4f20\u7b80\u5386",
      titleResumeDetail: "\u7b80\u5386\u8be6\u60c5",
      titleJobs: "\u5c97\u4f4d\u4e2d\u5fc3",
      titleJobCreate: "\u521b\u5efa\u5c97\u4f4d",
      titleJobDetail: "\u5c97\u4f4d\u8be6\u60c5",
      titleAnalysisCreate: "\u53d1\u8d77\u5206\u6790",
      titleAnalysisTask: "\u4efb\u52a1\u72b6\u6001",
      titleReports: "\u5206\u6790\u62a5\u544a",
      titleReportDetail: "\u62a5\u544a\u8be6\u60c5",
      titleProfile: "\u4e2a\u4eba\u8bbe\u7f6e",
      titleFallback: "\u8be6\u60c5\u9875",
    },
    auth: {
      login: {
        heroTitle: "\u767b\u5f55\u540e\uff0c\u76f4\u63a5\u5f00\u59cb\u8dd1\u771f\u5b9e\u5206\u6790\u3002",
        heroCopy: "\u73b0\u5728\u524d\u540e\u7aef\u548c AI \u94fe\u8def\u90fd\u5df2\u7ecf\u6253\u901a\uff0c\u4f60\u53ef\u4ee5\u4ece\u4e0a\u4f20\u7b80\u5386\u5f00\u59cb\uff0c\u4e00\u8def\u8d70\u5230\u5c97\u4f4d\u5339\u914d\u548c\u62a5\u544a\u67e5\u770b\u3002",
        pointResume: "\u4e0a\u4f20 PDF / DOCX / TXT \u7b80\u5386",
        pointStructure: "\u7528 DeepSeek \u89e3\u6790\u5c97\u4f4d\u4e0e\u7b80\u5386\u7ed3\u6784",
        pointReport: "\u751f\u6210\u53ef\u8ffd\u8e2a\u7684\u5206\u6790\u62a5\u544a",
        panelTitle: "\u6b22\u8fce\u56de\u6765",
        panelCopy: "\u8f93\u5165\u8d26\u53f7\u4fe1\u606f\uff0c\u7ee7\u7eed\u4f60\u7684\u7b80\u5386\u4f18\u5316\u6d41\u7a0b\u3002",
        email: "\u90ae\u7bb1",
        password: "\u5bc6\u7801",
        passwordPlaceholder: "\u81f3\u5c11 8 \u4f4d\u5bc6\u7801",
        submit: "\u767b\u5f55",
        noAccount: "\u8fd8\u6ca1\u6709\u8d26\u53f7\uff1f",
        registerNow: "\u7acb\u5373\u6ce8\u518c",
        validationEmailRequired: "\u8bf7\u8f93\u5165\u90ae\u7bb1",
        validationEmailInvalid: "\u90ae\u7bb1\u683c\u5f0f\u4e0d\u6b63\u786e",
        validationPasswordRequired: "\u8bf7\u8f93\u5165\u5bc6\u7801",
        success: "\u767b\u5f55\u6210\u529f",
      },
      register: {
        panelTitle: "\u521b\u5efa\u8d26\u53f7",
        panelCopy: "\u6ce8\u518c\u540e\u5c31\u80fd\u4e0a\u4f20\u7b80\u5386\u3001\u89e3\u6790\u5c97\u4f4d\u5e76\u751f\u6210\u5206\u6790\u62a5\u544a\u3002",
        nickname: "\u6635\u79f0",
        nicknamePlaceholder: "\u600e\u4e48\u79f0\u547c\u4f60",
        email: "\u90ae\u7bb1",
        password: "\u5bc6\u7801",
        passwordPlaceholder: "\u81f3\u5c11 8 \u4f4d\u5bc6\u7801",
        confirmPassword: "\u786e\u8ba4\u5bc6\u7801",
        confirmPasswordPlaceholder: "\u518d\u6b21\u8f93\u5165\u5bc6\u7801",
        submit: "\u6ce8\u518c\u5e76\u8fdb\u5165\u5de5\u4f5c\u53f0",
        hasAccount: "\u5df2\u7ecf\u6709\u8d26\u53f7\uff1f",
        toLogin: "\u53bb\u767b\u5f55",
        heroTitle: "\u4ece\u6ce8\u518c\u5f00\u59cb\uff0c\u628a\u7b80\u5386\u4f18\u5316\u6d41\u7a0b\u88c5\u8fdb\u540c\u4e00\u4e2a\u5de5\u4f5c\u53f0\u3002",
        heroCopy: "\u4f60\u4e0d\u9700\u8981\u518d\u5728\u6587\u6863\u3001\u6a21\u578b\u548c\u8868\u683c\u4e4b\u95f4\u6765\u56de\u5207\u3002\u8fd9\u91cc\u4f1a\u628a\u7b80\u5386\u3001JD\u3001\u5206\u6790\u7ed3\u679c\u548c\u4fee\u6539\u5efa\u8bae\u4e32\u6210\u4e00\u6761\u8def\u5f84\u3002",
        validationNicknameRequired: "\u8bf7\u8f93\u5165\u6635\u79f0",
        validationEmailRequired: "\u8bf7\u8f93\u5165\u90ae\u7bb1",
        validationEmailInvalid: "\u90ae\u7bb1\u683c\u5f0f\u4e0d\u6b63\u786e",
        validationPasswordRequired: "\u8bf7\u8f93\u5165\u5bc6\u7801",
        validationPasswordMin: "\u5bc6\u7801\u81f3\u5c11 8 \u4f4d",
        validationConfirmRequired: "\u8bf7\u518d\u6b21\u8f93\u5165\u5bc6\u7801",
        validationConfirmMismatch: "\u4e24\u6b21\u8f93\u5165\u7684\u5bc6\u7801\u4e0d\u4e00\u81f4",
        success: "\u6ce8\u518c\u6210\u529f",
      },
    },
    dashboard: {
      heroTitle: "\u4f60\u7684\u7b80\u5386\u5206\u6790\u5de5\u4f5c\u53f0\u5df2\u7ecf\u8fdb\u5165\u53ef\u7528\u72b6\u6001\u3002",
      heroCopy: "\u5f53\u524d\u524d\u7aef\u4f1a\u76f4\u63a5\u8fde\u63a5\u672c\u5730\u540e\u7aef\u548c DeepSeek\u3002\u4f60\u53ef\u4ee5\u4ece\u8fd9\u91cc\u5feb\u901f\u8df3\u5230\u4e0a\u4f20\u7b80\u5386\u3001\u521b\u5efa\u5c97\u4f4d\u6216\u67e5\u770b\u6700\u8fd1\u7684\u5206\u6790\u7ed3\u679c\u3002",
      actionUpload: "\u4e0a\u4f20\u65b0\u7b80\u5386",
      actionCreateJob: "\u521b\u5efa\u5c97\u4f4d",
      actionStartAnalysis: "\u53d1\u8d77\u5206\u6790",
      metricResumes: "\u7b80\u5386\u6570\u91cf",
      metricResumesNote: "\u5df2\u4e0a\u4f20\u5e76\u7eb3\u5165\u5f53\u524d\u5de5\u4f5c\u6d41\u7684\u7b80\u5386\u603b\u6570\u3002",
      metricJobs: "\u5c97\u4f4d\u6570\u91cf",
      metricJobsNote: "\u5df2\u6574\u7406\u5e76\u53ef\u76f4\u63a5\u5339\u914d\u7684\u5c97\u4f4d\u63cf\u8ff0\u3002",
      metricTasks: "\u5206\u6790\u4efb\u52a1",
      metricTasksNote: "\u5305\u542b\u5df2\u5b8c\u6210\u548c\u8fdb\u884c\u4e2d\u7684\u5206\u6790\u4efb\u52a1\u3002",
      metricReports: "\u62a5\u544a\u6c89\u6dc0",
      metricReportsNote: "\u5df2\u7ecf\u751f\u6210\uff0c\u53ef\u4f9b\u56de\u770b\u548c\u8fed\u4ee3\u7684\u5206\u6790\u62a5\u544a\u3002",
      recentReportsTitle: "\u6700\u8fd1\u62a5\u544a",
      recentReportsCopy: "\u4f18\u5148\u56de\u770b\u6700\u65b0\u7ed3\u679c\uff0c\u5feb\u901f\u8fdb\u5165\u4e0b\u4e00\u8f6e\u4f18\u5316\u3002",
      recentReportsAll: "\u67e5\u770b\u5168\u90e8",
      recentReportsEmpty: "\u8fd8\u6ca1\u6709\u62a5\u544a\uff0c\u5148\u53d1\u8d77\u4e00\u6b21\u5206\u6790\u5427\u3002",
      tableResume: "\u7b80\u5386",
      tableJob: "\u5c97\u4f4d",
      tableTotalScore: "\u603b\u5206",
      tableMatchScore: "\u5339\u914d\u5ea6",
      tableCreatedAt: "\u751f\u6210\u65f6\u95f4",
      tableAction: "\u64cd\u4f5c",
      tableView: "\u67e5\u770b",
      nextStepsTitle: "\u4e0b\u4e00\u6b65\u5efa\u8bae",
      nextStepsCopy: "\u6309\u7167\u8fd9\u6761\u987a\u5e8f\u63a8\u8fdb\uff0c\u4f1a\u66f4\u5feb\u8fdb\u5165\u7a33\u5b9a\u4ea7\u51fa\u3002",
      stepUploadTitle: "\u4e0a\u4f20\u7b80\u5386",
      stepUploadDesc: "\u81f3\u5c11\u51c6\u5907\u4e00\u4efd\u53ef\u4ee5\u53c2\u4e0e AI \u89e3\u6790\u7684\u7b80\u5386\u6587\u4ef6\u3002",
      stepJobTitle: "\u6574\u7406\u5c97\u4f4d",
      stepJobDesc: "\u8865\u5145\u76ee\u6807\u5c97\u4f4d JD\uff0c\u5e2e\u52a9\u6a21\u578b\u5224\u65ad\u6280\u80fd\u4e0e\u5173\u952e\u8bcd\u5339\u914d\u5ea6\u3002",
      stepReportTitle: "\u751f\u6210\u62a5\u544a",
      stepReportDesc: "\u53d1\u8d77 full_analysis\uff0c\u67e5\u770b strengths\u3001weaknesses \u548c next actions\u3002",
    },
    resumes: {
      list: {
        heroTitle: "\u628a\u53ef\u5206\u6790\u7684\u7b80\u5386\u6574\u7406\u6210\u4e00\u4e2a\u7a33\u5b9a\u5165\u53e3\u3002",
        heroCopy: "\u4e0a\u4f20\u4e4b\u540e\u4f60\u53ef\u4ee5\u91cd\u65b0\u89e3\u6790\u3001\u8bbe\u4e3a\u9ed8\u8ba4\u7b80\u5386\uff0c\u6216\u8005\u76f4\u63a5\u5e26\u7740\u5b83\u53d1\u8d77\u5c97\u4f4d\u5339\u914d\u5206\u6790\u3002",
        actionUpload: "\u4e0a\u4f20\u7b80\u5386",
        actionRefresh: "\u5237\u65b0\u5217\u8868",
        sectionTitle: "\u7b80\u5386\u5217\u8868",
        sectionCopy: "\u5f53\u524d\u5171 {total} \u4efd\u7b80\u5386\u3002",
        searchPlaceholder: "\u6309\u6807\u9898\u641c\u7d22",
        empty: "\u8fd8\u6ca1\u6709\u7b80\u5386\uff0c\u5148\u4e0a\u4f20\u7b2c\u4e00\u4efd\u5427\u3002",
        tableTitle: "\u6807\u9898",
        tableFileName: "\u6587\u4ef6\u540d",
        tableType: "\u7c7b\u578b",
        tableSize: "\u5927\u5c0f",
        tableStatus: "\u72b6\u6001",
        tableDefault: "\u9ed8\u8ba4",
        tableCreatedAt: "\u521b\u5efa\u65f6\u95f4",
        tableAction: "\u64cd\u4f5c",
        defaultYes: "\u9ed8\u8ba4",
        actionDetail: "\u8be6\u60c5",
        actionParse: "AI \u89e3\u6790",
        actionSetDefault: "\u8bbe\u4e3a\u9ed8\u8ba4",
        actionAnalyze: "\u53bb\u5206\u6790",
        actionDelete: "\u5220\u9664",
        parseSuccess: "\u7b80\u5386\u89e3\u6790\u5b8c\u6210",
        defaultUpdated: "\u9ed8\u8ba4\u7b80\u5386\u5df2\u66f4\u65b0",
        deleteConfirmTitle: "\u5220\u9664\u7b80\u5386",
        deleteConfirmMessage: "\u5220\u9664\u540e\u5c06\u4e0d\u518d\u51fa\u73b0\u5728\u5f53\u524d\u5217\u8868\u4e2d\uff0c\u786e\u8ba4\u7ee7\u7eed\u5417\uff1f",
        deleteSuccess: "\u7b80\u5386\u5df2\u5220\u9664",
      },
    },
    jobs: {
      list: {
        heroTitle: "\u628a\u76ee\u6807\u5c97\u4f4d\u6574\u7406\u6210\u53ef\u5339\u914d\u7684\u7ed3\u6784\u5316\u8f93\u5165\u3002",
        heroCopy: "\u5c97\u4f4d\u8d8a\u6e05\u6670\uff0c\u540e\u9762\u7684\u5173\u952e\u8bcd\u8986\u76d6\u3001\u7ecf\u9a8c\u5dee\u8ddd\u548c\u5efa\u8bae\u9879\u5c31\u8d8a\u7a33\u5b9a\u3002",
        actionCreate: "\u521b\u5efa\u5c97\u4f4d",
        actionRefresh: "\u5237\u65b0\u5217\u8868",
        sectionTitle: "\u5c97\u4f4d\u5217\u8868",
        sectionCopy: "\u5f53\u524d\u5171 {total} \u4e2a\u5c97\u4f4d\u3002",
        searchPlaceholder: "\u6309\u5c97\u4f4d\u6216\u516c\u53f8\u641c\u7d22",
        empty: "\u8fd8\u6ca1\u6709\u5c97\u4f4d\u63cf\u8ff0\uff0c\u5148\u521b\u5efa\u4e00\u4e2a\u5427\u3002",
        tableTitle: "\u5c97\u4f4d\u540d\u79f0",
        tableCompany: "\u516c\u53f8",
        tableIndustry: "\u884c\u4e1a",
        tableLocation: "\u5730\u70b9",
        tableStatus: "\u72b6\u6001",
        tableCreatedAt: "\u521b\u5efa\u65f6\u95f4",
        tableAction: "\u64cd\u4f5c",
        actionDetail: "\u8be6\u60c5",
        actionParse: "\u91cd\u65b0\u89e3\u6790",
        actionAnalyze: "\u53bb\u5206\u6790",
        actionDelete: "\u5220\u9664",
        parseSuccess: "\u5c97\u4f4d\u89e3\u6790\u5b8c\u6210",
        deleteConfirmTitle: "\u5220\u9664\u5c97\u4f4d",
        deleteConfirmMessage: "\u5220\u9664\u540e\u5c06\u4e0d\u518d\u51fa\u73b0\u5728\u5f53\u524d\u5217\u8868\u4e2d\uff0c\u786e\u8ba4\u7ee7\u7eed\u5417\uff1f",
        deleteSuccess: "\u5c97\u4f4d\u5df2\u5220\u9664",
      },
    },
    analysis: {
      create: {
        heroTitle: "\u628a\u7b80\u5386\u548c\u5c97\u4f4d\u653e\u5728\u4e00\u8d77\uff0c\u76f4\u63a5\u751f\u6210\u5b8c\u6574\u5206\u6790\u62a5\u544a\u3002",
        heroCopy: "\u5f53\u524d MVP \u9ed8\u8ba4\u6267\u884c full_analysis\u3002\u63a5\u53e3\u4f1a\u540c\u6b65\u8fd4\u56de\u7ed3\u679c\uff0c\u6240\u4ee5\u6210\u529f\u540e\u4f1a\u76f4\u63a5\u8df3\u5230\u62a5\u544a\u9875\u3002",
        sectionTitle: "\u5206\u6790\u914d\u7f6e",
        sectionCopy: "\u5148\u9009\u62e9\u4e00\u4efd\u7b80\u5386\uff0c\u518d\u9009\u62e9\u4e00\u4e2a\u5c97\u4f4d\u3002",
        labelResume: "\u9009\u62e9\u7b80\u5386",
        labelJob: "\u9009\u62e9\u5c97\u4f4d",
        labelTaskType: "\u5206\u6790\u7c7b\u578b",
        placeholderResume: "\u8bf7\u9009\u62e9\u7b80\u5386",
        placeholderJob: "\u8bf7\u9009\u62e9\u5c97\u4f4d",
        taskTypeValue: "full_analysis",
        actionSubmit: "\u5f00\u59cb\u5206\u6790",
        actionViewReports: "\u67e5\u770b\u5df2\u6709\u62a5\u544a",
        resumeSectionTitle: "\u53ef\u7528\u7b80\u5386",
        resumeSectionCopy: "\u5efa\u8bae\u4f18\u5148\u9009\u62e9\u5df2\u5b8c\u6210 AI \u89e3\u6790\u7684\u7b80\u5386\u3002",
        resumeEmpty: "\u8fd8\u6ca1\u6709\u7b80\u5386\uff0c\u5148\u4e0a\u4f20\u4e00\u4efd\u5427\u3002",
        jobSectionTitle: "\u53ef\u7528\u5c97\u4f4d",
        jobSectionCopy: "\u5efa\u8bae\u9009\u62e9\u5df2\u7ecf\u68c0\u67e5\u8fc7 JD \u5185\u5bb9\u7684\u5c97\u4f4d\u3002",
        jobEmpty: "\u8fd8\u6ca1\u6709\u5c97\u4f4d\uff0c\u5148\u521b\u5efa\u4e00\u4e2a\u5427\u3002",
        companyFallback: "\u672a\u586b\u5199\u516c\u53f8",
        validationResumeRequired: "\u8bf7\u9009\u62e9\u7b80\u5386",
        validationJobRequired: "\u8bf7\u9009\u62e9\u5c97\u4f4d",
        success: "\u5206\u6790\u5b8c\u6210",
      },
    },
    reports: {
      list: {
        heroTitle: "\u628a\u6bcf\u4e00\u6b21\u5206\u6790\u7ed3\u679c\u6c89\u6dc0\u6210\u53ef\u56de\u770b\u7684\u62a5\u544a\u3002",
        heroCopy: "\u8fd9\u91cc\u9002\u5408\u56de\u770b\u4e0d\u540c\u5c97\u4f4d\u4e0b\u7684\u5339\u914d\u5dee\u5f02\uff0c\u89c2\u5bdf\u5173\u952e\u8bcd\u8986\u76d6\u548c\u5efa\u8bae\u9879\u7684\u53d8\u5316\u8d8b\u52bf\u3002",
        actionCreate: "\u65b0\u5efa\u5206\u6790",
        actionRefresh: "\u5237\u65b0\u5217\u8868",
        sectionTitle: "\u62a5\u544a\u5217\u8868",
        sectionCopy: "\u5f53\u524d\u5171 {total} \u4efd\u62a5\u544a\u3002",
        empty: "\u8fd8\u6ca1\u6709\u62a5\u544a\uff0c\u5148\u8dd1\u4e00\u6761\u5206\u6790\u94fe\u8def\u5427\u3002",
        tableResume: "\u7b80\u5386",
        tableJob: "\u5c97\u4f4d",
        tableTotalScore: "\u603b\u5206",
        tableMatchScore: "\u5339\u914d\u5ea6",
        tableSummary: "\u6458\u8981",
        tableCreatedAt: "\u751f\u6210\u65f6\u95f4",
        tableAction: "\u64cd\u4f5c",
        actionDetail: "\u8be6\u60c5",
      },
    },
  },
  "en-US": {
    layout: {
      brandCopy: "Keep resumes, jobs, and analysis reports in one smooth working flow.",
      defaultUserName: "Unnamed User",
      loggedOut: "Not signed in",
      logout: "Log Out",
      newAnalysis: "New Analysis",
      uploadResume: "Upload Resume",
      languageLabel: "Language",
      languageChinese: "\u4e2d\u6587",
      languageEnglish: "English",
      navDashboard: "Overview",
      navDashboardHint: "See current progress",
      navResumes: "Resumes",
      navResumesHint: "Upload and parse",
      navJobs: "Jobs",
      navJobsHint: "Organize JD requirements",
      navAnalysis: "Analysis",
      navAnalysisHint: "Start a matching analysis",
      navReports: "Reports",
      navReportsHint: "Review saved results",
      navProfile: "Profile",
      navProfileHint: "Manage personal info",
      titleDashboard: "Workspace",
      titleResumes: "Resume Center",
      titleResumeUpload: "Upload Resume",
      titleResumeDetail: "Resume Detail",
      titleJobs: "Job Center",
      titleJobCreate: "Create Job",
      titleJobDetail: "Job Detail",
      titleAnalysisCreate: "Start Analysis",
      titleAnalysisTask: "Task Status",
      titleReports: "Analysis Reports",
      titleReportDetail: "Report Detail",
      titleProfile: "Profile Settings",
      titleFallback: "Detail Page",
    },
    auth: {
      login: {
        heroTitle: "Sign in and start real resume analysis right away.",
        heroCopy: "The frontend, backend, and AI flow are already connected. Start from resume upload and go all the way to job matching and report review.",
        pointResume: "Upload PDF / DOCX / TXT resumes",
        pointStructure: "Use DeepSeek to parse job and resume structure",
        pointReport: "Generate trackable analysis reports",
        panelTitle: "Welcome Back",
        panelCopy: "Enter your account information and continue your resume improvement flow.",
        email: "Email",
        password: "Password",
        passwordPlaceholder: "At least 8 characters",
        submit: "Sign In",
        noAccount: "Don\u2019t have an account yet?",
        registerNow: "Create one now",
        validationEmailRequired: "Please enter your email",
        validationEmailInvalid: "Please enter a valid email address",
        validationPasswordRequired: "Please enter your password",
        success: "Signed in successfully",
      },
      register: {
        panelTitle: "Create Account",
        panelCopy: "After registering, you can upload resumes, parse jobs, and generate analysis reports.",
        nickname: "Nickname",
        nicknamePlaceholder: "How should we call you?",
        email: "Email",
        password: "Password",
        passwordPlaceholder: "At least 8 characters",
        confirmPassword: "Confirm Password",
        confirmPasswordPlaceholder: "Enter the password again",
        submit: "Register and Enter Workspace",
        hasAccount: "Already have an account?",
        toLogin: "Go to sign in",
        heroTitle: "Start with registration and keep your whole resume improvement flow in one workspace.",
        heroCopy: "You no longer need to jump between documents, models, and spreadsheets. This app keeps resumes, JDs, analysis results, and revision suggestions in one path.",
        validationNicknameRequired: "Please enter a nickname",
        validationEmailRequired: "Please enter your email",
        validationEmailInvalid: "Please enter a valid email address",
        validationPasswordRequired: "Please enter your password",
        validationPasswordMin: "Password must be at least 8 characters",
        validationConfirmRequired: "Please confirm your password",
        validationConfirmMismatch: "The two passwords do not match",
        success: "Registered successfully",
      },
    },
    dashboard: {
      heroTitle: "Your resume analysis workspace is ready to use.",
      heroCopy: "The frontend is connected directly to your local backend and DeepSeek. Jump from here to upload resumes, create jobs, or review recent analysis results.",
      actionUpload: "Upload New Resume",
      actionCreateJob: "Create Job",
      actionStartAnalysis: "Start Analysis",
      metricResumes: "Resumes",
      metricResumesNote: "Total resumes uploaded and included in the current workflow.",
      metricJobs: "Jobs",
      metricJobsNote: "Job descriptions prepared and ready for matching.",
      metricTasks: "Analysis Tasks",
      metricTasksNote: "Includes completed and ongoing analysis tasks.",
      metricReports: "Saved Reports",
      metricReportsNote: "Generated reports available for review and iteration.",
      recentReportsTitle: "Recent Reports",
      recentReportsCopy: "Review the latest results first and move quickly into the next optimization round.",
      recentReportsAll: "View All",
      recentReportsEmpty: "No reports yet. Start an analysis first.",
      tableResume: "Resume",
      tableJob: "Job",
      tableTotalScore: "Score",
      tableMatchScore: "Match",
      tableCreatedAt: "Created At",
      tableAction: "Action",
      tableView: "View",
      nextStepsTitle: "Suggested Next Steps",
      nextStepsCopy: "Following this order helps you reach steady output faster.",
      stepUploadTitle: "Upload Resume",
      stepUploadDesc: "Prepare at least one resume file that can be parsed by AI.",
      stepJobTitle: "Prepare Job",
      stepJobDesc: "Add the target job description so the model can judge skills and keyword coverage.",
      stepReportTitle: "Generate Report",
      stepReportDesc: "Run full_analysis and review strengths, weaknesses, and next actions.",
    },
    resumes: {
      list: {
        heroTitle: "Turn analyzable resumes into a stable starting point.",
        heroCopy: "After uploading, you can re-parse, mark a default resume, or take it straight into job matching analysis.",
        actionUpload: "Upload Resume",
        actionRefresh: "Refresh List",
        sectionTitle: "Resume List",
        sectionCopy: "{total} resumes in the current workspace.",
        searchPlaceholder: "Search by title",
        empty: "No resumes yet. Upload the first one to get started.",
        tableTitle: "Title",
        tableFileName: "File Name",
        tableType: "Type",
        tableSize: "Size",
        tableStatus: "Status",
        tableDefault: "Default",
        tableCreatedAt: "Created At",
        tableAction: "Action",
        defaultYes: "Default",
        actionDetail: "Detail",
        actionParse: "AI Parse",
        actionSetDefault: "Set Default",
        actionAnalyze: "Analyze",
        actionDelete: "Delete",
        parseSuccess: "Resume parsing completed",
        defaultUpdated: "Default resume updated",
        deleteConfirmTitle: "Delete Resume",
        deleteConfirmMessage: "This resume will no longer appear in the current list. Do you want to continue?",
        deleteSuccess: "Resume deleted",
      },
    },
    jobs: {
      list: {
        heroTitle: "Shape target jobs into structured inputs ready for matching.",
        heroCopy: "The clearer the job description is, the steadier the later keyword coverage, experience gaps, and suggestions will be.",
        actionCreate: "Create Job",
        actionRefresh: "Refresh List",
        sectionTitle: "Job List",
        sectionCopy: "{total} jobs in the current workspace.",
        searchPlaceholder: "Search by job or company",
        empty: "No jobs yet. Create one to get started.",
        tableTitle: "Job Title",
        tableCompany: "Company",
        tableIndustry: "Industry",
        tableLocation: "Location",
        tableStatus: "Status",
        tableCreatedAt: "Created At",
        tableAction: "Action",
        actionDetail: "Detail",
        actionParse: "Re-parse",
        actionAnalyze: "Analyze",
        actionDelete: "Delete",
        parseSuccess: "Job parsing completed",
        deleteConfirmTitle: "Delete Job",
        deleteConfirmMessage: "This job will no longer appear in the current list. Do you want to continue?",
        deleteSuccess: "Job deleted",
      },
    },
    analysis: {
      create: {
        heroTitle: "Put a resume and a job together, then generate a full analysis report right away.",
        heroCopy: "The current MVP runs full_analysis by default. The API returns results synchronously, so success usually takes you straight to the report page.",
        sectionTitle: "Analysis Setup",
        sectionCopy: "Choose one resume first, then choose one job.",
        labelResume: "Choose Resume",
        labelJob: "Choose Job",
        labelTaskType: "Task Type",
        placeholderResume: "Please choose a resume",
        placeholderJob: "Please choose a job",
        taskTypeValue: "full_analysis",
        actionSubmit: "Start Analysis",
        actionViewReports: "View Existing Reports",
        resumeSectionTitle: "Available Resumes",
        resumeSectionCopy: "Prefer resumes that have already completed AI parsing.",
        resumeEmpty: "No resumes yet. Upload one first.",
        jobSectionTitle: "Available Jobs",
        jobSectionCopy: "Prefer jobs whose JD content has already been reviewed.",
        jobEmpty: "No jobs yet. Create one first.",
        companyFallback: "Company not set",
        validationResumeRequired: "Please choose a resume",
        validationJobRequired: "Please choose a job",
        success: "Analysis completed",
      },
    },
    reports: {
      list: {
        heroTitle: "Save every analysis result as a report you can review later.",
        heroCopy: "This page is useful for comparing matching gaps across different jobs and watching how keyword coverage and suggestions change over time.",
        actionCreate: "New Analysis",
        actionRefresh: "Refresh List",
        sectionTitle: "Report List",
        sectionCopy: "{total} reports in the current workspace.",
        empty: "No reports yet. Run an analysis flow first.",
        tableResume: "Resume",
        tableJob: "Job",
        tableTotalScore: "Score",
        tableMatchScore: "Match",
        tableSummary: "Summary",
        tableCreatedAt: "Created At",
        tableAction: "Action",
        actionDetail: "Detail",
      },
    },
  },
};

export function useUserMessages() {
  const localeStore = useLocaleStore();
  return computed(() => userMessages[localeStore.locale]);
}
