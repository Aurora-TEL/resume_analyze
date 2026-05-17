<template>
  <div class="app-page" v-loading="loading">
    <section class="hero-card">
      <p class="hero-kicker">Profile Settings</p>
      <h1 class="hero-title">{{ t.heroTitle }}</h1>
      <p class="hero-copy">{{ t.heroCopy }}</p>
    </section>

    <div class="two-column">
      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.profileTitle }}</h2>
            <p class="section-copy">{{ t.profileCopy }}</p>
          </div>
        </div>

        <el-form ref="profileFormRef" :model="profileForm" label-position="top">
          <el-form-item :label="t.labelEmail">
            <el-input :model-value="userStore.currentUser?.email || ''" disabled />
          </el-form-item>
          <el-form-item :label="t.labelNickname">
            <el-input v-model="profileForm.nickname" maxlength="100" />
          </el-form-item>
          <el-form-item :label="t.labelPhone">
            <el-input v-model="profileForm.phone" maxlength="50" />
          </el-form-item>
          <el-form-item :label="t.labelTargetPosition">
            <el-input v-model="profileForm.target_position" maxlength="100" />
          </el-form-item>
          <el-form-item :label="t.labelTargetCity">
            <el-input v-model="profileForm.target_city" maxlength="100" />
          </el-form-item>
          <el-form-item :label="t.labelWorkYears">
            <el-input-number v-model="profileForm.work_years" :min="0" :max="50" :precision="1" :step="0.5" />
          </el-form-item>
          <el-button type="primary" :loading="savingProfile" @click="handleSaveProfile">{{ t.saveProfile }}</el-button>
        </el-form>
      </section>

      <section class="section-card">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ t.passwordTitle }}</h2>
            <p class="section-copy">{{ t.passwordCopy }}</p>
          </div>
        </div>

        <el-form ref="passwordFormRef" :model="passwordForm" :rules="passwordRules" label-position="top">
          <el-form-item :label="t.labelOldPassword" prop="old_password">
            <el-input v-model="passwordForm.old_password" show-password />
          </el-form-item>
          <el-form-item :label="t.labelNewPassword" prop="new_password">
            <el-input v-model="passwordForm.new_password" show-password />
          </el-form-item>
          <el-form-item :label="t.labelConfirmPassword" prop="confirm_password">
            <el-input v-model="passwordForm.confirm_password" show-password />
          </el-form-item>
          <el-button type="primary" plain :loading="savingPassword" @click="handleSavePassword">{{ t.savePassword }}</el-button>
        </el-form>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";

import { updateCurrentUser, updatePassword } from "@/api/users";
import { useLocaleStore } from "@/stores/locale";
import { useUserStore } from "@/stores/user";

const zh = {
  heroTitle: "\u7ef4\u62a4\u4f60\u7684\u76ee\u6807\u5c97\u4f4d\u4fe1\u606f\uff0c\u8ba9\u540e\u7eed\u89e3\u6790\u66f4\u8d34\u8fd1\u6295\u9012\u65b9\u5411\u3002",
  heroCopy: "\u8fd9\u91cc\u4fdd\u5b58\u7684\u662f\u7528\u6237\u7ef4\u5ea6\u7684\u957f\u671f\u4fe1\u606f\uff0c\u6bd4\u5982\u6635\u79f0\u3001\u76ee\u6807\u5c97\u4f4d\u548c\u76ee\u6807\u57ce\u5e02\u3002\u4fee\u6539\u540e\u4f1a\u5f71\u54cd\u540e\u7eed\u90e8\u5206\u89e3\u6790\u63d0\u793a\u3002",
  profileTitle: "\u4e2a\u4eba\u8d44\u6599",
  profileCopy: "\u8fd9\u4e9b\u5b57\u6bb5\u4f1a\u5728\u7528\u6237\u4e3b\u94fe\u8def\u4e2d\u957f\u671f\u590d\u7528\u3002",
  labelEmail: "\u90ae\u7bb1",
  labelNickname: "\u6635\u79f0",
  labelPhone: "\u624b\u673a\u53f7",
  labelTargetPosition: "\u76ee\u6807\u5c97\u4f4d",
  labelTargetCity: "\u76ee\u6807\u57ce\u5e02",
  labelWorkYears: "\u5de5\u4f5c\u5e74\u9650",
  saveProfile: "\u4fdd\u5b58\u8d44\u6599",
  passwordTitle: "\u4fee\u6539\u5bc6\u7801",
  passwordCopy: "\u5efa\u8bae\u5b9a\u671f\u66f4\u65b0\u5bc6\u7801\uff0c\u4fdd\u6301\u672c\u5730\u8c03\u8bd5\u8d26\u53f7\u6574\u6d01\u53ef\u63a7\u3002",
  labelOldPassword: "\u65e7\u5bc6\u7801",
  labelNewPassword: "\u65b0\u5bc6\u7801",
  labelConfirmPassword: "\u786e\u8ba4\u65b0\u5bc6\u7801",
  savePassword: "\u66f4\u65b0\u5bc6\u7801",
  validationOldPassword: "\u8bf7\u8f93\u5165\u65e7\u5bc6\u7801",
  validationNewPassword: "\u8bf7\u8f93\u5165\u65b0\u5bc6\u7801",
  validationNewPasswordMin: "\u65b0\u5bc6\u7801\u81f3\u5c11 8 \u4f4d",
  validationConfirmPassword: "\u8bf7\u518d\u6b21\u8f93\u5165\u65b0\u5bc6\u7801",
  validationConfirmMismatch: "\u4e24\u6b21\u8f93\u5165\u7684\u65b0\u5bc6\u7801\u4e0d\u4e00\u81f4",
  profileUpdated: "\u8d44\u6599\u5df2\u66f4\u65b0",
  passwordUpdated: "\u5bc6\u7801\u5df2\u66f4\u65b0",
};

