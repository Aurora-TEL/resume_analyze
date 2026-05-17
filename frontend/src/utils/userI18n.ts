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
  },
};

export function useUserMessages() {
  const localeStore = useLocaleStore();
  return computed(() => userMessages[localeStore.locale]);
}
