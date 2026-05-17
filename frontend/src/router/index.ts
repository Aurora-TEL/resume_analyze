import { createRouter, createWebHistory } from "vue-router";

import AdminLayout from "@/layouts/AdminLayout.vue";
import BlankLayout from "@/layouts/BlankLayout.vue";
import UserLayout from "@/layouts/UserLayout.vue";
import { useAuthStore } from "@/stores/auth";
import { useUserStore } from "@/stores/user";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/dashboard",
    },
    {
      path: "/",
      component: BlankLayout,
      children: [
        {
          path: "login",
          component: () => import("@/views/auth/Login.vue"),
        },
        {
          path: "register",
          component: () => import("@/views/auth/Register.vue"),
        },
      ],
    },
    {
      path: "/",
      component: UserLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: "dashboard",
          component: () => import("@/views/dashboard/Dashboard.vue"),
        },
        {
          path: "resumes",
          component: () => import("@/views/resumes/ResumeList.vue"),
        },
        {
          path: "resumes/upload",
          component: () => import("@/views/resumes/ResumeUploadPage.vue"),
        },
        {
          path: "resumes/:id",
          component: () => import("@/views/resumes/ResumeDetail.vue"),
        },
        {
          path: "jobs",
          component: () => import("@/views/jobs/JobList.vue"),
        },
        {
          path: "jobs/create",
          component: () => import("@/views/jobs/JobCreate.vue"),
        },
        {
          path: "jobs/:id",
          component: () => import("@/views/jobs/JobDetail.vue"),
        },
        {
          path: "analysis/create",
          component: () => import("@/views/analysis/AnalysisCreate.vue"),
        },
        {
          path: "analysis/tasks/:id",
          component: () => import("@/views/analysis/AnalysisTaskDetail.vue"),
        },
        {
          path: "reports",
          component: () => import("@/views/reports/ReportList.vue"),
        },
        {
          path: "reports/:id",
          component: () => import("@/views/reports/ReportDetail.vue"),
        },
        {
          path: "profile",
          component: () => import("@/views/profile/Profile.vue"),
        },
      ],
    },
    {
      path: "/admin",
      component: AdminLayout,
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: "",
          component: () => import("@/views/admin/AdminDashboard.vue"),
        },
        {
          path: "analysis-tasks",
          component: () => import("@/views/admin/AnalysisTaskManage.vue"),
        },
        {
          path: "api-logs",
          component: () => import("@/views/admin/ApiLogManage.vue"),
        },
        {
          path: "prompt-templates",
          component: () => import("@/views/admin/PromptTemplateManage.vue"),
        },
      ],
    },
  ],
});

router.beforeEach(async (to) => {
  const authStore = useAuthStore();
  const userStore = useUserStore();

  const isAuthPage = to.path === "/login" || to.path === "/register";

  if (authStore.isAuthenticated && (!userStore.hydrated || !userStore.currentUser)) {
    try {
      await userStore.fetchCurrentUser();
    } catch {
      authStore.logout();
      userStore.clearCurrentUser();
      if (!isAuthPage) {
        return "/login";
      }
    }
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return "/login";
  }

  if (isAuthPage && authStore.isAuthenticated) {
    return userStore.currentUser?.role === "admin" ? "/admin" : "/dashboard";
  }

  if (to.meta.requiresAdmin && userStore.currentUser?.role !== "admin") {
    return "/dashboard";
  }

  return true;
});

export default router;
