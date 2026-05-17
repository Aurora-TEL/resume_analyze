import { computed } from "vue";

import { useLocaleStore } from "@/stores/locale";

export type AdminLocale = "zh-CN" | "en-US";

type AdminMessages = {
  layout: {
    brandKicker: string;
    brandTitle: string;
    brandCopy: string;
    defaultAdminName: string;
    backToUserApp: string;
    operations: string;
    navOverview: string;
    navOverviewHint: string;
    navTasks: string;
    navTasksHint: string;
    navApiLogs: string;
    navApiLogsHint: string;
    navPromptTemplates: string;
    navPromptTemplatesHint: string;
    titleOverview: string;
    titleTasks: string;
    titleApiLogs: string;
    titlePromptTemplates: string;
    titleDefault: string;
    languageLabel: string;
    languageChinese: string;
    languageEnglish: string;
  };
  overview: {
    kicker: string;
    title: string;
    copy: string;
    users: string;
    usersNote: string;
    resumesJobs: string;
    resumesJobsNote: string;
    analysisTasks: string;
    analysisTasksNote: (pending: number, running: number) => string;
    aiCalls: string;
    aiCallsNote: (failed: number) => string;
    alertsTitle: string;
    alertsCopy: string;
    alertsWarning: string;
    alertsOk: string;
    failedTasks: string;
    promptTemplates: string;
    reports: string;
    latestApiError: string;
    noRecentError: string;
    quickLinksTitle: string;
    quickLinksCopy: string;
    taskCenterTitle: string;
    taskCenterCopy: string;
    apiLogsTitle: string;
    apiLogsCopy: string;
    promptTitle: string;
    promptCopy: string;
  };
  tasks: {
    title: string;
    copy: string;
    searchPlaceholder: string;
    statusPlaceholder: string;
    taskTypePlaceholder: string;
    fullAnalysis: string;
    jobMatch: string;
    resumeScore: string;
    user: string;
    resume: string;
    job: string;
    taskType: string;
    status: string;
    progress: string;
    createdAt: string;
    errorMessage: string;
  };
  apiLogs: {
    title: string;
    copy: string;
    searchPlaceholder: string;
    statusPlaceholder: string;
    scenePlaceholder: string;
    user: string;
    scene: string;
    model: string;
    status: string;
    tokens: string;
    latency: string;
    template: string;
    errorMessage: string;
    createdAt: string;
  };
  promptTemplates: {
    title: string;
    copy: string;
    newTemplate: string;
    searchPlaceholder: string;
    scenePlaceholder: string;
    statusPlaceholder: string;
    name: string;
    scene: string;
    version: string;
    status: string;
    editor: string;
    description: string;
    updatedAt: string;
    actions: string;
    edit: string;
    delete: string;
    editTitle: string;
    createTitle: string;
    formName: string;
    formScene: string;
    formVersion: string;
    formStatus: string;
    formDescription: string;
    formContent: string;
    cancel: string;
    save: string;
    createSuccess: string;
    updateSuccess: string;
    deleteSuccess: string;
    deleteConfirmTitle: string;
    deleteConfirmMessage: string;
  };
};