const en = {
  heroTitle: "Maintain your target job information so later analysis stays close to your application direction.",
  heroCopy: "This page stores long-term user-level information such as nickname, target position, and target city. Updates here can affect later analysis prompts.",
  profileTitle: "Profile Information",
  profileCopy: "These fields are reused throughout the main user workflow.",
  labelEmail: "Email",
  labelNickname: "Nickname",
  labelPhone: "Phone",
  labelTargetPosition: "Target Position",
  labelTargetCity: "Target City",
  labelWorkYears: "Work Years",
  saveProfile: "Save Profile",
  passwordTitle: "Change Password",
  passwordCopy: "It is a good idea to refresh the password regularly so the local test account stays tidy and controlled.",
  labelOldPassword: "Old Password",
  labelNewPassword: "New Password",
  labelConfirmPassword: "Confirm New Password",
  savePassword: "Update Password",
  validationOldPassword: "Please enter the old password",
  validationNewPassword: "Please enter the new password",
  validationNewPasswordMin: "The new password must be at least 8 characters",
  validationConfirmPassword: "Please confirm the new password",
  validationConfirmMismatch: "The two new passwords do not match",
  profileUpdated: "Profile updated",
  passwordUpdated: "Password updated",
};

const localeStore = useLocaleStore();
const t = computed(() => (localeStore.locale === "zh-CN" ? zh : en));
const userStore = useUserStore();
const loading = ref(false);
const savingProfile = ref(false);
const savingPassword = ref(false);
const profileFormRef = ref<FormInstance>();
const passwordFormRef = ref<FormInstance>();

const profileForm = reactive({
  nickname: "",
  phone: "",
  target_position: "",
  target_city: "",
  work_years: 0,
});

const passwordForm = reactive({
  old_password: "",
  new_password: "",
  confirm_password: "",
});

const passwordRules = computed<FormRules>(() => ({
  old_password: [{ required: true, message: t.value.validationOldPassword, trigger: "blur" }],
  new_password: [
    { required: true, message: t.value.validationNewPassword, trigger: "blur" },
    { min: 8, message: t.value.validationNewPasswordMin, trigger: "blur" },
  ],
  confirm_password: [
    { required: true, message: t.value.validationConfirmPassword, trigger: "blur" },
    {
      validator: (_rule, value, callback) => {
        if (value !== passwordForm.new_password) {
          callback(new Error(t.value.validationConfirmMismatch));
          return;
        }
        callback();
      },
      trigger: "blur",
    },
  ],
}));

function syncProfileForm() {
  profileForm.nickname = userStore.currentUser?.nickname || "";
  profileForm.phone = userStore.currentUser?.phone || "";
  profileForm.target_position = userStore.currentUser?.target_position || "";
  profileForm.target_city = userStore.currentUser?.target_city || "";
  profileForm.work_years = Number(userStore.currentUser?.work_years || 0);
}

async function loadProfile() {
  loading.value = true;
  try {
    await userStore.fetchCurrentUser(true);
    syncProfileForm();
  } finally {
    loading.value = false;
  }
}

async function handleSaveProfile() {
  savingProfile.value = true;
  try {
    const result = await updateCurrentUser({
      nickname: profileForm.nickname || null,
      phone: profileForm.phone || null,
      target_position: profileForm.target_position || null,
      target_city: profileForm.target_city || null,
      work_years: profileForm.work_years,
    });
    userStore.setCurrentUser(result);
    syncProfileForm();
    ElMessage.success(t.value.profileUpdated);
  } finally {
    savingProfile.value = false;
  }
}

async function handleSavePassword() {
  const valid = await passwordFormRef.value?.validate().catch(() => false);
  if (!valid) {
    return;
  }

  savingPassword.value = true;
  try {
    await updatePassword({
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password,
    });
    passwordForm.old_password = "";
    passwordForm.new_password = "";
    passwordForm.confirm_password = "";
    ElMessage.success(t.value.passwordUpdated);
  } finally {
    savingPassword.value = false;
  }
}

onMounted(loadProfile);
</script>