const adminMessages: Record<AdminLocale, AdminMessages> = {
  "zh-CN": {
    layout: {
      brandKicker: "\u7ba1\u7406\u540e\u53f0",
      brandTitle: "\u63a7\u5236\u53f0",
      brandCopy:
        "\u628a\u4efb\u52a1\u3001AI \u8c03\u7528\u65e5\u5fd7\u548c Prompt \u6a21\u677f\u96c6\u4e2d\u5230\u4e00\u4e2a\u5de5\u4f5c\u53f0\u91cc\uff0c\u65b9\u4fbf\u7edf\u4e00\u6392\u67e5\u548c\u7ef4\u62a4\u3002",
      defaultAdminName: "\u7ba1\u7406\u5458",
      backToUserApp: "\u8fd4\u56de\u7528\u6237\u7aef",
      operations: "\u8fd0\u8425\u7ba1\u7406",
      navOverview: "\u603b\u89c8",
      navOverviewHint: "\u5173\u952e\u6307\u6807\u4e0e\u5f02\u5e38\u63d0\u9192",
      navTasks: "\u4efb\u52a1\u4e2d\u5fc3",
      navTasksHint: "\u5206\u6790\u4efb\u52a1\u8fdb\u5ea6\u4e0e\u5931\u8d25\u6392\u67e5",
      navApiLogs: "AI \u65e5\u5fd7",
      navApiLogsHint: "\u6a21\u578b\u8c03\u7528\u3001\u8017\u65f6\u548c\u9519\u8bef",
      navPromptTemplates: "Prompt \u6a21\u677f",
      navPromptTemplatesHint: "\u6a21\u677f\u7248\u672c\u4e0e\u5185\u5bb9\u7ba1\u7406",
      titleOverview: "\u540e\u53f0\u603b\u89c8",
      titleTasks: "\u5206\u6790\u4efb\u52a1\u7ba1\u7406",
      titleApiLogs: "AI \u8c03\u7528\u65e5\u5fd7",
      titlePromptTemplates: "Prompt \u6a21\u677f\u7ba1\u7406",
      titleDefault: "\u540e\u53f0\u63a7\u5236\u53f0",
      languageLabel: "\u8bed\u8a00",
      languageChinese: "\u4e2d\u6587",
      languageEnglish: "English",
    },
    overview: {
      kicker: "\u540e\u53f0\u603b\u89c8",
      title: "\u628a\u4efb\u52a1\u3001AI \u8c03\u7528\u548c\u7cfb\u7edf\u4fe1\u53f7\u653e\u8fdb\u4e00\u4e2a\u6e05\u6670\u7684\u5de5\u4f5c\u89c6\u56fe\u91cc\u3002",
      copy: "\u8fd9\u4e2a\u5de5\u4f5c\u53f0\u4f18\u5148\u670d\u52a1\u6392\u67e5\u548c\u8fd0\u8425\uff0c\u8ba9\u5173\u952e\u72b6\u6001\u4e00\u773c\u53ef\u89c1\u3002",
      users: "\u7528\u6237\u6570",
      usersNote: "\u5f53\u524d\u7cfb\u7edf\u91cc\u5df2\u6ce8\u518c\u7684\u5168\u90e8\u8d26\u53f7\u3002",
      resumesJobs: "\u7b80\u5386 / \u5c97\u4f4d",
      resumesJobsNote: "\u5df2\u7ecf\u8fdb\u5165\u4e1a\u52a1\u6d41\u7a0b\u7684\u8d44\u6e90\u603b\u91cf\u3002",
      analysisTasks: "\u5206\u6790\u4efb\u52a1",
      analysisTasksNote: (pending, running) => `\u5f85\u5904\u7406 ${pending}\uff0c\u8fdb\u884c\u4e2d ${running}\u3002`,
      aiCalls: "AI \u8c03\u7528",
      aiCallsNote: (failed) => `\u5931\u8d25 ${failed} \u6b21\u3002`,
      alertsTitle: "\u5f02\u5e38\u63d0\u9192",
      alertsCopy: "\u5982\u679c\u4efb\u52a1\u6267\u884c\u6216 AI \u8c03\u7528\u51fa\u73b0\u6ce2\u52a8\uff0c\u4f18\u5148\u770b\u8fd9\u91cc\u3002",
      alertsWarning: "\u5b58\u5728\u9700\u8981\u5173\u6ce8\u7684\u5931\u8d25\u8bb0\u5f55",
      alertsOk: "\u5f53\u524d\u6ca1\u6709\u660e\u663e\u5f02\u5e38",
      failedTasks: "\u5931\u8d25\u4efb\u52a1",
      promptTemplates: "Prompt \u6a21\u677f",
      reports: "\u5206\u6790\u62a5\u544a",
      latestApiError: "\u6700\u8fd1\u4e00\u6b21 API \u9519\u8bef",
      noRecentError: "\u6682\u65e0\u9519\u8bef",
      quickLinksTitle: "\u5feb\u6377\u5165\u53e3",
      quickLinksCopy: "\u4ece\u8fd9\u91cc\u76f4\u63a5\u8df3\u5230\u6700\u5e38\u7528\u7684\u7ba1\u7406\u9875\u9762\u3002",
      taskCenterTitle: "\u4efb\u52a1\u4e2d\u5fc3",
      taskCenterCopy: "\u67e5\u770b\u5931\u8d25\u4efb\u52a1\u548c\u5361\u4f4f\u7684\u6267\u884c\u94fe\u8def\u3002",
      apiLogsTitle: "AI \u65e5\u5fd7",
      apiLogsCopy: "\u68c0\u67e5\u6a21\u578b\u9519\u8bef\u3001\u8017\u65f6\u548c token \u6d88\u8017\u3002",
      promptTitle: "Prompt \u6a21\u677f",
      promptCopy: "\u7ef4\u62a4\u573a\u666f\u6a21\u677f\u3001\u7248\u672c\u548c\u542f\u7528\u72b6\u6001\u3002",
    },
    tasks: {
      title: "\u5206\u6790\u4efb\u52a1\u7ba1\u7406",
      copy: "\u9002\u5408\u6392\u67e5\u5931\u8d25\u4efb\u52a1\u3001\u5361\u4f4f\u4efb\u52a1\u548c\u5f02\u5e38\u7528\u6237\u8f93\u5165\u3002",
      searchPlaceholder: "\u6309\u7528\u6237\u3001\u7b80\u5386\u6216\u5c97\u4f4d\u641c\u7d22",
      statusPlaceholder: "\u72b6\u6001",
      taskTypePlaceholder: "\u4efb\u52a1\u7c7b\u578b",
      fullAnalysis: "\u5b8c\u6574\u5206\u6790",
      jobMatch: "\u5c97\u4f4d\u5339\u914d",
      resumeScore: "\u7b80\u5386\u8bc4\u5206",
      user: "\u7528\u6237",
      resume: "\u7b80\u5386",
      job: "\u5c97\u4f4d",
      taskType: "\u4efb\u52a1\u7c7b\u578b",
      status: "\u72b6\u6001",
      progress: "\u8fdb\u5ea6",
      createdAt: "\u521b\u5efa\u65f6\u95f4",
      errorMessage: "\u9519\u8bef\u4fe1\u606f",
    },
    apiLogs: {
      title: "AI \u8c03\u7528\u65e5\u5fd7",
      copy: "\u67e5\u770b\u5931\u8d25\u539f\u56e0\u3001\u8017\u65f6\u548c token \u6d88\u8017\uff0c\u4fbf\u4e8e\u6392\u67e5\u6a21\u578b\u4fa7\u95ee\u9898\u3002",
      searchPlaceholder: "\u6309\u7528\u6237\u3001\u6a21\u578b\u6216\u9519\u8bef\u641c\u7d22",
      statusPlaceholder: "\u72b6\u6001",
      scenePlaceholder: "\u573a\u666f",
      user: "\u7528\u6237",
      scene: "\u573a\u666f",
      model: "\u6a21\u578b",
      status: "\u72b6\u6001",
      tokens: "Tokens",
      latency: "\u8017\u65f6",
      template: "\u6a21\u677f",
      errorMessage: "\u9519\u8bef\u4fe1\u606f",
      createdAt: "\u521b\u5efa\u65f6\u95f4",
    },
    promptTemplates: {
      title: "Prompt \u6a21\u677f\u7ba1\u7406",
      copy: "\u7ef4\u62a4\u6a21\u677f\u7248\u672c\u3001\u542f\u7528\u72b6\u6001\u548c\u573a\u666f\u5185\u5bb9\uff0c\u76f4\u63a5\u5f71\u54cd AI \u8f93\u51fa\u8d28\u91cf\u3002",
      newTemplate: "\u65b0\u589e\u6a21\u677f",
      searchPlaceholder: "\u6309\u540d\u79f0\u6216\u5185\u5bb9\u641c\u7d22",
      scenePlaceholder: "\u573a\u666f",
      statusPlaceholder: "\u72b6\u6001",
      name: "\u540d\u79f0",
      scene: "\u573a\u666f",
      version: "\u7248\u672c",
      status: "\u72b6\u6001",
      editor: "\u7f16\u8f91\u4eba",
      description: "\u8bf4\u660e",
      updatedAt: "\u66f4\u65b0\u65f6\u95f4",
      actions: "\u64cd\u4f5c",
      edit: "\u7f16\u8f91",
      delete: "\u5220\u9664",
      editTitle: "\u7f16\u8f91\u6a21\u677f",
      createTitle: "\u65b0\u589e\u6a21\u677f",
      formName: "\u540d\u79f0",
      formScene: "\u573a\u666f",
      formVersion: "\u7248\u672c",
      formStatus: "\u72b6\u6001",
      formDescription: "\u8bf4\u660e",
      formContent: "\u6a21\u677f\u5185\u5bb9",
      cancel: "\u53d6\u6d88",
      save: "\u4fdd\u5b58",
      createSuccess: "\u6a21\u677f\u5df2\u521b\u5efa",
      updateSuccess: "\u6a21\u677f\u5df2\u66f4\u65b0",
      deleteSuccess: "\u6a21\u677f\u5df2\u5220\u9664",
      deleteConfirmTitle: "\u5220\u9664\u6a21\u677f",
      deleteConfirmMessage:
        "\u5220\u9664\u540e\u6a21\u677f\u4f1a\u6807\u8bb0\u4e3a deleted\uff0c\u5e76\u4ece\u6b63\u5e38\u4f7f\u7528\u6d41\u7a0b\u4e2d\u9690\u85cf\uff0c\u786e\u8ba4\u7ee7\u7eed\u5417\uff1f",
    },
  },
  "en-US": {
    layout: {
      brandKicker: "Admin Workspace",
      brandTitle: "Control Console",
      brandCopy: "Monitor tasks, API logs, and prompt templates in one place so admin work stays focused and fast.",
      defaultAdminName: "Administrator",
      backToUserApp: "Back to User App",
      operations: "Operations",
      navOverview: "Overview",
      navOverviewHint: "Key metrics and alerts",
      navTasks: "Tasks",
      navTasksHint: "Inspect analysis task progress and failures",
      navApiLogs: "API Logs",
      navApiLogsHint: "Track model usage, latency, and errors",
      navPromptTemplates: "Prompt Templates",
      navPromptTemplatesHint: "Manage prompt versions and content",
      titleOverview: "Admin Overview",
      titleTasks: "Analysis Task Management",
      titleApiLogs: "AI API Logs",
      titlePromptTemplates: "Prompt Template Management",
      titleDefault: "Admin Console",
      languageLabel: "Language",
      languageChinese: "\u4e2d\u6587",
      languageEnglish: "English",
    },
    overview: {
      kicker: "Admin Overview",
      title: "Keep tasks, AI calls, and system signals in one working view.",
      copy: "This console is optimized for monitoring and troubleshooting so the most important operational signals stay visible.",
      users: "Users",
      usersNote: "All registered accounts in the current system.",
      resumesJobs: "Resumes / Jobs",
      resumesJobsNote: "Resources already in the business flow.",
      analysisTasks: "Analysis Tasks",
      analysisTasksNote: (pending, running) => `Pending ${pending}, running ${running}.`,
      aiCalls: "AI Calls",
      aiCallsNote: (failed) => `Failed ${failed} times.`,
      alertsTitle: "Alerts",
      alertsCopy: "If task execution or AI calls wobble, check here first.",
      alertsWarning: "There are failed records that need attention",
      alertsOk: "No obvious failures at the moment",
      failedTasks: "Failed Tasks",
      promptTemplates: "Prompt Templates",
      reports: "Reports",
      latestApiError: "Latest API Error",
      noRecentError: "No recent error",
      quickLinksTitle: "Quick Links",
      quickLinksCopy: "Jump straight into the most common admin views.",
      taskCenterTitle: "Task Center",
      taskCenterCopy: "Review failed tasks and blocked progress.",
      apiLogsTitle: "AI Logs",
      apiLogsCopy: "Inspect model errors, latency, and token usage.",
      promptTitle: "Prompt Templates",
      promptCopy: "Manage prompt scenes, versions, and activation status.",
    },
    tasks: {
      title: "Analysis Task Management",
      copy: "Use this view to inspect failed tasks, blocked jobs, and unusual user inputs.",
      searchPlaceholder: "Search by user, resume, or job",
      statusPlaceholder: "Status",
      taskTypePlaceholder: "Task Type",
      fullAnalysis: "Full Analysis",
      jobMatch: "Job Match",
      resumeScore: "Resume Score",
      user: "User",
      resume: "Resume",
      job: "Job",
      taskType: "Task Type",
      status: "Status",
      progress: "Progress",
      createdAt: "Created At",
      errorMessage: "Error Message",
    },
    apiLogs: {
      title: "AI API Logs",
      copy: "Review failures, latency, and token usage to troubleshoot model-side issues.",
      searchPlaceholder: "Search by user, model, or error",
      statusPlaceholder: "Status",
      scenePlaceholder: "Scene",
      user: "User",
      scene: "Scene",
      model: "Model",
      status: "Status",
      tokens: "Tokens",
      latency: "Latency",
      template: "Template",
      errorMessage: "Error Message",
      createdAt: "Created At",
    },
    promptTemplates: {
      title: "Prompt Template Management",
      copy: "Manage template versions, activation status, and scene content that directly shape AI output quality.",
      newTemplate: "New Template",
      searchPlaceholder: "Search by name or content",
      scenePlaceholder: "Scene",
      statusPlaceholder: "Status",
      name: "Name",
      scene: "Scene",
      version: "Version",
      status: "Status",
      editor: "Editor",
      description: "Description",
      updatedAt: "Updated At",
      actions: "Actions",
      edit: "Edit",
      delete: "Delete",
      editTitle: "Edit Template",
      createTitle: "New Template",
      formName: "Name",
      formScene: "Scene",
      formVersion: "Version",
      formStatus: "Status",
      formDescription: "Description",
      formContent: "Template Content",
      cancel: "Cancel",
      save: "Save",
      createSuccess: "Template created",
      updateSuccess: "Template updated",
      deleteSuccess: "Template deleted",
      deleteConfirmTitle: "Delete Template",
      deleteConfirmMessage: "The template will be marked as deleted and hidden from normal use. Continue?",
    },
  },
};

const statusTextMap: Record<AdminLocale, Record<string, string>> = {
  "zh-CN": {
    pending: "\u7b49\u5f85\u4e2d",
    running: "\u8fdb\u884c\u4e2d",
    success: "\u6210\u529f",
    failed: "\u5931\u8d25",
    canceled: "\u5df2\u53d6\u6d88",
    active: "\u542f\u7528",
    inactive: "\u505c\u7528",
    deleted: "\u5df2\u5220\u9664",
  },
  "en-US": {
    pending: "Pending",
    running: "Running",
    success: "Success",
    failed: "Failed",
    canceled: "Canceled",
    active: "Active",
    inactive: "Inactive",
    deleted: "Deleted",
  },
};

const taskTypeTextMap: Record<AdminLocale, Record<string, string>> = {
  "zh-CN": {
    full_analysis: "\u5b8c\u6574\u5206\u6790",
    job_match: "\u5c97\u4f4d\u5339\u914d",
    resume_score: "\u7b80\u5386\u8bc4\u5206",
  },
  "en-US": {
    full_analysis: "Full Analysis",
    job_match: "Job Match",
    resume_score: "Resume Score",
  },
};

export function useAdminMessages() {
  const localeStore = useLocaleStore();
  return computed(() => adminMessages[localeStore.locale]);
}

export function useAdminLocaleHelpers() {
  const localeStore = useLocaleStore();

  function statusText(value?: string | null) {
    if (!value) {
      return "-";
    }
    return statusTextMap[localeStore.locale][value] || value;
  }

  function taskTypeText(value?: string | null) {
    if (!value) {
      return "-";
    }
    return taskTypeTextMap[localeStore.locale][value] || value;
  }

  return {
    statusText,
    taskTypeText,
  };
}
