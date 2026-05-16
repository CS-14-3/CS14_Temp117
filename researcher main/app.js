// 初始化 Lucide 图标 
lucide.createIcons(); 

const TRANSLATION_API_URL = 'http://localhost:5001/api/translations/generate';
const UI_TRANSLATION_CACHE_KEY = 'surveyArchitectUITranslationCacheV5';
const UI_LOCALE_LABELS = {
  en: 'EN',
  'zh-Hans': '中文',
  es: 'ES'
};

const UI_TEXT = {
  'account.manage': 'Manage Survey Architect Account',
  'account.addAnother': 'Add another account',
  'account.signOut': 'Sign out',
  'account.legal': 'Privacy Policy • Terms of Service',
  'account.greeting': 'Hi, {{username}}!',
  'nav.profile': 'Profile',
  'nav.newSurvey': 'New Survey',
  'nav.history': 'History',
  'nav.results': 'Results',
  'nav.dataExport': 'Data Export',
  'editor.title': 'Edit Your Survey Post',
  'editor.subtitle': 'Create experiment content by entering a news link and adjusting social variables.',
  'editor.createNewSurvey': 'Create New Survey',
  'editor.newsLink': 'News Link',
  'editor.newsLinkPlaceholder': 'Paste BBC, Facebook, or X link...',
  'editor.fetchImage': 'Fetch Image',
  'editor.fetching': 'Fetching...',
  'editor.versionA': 'Version A',
  'editor.versionB': 'Version B',
  'editor.platformStyle': 'Platform Style',
  'editor.publishSurveyLink': 'Publish Survey Link',
  'editor.newsTab': 'news {{number}}',
  'editor.noActiveSurvey': 'No active survey',
  'editor.noSurveyTitle': 'No active survey yet.',
  'editor.noSurveyDescription': 'Create a new survey before editing, generating invite codes, or publishing.',
  'editor.noSurveyPreview': 'Create a new survey to start building the preview.',
  'preview.newsIndicator': 'NEWS {{number}}',
  'post.viewAllComments': 'View all {{count}} comments',
  'post.comments': 'comments',
  'question.block': 'Question Block',
  'question.enable': 'Enable',
  'question.type': 'Question Type',
  'question.singleChoice': 'Single Choice',
  'question.multipleChoice': 'Multiple Choice',
  'question.text': 'Question Text',
  'question.textPlaceholder': 'Enter question text',
  'question.options': 'Options',
  'question.addOption': 'Add option',
  'question.required': 'Required answer',
  'question.requiredShort': 'Required',
  'translation.languages': 'Content Languages',
  'translation.generate': 'Generate Translations',
  'translation.source': 'Source Language',
  'translation.targets': 'Target Languages',
  'invite.accessControl': 'Participant Access Control',
  'invite.description': 'Generate a unique invite code to ensure anonymity',
  'invite.generate': 'Generate Invite Code',
  'invite.regenerate': 'Regenerate',
  'icon.select': 'Select Icon',
  'dialog.surveyTitle': 'Survey Title',
  'dialog.surveyTitlePlaceholder': 'Enter survey title',
  'dialog.surveyTitleError': 'Please enter a survey title.',
  'dialog.cancel': 'Cancel',
  'dialog.create': 'Create',
  'alert.surveyPublished': 'Survey published.',
  'alert.newsLinkRequired': 'Please paste a news link first.',
  'alert.scrapingFailed': 'Scraping failed: {{error}}',
  'alert.backendError': 'Backend service error. Please make sure the Flask server is running on port 5001.',
  'alert.createSurveyBeforeEditing': 'Please create a new survey before editing.',
  'alert.inviteCodeRequired': 'Please generate an invite code before publishing.',
  'alert.translationUnavailable': 'Translation service is unavailable. Please check the backend service.',
  'alert.translationNotReady': 'Translation generation is not available yet.',
  'profile.title': 'Profile',
  'profile.subtitle': 'Researcher account and project status.',
  'profile.role': 'Role: Researcher',
  'profile.username': 'Username',
  'profile.lastLogin': 'Last login',
  'profile.currentSurvey': 'Current survey',
  'profile.projectStats': 'Project Stats',
  'profile.totalSurveys': 'Total surveys',
  'profile.publishedSurveys': 'Published surveys',
  'profile.exportReadySurveys': 'Export-ready surveys',
  'profile.participantResults': 'Participant results',
  'profile.settings': 'Researcher Settings',
  'profile.displayName': 'Display Name',
  'profile.exportFormats': 'Available Export Formats',
  'profile.dataNotice': 'Data Notice',
  'profile.dataNoticeText': 'Gaze records should be reviewed and exported from History after participant completion.',
  'history.title': 'Survey History',
  'history.emptySubtitle': 'Published surveys will appear here after you click Publish Survey Link.',
  'history.subtitle': 'Published surveys are shown as summaries. Expand a survey to inspect published news items.',
  'history.noPublished': 'No published surveys yet.',
  'history.draftsExcluded': 'Drafts and link experiments stay out of History until they are published.',
  'history.created': 'Created {{date}}',
  'history.viewDetails': 'View Details',
  'history.hideDetails': 'Hide Details',
  'history.dataExport': 'Data Export',
  'history.status': 'Status',
  'history.news': 'News',
  'history.versions': 'Versions',
  'history.participants': 'Participants',
  'history.platformStyles': 'Platform Styles',
  'history.publishedPosts': 'Published Posts',
  'history.publishRecord': 'Publish {{number}}',
  'history.publishedAt': 'Published {{date}}',
  'history.newsItem': 'News {{number}}',
  'history.version': 'version',
  'history.versionPlural': 'versions',
  'history.platformStyleCount': 'platform styles',
  'history.openLink': 'Open Link',
  'history.noOriginalLink': 'No original link',
  'history.viewVersions': 'View Versions',
  'history.hideVersions': 'Hide Versions',
  'history.platform': 'platform',
  'history.platformPlural': 'platforms',
  'history.noActionButtons': 'No action buttons',
  'history.unknownAccount': 'Unknown account',
  'history.imageHidden': 'Image hidden',
  'history.noImage': 'No image',
  'export.title': 'Data Export',
  'export.emptySubtitle': 'Export gaze data received after participants close their survey page.',
  'export.subtitle': 'Export camera gaze data received from completed participant sessions.',
  'export.button': 'Export Data',
  'export.refresh': 'Refresh',
  'export.gazeEndpoint': 'Gaze Data Endpoint',
  'export.noGaze': 'No gaze data received yet.',
  'export.gazeSubmit': 'Participant pages can submit data to {{endpoint}} when they close.',
  'export.gazeSubmitComplete': 'Participant pages submit completed gaze records to {{endpoint}}.',
  'export.inviteCode': 'Invite Code',
  'export.noInviteCode': 'No invite code',
  'export.close': 'Close',
  'export.exportJson': 'Export JSON',
  'export.exportCsv': 'Export CSV',
  'export.completed': 'Completed {{date}}',
  'export.gazeSamples': 'Gaze samples',
  'export.newsItems': 'News items',
  'export.samplesClosed': '{{samples}} samples · closed {{date}}',
  'status.draft': 'Draft',
  'status.published': 'Published',
  'status.completed': 'Completed',
  'status.unknown': 'Unknown date',
  'results.title': 'Study Results',
  'results.subtitle': 'Completed eye-tracking sessions collected from participants.',
  'results.loading': 'Loading sessions...',
  'results.emptyTitle': 'No study sessions found',
  'results.emptySubtitle': 'Sessions appear here after participants complete the study.',
  'results.loadError': 'Could not connect to study backend',
  'results.participant': 'Participant {{id}}',
  'results.sessions': '{{count}} sessions',
  'results.latest': 'Latest: {{date}} - {{size}}',
  'results.downloadJson': 'JSON',
  'results.viewAnalysis': 'View Analysis',
  'language.translatePage': 'Translate page',
  'language.loading': 'Translating...',
  'notification.participantCompleted': 'Participant completed the survey. Gaze data is ready to export.',
  'notification.viewHistory': 'View History',
  'notification.dismiss': 'Dismiss'
};

function readLocalStorageJson(key, fallback) {
  try {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : fallback;
  } catch (error) {
    return fallback;
  }
}

let uiTranslationCache = readLocalStorageJson(UI_TRANSLATION_CACHE_KEY, {});
let currentUILocale = 'en';

function interpolateText(text, replacements = {}) {
  return String(text).replace(/\{\{(\w+)\}\}/g, (_, key) => (
    replacements[key] === undefined ? '' : String(replacements[key])
  ));
}

function t(key, replacements = {}) {
  const sourceText = UI_TEXT[key] || key;
  const translatedText = currentUILocale === 'en'
    ? sourceText
    : uiTranslationCache[currentUILocale]?.entries?.[`ui.${key}`] || sourceText;
  return interpolateText(translatedText, replacements);
}

function getUiTranslationEntries() {
  return Object.entries(UI_TEXT).map(([key, text]) => ({
    key: `ui.${key}`,
    text
  }));
}

function applyStaticTranslations() {
  document.documentElement.lang = currentUILocale === 'zh-Hans' ? 'zh-CN' : currentUILocale;

  document.querySelectorAll('[data-i18n]').forEach((element) => {
    element.textContent = t(element.getAttribute('data-i18n'));
  });

  document.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {
    element.setAttribute('placeholder', t(element.getAttribute('data-i18n-placeholder')));
  });
}

function updateLanguageMenuState(isLoading = false) {
  const currentLabel = document.getElementById('ui-language-current');
  const languageButton = document.getElementById('ui-language-btn');

  if (currentLabel) {
    currentLabel.textContent = isLoading ? '...' : UI_LOCALE_LABELS[currentUILocale];
  }

  if (languageButton) {
    languageButton.disabled = isLoading;
    languageButton.classList.toggle('opacity-60', isLoading);
    languageButton.title = isLoading ? t('language.loading') : t('language.translatePage');
  }

  document.querySelectorAll('[data-ui-locale]').forEach((button) => {
    const isActive = button.getAttribute('data-ui-locale') === currentUILocale;
    button.classList.toggle('bg-sky-50', isActive);
    button.classList.toggle('text-sky-700', isActive);
  });
}

async function ensureUiTranslation(locale) {
  if (locale === 'en' || uiTranslationCache[locale]) {
    return true;
  }

  const response = await fetch(TRANSLATION_API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      surveyId: 'researcher-ui',
      sourceLocale: 'en',
      targetLocales: [locale],
      entries: getUiTranslationEntries()
    })
  });
  const result = await response.json();

  if (!response.ok || !result.success || !result.translations?.[locale]) {
    throw new Error(result.error || t('alert.translationNotReady'));
  }

  uiTranslationCache = {
    ...uiTranslationCache,
    [locale]: result.translations[locale]
  };
  localStorage.setItem(UI_TRANSLATION_CACHE_KEY, JSON.stringify(uiTranslationCache));
  return true;
}

async function ensureCurrentSurveyContentTranslation(locale) {
  const currentSurvey = getCurrentSurvey();
  if (locale === 'en' || !currentSurvey) {
    return true;
  }

  currentSurvey.translations = currentSurvey.translations && typeof currentSurvey.translations === 'object'
    ? currentSurvey.translations
    : {};
  const entries = collectSurveyTranslationEntries(currentSurvey);
  if (entries.length === 0) {
    return true;
  }
  const existingEntries = currentSurvey.translations[locale]?.entries || {};
  if (
    currentSurvey.translations[locale]?.status === 'ready' &&
    entries.every((entry) => typeof existingEntries[entry.key] === 'string')
  ) {
    return true;
  }

  const response = await fetch(TRANSLATION_API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      surveyId: currentSurvey.id,
      sourceLocale: 'en',
      targetLocales: [locale],
      entries
    })
  });
  const result = await response.json();

  if (!response.ok || !result.success || !result.translations?.[locale]) {
    throw new Error(result.error || t('alert.translationNotReady'));
  }

  currentSurvey.translations = {
    ...currentSurvey.translations,
    [locale]: result.translations[locale]
  };
  saveAppStateToLocalStorage();
  return true;
}

function getSurveyTranslationValue(key, fallback = '') {
  if (currentUILocale === 'en') {
    return fallback;
  }

  const currentSurvey = getCurrentSurvey();
  return currentSurvey?.translations?.[currentUILocale]?.entries?.[key] || fallback;
}

function getTranslatedQuestionBlock(questionBlock, newsIndex, versionKey, platform) {
  const normalizedQuestionBlock = normalizeQuestionBlock(questionBlock);
  if (currentUILocale === 'en') {
    return normalizedQuestionBlock;
  }

  return {
    ...normalizedQuestionBlock,
    questionText: getSurveyTranslationValue(
      `news.${newsIndex}.${versionKey}.${platform}.question.text`,
      normalizedQuestionBlock.questionText
    ),
    options: normalizedQuestionBlock.options.map((option, optionIndex) => ({
      ...option,
      label: getSurveyTranslationValue(
        `news.${newsIndex}.${versionKey}.${platform}.question.option.${optionIndex}`,
        option.label
      )
    }))
  };
}

function getTranslatedVersionData(version, newsIndex, versionKey) {
  const platform = version.platform || 'instagram';
  const translatedVersion = clonePlainData(version);
  if (currentUILocale === 'en') {
    return translatedVersion;
  }

  translatedVersion.caption = getSurveyTranslationValue(
    `news.${newsIndex}.${versionKey}.${platform}.caption`,
    translatedVersion.caption
  );
  if (translatedVersion.likesLabel) {
    translatedVersion.likesLabel = getSurveyTranslationValue(
      `news.${newsIndex}.${versionKey}.${platform}.likesLabel`,
      translatedVersion.likesLabel
    );
  }
  if (translatedVersion.timeLabel) {
    translatedVersion.timeLabel = getSurveyTranslationValue(
      `news.${newsIndex}.${versionKey}.${platform}.timeLabel`,
      translatedVersion.timeLabel
    );
  }
  if (Array.isArray(translatedVersion.actionButtons)) {
    translatedVersion.actionButtons = translatedVersion.actionButtons.map((button, buttonIndex) => ({
      ...button,
      label: getSurveyTranslationValue(
        `news.${newsIndex}.${versionKey}.${platform}.action.${buttonIndex}.label`,
        button.label
      )
    }));
  }
  translatedVersion.questionBlock = getTranslatedQuestionBlock(
    translatedVersion.questionBlock,
    newsIndex,
    versionKey,
    platform
  );
  return translatedVersion;
}

function rerenderCurrentLanguageView() {
  applyStaticTranslations();
  renderResearcherIdentity();
  renderSurveyTitle();
  ensureCreateSurveyButton();
  renderVersionTabs();
  renderNewsTabs();
  renderQuestionBlockEditor();
  renderInviteCode();
  renderPreview();
  updateEditorSurveyAvailability();

  const profileView = document.getElementById('profile-view');
  const historyView = document.getElementById('history-view');
  const dataExportView = document.getElementById('data-export-view');
  if (profileView && !profileView.classList.contains('hidden')) {
    renderProfileView();
  }
  if (historyView && !historyView.classList.contains('hidden')) {
    renderHistoryView();
  }
  if (dataExportView && !dataExportView.classList.contains('hidden')) {
    renderDataExportView();
  }
  updateLanguageMenuState();
  lucide.createIcons();
}

async function changeUILocale(locale) {
  if (!UI_LOCALE_LABELS[locale] || locale === currentUILocale) {
    return;
  }

  const previousLocale = currentUILocale;
  currentUILocale = locale;
  updateLanguageMenuState(true);

  try {
    await ensureUiTranslation(locale);
    await ensureCurrentSurveyContentTranslation(locale);
    rerenderCurrentLanguageView();
  } catch (error) {
    console.error('Failed to translate UI:', error);
    currentUILocale = previousLocale;
    updateLanguageMenuState();
    alert(error.message || t('alert.translationUnavailable'));
  }
}

// 0. 用户下拉菜单切换逻辑
const uiLanguageBtn = document.getElementById('ui-language-btn');
const uiLanguageDropdown = document.getElementById('ui-language-dropdown');
const userMenuBtn = document.getElementById('user-menu-btn'); 
const userDropdown = document.getElementById('user-dropdown'); 
const closeDropdownBtn = document.getElementById('close-dropdown-btn'); 

const researcherSignOutBtn = document.getElementById('researcher-sign-out-btn');
const researcherSessionStorageKey = 'surveyLabResearcherSession';

function getResearcherSession() {
  const storedSession = localStorage.getItem(researcherSessionStorageKey);
  if (!storedSession) {
    return null;
  }

  try {
    return JSON.parse(storedSession);
  } catch (error) {
    return null;
  }
}

function getResearcherUsername() {
  const session = getResearcherSession();
  return session && session.username ? session.username.trim() : 'Researcher';
}

function renderResearcherIdentity() {
  const username = getResearcherUsername();
  const initial = username.charAt(0).toUpperCase() || 'R';
  const userAvatar = document.getElementById('user-menu-btn');
  const dropdownAvatar = userDropdown.querySelector('.w-16.h-16.rounded-full');
  const greeting = userDropdown.querySelector('h2');

  if (userAvatar) {
    userAvatar.textContent = initial;
  }

  if (dropdownAvatar) {
    const cameraBadge = dropdownAvatar.querySelector('.absolute');
    dropdownAvatar.textContent = initial;
    if (cameraBadge) {
      dropdownAvatar.appendChild(cameraBadge);
    }
  }

  if (greeting) {
    greeting.textContent = t('account.greeting', { username });
  }
}

renderResearcherIdentity();

function handleResearcherSignOut() {
  localStorage.removeItem(researcherSessionStorageKey);
  localStorage.removeItem(APP_STATE_STORAGE_KEY);
  localStorage.removeItem(GAZE_DATA_STORAGE_KEY);
  window.location.href = '/login';
}

if (researcherSignOutBtn) {
  researcherSignOutBtn.addEventListener('click', handleResearcherSignOut);
}

if (uiLanguageBtn && uiLanguageDropdown) {
  uiLanguageBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    userDropdown.classList.add('hidden');
    uiLanguageDropdown.classList.toggle('hidden');
  });

  uiLanguageDropdown.addEventListener('click', (e) => {
    const localeButton = e.target.closest('[data-ui-locale]');
    if (!localeButton) return;
    uiLanguageDropdown.classList.add('hidden');
    changeUILocale(localeButton.getAttribute('data-ui-locale'));
  });
}

// 切换用户菜单 
userMenuBtn.addEventListener('click', (e) => { 
  e.stopPropagation(); // 防止冒泡触发 document 的 click 
  if (uiLanguageDropdown) {
    uiLanguageDropdown.classList.add('hidden');
  }
  userDropdown.classList.toggle('hidden'); 
}); 

closeDropdownBtn.addEventListener('click', () => { 
  userDropdown.classList.add('hidden'); 
}); 

// 点击外部区域关闭下拉菜单
document.addEventListener('click', (e) => { 
  if (!userMenuBtn.contains(e.target) && !userDropdown.contains(e.target)) { 
    userDropdown.classList.add('hidden'); 
  } 
  if (uiLanguageBtn && uiLanguageDropdown && !uiLanguageBtn.contains(e.target) && !uiLanguageDropdown.contains(e.target)) {
    uiLanguageDropdown.classList.add('hidden');
  }
}); 

// 4. 生成邀请码逻辑 (完全保留你原来的代码)
const btnGenerateCode = document.getElementById('btn-generate-code'); 
const displayInviteCode = document.getElementById('invite-code-display'); 
btnGenerateCode.addEventListener('click', () => { 
  const currentSurvey = getCurrentSurvey();
  if (!currentSurvey) {
    return;
  }

  const code = Math.random().toString(36).substring(2, 8).toUpperCase(); 
  displayInviteCode.textContent = code; 
  displayInviteCode.classList.remove('hidden'); 
  btnGenerateCode.textContent = t('invite.regenerate'); 
  currentSurvey.inviteCode = code;
  saveAppStateToLocalStorage();
});

// ==============================================================
// === 以下为新增的 A/B 状态机与多平台预览逻辑 =====================
// ==============================================================

const createDefaultQuestionBlock = () => ({
  enabled: false,
  type: 'single',
  questionText: 'How credible is this post?',
  required: true,
  options: [
    { id: 'option_1', label: 'Very credible' },
    { id: 'option_2', label: 'Somewhat credible' },
    { id: 'option_3', label: 'Not sure' }
  ]
});

// 初始版本数据模板
const createDefaultVersion = (platform = 'instagram') => ({
  platform: platform,
  username: 'sydney_news_hub',
  location: 'Sydney, Australia',
  avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Felix',
  caption: 'This is a simulated news post caption. Researchers can edit this text in real-time on the left.',
  image: '',
  likes: 1050,
  comments: 42,
  shares: 5,
  likesLabel: 'likes',
  timeLabel: '1 hour ago',
  handle: '@sydneynews',
  // 新增：动态按钮列表，支持更改数量
  actionButtons: [
    { id: 'like', icon: 'heart', label: 'Like', active: true },
    { id: 'comment', icon: 'message-circle', label: 'Comment', active: true },
    { id: 'share', icon: 'send', label: 'Share', active: true },
    { id: 'save', icon: 'bookmark', label: 'Save', active: true }
  ],
  icons: {
    like: 'heart',
    comment: 'message-circle',
    share: 'send',
    save: 'bookmark',
    more: 'more-horizontal',
    verify: 'badge-check',
    repost: 'repeat-2',
    analytics: 'bar-chart-2',
    forward: 'forward',
    music: 'music',
    play: 'play-circle'
  },
  hiddenElements: {}, // 新增：记录被隐藏/删除的元素
  questionBlock: createDefaultQuestionBlock()
});

const createDefaultNews = (platform = 'instagram') => ({
  link: '',
  versions: {
    'vA': createDefaultVersion(platform),
    'vB': {
      ...createDefaultVersion(platform),
      caption: 'Testing Version B with completely different variables and platform style.',
      likes: 56,
      comments: 3,
      shares: 12,
      actionButtons: [
         { id: 'like', icon: 'heart', label: 'Like', active: true },
         { id: 'comment', icon: 'message-circle', label: 'Comment', active: true },
         { id: 'share', icon: 'send', label: 'Share', active: true }
       ]
    }
  }
});

// 模拟的多新闻 A/B 版本数据状态
const surveyState = {
  currentNewsIndex: 0,
  currentVersion: 'vA',
  news: [createDefaultNews('instagram')]
};

const APP_STATE_STORAGE_KEY = 'surveyArchitectAppState';
const GAZE_DATA_STORAGE_KEY = 'surveyArchitectParticipantGazeData';
const GAZE_DATA_API_URL = 'http://localhost:5001/api/gaze-data';
const CONTENT_LOCALE_LABELS = {
  en: 'English',
  zh: 'Chinese',
  ar: 'Arabic',
  es: 'Spanish'
};

const appState = {
  currentSurveyId: null,
  surveys: []
};

let hasWarnedGazeDataSyncFailure = false;
let hasStartedGazePolling = false;
const expandedHistorySurveys = new Set();
const expandedHistoryNews = new Set();

function createNewSurvey(title) {
  return {
    id: `survey_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`,
    title,
    status: 'draft',
    inviteCode: '',
    createdAt: new Date().toISOString(),
    publishedAt: null,
    completedAt: null,
    news: [createDefaultNews('instagram')],
    translationConfig: {
      sourceLocale: 'en',
      targetLocales: []
    },
    translations: {},
    participantResults: [],
    exportReady: false,
    publishedSnapshot: null,
    publishedPosts: []
  };
}

function getCurrentSurvey() {
  return appState.surveys.find((survey) => survey.id === appState.currentSurveyId) || null;
}

function clonePlainData(value) {
  return JSON.parse(JSON.stringify(value));
}

function getVersionSnapshot(version) {
  const snapshot = {};
  Object.keys(version || {}).forEach((key) => {
    if (key !== 'platformVariants') {
      snapshot[key] = version[key];
    }
  });
  return clonePlainData(snapshot);
}

function normalizeVersionSnapshot(snapshot, fallbackPlatform = 'instagram') {
  const defaults = createDefaultVersion(fallbackPlatform);
  const normalized = {
    ...defaults,
    ...(snapshot && typeof snapshot === 'object' ? snapshot : {})
  };

  normalized.icons = {
    ...defaults.icons,
    ...(snapshot && snapshot.icons && typeof snapshot.icons === 'object' ? snapshot.icons : {})
  };
  normalized.hiddenElements = normalized.hiddenElements && typeof normalized.hiddenElements === 'object'
    ? normalized.hiddenElements
    : {};
  normalized.actionButtons = Array.isArray(normalized.actionButtons)
    ? normalized.actionButtons
    : defaults.actionButtons;
  normalized.questionBlock = normalizeQuestionBlock(normalized.questionBlock);

  return normalized;
}

function normalizeQuestionBlock(questionBlock) {
  const defaults = createDefaultQuestionBlock();
  const source = questionBlock && typeof questionBlock === 'object' ? questionBlock : {};
  const hasEnabledFlag = Object.prototype.hasOwnProperty.call(source, 'enabled');
  const hasQuestionContent = typeof source.questionText === 'string' && source.questionText.trim();
  const hasOptionContent = Array.isArray(source.options)
    && source.options.some((option) => {
      if (option && typeof option === 'object') {
        return String(option.label || '').trim();
      }
      return String(option || '').trim();
    });
  const options = Array.isArray(source.options)
    ? source.options
        .map((option, index) => ({
          id: option && option.id ? String(option.id) : `option_${index + 1}`,
          label: option && option.label ? String(option.label) : `Option ${index + 1}`
        }))
        .filter((option) => option.label.trim())
    : defaults.options;

  return {
    ...defaults,
    ...source,
    enabled: hasEnabledFlag ? Boolean(source.enabled) : Boolean(hasQuestionContent && hasOptionContent),
    type: source.type === 'multiple' ? 'multiple' : 'single',
    questionText: typeof source.questionText === 'string' && source.questionText.trim()
      ? source.questionText
      : defaults.questionText,
    required: source.required !== false,
    options: (options.length >= 2 ? options : defaults.options).slice(0, 4)
  };
}

function applyVersionSnapshot(version, snapshot) {
  const variants = version.platformVariants && typeof version.platformVariants === 'object'
    ? version.platformVariants
    : {};

  Object.keys(version).forEach((key) => {
    if (key !== 'platformVariants') {
      delete version[key];
    }
  });

  Object.assign(version, clonePlainData(snapshot));
  version.platformVariants = variants;
}

function ensureVersionPlatformVariants(version) {
  if (!version.platformVariants || typeof version.platformVariants !== 'object') {
    version.platformVariants = {};
  }

  const currentPlatform = version.platform || 'instagram';
  if (!version.platformVariants[currentPlatform]) {
    version.platformVariants[currentPlatform] = getVersionSnapshot(version);
  }

  return version.platformVariants;
}

function syncCurrentPlatformVariant(version) {
  if (!version || typeof version !== 'object') return;

  const variants = ensureVersionPlatformVariants(version);
  const currentPlatform = version.platform || 'instagram';
  variants[currentPlatform] = getVersionSnapshot(version);
}

function syncSurveyPlatformVariants() {
  surveyState.news.forEach((news) => {
    Object.values(news.versions || {}).forEach(syncCurrentPlatformVariant);
  });
}

function switchVersionPlatform(version, nextPlatform) {
  if (!version || !nextPlatform) return;

  syncCurrentPlatformVariant(version);
  const variants = ensureVersionPlatformVariants(version);

  if (!variants[nextPlatform]) {
    const nextSnapshot = getVersionSnapshot(version);
    nextSnapshot.platform = nextPlatform;
    variants[nextPlatform] = nextSnapshot;
  }

  applyVersionSnapshot(version, variants[nextPlatform]);
  version.platform = nextPlatform;
  syncCurrentPlatformVariant(version);
}

function updateVersionAcrossPlatformVariants(version, updates) {
  if (!version || typeof version !== 'object') return;

  Object.assign(version, updates);
  const variants = ensureVersionPlatformVariants(version);
  Object.keys(variants).forEach((platform) => {
    variants[platform] = {
      ...variants[platform],
      ...updates
    };
  });
  syncCurrentPlatformVariant(version);
}

function normalizeVersion(version, fallbackPlatform = 'instagram') {
  const normalized = normalizeVersionSnapshot(version, fallbackPlatform);
  const rawVariants = version && version.platformVariants && typeof version.platformVariants === 'object'
    ? version.platformVariants
    : {};
  const variants = {};

  Object.entries(rawVariants).forEach(([platform, snapshot]) => {
    variants[platform] = normalizeVersionSnapshot(
      {
        ...(snapshot && typeof snapshot === 'object' ? snapshot : {}),
        platform: snapshot && snapshot.platform ? snapshot.platform : platform
      },
      platform
    );
  });

  normalized.platformVariants = variants;
  syncCurrentPlatformVariant(normalized);
  return normalized;
}

function normalizeNewsItem(newsItem, includeDefaultVersions = true) {
  const defaultNews = createDefaultNews('instagram');
  if (!newsItem || typeof newsItem !== 'object') {
    return defaultNews;
  }

  const versions = newsItem.versions && typeof newsItem.versions === 'object'
    ? newsItem.versions
    : {};
  const fallbackPlatform = versions.vA?.platform || versions.vB?.platform || 'instagram';
  const normalizedVersions = {};
  const versionKeys = includeDefaultVersions
    ? new Set(['vA', 'vB', ...Object.keys(versions)])
    : new Set(Object.keys(versions));

  versionKeys.forEach((versionKey) => {
    const fallbackVersion = defaultNews.versions[versionKey] || createDefaultVersion(fallbackPlatform);
    normalizedVersions[versionKey] = normalizeVersion(versions[versionKey] || fallbackVersion, fallbackPlatform);
  });

  return {
    ...newsItem,
    link: typeof newsItem.link === 'string' ? newsItem.link : '',
    versions: normalizedVersions
  };
}

function getPublishedNewsSnapshot(newsItem, selectedVersionKey) {
  const normalizedNews = normalizeNewsItem(newsItem, false);
  const versions = normalizedNews.versions || {};
  const versionKeys = Object.keys(versions);
  const publishedVersionKey = versions[selectedVersionKey]
    ? selectedVersionKey
    : (versions.vA ? 'vA' : versionKeys[0]);
  const publishedVersion = publishedVersionKey
    ? getPublishedVersionSnapshot(versions[publishedVersionKey])
    : null;

  return {
    ...normalizedNews,
    publishedVersionKey,
    versions: publishedVersionKey
      ? { [publishedVersionKey]: publishedVersion }
      : {}
  };
}

function getPublishedVersionSnapshot(version) {
  const normalizedVersion = normalizeVersion(version, version?.platform || 'instagram');
  const platform = normalizedVersion.platform
    || Object.keys(normalizedVersion.platformVariants || {})[0]
    || 'instagram';
  const variants = ensureVersionPlatformVariants(normalizedVersion);
  const publishedVariant = normalizeVersionSnapshot(variants[platform] || normalizedVersion, platform);
  publishedVariant.platform = platform;

  return {
    ...clonePlainData(publishedVariant),
    platform,
    platformVariants: {
      [platform]: clonePlainData(publishedVariant)
    }
  };
}

function normalizePublishedSnapshot(snapshot) {
  if (!snapshot || typeof snapshot !== 'object') {
    return null;
  }

  const publishedVersionKey = snapshot.publishedVersionKey || 'vA';

  return {
    ...snapshot,
    publishedVersionKey,
    translationConfig: normalizeTranslationConfig(snapshot.translationConfig),
    translations: snapshot.translations && typeof snapshot.translations === 'object'
      ? snapshot.translations
      : {},
    news: Array.isArray(snapshot.news) && snapshot.news.length
      ? snapshot.news.map((news) => getPublishedNewsSnapshot(news, news.publishedVersionKey || publishedVersionKey))
      : []
  };
}

function createPublishedSnapshot(survey, selectedVersionKey = 'vA') {
  return {
    id: survey.id,
    title: survey.title,
    status: 'published',
    inviteCode: survey.inviteCode,
    createdAt: survey.createdAt,
    publishedAt: survey.publishedAt,
    completedAt: survey.completedAt,
    publishedVersionKey: selectedVersionKey,
    news: (survey.news || []).map((news) => getPublishedNewsSnapshot(news, selectedVersionKey)),
    translationConfig: clonePlainData(survey.translationConfig || {
      sourceLocale: 'en',
      targetLocales: []
    }),
    translations: clonePlainData(survey.translations || {}),
    participantResults: [],
    exportReady: false
  };
}

function normalizePublishedPost(post) {
  if (!post || typeof post !== 'object') {
    return null;
  }

  const platform = post.platform || post.variant?.platform || 'instagram';
  const versionKey = post.versionKey || post.publishedVersionKey || 'vA';
  const newsIndex = Number.isFinite(Number(post.newsIndex))
    ? Number(post.newsIndex)
    : 0;
  const variant = normalizeVersionSnapshot(post.variant || post.snapshot || {}, platform);
  variant.platform = platform;

  return {
    id: post.id || `published_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`,
    surveyId: post.surveyId || '',
    newsIndex,
    newsLink: typeof post.newsLink === 'string' ? post.newsLink : '',
    versionKey,
    platform,
    publishedAt: post.publishedAt || new Date().toISOString(),
    variant
  };
}

function createPublishedPost(survey, newsIndex, versionKey, publishedAt) {
  const news = survey.news[newsIndex];
  const version = news?.versions?.[versionKey];
  const publishedVersion = getPublishedVersionSnapshot(version);
  const platform = publishedVersion.platform || 'instagram';
  const variant = clonePlainData(publishedVersion.platformVariants?.[platform] || publishedVersion);
  variant.platform = platform;

  return {
    id: `published_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`,
    surveyId: survey.id,
    newsIndex,
    newsLink: news?.link || '',
    versionKey,
    platform,
    publishedAt,
    variant
  };
}

function createHistoryRecordFromPublishedPosts(survey, publishedPosts) {
  const newsRecords = [];

  publishedPosts.forEach((post) => {
    const newsIndex = Number.isFinite(Number(post.newsIndex)) ? Number(post.newsIndex) : 0;
    const sourceNews = survey.news?.[newsIndex] || {};

    if (!newsRecords[newsIndex]) {
      newsRecords[newsIndex] = {
        sourceIndex: newsIndex,
        link: post.newsLink || sourceNews.link || '',
        versions: {},
        publishedPosts: []
      };
    }

    const news = newsRecords[newsIndex];
    if (!news.link && post.newsLink) {
      news.link = post.newsLink;
    }
    news.publishedPosts.push(post);

    if (!news.versions[post.versionKey]) {
      news.versions[post.versionKey] = {
        platformGroups: {},
        publishedRecords: []
      };
    }

    const version = news.versions[post.versionKey];
    if (!version.platformGroups[post.platform]) {
      version.platformGroups[post.platform] = [];
    }

    version.platformGroups[post.platform].push(post);
    version.publishedRecords.push(post);
  });

  return {
    ...survey,
    publishedPosts,
    news: newsRecords
      .filter(Boolean)
      .map((news) => ({
        ...news,
        publishedVersionKeys: Object.keys(news.versions || {})
      }))
  };
}

function createPublishedPostsFromSnapshot(snapshot) {
  const normalizedSnapshot = normalizePublishedSnapshot(snapshot);
  if (!normalizedSnapshot) {
    return [];
  }

  const publishedAt = normalizedSnapshot.publishedAt || new Date().toISOString();
  const posts = [];

  (normalizedSnapshot.news || []).forEach((news, newsIndex) => {
    getVersionEntries(news).forEach(([versionKey, version]) => {
      getPlatformVariantEntries(version).forEach(([platform, variant]) => {
        posts.push(normalizePublishedPost({
          id: `legacy_${normalizedSnapshot.id || 'survey'}_${newsIndex}_${versionKey}_${platform}_${publishedAt}`,
          surveyId: normalizedSnapshot.id || '',
          newsIndex,
          newsLink: news.link || '',
          versionKey,
          platform,
          publishedAt,
          variant
        }));
      });
    });
  });

  return posts.filter(Boolean);
}

function normalizeTranslationConfig(config) {
  const source = config && typeof config === 'object' ? config : {};
  const sourceLocale = CONTENT_LOCALE_LABELS[source.sourceLocale] ? source.sourceLocale : 'en';
  const targetLocales = Array.isArray(source.targetLocales)
    ? source.targetLocales.filter((locale, index, locales) => (
      CONTENT_LOCALE_LABELS[locale] &&
      locale !== sourceLocale &&
      locales.indexOf(locale) === index
    ))
    : [];

  return {
    sourceLocale,
    targetLocales
  };
}

function getHistorySurveyRecord(survey) {
  const publishedPosts = Array.isArray(survey.publishedPosts)
    ? survey.publishedPosts.map(normalizePublishedPost).filter(Boolean)
    : [];

  if (publishedPosts.length > 0) {
    const source = createHistoryRecordFromPublishedPosts(survey, publishedPosts);

    return {
      ...source,
      id: survey.id,
      title: source.title || survey.title,
      status: survey.status === 'completed' ? 'completed' : 'published',
      participantResults: Array.isArray(survey.participantResults) ? survey.participantResults : [],
      exportReady: Boolean(survey.exportReady),
      completedAt: survey.completedAt || source.completedAt,
      publishedAt: survey.publishedAt || publishedPosts[publishedPosts.length - 1].publishedAt
    };
  }

  const publishedSnapshot = normalizePublishedSnapshot(survey.publishedSnapshot);
  if (!publishedSnapshot && !survey.publishedAt) {
    return null;
  }

  const source = publishedSnapshot || {
    ...survey,
    news: Array.isArray(survey.news) ? survey.news.map(normalizeNewsItem) : []
  };

  return {
    ...source,
    id: survey.id,
    title: source.title || survey.title,
    status: survey.status === 'completed' ? 'completed' : (source.status || 'published'),
    participantResults: Array.isArray(survey.participantResults) ? survey.participantResults : [],
    exportReady: Boolean(survey.exportReady),
    completedAt: survey.completedAt || source.completedAt,
    publishedAt: survey.publishedAt || source.publishedAt
  };
}

function normalizeSurvey(survey) {
  const fallbackSurvey = createNewSurvey('Untitled Survey');
  const normalized = {
    ...fallbackSurvey,
    ...(survey && typeof survey === 'object' ? survey : {})
  };

  normalized.id = typeof normalized.id === 'string' && normalized.id
    ? normalized.id
    : fallbackSurvey.id;
  normalized.title = typeof normalized.title === 'string' && normalized.title.trim()
    ? normalized.title.trim()
    : 'Untitled Survey';
  normalized.news = Array.isArray(normalized.news) && normalized.news.length
    ? normalized.news.map(normalizeNewsItem)
    : [createDefaultNews('instagram')];
  normalized.translationConfig = normalizeTranslationConfig(normalized.translationConfig);
  normalized.translations = normalized.translations && typeof normalized.translations === 'object'
    ? normalized.translations
    : {};
  normalized.participantResults = Array.isArray(normalized.participantResults)
    ? normalized.participantResults.map(normalizeParticipantGazeResult).filter(Boolean)
    : [];
  normalized.exportReady = Boolean(normalized.exportReady);
  normalized.publishedSnapshot = normalizePublishedSnapshot(normalized.publishedSnapshot);
  const normalizedPublishedPosts = Array.isArray(normalized.publishedPosts)
    ? normalized.publishedPosts.map(normalizePublishedPost).filter(Boolean)
    : [];
  normalized.publishedPosts = normalizedPublishedPosts.length > 0
    ? normalizedPublishedPosts
    : createPublishedPostsFromSnapshot(normalized.publishedSnapshot);

  return normalized;
}

function normalizeParticipantGazeResult(payload) {
  if (!payload || typeof payload !== 'object') {
    return null;
  }

  const rawPayload = payload.rawPayload && typeof payload.rawPayload === 'object'
    ? payload.rawPayload
    : (payload.raw_payload && typeof payload.raw_payload === 'object' ? payload.raw_payload : payload);
  const gazeData = Array.isArray(payload.gazeData)
    ? payload.gazeData
    : (
      Array.isArray(payload.gazeLogs)
        ? payload.gazeLogs
        : (Array.isArray(payload.samples) ? payload.samples : [])
    );
  const sampleCountValue = payload.sampleCount ?? payload.sample_count;
  const sampleCount = Number.isFinite(Number(sampleCountValue))
    ? Number(sampleCountValue)
    : gazeData.length;
  const participantId = payload.participantId || payload.participant_id || '';

  return {
    id: payload.id || payload.resultId || `gaze_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`,
    surveyId: payload.surveyId || payload.survey_id || appState.currentSurveyId,
    inviteCode: payload.inviteCode || payload.invite_code || '',
    participantId,
    participantLabel: payload.participantLabel || payload.participant_label || participantId || 'Participant',
    status: payload.status || 'completed',
    startedAt: payload.startedAt || payload.started_at || payload.studyStartedAt || payload.study_started_at || '',
    closedAt: payload.closedAt || payload.closed_at || payload.studyEndedAt || payload.study_ended_at || new Date().toISOString(),
    receivedAt: payload.receivedAt || payload.received_at || new Date().toISOString(),
    sampleCount,
    gazeData,
    qualityScore: payload.qualityScore ?? payload.quality_score ?? '',
    metadata: payload.metadata && typeof payload.metadata === 'object' ? payload.metadata : {},
    rawPayload
  };
}

function bindSurveyToEditor(survey) {
  if (!survey) return;

  survey.news = Array.isArray(survey.news) && survey.news.length
    ? survey.news
    : [createDefaultNews('instagram')];
  surveyState.currentNewsIndex = 0;
  surveyState.currentVersion = 'vA';
  surveyState.news = survey.news;
}

function saveAppStateToLocalStorage() {
  syncSurveyPlatformVariants();
  const currentSurvey = getCurrentSurvey();
  if (currentSurvey) {
    currentSurvey.news = surveyState.news;
  }

  try {
    localStorage.setItem(APP_STATE_STORAGE_KEY, JSON.stringify(appState));
  } catch (error) {
    console.warn('Unable to save survey data:', error);
  }
}

function loadAppStateFromLocalStorage() {
  try {
    const storedState = localStorage.getItem(APP_STATE_STORAGE_KEY);
    if (!storedState) return false;

    const parsedState = JSON.parse(storedState);
    if (!parsedState || !Array.isArray(parsedState.surveys) || parsedState.surveys.length === 0) {
      return false;
    }

    appState.surveys = parsedState.surveys.map(normalizeSurvey);
    appState.currentSurveyId = typeof parsedState.currentSurveyId === 'string'
      ? parsedState.currentSurveyId
      : appState.surveys[0].id;

    if (!getCurrentSurvey()) {
      appState.currentSurveyId = appState.surveys[0].id;
    }

    bindSurveyToEditor(getCurrentSurvey());
    return true;
  } catch (error) {
    console.warn('Unable to load survey data:', error);
    return false;
  }
}

async function initializeAppState() {
  // 检查服务器是否重启并清空本地存储
  try {
    const response = await fetch('/api/server-info');
    if (response.ok) {
      const info = await response.json();
      const lastStartTime = localStorage.getItem('SERVER_START_TIME');
      
      // 如果本地没有时间戳，或者本地时间戳与服务器不一致，说明服务器重启过
      if (lastStartTime !== info.start_time) {
        console.log('Server restart detected. Clearing local storage...');
        localStorage.clear();
        localStorage.setItem('SERVER_START_TIME', info.start_time);
        
        // 如果是在登录后的页面，清空后直接跳回登录页
        if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/register')) {
          window.location.href = '/login';
          return;
        }
      }
    }
  } catch (error) {
    console.warn('Failed to check server status:', error);
  }

  if (loadAppStateFromLocalStorage()) {
    return;
  }

  appState.surveys = [];
  appState.currentSurveyId = null;
  surveyState.currentNewsIndex = 0;
  surveyState.currentVersion = 'vA';
  surveyState.news = [createDefaultNews('instagram')];
}

function showParticipantCompletionNotification(survey) {
  let container = document.getElementById('participant-completion-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'participant-completion-toast-container';
    container.className = 'fixed right-5 bottom-5 z-[2300] w-[min(360px,calc(100vw-2.5rem))] space-y-3';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'bg-white border border-gray-200 rounded-lg shadow-xl p-4';
  toast.innerHTML = `
    <div class="flex items-start gap-3">
      <div class="w-9 h-9 rounded-full bg-sky-100 text-sky-600 flex items-center justify-center shrink-0">
        <i data-lucide="check-circle-2" class="w-5 h-5"></i>
      </div>
      <div class="min-w-0 flex-1">
        <p class="text-sm font-semibold text-gray-900">${escapeHtml(t('notification.participantCompleted'))}</p>
        <div class="flex flex-wrap gap-2 mt-3">
          <button type="button" data-action="toast-view-history" class="bg-sky-500 hover:bg-sky-600 text-white text-xs font-bold px-3 py-2 rounded-md transition-colors">
            ${escapeHtml(t('notification.viewHistory'))}
          </button>
          <button type="button" data-action="toast-dismiss" class="bg-white border border-gray-300 text-gray-700 text-xs font-bold px-3 py-2 rounded-md hover:bg-gray-50 transition-colors">
            ${escapeHtml(t('notification.dismiss'))}
          </button>
        </div>
      </div>
    </div>
  `;

  toast.addEventListener('click', (event) => {
    const target = event.target.closest('[data-action]');
    if (!target) return;

    if (target.getAttribute('data-action') === 'toast-view-history') {
      if (survey && survey.id) {
        expandedHistorySurveys.add(survey.id);
      }
      showHistoryView();
      toast.remove();
      return;
    }

    if (target.getAttribute('data-action') === 'toast-dismiss') {
      toast.remove();
    }
  });

  container.appendChild(toast);
  lucide.createIcons({ scope: toast });
  window.setTimeout(() => {
    toast.remove();
  }, 10000);
}

function storeParticipantGazeResult(payload, options = {}) {
  const result = normalizeParticipantGazeResult(payload);
  if (!result) {
    return false;
  }

  const targetSurvey = appState.surveys.find((survey) => survey.id === result.surveyId);
  if (!targetSurvey) {
    return false;
  }

  result.surveyId = targetSurvey.id;
  if (!Array.isArray(targetSurvey.participantResults)) {
    targetSurvey.participantResults = [];
  }

  const existingIndex = targetSurvey.participantResults.findIndex((storedResult) => (
    storedResult.id === result.id ||
    (
      storedResult.participantLabel === result.participantLabel &&
      storedResult.closedAt === result.closedAt
    )
  ));

  if (existingIndex >= 0) {
    targetSurvey.participantResults[existingIndex] = {
      ...targetSurvey.participantResults[existingIndex],
      ...result
    };
  } else {
    targetSurvey.participantResults.push(result);
    if (options.notify !== false) {
      showParticipantCompletionNotification(targetSurvey);
    }
  }

  targetSurvey.status = 'completed';
  targetSurvey.completedAt = result.closedAt || result.receivedAt;
  targetSurvey.exportReady = true;
  saveAppStateToLocalStorage();
  renderDataExportView();
  return true;
}

function storeParticipantGazeResults(payload, options = {}) {
  const results = Array.isArray(payload) ? payload : [payload];
  return results.reduce((count, result) => (
    storeParticipantGazeResult(result, options) ? count + 1 : count
  ), 0);
}

function receiveParticipantGazeData(payload) {
  return storeParticipantGazeResults(payload);
}

function collectPendingParticipantGazeData() {
  try {
    const pendingData = localStorage.getItem(GAZE_DATA_STORAGE_KEY);
    if (!pendingData) {
      return 0;
    }

    const parsedData = JSON.parse(pendingData);
    const storedCount = storeParticipantGazeResults(parsedData);
    if (storedCount > 0) {
      localStorage.removeItem(GAZE_DATA_STORAGE_KEY);
    }
    return storedCount;
  } catch (error) {
    console.warn('Unable to read pending participant gaze data:', error);
    return 0;
  }
}

async function syncGazeDataFromServer(options = {}) {
  try {
    let payload = [];
    const surveyIds = appState.surveys.map((survey) => survey.id);

    for (const surveyId of surveyIds) {
      const response = await fetch(`${GAZE_DATA_API_URL}?surveyId=${encodeURIComponent(surveyId)}`);
      if (!response.ok) {
        continue;
      }

      const result = await response.json();
      const results = Array.isArray(result)
        ? result
        : (Array.isArray(result.results) ? result.results : []);
      payload = payload.concat(results);
    }

    const storedCount = storeParticipantGazeResults(payload, options);
    if (storedCount > 0) {
      renderDataExportView();
    }
  } catch (error) {
    if (!hasWarnedGazeDataSyncFailure) {
      console.warn('Unable to sync gaze data from server:', error);
      hasWarnedGazeDataSyncFailure = true;
    }
  }
}

function startParticipantGazeDataListeners() {
  window.receiveParticipantGazeData = receiveParticipantGazeData;

  window.addEventListener('message', (event) => {
    const data = event.data;
    if (!data || typeof data !== 'object') {
      return;
    }

    if (data.type === 'participant-gaze-data' || data.type === 'SURVEY_GAZE_DATA') {
      storeParticipantGazeResults(data.payload || data.result || data.results || data);
    }
  });

  window.addEventListener('storage', (event) => {
    if (event.key !== GAZE_DATA_STORAGE_KEY || !event.newValue) {
      return;
    }

    collectPendingParticipantGazeData();
  });

  collectPendingParticipantGazeData();
  syncGazeDataFromServer({ notify: false });

  if (!hasStartedGazePolling) {
    hasStartedGazePolling = true;
    window.setInterval(() => {
      syncGazeDataFromServer();
    }, 10000);
  }
}

function showSurveyTitleDialog() {
  return new Promise((resolve) => {
    const overlay = document.createElement('div');
    overlay.className = 'fixed inset-0 bg-black/40 z-[2000] flex items-center justify-center px-4';
    overlay.innerHTML = `
      <div class="w-full max-w-sm bg-white rounded-lg shadow-xl border border-gray-200 p-5">
        <label for="new-survey-title-input" class="block text-sm font-semibold text-gray-900 mb-2">${escapeHtml(t('dialog.surveyTitle'))}</label>
        <input
          id="new-survey-title-input"
          type="text"
          class="w-full bg-gray-50 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:border-gray-500"
          placeholder="${escapeHtml(t('dialog.surveyTitlePlaceholder'))}"
        />
        <p id="new-survey-title-error" class="hidden text-xs text-red-500 mt-2">${escapeHtml(t('dialog.surveyTitleError'))}</p>
        <div class="flex justify-end space-x-2 mt-5">
          <button type="button" data-action="cancel" class="px-4 py-2 rounded-md border border-gray-300 text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-colors">${escapeHtml(t('dialog.cancel'))}</button>
          <button type="button" data-action="create" class="px-4 py-2 rounded-md bg-sky-500 text-white text-sm font-semibold hover:bg-sky-600 transition-colors">${escapeHtml(t('dialog.create'))}</button>
        </div>
      </div>
    `;

    const input = overlay.querySelector('#new-survey-title-input');
    const errorText = overlay.querySelector('#new-survey-title-error');

    const close = (value) => {
      overlay.remove();
      resolve(value);
    };

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay || e.target.getAttribute('data-action') === 'cancel') {
        close(null);
      }

      if (e.target.getAttribute('data-action') === 'create') {
        const title = input.value.trim();
        if (!title) {
          errorText.classList.remove('hidden');
          input.focus();
          return;
        }
        close(title);
      }
    });

    input.addEventListener('input', () => {
      errorText.classList.add('hidden');
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        close(null);
      }

      if (e.key === 'Enter') {
        e.preventDefault();
        const title = input.value.trim();
        if (!title) {
          errorText.classList.remove('hidden');
          return;
        }
        close(title);
      }
    });

    document.body.appendChild(overlay);
    input.focus();
  });
}

async function handleNewSurveyClick() {
  const title = await showSurveyTitleDialog();

  if (!title || !title.trim()) {
    return;
  }

  const newSurvey = createNewSurvey(title.trim());
  appState.surveys.push(newSurvey);
  appState.currentSurveyId = newSurvey.id;
  bindSurveyToEditor(newSurvey);
  saveAppStateToLocalStorage();
  showEditorView();
}

async function handlePublishSurveyClick() {
  const currentSurvey = getCurrentSurvey();
  if (!currentSurvey) {
    return;
  }

  syncSurveyPlatformVariants();
  currentSurvey.news = surveyState.news;
  if (!currentSurvey.inviteCode) {
    alert(t('alert.inviteCodeRequired'));
    return;
  }
  currentSurvey.status = currentSurvey.status === 'completed' ? 'completed' : 'published';
  const publishedAt = new Date().toISOString();
  currentSurvey.publishedAt = publishedAt;
  
  const snapshot = createPublishedSnapshot(currentSurvey, surveyState.currentVersion);
  currentSurvey.publishedSnapshot = snapshot;

  // 调用后端 API 发布到 JSON 数据库 (保持之前修复的功能)
  try {
    const response = await fetch('/api/publish', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(snapshot)
    });
    
    const result = await response.json();
    if (result.success) {
      saveAppStateToLocalStorage();
      renderHistoryView();
      alert(`${t('alert.surveyPublished')}\nInvitation Code: ${snapshot.inviteCode}`);
    } else {
      alert(`Publish failed: ${result.error}`);
    }
  } catch (error) {
    console.error('Publish error:', error);
    alert('Failed to connect to server for publishing.');
  }
}

function renderSurveyTitle() {
  const headerBrand = document.querySelector('header .font-bold');
  if (!headerBrand) return;

  let titleElement = document.getElementById('current-survey-title');
  if (!titleElement) {
    titleElement = document.createElement('span');
    titleElement.id = 'current-survey-title';
    titleElement.className = 'ml-3 pl-3 border-l border-gray-200 text-sm font-bold text-black truncate max-w-[320px]';
    headerBrand.appendChild(titleElement);
  }

  const currentSurvey = getCurrentSurvey();
  titleElement.textContent = currentSurvey ? currentSurvey.title : '';
}

function ensureCreateSurveyButton() {
  if (document.getElementById('btn-create-new-survey')) {
    document.getElementById('btn-create-new-survey').textContent = t('editor.createNewSurvey');
    return;
  }

  const editorTitle = document.getElementById('editor-title');
  if (!editorTitle || !editorTitle.parentElement) {
    return;
  }

  const editorHeader = editorTitle.parentElement;
  const titleRow = document.createElement('div');
  titleRow.className = 'flex items-center justify-between gap-4 mb-2';

  editorTitle.classList.remove('mb-2');
  editorHeader.insertBefore(titleRow, editorTitle);
  titleRow.appendChild(editorTitle);

  const createButton = document.createElement('button');
  createButton.id = 'btn-create-new-survey';
  createButton.type = 'button';
  createButton.className = 'shrink-0 bg-sky-500 hover:bg-sky-600 text-white text-xs font-bold px-4 py-2 rounded-md transition-colors whitespace-nowrap';
  createButton.textContent = t('editor.createNewSurvey');
  createButton.addEventListener('click', handleNewSurveyClick);
  titleRow.appendChild(createButton);
}

function bindPublishSurveyButton() {
  const publishButton = document.getElementById('btn-publish-survey');
  if (!publishButton || publishButton.dataset.publishBound === 'true') {
    return;
  }

  publishButton.dataset.publishBound = 'true';
  publishButton.addEventListener('click', handlePublishSurveyClick);
}

function ensureDataExportNavigation() {
  const exportNavItem = getNavItemByKey('dataExport');
  if (exportNavItem) {
    exportNavItem.remove();
  }
}

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function formatSurveyDate(value) {
  if (!value) return t('status.unknown');

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return t('status.unknown');
  }

  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function getNavItemByKey(key) {
  return document.querySelector(`.nav-item[data-nav-key="${key}"]`);
}

function setActiveNavItem(key) {
  document.querySelectorAll('.nav-item').forEach((item) => {
    item.classList.remove('active');
  });

  const activeItem = getNavItemByKey(key);
  if (activeItem) {
    activeItem.classList.add('active');
  }
}

function getMainWorkspace() {
  return document.querySelector('main');
}

function ensureProfileView() {
  let profileView = document.getElementById('profile-view');
  if (profileView) {
    return profileView;
  }

  const mainWorkspace = getMainWorkspace();
  if (!mainWorkspace) {
    return null;
  }

  profileView = document.createElement('section');
  profileView.id = 'profile-view';
  profileView.className = 'hidden flex-1 overflow-y-auto hide-scrollbar bg-white p-6 md:p-10';
  profileView.addEventListener('click', handleProfileClick);
  mainWorkspace.appendChild(profileView);
  return profileView;
}

function ensureHistoryView() {
  let historyView = document.getElementById('history-view');
  if (historyView) {
    return historyView;
  }

  const mainWorkspace = getMainWorkspace();
  if (!mainWorkspace) {
    return null;
  }

  historyView = document.createElement('section');
  historyView.id = 'history-view';
  historyView.className = 'hidden flex-1 overflow-y-auto hide-scrollbar bg-white p-6 md:p-10';
  historyView.addEventListener('click', handleHistoryClick);
  mainWorkspace.appendChild(historyView);
  return historyView;
}

function ensureDataExportView() {
  let dataExportView = document.getElementById('data-export-view');
  if (dataExportView) {
    return dataExportView;
  }

  const mainWorkspace = getMainWorkspace();
  if (!mainWorkspace) {
    return null;
  }

  dataExportView = document.createElement('section');
  dataExportView.id = 'data-export-view';
  dataExportView.className = 'hidden flex-1 overflow-y-auto hide-scrollbar bg-white p-6 md:p-10';
  dataExportView.addEventListener('click', handleDataExportClick);
  mainWorkspace.appendChild(dataExportView);
  return dataExportView;
}

function ensureResultsView() {
  let resultsView = document.getElementById('results-view');
  if (resultsView) {
    return resultsView;
  }

  const mainWorkspace = getMainWorkspace();
  if (!mainWorkspace) {
    return null;
  }

  resultsView = document.createElement('section');
  resultsView.id = 'results-view';
  resultsView.className = 'hidden flex-1 overflow-y-auto hide-scrollbar bg-white p-6 md:p-10';
  mainWorkspace.appendChild(resultsView);
  return resultsView;
}

function getResearcherAccount() {
  try {
    const storedAccount = localStorage.getItem('surveyLabResearcherAccount');
    return storedAccount ? JSON.parse(storedAccount) : null;
  } catch (error) {
    return null;
  }
}

function getProfileStats() {
  const surveys = appState.surveys || [];
  return {
    totalSurveys: surveys.length,
    publishedSurveys: surveys.filter((survey) => survey.publishedAt || survey.publishedSnapshot).length,
    exportReadySurveys: surveys.filter((survey) => survey.exportReady).length,
    participantResults: surveys.reduce((count, survey) => (
      count + (Array.isArray(survey.participantResults) ? survey.participantResults.length : 0)
    ), 0)
  };
}

function renderProfileStatCard(label, value) {
  return `
    <div class="bg-gray-50 rounded-lg p-4 border border-gray-100">
      <span class="block text-2xl font-bold text-gray-900">${value}</span>
      <span class="text-xs font-semibold text-gray-500 uppercase">${label}</span>
    </div>
  `;
}

function renderProfileView() {
  const profileView = ensureProfileView();
  if (!profileView) return;

  const username = getResearcherUsername();
  const initial = username.charAt(0).toUpperCase() || 'R';
  const session = getResearcherSession();
  const account = getResearcherAccount();
  const currentSurvey = getCurrentSurvey();
  const stats = getProfileStats();

  profileView.innerHTML = `
    <header class="mb-8">
      <h1 class="text-2xl font-semibold mb-2">${escapeHtml(t('profile.title'))}</h1>
      <p class="text-sm text-gray-500">${escapeHtml(t('profile.subtitle'))}</p>
    </header>

    <div class="space-y-6 max-w-5xl">
      <section class="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-5">
          <div class="flex items-center gap-4">
            <div class="w-16 h-16 rounded-full bg-blue-600 text-white flex items-center justify-center text-2xl font-bold">
              ${escapeHtml(initial)}
            </div>
            <div>
              <h2 class="text-xl font-bold text-gray-900">${escapeHtml(username)}</h2>
              <p class="text-sm text-gray-500">${escapeHtml(t('profile.role'))}</p>
            </div>
          </div>
          <button type="button" data-action="profile-sign-out" class="bg-gray-900 hover:bg-black text-white text-xs font-bold px-4 py-2 rounded-md transition-colors">
            ${escapeHtml(t('account.signOut'))}
          </button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-5">
          <div class="bg-gray-50 rounded-lg p-4">
            <span class="block text-xs font-semibold text-gray-500 uppercase mb-1">${escapeHtml(t('profile.username'))}</span>
            <span class="text-sm font-semibold text-gray-900">${escapeHtml(account?.username || username)}</span>
          </div>
          <div class="bg-gray-50 rounded-lg p-4">
            <span class="block text-xs font-semibold text-gray-500 uppercase mb-1">${escapeHtml(t('profile.lastLogin'))}</span>
            <span class="text-sm font-semibold text-gray-900">${escapeHtml(formatSurveyDate(session?.loggedInAt))}</span>
          </div>
          <div class="bg-gray-50 rounded-lg p-4">
            <span class="block text-xs font-semibold text-gray-500 uppercase mb-1">${escapeHtml(t('profile.currentSurvey'))}</span>
            <span class="text-sm font-semibold text-gray-900">${escapeHtml(currentSurvey?.title || t('editor.noActiveSurvey'))}</span>
          </div>
        </div>
      </section>

      <section>
        <h2 class="text-lg font-bold text-gray-900 mb-3">${escapeHtml(t('profile.projectStats'))}</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          ${renderProfileStatCard(t('profile.totalSurveys'), stats.totalSurveys)}
          ${renderProfileStatCard(t('profile.publishedSurveys'), stats.publishedSurveys)}
          ${renderProfileStatCard(t('profile.exportReadySurveys'), stats.exportReadySurveys)}
          ${renderProfileStatCard(t('profile.participantResults'), stats.participantResults)}
        </div>
      </section>

      <section class="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
        <h2 class="text-lg font-bold text-gray-900 mb-4">${escapeHtml(t('profile.settings'))}</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-bold uppercase text-gray-400 mb-2">${escapeHtml(t('profile.displayName'))}</label>
            <input type="text" value="${escapeHtml(username)}" readonly class="w-full bg-gray-50 border border-gray-300 rounded-md px-3 py-2 text-sm text-gray-700 focus:outline-none" />
          </div>
          <div>
            <label class="block text-xs font-bold uppercase text-gray-400 mb-2">${escapeHtml(t('profile.exportFormats'))}</label>
            <div class="flex gap-2">
              <span class="inline-flex items-center rounded-md bg-gray-100 px-3 py-2 text-xs font-bold text-gray-700">JSON</span>
              <span class="inline-flex items-center rounded-md bg-gray-100 px-3 py-2 text-xs font-bold text-gray-700">CSV</span>
            </div>
          </div>
        </div>
      </section>

      <section class="bg-blue-50 border border-blue-100 rounded-lg p-5">
        <h2 class="text-lg font-bold text-blue-900 mb-2">${escapeHtml(t('profile.dataNotice'))}</h2>
        <p class="text-sm text-blue-700">${escapeHtml(t('profile.dataNoticeText'))}</p>
      </section>
    </div>
  `;
}

function getVersionEntries(news) {
  return Object.entries(news.versions || {});
}

function getPlatformVariantEntries(version) {
  const variants = version.platformVariants && typeof version.platformVariants === 'object'
    ? version.platformVariants
    : {};
  const entries = Object.entries(variants);

  if (entries.length > 0) {
    return entries;
  }

  return [[version.platform || 'unknown', version]];
}

function getPlatformGroupEntries(version) {
  return version.platformGroups && typeof version.platformGroups === 'object'
    ? Object.entries(version.platformGroups)
    : [];
}

function formatVersionLabel(versionKey) {
  if (/^v[a-z0-9]+$/i.test(versionKey)) {
    const versionLetter = versionKey.slice(1).toUpperCase();
    return versionLetter === 'A' ? t('editor.versionA') : versionLetter === 'B' ? t('editor.versionB') : `Version ${versionLetter}`;
  }

  return versionKey;
}

function getNewsPublishedVersionKeys(news) {
  if (Array.isArray(news.publishedVersionKeys) && news.publishedVersionKeys.length > 0) {
    return news.publishedVersionKeys;
  }

  if (news.publishedVersionKey) {
    return [news.publishedVersionKey];
  }

  return Object.keys(news.versions || {});
}

function formatNewsPublishedVersionLabel(news) {
  return getNewsPublishedVersionKeys(news)
    .map(formatVersionLabel)
    .join(', ');
}

function formatPlatformLabel(platform) {
  const labels = {
    instagram: 'Instagram',
    facebook: 'Facebook',
    x: 'X',
    tiktok: 'TikTok'
  };

  return labels[platform] || platform;
}

function getSurveyVersionCount(survey) {
  return (survey.news || []).reduce((count, news) => (
    count + getVersionEntries(news).length
  ), 0);
}

function getVersionPlatformVariantCount(version) {
  const platformGroups = getPlatformGroupEntries(version);
  if (platformGroups.length > 0) {
    return platformGroups.length;
  }

  return getPlatformVariantEntries(version).length;
}

function getVersionPublishedPostCount(version) {
  const platformGroups = getPlatformGroupEntries(version);
  if (platformGroups.length > 0) {
    return platformGroups.reduce((count, [, records]) => (
      count + (Array.isArray(records) ? records.length : 0)
    ), 0);
  }

  return getPlatformVariantEntries(version).length;
}

function getNewsPublishedPostCount(news) {
  if (Array.isArray(news.publishedPosts)) {
    return news.publishedPosts.length;
  }

  return getVersionEntries(news).reduce((count, [, version]) => (
    count + getVersionPublishedPostCount(version)
  ), 0);
}

function getSurveyPublishedPostCount(survey) {
  if (Array.isArray(survey.publishedPosts)) {
    return survey.publishedPosts.length;
  }

  return (survey.news || []).reduce((count, news) => (
    count + getNewsPublishedPostCount(news)
  ), 0);
}

function getNewsPlatformVariantCount(news) {
  return getVersionEntries(news).reduce((count, [, version]) => (
    count + getVersionPlatformVariantCount(version)
  ), 0);
}

function getSurveyPlatformVariantCount(survey) {
  return (survey.news || []).reduce((count, news) => (
    count + getNewsPlatformVariantCount(news)
  ), 0);
}

function formatStatusLabel(status) {
  if (!status) return t('status.draft');

  const normalizedStatus = String(status).toLowerCase();
  if (normalizedStatus === 'draft') return t('status.draft');
  if (normalizedStatus === 'published') return t('status.published');
  if (normalizedStatus === 'completed') return t('status.completed');

  return String(status)
    .replace(/[-_]+/g, ' ')
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function isHistoryElementHidden(variant, key) {
  return Boolean(variant.hiddenElements && variant.hiddenElements[key]);
}

function renderHistoryActionButtons(variant) {
  const buttons = Array.isArray(variant.actionButtons)
    ? variant.actionButtons.filter((button) => button && button.active !== false)
    : [];

  if (buttons.length === 0) {
    return `<span class="text-xs font-semibold text-gray-400">${escapeHtml(t('history.noActionButtons'))}</span>`;
  }

  return buttons.map((button) => `
    <span class="inline-flex items-center gap-1 rounded-md bg-gray-50 border border-gray-200 px-2 py-1 text-xs font-semibold text-gray-600">
      <i data-lucide="${escapeHtml(button.icon || 'circle')}" class="w-3.5 h-3.5"></i>
      ${escapeHtml(button.label || button.id || 'Action')}
    </span>
  `).join('');
}

function renderPlatformVariantHistory(variant, platform) {
  const title = variant.caption || 'Untitled content';
  const questionBlock = normalizeQuestionBlock(variant.questionBlock);
  const imageContent = !isHistoryElementHidden(variant, 'image') && variant.image
    ? `<img src="${escapeHtml(variant.image)}" alt="" class="w-full h-full object-cover" />`
    : `<div class="w-full h-full flex items-center justify-center text-xs font-medium text-gray-400">${escapeHtml(isHistoryElementHidden(variant, 'image') ? t('history.imageHidden') : t('history.noImage'))}</div>`;
  const avatarContent = !isHistoryElementHidden(variant, 'avatar') && variant.avatar
    ? `<img src="${escapeHtml(variant.avatar)}" alt="" class="w-full h-full object-cover" />`
    : `<span class="text-xs font-bold text-gray-500">${escapeHtml((variant.username || 'P').charAt(0).toUpperCase())}</span>`;
  const showEngagement = !isHistoryElementHidden(variant, 'likes') || !isHistoryElementHidden(variant, 'comments') || !isHistoryElementHidden(variant, 'shares');

  return `
    <div class="border border-gray-200 rounded-lg bg-white overflow-hidden">
      <div class="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
        <h5 class="text-sm font-bold text-black">${escapeHtml(formatPlatformLabel(platform))}</h5>
        <span class="text-xs font-semibold text-gray-500 uppercase">${escapeHtml(platform)}</span>
      </div>
      <div class="p-4">
        <div class="border border-gray-200 rounded-lg bg-white overflow-hidden">
          <div class="flex items-center justify-between gap-3 p-3 border-b border-gray-100">
            <div class="flex items-center gap-3 min-w-0">
              <div class="w-9 h-9 rounded-full bg-gray-100 overflow-hidden flex items-center justify-center shrink-0">
                ${avatarContent}
              </div>
              <div class="min-w-0">
                ${!isHistoryElementHidden(variant, 'username') ? `<p class="text-sm font-bold text-gray-900 truncate">${escapeHtml(variant.username || variant.handle || t('history.unknownAccount'))}</p>` : ''}
                ${!isHistoryElementHidden(variant, 'location') && variant.location ? `<p class="text-xs text-gray-500 truncate">${escapeHtml(variant.location)}</p>` : ''}
              </div>
            </div>
            ${!isHistoryElementHidden(variant, 'more-icon') ? `<i data-lucide="${escapeHtml(variant.icons?.more || 'more-horizontal')}" class="w-4 h-4 text-gray-400 shrink-0"></i>` : ''}
          </div>
          <div class="aspect-video bg-gray-50 border-b border-gray-100 overflow-hidden">
            ${imageContent}
          </div>
          <div class="p-3 space-y-3">
            <div class="flex flex-wrap gap-2">
              ${renderHistoryActionButtons(variant)}
            </div>
            ${showEngagement ? `
              <div class="grid grid-cols-3 gap-2 text-xs text-gray-500">
                ${!isHistoryElementHidden(variant, 'likes') ? `
                  <div>
                    <span class="block font-bold text-gray-900">${Number(variant.likes || 0).toLocaleString()}</span>
                    likes
                  </div>
                ` : ''}
                ${!isHistoryElementHidden(variant, 'comments') ? `
                  <div>
                    <span class="block font-bold text-gray-900">${Number(variant.comments || 0).toLocaleString()}</span>
                    comments
                  </div>
                ` : ''}
                ${!isHistoryElementHidden(variant, 'shares') ? `
                  <div>
                    <span class="block font-bold text-gray-900">${Number(variant.shares || 0).toLocaleString()}</span>
                    shares
                  </div>
                ` : ''}
              </div>
            ` : ''}
            ${!isHistoryElementHidden(variant, 'caption') ? `
              <p class="text-sm text-gray-900 leading-snug">
                ${!isHistoryElementHidden(variant, 'username') ? `<span class="font-bold">${escapeHtml(variant.username || '')}</span> ` : ''}
                ${escapeHtml(title)}
              </p>
            ` : ''}
            ${!isHistoryElementHidden(variant, 'timeLabel') && variant.timeLabel ? `<p class="text-[11px] font-semibold text-gray-400 uppercase">${escapeHtml(variant.timeLabel)}</p>` : ''}
            ${renderQuestionBlock(variant)}
          </div>
        </div>
      </div>
    </div>
  `;
}

function renderVersionHistory(version, label) {
  const platformGroups = getPlatformGroupEntries(version);
  if (platformGroups.length > 0) {
    const publishedPostCount = getVersionPublishedPostCount(version);

    return `
      <div class="border border-gray-200 rounded-lg bg-white p-4">
        <div class="flex items-center justify-between gap-3 mb-4">
          <h4 class="text-sm font-bold text-black">${escapeHtml(label)}</h4>
          <span class="text-xs font-semibold text-gray-500 uppercase">${publishedPostCount} ${escapeHtml(t('history.publishedPosts'))}</span>
        </div>
        <div class="space-y-4">
          ${platformGroups.map(([platform, records]) => (
            renderPublishedPlatformGroup(platform, records)
          )).join('')}
        </div>
      </div>
    `;
  }

  const platformEntries = getPlatformVariantEntries(version);

  return `
    <div class="border border-gray-200 rounded-lg bg-white p-4">
      <div class="flex items-center justify-between gap-3 mb-4">
        <h4 class="text-sm font-bold text-black">${escapeHtml(label)}</h4>
        <span class="text-xs font-semibold text-gray-500 uppercase">${platformEntries.length} ${escapeHtml(platformEntries.length === 1 ? t('history.platform') : t('history.platformPlural'))}</span>
      </div>
      <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
        ${platformEntries.map(([platform, variant]) => (
          renderPlatformVariantHistory(variant, platform)
        )).join('')}
      </div>
    </div>
  `;
}

function renderPublishedPlatformGroup(platform, records) {
  const publishedRecords = Array.isArray(records) ? records : [];

  return `
    <div class="border border-gray-200 rounded-lg bg-gray-50 p-4">
      <div class="flex items-center justify-between gap-3 mb-3">
        <h5 class="text-sm font-bold text-gray-900">${escapeHtml(formatPlatformLabel(platform))}</h5>
        <span class="text-xs font-semibold text-gray-500 uppercase">${publishedRecords.length} ${escapeHtml(t('history.publishedPosts'))}</span>
      </div>
      <div class="space-y-4">
        ${publishedRecords.map((record, index) => renderPublishedPostHistory(record, platform, index)).join('')}
      </div>
    </div>
  `;
}

function renderPublishedPostHistory(record, platform, index) {
  return `
    <div class="space-y-2">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <span class="text-xs font-bold text-gray-900">${escapeHtml(t('history.publishRecord', { number: index + 1 }))}</span>
        <span class="text-xs font-semibold text-gray-500">${escapeHtml(t('history.publishedAt', { date: formatSurveyDate(record.publishedAt) }))}</span>
      </div>
      ${renderPlatformVariantHistory(record.variant, platform)}
    </div>
  `;
}

function renderNewsHistory(news, index, surveyId) {
  const versionEntries = getVersionEntries(news);
  const publishedVersionLabel = formatNewsPublishedVersionLabel(news);
  const publishedPostCount = getNewsPublishedPostCount(news);
  const sourceIndex = Number.isFinite(Number(news.sourceIndex)) ? Number(news.sourceIndex) : index;
  const newsKey = `${surveyId}::${sourceIndex}`;
  const isExpanded = expandedHistoryNews.has(newsKey);

  return `
    <div class="border border-gray-200 rounded-lg bg-gray-50 p-4">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        <div>
          <div class="flex flex-wrap items-center gap-2">
            <h3 class="text-sm font-bold text-gray-900">${escapeHtml(t('history.newsItem', { number: sourceIndex + 1 }))}</h3>
            ${publishedVersionLabel ? `<span class="text-xs font-semibold text-gray-500 uppercase">${escapeHtml(publishedVersionLabel)}</span>` : ''}
            <span class="text-xs font-semibold text-gray-500 uppercase">${getNewsPlatformVariantCount(news)} ${escapeHtml(t('history.platformStyles'))}</span>
            <span class="text-xs font-semibold text-gray-500 uppercase">${publishedPostCount} ${escapeHtml(t('history.publishedPosts'))}</span>
          </div>
          ${news.link ? `<a href="${escapeHtml(news.link)}" target="_blank" rel="noopener noreferrer" class="text-xs font-semibold text-sky-600 hover:text-sky-700 mt-1 inline-block">${escapeHtml(t('history.openLink'))}</a>` : `<p class="text-xs text-gray-500 mt-1">${escapeHtml(t('history.noOriginalLink'))}</p>`}
        </div>
        <button
          type="button"
          data-action="toggle-history-news"
          data-news-key="${escapeHtml(newsKey)}"
          class="bg-white border border-gray-300 text-gray-700 text-xs font-bold px-4 py-2 rounded-md hover:bg-gray-50 transition-colors"
        >
          ${escapeHtml(isExpanded ? t('history.hideVersions') : t('history.viewVersions'))}
        </button>
      </div>
      ${isExpanded ? `
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-4">
          ${versionEntries.map(([versionKey, version]) => (
            renderVersionHistory(version, formatVersionLabel(versionKey))
          )).join('')}
        </div>
      ` : ''}
    </div>
  `;
}

function renderSurveyHistoryCard(survey) {
  const isExpanded = expandedHistorySurveys.has(survey.id);

  return `
    <article class="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
      <div class="flex flex-col xl:flex-row xl:items-start xl:justify-between gap-4">
        <div>
          <h2 class="text-lg font-bold text-black">${escapeHtml(survey.title)}</h2>
          <p class="text-xs text-gray-500 mt-1">${escapeHtml(t('history.created', { date: formatSurveyDate(survey.createdAt) }))}</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <button
            type="button"
            data-action="toggle-history-survey"
            data-survey-id="${escapeHtml(survey.id)}"
            class="bg-sky-500 hover:bg-sky-600 text-white text-xs font-bold px-4 py-2 rounded-md transition-colors"
          >
            ${escapeHtml(isExpanded ? t('history.hideDetails') : t('history.viewDetails'))}
          </button>
          <button
            type="button"
            data-action="history-open-data-export"
            data-survey-id="${escapeHtml(survey.id)}"
            class="bg-white border border-gray-300 text-gray-700 text-xs font-bold px-4 py-2 rounded-md hover:bg-gray-50 transition-colors"
          >
            ${escapeHtml(t('history.dataExport'))}
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-3 mt-5">
        <div class="bg-gray-50 rounded-lg p-4">
          <span class="block text-lg font-bold text-gray-900">${escapeHtml(formatStatusLabel(survey.status))}</span>
          <span class="text-xs font-semibold text-gray-500 uppercase">${escapeHtml(t('history.status'))}</span>
        </div>
        <div class="bg-gray-50 rounded-lg p-4">
          <span class="block text-lg font-bold text-gray-900">${(survey.news || []).length}</span>
          <span class="text-xs font-semibold text-gray-500 uppercase">${escapeHtml(t('history.news'))}</span>
        </div>
        <div class="bg-gray-50 rounded-lg p-4">
          <span class="block text-lg font-bold text-gray-900">${getSurveyPublishedPostCount(survey)}</span>
          <span class="text-xs font-semibold text-gray-500 uppercase">${escapeHtml(t('history.publishedPosts'))}</span>
        </div>
        <div class="bg-gray-50 rounded-lg p-4">
          <span class="block text-lg font-bold text-gray-900">${getSurveyPlatformVariantCount(survey)}</span>
          <span class="text-xs font-semibold text-gray-500 uppercase">${escapeHtml(t('history.platformStyles'))}</span>
        </div>
      </div>

      ${isExpanded ? `
        <div class="mt-5 border-t border-gray-100 pt-5 space-y-3">
          ${(survey.news || []).map((news, index) => renderNewsHistory(news, index, survey.id)).join('')}
        </div>
      ` : ''}
    </article>
  `;
}

function renderHistoryView() {
  const historyView = ensureHistoryView();
  if (!historyView) return;

  const historySurveys = appState.surveys
    .map(getHistorySurveyRecord)
    .filter(Boolean)
    .slice()
    .sort((a, b) => new Date(b.publishedAt || b.createdAt) - new Date(a.publishedAt || a.createdAt));

  if (historySurveys.length === 0) {
    historyView.innerHTML = `
      <header class="mb-8">
        <h1 class="text-2xl font-semibold mb-2">${escapeHtml(t('history.title'))}</h1>
        <p class="text-sm text-gray-500">${escapeHtml(t('history.emptySubtitle'))}</p>
      </header>
      <div class="border border-dashed border-gray-300 rounded-lg bg-gray-50 p-8 text-center">
        <p class="text-sm font-semibold text-gray-900">${escapeHtml(t('history.noPublished'))}</p>
        <p class="text-sm text-gray-500 mt-1">${escapeHtml(t('history.draftsExcluded'))}</p>
      </div>
    `;
    return;
  }

  historyView.innerHTML = `
    <header class="mb-8">
      <h1 class="text-2xl font-semibold mb-2">${escapeHtml(t('history.title'))}</h1>
      <p class="text-sm text-gray-500">${escapeHtml(t('history.subtitle'))}</p>
    </header>
    <div class="space-y-5">
      ${historySurveys.map(renderSurveyHistoryCard).join('')}
    </div>
  `;
  lucide.createIcons({ scope: historyView });
}

function handleHistoryClick(e) {
  const target = e.target.closest('[data-action]');
  if (!target) return;

  const action = target.getAttribute('data-action');
  if (action === 'toggle-history-survey') {
    const surveyId = target.getAttribute('data-survey-id');
    if (expandedHistorySurveys.has(surveyId)) {
      expandedHistorySurveys.delete(surveyId);
    } else {
      expandedHistorySurveys.add(surveyId);
    }
    renderHistoryView();
    return;
  }

  if (action === 'toggle-history-news') {
    const newsKey = target.getAttribute('data-news-key');
    if (expandedHistoryNews.has(newsKey)) {
      expandedHistoryNews.delete(newsKey);
    } else {
      expandedHistoryNews.add(newsKey);
    }
    renderHistoryView();
    return;
  }

  if (action === 'history-open-data-export') {
    openHistoryDataExportModal(target.getAttribute('data-survey-id'));
  }
}

function openHistoryDataExportModal(surveyId) {
  const survey = appState.surveys.find((item) => item.id === surveyId);
  if (!survey) return;

  collectPendingParticipantGazeData();
  const hasGazeData = Array.isArray(survey.participantResults) && survey.participantResults.length > 0;
  const disabledExportClass = hasGazeData
    ? ''
    : ' opacity-60 cursor-not-allowed';
  const disabledExportAttr = hasGazeData ? '' : 'disabled';

  const overlay = document.createElement('div');
  overlay.className = 'fixed inset-0 bg-black/40 z-[2200] flex items-center justify-center px-4';
  overlay.innerHTML = `
    <div class="w-full max-w-md bg-white rounded-lg shadow-xl border border-gray-200 p-5">
      <div class="flex items-start justify-between gap-4 mb-5">
        <h2 class="text-lg font-bold text-gray-900">${escapeHtml(t('export.title'))}</h2>
        <button type="button" data-action="close-export-modal" class="text-gray-400 hover:text-gray-700">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <span class="block text-xs font-bold uppercase text-gray-400 mb-2">${escapeHtml(t('export.inviteCode'))}</span>
        <span class="font-mono text-lg font-bold text-gray-900">${escapeHtml(survey.inviteCode || t('export.noInviteCode'))}</span>
      </div>
      ${hasGazeData ? '' : `
        <div class="mt-4 border border-dashed border-gray-300 rounded-lg bg-gray-50 p-4 text-center">
          <p class="text-sm font-semibold text-gray-900">${escapeHtml(t('export.noGaze'))}</p>
        </div>
      `}
      <div class="flex flex-wrap justify-end gap-2 mt-5">
        <button type="button" data-action="history-export-json" data-survey-id="${escapeHtml(survey.id)}" ${disabledExportAttr} class="bg-sky-500 hover:bg-sky-600 text-white text-xs font-bold px-4 py-2 rounded-md transition-colors${disabledExportClass}">
          ${escapeHtml(t('export.exportJson'))}
        </button>
        <button type="button" data-action="history-export-csv" data-survey-id="${escapeHtml(survey.id)}" ${disabledExportAttr} class="bg-white border border-gray-300 text-gray-700 text-xs font-bold px-4 py-2 rounded-md hover:bg-gray-50 transition-colors${disabledExportClass}">
          ${escapeHtml(t('export.exportCsv'))}
        </button>
        <button type="button" data-action="close-export-modal" class="bg-white border border-gray-300 text-gray-700 text-xs font-bold px-4 py-2 rounded-md hover:bg-gray-50 transition-colors">
          ${escapeHtml(t('export.close'))}
        </button>
      </div>
    </div>
  `;

  overlay.addEventListener('click', async (event) => {
    const target = event.target.closest('[data-action]');

    if (event.target === overlay || target?.getAttribute('data-action') === 'close-export-modal') {
      overlay.remove();
      return;
    }

    if (!target) return;

    const action = target.getAttribute('data-action');
    if (action === 'history-export-json' || action === 'history-export-csv') {
      target.disabled = true;
      target.classList.add('opacity-60', 'cursor-not-allowed');
      collectPendingParticipantGazeData();
      await syncGazeDataFromServer({ notify: false });
      exportSurveyData(
        target.getAttribute('data-survey-id'),
        action === 'history-export-json' ? 'json' : 'csv'
      );
      target.disabled = false;
      target.classList.remove('opacity-60', 'cursor-not-allowed');
    }
  });

  document.body.appendChild(overlay);
  lucide.createIcons({ scope: overlay });
}

function getGazeResultSampleCount(result) {
  if (Number.isFinite(Number(result.sampleCount))) {
    return Number(result.sampleCount);
  }
  return Array.isArray(result.gazeData) ? result.gazeData.length : 0;
}

function getSurveyGazeSampleCount(survey) {
  return (survey.participantResults || []).reduce((count, result) => (
    count + getGazeResultSampleCount(result)
  ), 0);
}

function getExportableSurveys() {
  return appState.surveys
    .filter((survey) => Array.isArray(survey.participantResults) && survey.participantResults.length > 0)
    .slice()
    .sort((a, b) => new Date(b.completedAt || b.createdAt) - new Date(a.completedAt || a.createdAt));
}

function renderDataExportView() {
  const dataExportView = document.getElementById('data-export-view');
  if (!dataExportView) return;

  const exportableSurveys = getExportableSurveys();

  if (exportableSurveys.length === 0) {
    dataExportView.innerHTML = `
      <header class="mb-8 flex flex-col md:flex-row md:items-start md:justify-between gap-4">
        <div>
          <h1 class="text-2xl font-semibold mb-2">${escapeHtml(t('export.title'))}</h1>
          <p class="text-sm text-gray-500">${escapeHtml(t('export.emptySubtitle'))}</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <button type="button" data-action="export-data-summary" disabled class="bg-sky-200 text-white text-xs font-bold px-4 py-2 rounded-md cursor-not-allowed">
            ${escapeHtml(t('export.button'))}
          </button>
          <button type="button" data-action="refresh-gaze-data" class="bg-white border border-gray-300 text-gray-700 text-xs font-bold px-4 py-2 rounded-md hover:bg-gray-50 transition-colors">
            ${escapeHtml(t('export.refresh'))}
          </button>
        </div>
      </header>
      <div class="grid grid-cols-1 gap-4">
        <section class="border border-dashed border-gray-300 rounded-lg bg-gray-50 p-6">
          <p class="text-sm font-semibold text-gray-900">${escapeHtml(t('export.gazeEndpoint'))}</p>
          <p class="text-sm text-gray-500 mt-2">${escapeHtml(t('export.noGaze'))}</p>
          <p class="text-sm text-gray-500 mt-1">${escapeHtml(t('export.gazeSubmit', { endpoint: '/api/gaze-data' }))}</p>
        </section>
      </div>
    `;
    return;
  }

  dataExportView.innerHTML = `
    <header class="mb-8 flex flex-col md:flex-row md:items-start md:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-semibold mb-2">${escapeHtml(t('export.title'))}</h1>
        <p class="text-sm text-gray-500">${escapeHtml(t('export.subtitle'))}</p>
      </div>
      <div class="flex flex-wrap gap-2">
        <button type="button" data-action="export-data-summary" class="bg-sky-500 hover:bg-sky-600 text-white text-xs font-bold px-4 py-2 rounded-md transition-colors">
          ${escapeHtml(t('export.button'))}
        </button>
        <button type="button" data-action="refresh-gaze-data" class="bg-white border border-gray-300 text-gray-700 text-xs font-bold px-4 py-2 rounded-md hover:bg-gray-50 transition-colors">
          ${escapeHtml(t('export.refresh'))}
        </button>
      </div>
    </header>
    <div class="grid grid-cols-1 gap-4 mb-5">
      <section class="border border-gray-200 rounded-lg bg-white p-5 shadow-sm">
        <p class="text-sm font-semibold text-gray-900">${escapeHtml(t('export.gazeEndpoint'))}</p>
        <p class="text-sm text-gray-500 mt-2">${escapeHtml(t('export.gazeSubmitComplete', { endpoint: '/api/gaze-data' }))}</p>
      </section>
    </div>
    <div class="space-y-5">
      ${exportableSurveys.map((survey) => `
        <article class="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
          <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4">
            <div>
              <h2 class="text-lg font-bold text-black">${escapeHtml(survey.title)}</h2>
              <p class="text-xs text-gray-500 mt-1">
                ${escapeHtml(t('export.completed', { date: formatSurveyDate(survey.completedAt || survey.createdAt) }))}
              </p>
            </div>
            <div class="flex flex-wrap gap-2">
              <button type="button" data-action="export-json" data-survey-id="${escapeHtml(survey.id)}" class="bg-sky-500 hover:bg-sky-600 text-white text-xs font-bold px-4 py-2 rounded-md transition-colors">
                ${escapeHtml(t('export.exportJson'))}
              </button>
              <button type="button" data-action="export-csv" data-survey-id="${escapeHtml(survey.id)}" class="bg-white border border-gray-300 text-gray-700 text-xs font-bold px-4 py-2 rounded-md hover:bg-gray-50 transition-colors">
                ${escapeHtml(t('export.exportCsv'))}
              </button>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-5">
            <div class="bg-gray-50 rounded-lg p-4">
              <span class="block text-xl font-bold text-gray-900">${survey.participantResults.length}</span>
              <span class="text-xs font-semibold text-gray-500 uppercase">${escapeHtml(t('profile.participantResults'))}</span>
            </div>
            <div class="bg-gray-50 rounded-lg p-4">
              <span class="block text-xl font-bold text-gray-900">${getSurveyGazeSampleCount(survey).toLocaleString()}</span>
              <span class="text-xs font-semibold text-gray-500 uppercase">${escapeHtml(t('export.gazeSamples'))}</span>
            </div>
            <div class="bg-gray-50 rounded-lg p-4">
              <span class="block text-xl font-bold text-gray-900">${survey.news.length}</span>
              <span class="text-xs font-semibold text-gray-500 uppercase">${escapeHtml(t('export.newsItems'))}</span>
            </div>
          </div>
          <div class="mt-5 border-t border-gray-100 pt-4 space-y-2">
            ${survey.participantResults.map((result) => `
              <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-1 text-sm">
                <span class="font-semibold text-gray-900">${escapeHtml(result.participantLabel || result.participantId || result.id)}</span>
                <span class="text-xs text-gray-500">
                  ${escapeHtml(t('export.samplesClosed', {
                    samples: getGazeResultSampleCount(result).toLocaleString(),
                    date: formatSurveyDate(result.closedAt)
                  }))}
                </span>
              </div>
            `).join('')}
          </div>
        </article>
      `).join('')}
    </div>
  `;
}

function getSurveyExportPayload(survey) {
  return {
    id: survey.id,
    title: survey.title,
    status: survey.status,
    inviteCode: survey.inviteCode,
    createdAt: survey.createdAt,
    publishedAt: survey.publishedAt,
    completedAt: survey.completedAt,
    exportReady: survey.exportReady,
    news: survey.news,
    participantResults: survey.participantResults || []
  };
}

function slugifyFilename(value) {
  return String(value || 'survey')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '') || 'survey';
}

function downloadTextFile(filename, content, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function csvCell(value) {
  const text = String(value ?? '');
  return `"${text.replace(/"/g, '""')}"`;
}

function getSampleValue(sample, keys) {
  for (const key of keys) {
    if (sample && sample[key] !== undefined && sample[key] !== null) {
      return sample[key];
    }
  }
  return '';
}

function convertSurveyGazeDataToCsv(survey) {
  const rows = [[
    'surveyId',
    'surveyTitle',
    'inviteCode',
    'participantId',
    'participantLabel',
    'resultId',
    'startedAt',
    'closedAt',
    'receivedAt',
    'qualityScore',
    'sampleIndex',
    'timestamp',
    'x',
    'y',
    'confidence',
    'newsIndex',
    'version'
  ]];

  (survey.participantResults || []).forEach((result) => {
    (result.gazeData || []).forEach((sample, index) => {
      rows.push([
        survey.id,
        survey.title,
        result.inviteCode,
        result.participantId,
        result.participantLabel,
        result.id,
        result.startedAt,
        result.closedAt,
        result.receivedAt,
        result.qualityScore,
        index,
        getSampleValue(sample, ['timestamp', 'time', 't']),
        getSampleValue(sample, ['x', 'gazeX', 'clientX', 'screenX']),
        getSampleValue(sample, ['y', 'gazeY', 'clientY', 'screenY']),
        getSampleValue(sample, ['confidence', 'score']),
        getSampleValue(sample, ['newsIndex', 'news_index']),
        getSampleValue(sample, ['version', 'variant'])
      ]);
    });
  });

  return rows.map((row) => row.map(csvCell).join(',')).join('\n');
}

function exportSurveyData(surveyId, format) {
  const survey = appState.surveys.find((item) => item.id === surveyId);
  if (!survey) return;

  const baseFilename = `${slugifyFilename(survey.title)}-gaze-data`;
  if (format === 'json') {
    downloadTextFile(
      `${baseFilename}.json`,
      JSON.stringify(getSurveyExportPayload(survey), null, 2),
      'application/json'
    );
    return;
  }

  downloadTextFile(
    `${baseFilename}.csv`,
    convertSurveyGazeDataToCsv(survey),
    'text/csv'
  );
}

function handleDataExportClick(e) {
  const target = e.target.closest('[data-action]');
  if (!target) return;

  const action = target.getAttribute('data-action');
  if (action === 'refresh-gaze-data') {
    syncGazeDataFromServer({ notify: false });
    collectPendingParticipantGazeData();
    renderDataExportView();
    return;
  }

  if (action === 'export-data-summary') {
    const exportableSurvey = getExportableSurveys()[0];
    if (exportableSurvey) {
      exportSurveyData(exportableSurvey.id, 'json');
    }
    return;
  }

  if (action === 'export-json' || action === 'export-csv') {
    exportSurveyData(
      target.getAttribute('data-survey-id'),
      action === 'export-json' ? 'json' : 'csv'
    );
  }
}

function handleProfileClick(e) {
  const target = e.target.closest('[data-action]');
  if (!target) return;

  if (target.getAttribute('data-action') === 'profile-sign-out') {
    handleResearcherSignOut();
  }
}

async function renderResultsView() {
  const resultsView = ensureResultsView();
  if (!resultsView) return;

  resultsView.innerHTML = `
    <header class="mb-8">
      <h1 class="text-2xl font-semibold mb-2">${escapeHtml(t('results.title'))}</h1>
      <p class="text-sm text-gray-500">${escapeHtml(t('results.subtitle'))}</p>
    </header>
    <div id="results-loading" class="text-center py-12 text-gray-400">
      <div class="text-2xl mb-3">...</div>
      <p class="text-sm">${escapeHtml(t('results.loading'))}</p>
    </div>
    <div id="results-list" class="hidden space-y-3"></div>
    <div id="results-empty" class="hidden text-center py-16">
      <p class="text-sm font-semibold text-gray-500">${escapeHtml(t('results.emptyTitle'))}</p>
      <p class="text-xs text-gray-400 mt-1">${escapeHtml(t('results.emptySubtitle'))}</p>
    </div>
  `;

  try {
    const response = await fetch('/api/study-sessions');
    const data = await response.json();
    const loading = document.getElementById('results-loading');
    if (loading) {
      loading.classList.add('hidden');
    }

    const sessions = data && data.success && Array.isArray(data.sessions) ? data.sessions : [];
    if (sessions.length === 0) {
      const empty = document.getElementById('results-empty');
      if (empty) {
        empty.classList.remove('hidden');
      }
      return;
    }

    const groupedSessions = sessions.reduce((groups, session) => {
      const participantId = session.participantId || 'unknown';
      if (!groups[participantId]) {
        groups[participantId] = [];
      }
      groups[participantId].push(session);
      return groups;
    }, {});

    const groups = Object.values(groupedSessions).map((participantSessions) => ({
      participantId: participantSessions[0].participantId || 'unknown',
      latestSession: participantSessions[0],
      sessionCount: participantSessions.length,
      totalSizeKb: participantSessions.reduce((sum, session) => sum + (Number(session.fileSizeKb) || 0), 0)
    }));

    const list = document.getElementById('results-list');
    if (!list) return;

    list.classList.remove('hidden');
    list.innerHTML = groups.map((group) => {
      const session = group.latestSession;
      const initials = (group.participantId || '??').slice(0, 2).toUpperCase();
      const filename = session.filename || '';
      const latestLabel = session.completedAt
        ? formatSurveyDate(session.completedAt)
        : (session.dateLabel || 'Unknown date');
      const totalSize = group.totalSizeKb > 0
        ? `${Math.round(group.totalSizeKb).toLocaleString()} KB data`
        : 'data ready';
      const viewerUrl = `/viewer?autoload=${encodeURIComponent(filename)}`;

      return `
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 p-4 bg-gray-50 border border-gray-200 rounded-lg hover:bg-white hover:border-gray-300 transition-all">
          <div class="flex items-center gap-4 min-w-0">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-sky-400 to-indigo-500 flex items-center justify-center text-white font-bold text-sm shrink-0">
              ${escapeHtml(initials)}
            </div>
            <div class="min-w-0">
              <div class="flex flex-wrap items-center gap-2">
                <span class="font-semibold text-sm text-gray-900">${escapeHtml(t('results.participant', { id: group.participantId }))}</span>
                <span class="text-xs font-semibold text-sky-600 bg-sky-50 border border-sky-200 px-2 py-0.5 rounded-full">${escapeHtml(t('results.sessions', { count: group.sessionCount }))}</span>
              </div>
              <div class="text-xs text-gray-500">${escapeHtml(t('results.latest', { date: latestLabel, size: totalSize }))}</div>
            </div>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <a href="/api/study-data/${encodeURIComponent(filename)}" download="${escapeHtml(filename)}"
               class="bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 text-xs font-bold px-3 py-2 rounded-md transition-colors whitespace-nowrap">
              ${escapeHtml(t('results.downloadJson'))}
            </a>
            <a href="${escapeHtml(viewerUrl)}" target="_blank" rel="noopener"
               class="bg-gray-900 hover:bg-black text-white text-xs font-bold px-4 py-2 rounded-md transition-colors whitespace-nowrap">
              ${escapeHtml(t('results.viewAnalysis'))} &rarr;
            </a>
          </div>
        </div>
      `;
    }).join('');
  } catch (error) {
    const loading = document.getElementById('results-loading');
    if (loading) {
      loading.innerHTML = `
        <p class="text-sm font-medium text-red-500">${escapeHtml(t('results.loadError'))}</p>
        <p class="text-xs text-gray-400 mt-1">${escapeHtml(String(error && error.message ? error.message : error))}</p>
      `;
    }
  }
}

function showEditorView() {
  const mainWorkspace = getMainWorkspace();
  const profileView = ensureProfileView();
  const historyView = ensureHistoryView();
  const dataExportView = ensureDataExportView();
  const resultsView = ensureResultsView();

  if (mainWorkspace) {
    Array.from(mainWorkspace.children).forEach((child) => {
      if (child === profileView || child === historyView || child === dataExportView || child === resultsView) {
        child.classList.add('hidden');
      } else {
        child.classList.remove('hidden');
      }
    });
  }

  setActiveNavItem('editor');
  renderAll();
}

function showHistoryView() {
  saveAppStateToLocalStorage();
  renderHistoryView();

  const mainWorkspace = getMainWorkspace();
  const profileView = ensureProfileView();
  const historyView = ensureHistoryView();
  const dataExportView = ensureDataExportView();
  const resultsView = ensureResultsView();

  if (mainWorkspace) {
    Array.from(mainWorkspace.children).forEach((child) => {
      if (child === historyView) {
        child.classList.remove('hidden');
      } else {
        child.classList.add('hidden');
      }
    });
  }

  setActiveNavItem('history');
}

function showProfileView() {
  saveAppStateToLocalStorage();
  renderProfileView();

  const mainWorkspace = getMainWorkspace();
  const profileView = ensureProfileView();
  const resultsView = ensureResultsView();

  if (mainWorkspace) {
    Array.from(mainWorkspace.children).forEach((child) => {
      if (child === profileView) {
        child.classList.remove('hidden');
      } else {
        child.classList.add('hidden');
      }
    });
  }

  setActiveNavItem('profile');
}

function showDataExportView() {
  saveAppStateToLocalStorage();
  collectPendingParticipantGazeData();
  const dataExportView = ensureDataExportView();
  syncGazeDataFromServer({ notify: false });
  renderDataExportView();

  const mainWorkspace = getMainWorkspace();
  const profileView = ensureProfileView();
  const historyView = ensureHistoryView();
  const resultsView = ensureResultsView();

  if (mainWorkspace) {
    Array.from(mainWorkspace.children).forEach((child) => {
      if (child === dataExportView) {
        child.classList.remove('hidden');
      } else {
        child.classList.add('hidden');
      }
    });
  }

  if (historyView) {
    historyView.classList.add('hidden');
  }

  if (profileView) {
    profileView.classList.add('hidden');
  }

  if (resultsView) {
    resultsView.classList.add('hidden');
  }

  setActiveNavItem('dataExport');
}

function showResultsView() {
  saveAppStateToLocalStorage();
  renderResultsView();

  const mainWorkspace = getMainWorkspace();
  const resultsView = ensureResultsView();

  if (mainWorkspace) {
    Array.from(mainWorkspace.children).forEach((child) => {
      if (child === resultsView) {
        child.classList.remove('hidden');
      } else {
        child.classList.add('hidden');
      }
    });
  }

  setActiveNavItem('results');
}

function bindNewSurveyNavigation() {
  const newSurveyNavItem = getNavItemByKey('editor');

  if (newSurveyNavItem) {
    newSurveyNavItem.addEventListener('click', showEditorView);
  }
}

function bindProfileNavigation() {
  const profileNavItem = getNavItemByKey('profile');

  if (profileNavItem) {
    profileNavItem.addEventListener('click', showProfileView);
  }
}

function bindHistoryNavigation() {
  const historyNavItem = getNavItemByKey('history');

  if (historyNavItem) {
    historyNavItem.addEventListener('click', showHistoryView);
  }
}

function bindDataExportNavigation() {
  const dataExportNavItem = getNavItemByKey('dataExport');

  if (dataExportNavItem) {
    dataExportNavItem.addEventListener('click', showDataExportView);
  }
}

// DOM 获取 (更新版)
function bindResultsNavigation() {
  const resultsNavItem = getNavItemByKey('results');

  if (resultsNavItem) {
    resultsNavItem.addEventListener('click', showResultsView);
  }
}

const tabs = document.querySelectorAll('.version-tab');
const newsTabsContainer = document.getElementById('news-tabs-container');
const noSurveyNotice = document.getElementById('no-survey-notice');
const btnCreateSurveyEmptyState = document.getElementById('btn-create-survey-empty-state');
const previewNewsIndicator = document.getElementById('preview-news-indicator');
const inputNewsLink = document.getElementById('input-news-link');
const btnFetchNews = document.getElementById('btn-fetch-news');
const inputPlatform = document.getElementById('input-platform');
const previewContainer = document.getElementById('preview-container');
const previewBadgeName = document.getElementById('preview-platform-name');
const inputQuestionEnabled = document.getElementById('input-question-enabled');
const questionBlockControls = document.getElementById('question-block-controls');
const inputQuestionType = document.getElementById('input-question-type');
const inputQuestionText = document.getElementById('input-question-text');
const questionOptionsList = document.getElementById('question-options-list');
const btnAddQuestionOption = document.getElementById('btn-add-question-option');
const inputQuestionRequired = document.getElementById('input-question-required');
const inputSourceLocale = document.getElementById('input-source-locale');
const targetLocaleInputs = document.querySelectorAll('[data-target-locale]');
const btnGenerateTranslations = document.getElementById('btn-generate-translations');
const translationStatusList = document.getElementById('translation-status-list');

const imageUploadInput = document.getElementById('image-upload-input');
const avatarUploadInput = document.getElementById('avatar-upload-input');
const iconPickerModal = document.getElementById('icon-picker-modal');
const iconGrid = document.getElementById('icon-grid');
const closeIconPicker = document.getElementById('close-icon-picker');

let lastNoSurveyEditWarningAt = 0;

function showNoSurveyEditWarning() {
  const now = Date.now();
  if (now - lastNoSurveyEditWarningAt < 500) {
    return;
  }

  lastNoSurveyEditWarningAt = now;
  alert(t('alert.createSurveyBeforeEditing'));
}

function getClosestElement(target) {
  if (!target) return null;
  if (target.nodeType === Node.ELEMENT_NODE) return target;
  return target.parentElement || null;
}

function isCreateSurveyControl(target) {
  const element = getClosestElement(target);
  return Boolean(element?.closest('#btn-create-new-survey, #btn-create-survey-empty-state'));
}

function isNoSurveyEditorTarget(target) {
  const element = getClosestElement(target);
  if (!element || getCurrentSurvey() || isCreateSurveyControl(element)) {
    return false;
  }

  return Boolean(element.closest([
    '#news-tabs-container',
    '#input-news-link',
    '#btn-fetch-news',
    '.version-tab',
    '#input-platform',
    '#question-block-editor',
    '#translation-editor',
    '#btn-generate-code',
    '#btn-publish-survey',
    '#preview-container',
    '#preview-platform-name',
    '#preview-news-indicator'
  ].join(', ')));
}

function handleNoSurveyEditorInteraction(event) {
  if (!isNoSurveyEditorTarget(event.target)) {
    return;
  }

  event.preventDefault();
  event.stopPropagation();
  event.stopImmediatePropagation();

  if (event.type === 'focusin' && typeof event.target.blur === 'function') {
    event.target.blur();
  }

  showNoSurveyEditWarning();
}

function bindNoSurveyEditGuard() {
  const mainWorkspace = getMainWorkspace();
  if (!mainWorkspace || mainWorkspace.dataset.noSurveyGuardBound === 'true') {
    return;
  }

  mainWorkspace.dataset.noSurveyGuardBound = 'true';
  ['pointerdown', 'click', 'focusin', 'keydown'].forEach((eventName) => {
    mainWorkspace.addEventListener(eventName, handleNoSurveyEditorInteraction, true);
  });
}

// 可选图标库 (包含额外的形状和常用功能图标)
const availableIcons = [
  'heart', 'message-circle', 'send', 'bookmark', 'more-horizontal', 
  'thumbs-up', 'message-square', 'share-2', 'repeat-2', 'badge-check',
  'bar-chart-2', 'play-circle', 'forward', 'music', 'user', 'plus',
  'x', 'check', 'alert-circle', 'info', 'settings', 'bell', 'search',
  'camera', 'image', 'video', 'link', 'hash', 'at-sign', 'mail',
  'circle', 'square', 'triangle', 'star', 'flag', 'shield', 'lock', 
  'unlock', 'eye', 'eye-off', 'trash-2', 'edit-3', 'download', 'upload',
  'external-link', 'refresh-cw', 'trending-up', 'map-pin', 'calendar', 'clock'
];

// 多平台 UI 模板 (更新：支持动态渲染操作按钮及交互)
// --- 渲染模板 ---

// 辅助函数：为元素添加移除功能包装
const withRemoval = (content, key, data, extraClasses = '', aspectClass = '') => {
  const isHidden = data.hiddenElements[key];
  const positionClass = /\b(absolute|fixed|relative|sticky)\b/.test(extraClasses) ? '' : 'relative';

  // 对于新闻图片，如果被隐藏，返回占位符
  if (isHidden && key === 'image') {
    return `
      <div class="group ${positionClass} ${extraClasses}" data-editable-container="${key}">
        <div class="image-placeholder w-full ${aspectClass || 'aspect-square'} flex items-center justify-center bg-gray-50 border border-dashed border-gray-200 text-gray-300">
           <i data-lucide="image-off" class="w-10 h-10"></i>
        </div>
        <div class="remove-element-btn !opacity-100" data-action="restore-element" data-key="${key}" title="Restore Element">
          <i data-lucide="plus" class="w-2.5 h-2.5"></i>
        </div>
      </div>
    `;
  }

  if (isHidden) return '';
  
  return `
    <div class="group ${positionClass} ${extraClasses}" data-editable-container="${key}">
      ${content}
      <div class="remove-element-btn" data-action="remove-element" data-key="${key}">
        <i data-lucide="x" class="w-2.5 h-2.5"></i>
      </div>
    </div>
  `;
};

function renderQuestionBlock(data, theme = 'light') {
  const questionBlock = normalizeQuestionBlock(data.questionBlock);
  if (!questionBlock.enabled) {
    return '';
  }

  const isDark = theme === 'dark';
  const choiceType = questionBlock.type === 'multiple' ? 'checkbox' : 'radio';
  const wrapperClass = isDark
    ? 'mt-3 rounded-xl bg-black/55 border border-white/20 p-3 backdrop-blur-sm text-white'
    : 'mt-3 rounded-lg border border-gray-200 bg-gray-50 p-3 text-gray-900';
  const labelClass = isDark ? 'text-[11px] text-white/60' : 'text-[11px] text-gray-500';
  const optionClass = isDark
    ? 'flex items-center gap-2 rounded-lg border border-white/15 bg-white/10 px-3 py-2 text-xs text-white'
    : 'flex items-center gap-2 rounded-md border border-gray-200 bg-white px-3 py-2 text-xs text-gray-700';

  return `
    <div class="${wrapperClass}">
      <div class="flex items-start justify-between gap-3 mb-2">
        <p class="text-sm font-bold leading-snug">${escapeHtml(questionBlock.questionText)}</p>
        ${questionBlock.required ? `<span class="${labelClass} font-bold uppercase">${escapeHtml(t('question.requiredShort'))}</span>` : ''}
      </div>
      <div class="space-y-2">
        ${questionBlock.options.map((option) => `
          <label class="${optionClass}">
            <input type="${choiceType}" disabled class="w-3.5 h-3.5" />
            <span>${escapeHtml(option.label)}</span>
          </label>
        `).join('')}
      </div>
    </div>
  `;
}

const templates = {
  instagram: (data) => `
    <div class="bg-white border border-gray-200 rounded-lg shadow-sm w-full overflow-hidden">
      <div class="flex items-center justify-between p-3 border-b border-gray-100">
        <div class="flex items-center space-x-3">
          ${withRemoval(`
            <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-yellow-400 to-fuchsia-600 p-0.5" data-editable data-editable-type="avatar">
              <div class="w-full h-full rounded-full bg-white p-0.5">
                <div class="w-full h-full rounded-full bg-gray-200 overflow-hidden">
                  <img src="${data.avatar}" alt="avatar" />
                </div>
              </div>
            </div>
          `, 'avatar', data)}
          <div class="flex flex-col">
            ${withRemoval(`<span class="text-sm font-semibold cursor-pointer" data-editable data-editable-type="text" data-key="username">${data.username}</span>`, 'username', data)}
            ${withRemoval(`<span class="text-xs text-gray-500 cursor-pointer" data-editable data-editable-type="text" data-key="location">${data.location}</span>`, 'location', data)}
          </div>
        </div>
        ${withRemoval(`<i data-lucide="${data.icons.more}" class="text-gray-600 cursor-pointer w-5 h-5" data-editable data-editable-type="icon" data-key="more"></i>`, 'more-icon', data)}
      </div>
      
      ${withRemoval(`
        <div class="aspect-square bg-gray-100 flex items-center justify-center relative group overflow-hidden cursor-pointer" data-editable data-editable-type="image">
          ${data.image 
            ? `<img src="${data.image}" class="w-full h-full object-cover" alt="News Image" />`
            : `<div class="flex flex-col items-center text-gray-400">
                 <i data-lucide="image" class="w-12 h-12 mb-2"></i>
                 <span class="text-xs font-medium">Click to upload news image</span>
               </div>`
          }
        </div>
      `, 'image', data)}
      <div class="p-3">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center space-x-4">
            ${data.actionButtons.map((btn, index) => `
              <div class="relative group/btn" data-editable-container="action-button-${index}">
                <i data-lucide="${btn.icon}" class="w-6 h-6 hover:text-gray-500 cursor-pointer" data-editable data-editable-type="action-button" data-index="${index}"></i>
                <div class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-4 h-4 flex items-center justify-center opacity-0 group-hover/btn:opacity-100 cursor-pointer transition-opacity" data-action="remove-button" data-index="${index}">
                  <i data-lucide="x" class="w-2.5 h-2.5"></i>
                </div>
              </div>
            `).join('')}
            <div class="w-6 h-6 border-2 border-dashed border-gray-300 rounded-md flex items-center justify-center text-gray-400 hover:border-gray-500 hover:text-gray-500 cursor-pointer transition-all" data-action="add-button">
              <i data-lucide="plus" class="w-4 h-4"></i>
            </div>
          </div>
          ${withRemoval(`<i data-lucide="${data.icons.save}" class="w-6 h-6 hover:text-gray-500 cursor-pointer" data-editable data-editable-type="icon" data-key="save"></i>`, 'save-icon', data)}
        </div>
        <div class="text-sm font-semibold mb-2">
          ${withRemoval(`
            <span class="cursor-pointer" data-editable data-editable-type="text" data-key="likes">${data.likes.toLocaleString()}</span> 
            <span class="cursor-pointer" data-editable data-editable-type="text" data-key="likesLabel">${data.likesLabel}</span>
          `, 'likes', data)}
        </div>
        <div class="text-sm leading-relaxed mb-2">
          ${!data.hiddenElements['username'] ? `<span class="font-semibold mr-2">${data.username}</span>` : ''}
          ${withRemoval(`<span class="cursor-pointer" data-editable data-editable-type="text" data-key="caption">${data.caption}</span>`, 'caption', data)} 
        </div>
        ${withRemoval(`
          <div class="text-sm text-gray-500 cursor-pointer">
            ${t('post.viewAllComments', {
              count: `<span data-editable data-editable-type="text" data-key="comments">${data.comments.toLocaleString()}</span>`
            })}
          </div>
        `, 'comments', data)}
        ${withRemoval(`<div class="text-[10px] text-gray-400 mt-2 uppercase cursor-pointer" data-editable data-editable-type="text" data-key="timeLabel">${data.timeLabel}</div>`, 'timeLabel', data)}
        ${renderQuestionBlock(data)}
      </div>
    </div>
  `,
  facebook: (data) => `
    <div class="bg-white border border-gray-200 rounded-xl shadow-sm w-full">
      <div class="p-4 flex items-center space-x-2">
        ${withRemoval(`
          <div class="w-10 h-10 rounded-full bg-gray-200 overflow-hidden shrink-0 cursor-pointer" data-editable data-editable-type="avatar">
             <img src="${data.avatar}" />
          </div>
        `, 'avatar', data)}
        <div>
          ${withRemoval(`<p class="font-bold text-sm leading-tight text-gray-900 cursor-pointer" data-editable data-editable-type="text" data-key="username">${data.username}</p>`, 'username', data)}
          <p class="text-xs text-gray-500 flex items-center">
            ${withRemoval(`<span class="cursor-pointer" data-editable data-editable-type="text" data-key="timeLabel">${data.timeLabel}</span>`, 'timeLabel', data)} · 
            <i data-lucide="globe" class="w-3 h-3 ml-1"></i>
          </p>
        </div>
      </div>
      <div class="px-4 pb-3 text-sm text-gray-800">
         ${withRemoval(`<span class="cursor-pointer" data-editable data-editable-type="text" data-key="caption">${data.caption}</span>`, 'caption', data)}
       </div>
       ${withRemoval(`
         <div class="w-full aspect-video bg-gray-100 flex flex-col items-center justify-center border-y border-gray-200 text-gray-400 overflow-hidden cursor-pointer" data-editable data-editable-type="image">
           ${data.image
             ? `<img src="${data.image}" class="w-full h-full object-cover" alt="News Image" />`
             : `<i data-lucide="image" class="w-12 h-12 mb-2 opacity-50"></i>
                <span class="text-sm">[Click to Upload News Image]</span>`
           }
         </div>
       `, 'image', data)}
       <div class="px-4 pb-3">${renderQuestionBlock(data)}</div>
       <div class="px-4 py-2 flex justify-between items-center text-xs text-gray-500 border-b border-gray-200">
        <div class="flex items-center">
          ${withRemoval(`
            <div class="bg-blue-500 text-white rounded-full p-1 mr-1 w-5 h-5 flex items-center justify-center" data-editable data-editable-type="icon" data-key="like">
              <i data-lucide="thumbs-up" class="w-3 h-3"></i>
            </div> 
            <span class="cursor-pointer" data-editable data-editable-type="text" data-key="likes">${data.likes.toLocaleString()}</span>
          `, 'likes', data, 'flex items-center')}
        </div>
        <div class="flex items-center space-x-2">
          ${withRemoval(`<span class="cursor-pointer" data-editable data-editable-type="text" data-key="comments">${data.comments.toLocaleString()}</span> ${escapeHtml(t('post.comments'))}`, 'comments', data)} · 
          ${withRemoval(`<span class="cursor-pointer" data-editable data-editable-type="text" data-key="shares">${data.shares.toLocaleString()}</span> shares`, 'shares', data)}
        </div>
      </div>
      <div class="px-2 py-1 flex justify-between items-center relative group/actions">
        ${data.actionButtons.map((btn, index) => `
          <div class="flex-1 relative group/btn" data-editable-container="action-button-${index}">
            <button class="w-full flex items-center justify-center space-x-2 py-2 text-gray-600 hover:bg-gray-100 rounded-lg text-sm font-medium">
              <i data-lucide="${btn.icon}" class="w-5 h-5 cursor-pointer" data-editable data-editable-type="action-button" data-index="${index}"></i>
              <span class="hidden sm:inline" data-editable data-editable-type="text" data-key="action-button-label" data-index="${index}">${btn.label}</span>
            </button>
            <div class="absolute top-0 right-0 bg-red-500 text-white rounded-full w-4 h-4 flex items-center justify-center opacity-0 group-hover/btn:opacity-100 cursor-pointer transition-opacity z-10" data-action="remove-button" data-index="${index}">
              <i data-lucide="x" class="w-2.5 h-2.5"></i>
            </div>
          </div>
        `).join('')}
        <div class="px-4 py-2 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center text-gray-400 hover:border-gray-500 hover:text-gray-500 cursor-pointer transition-all ml-1" data-action="add-button">
          <i data-lucide="plus" class="w-4 h-4"></i>
        </div>
      </div>
    </div>
  `,
  x: (data) => `
    <div class="bg-white border border-gray-200 shadow-sm w-full p-4">
      <div class="flex space-x-3">
        ${withRemoval(`
          <div class="w-12 h-12 rounded-full bg-gray-200 overflow-hidden shrink-0 cursor-pointer" data-editable data-editable-type="avatar">
             <img src="${data.avatar}" />
          </div>
        `, 'avatar', data)}
        <div class="flex-1">
          <div class="flex items-center text-sm">
            ${withRemoval(`<span class="font-bold text-gray-900 mr-1 cursor-pointer" data-editable data-editable-type="text" data-key="username">${data.username}</span>`, 'username', data)}
            ${withRemoval(`<i data-lucide="${data.icons.verify}" class="w-4 h-4 text-blue-500 mr-1 cursor-pointer" data-editable data-editable-type="icon" data-key="verify"></i>`, 'verify-icon', data)}
            ${withRemoval(`<span class="text-gray-500 cursor-pointer" data-editable data-editable-type="text" data-key="handle">${data.handle}</span>`, 'handle', data)}
            <span class="text-gray-500 mx-1">·</span>
            ${withRemoval(`<span class="text-gray-500 cursor-pointer" data-editable data-editable-type="text" data-key="timeLabel">${data.timeLabel}</span>`, 'timeLabel', data)}
          </div>
          <div class="mt-1 mb-3">
            ${withRemoval(`<p class="text-[15px] text-gray-900 cursor-pointer" data-editable data-editable-type="text" data-key="caption">${data.caption}</p>`, 'caption', data)}
          </div>
          ${withRemoval(`
            <div class="w-full aspect-video bg-gray-100 rounded-2xl border border-gray-200 flex flex-col items-center justify-center text-gray-400 overflow-hidden cursor-pointer" data-editable data-editable-type="image">
               ${data.image
                 ? `<img src="${data.image}" class="w-full h-full object-cover" alt="News Image" />`
                 : `<i data-lucide="image" class="w-10 h-10 mb-2 opacity-50"></i>
                    <span class="text-sm">[Click to Upload]</span>`
               }
            </div>
          `, 'image', data)}
          ${renderQuestionBlock(data)}
          <div class="flex justify-between mt-3 text-gray-500 max-w-md items-center">
            ${data.actionButtons.map((btn, index) => `
              <div class="relative group/btn flex items-center space-x-2 hover:text-blue-500 cursor-pointer" data-editable-container="action-button-${index}">
                <div class="flex items-center space-x-2" data-editable data-editable-type="action-button" data-index="${index}">
                  <i data-lucide="${btn.icon}" class="w-4 h-4"></i>
                  <span class="text-xs">${btn.id === 'like' ? data.likes.toLocaleString() : (btn.id === 'comment' ? data.comments.toLocaleString() : (btn.id === 'share' ? data.shares.toLocaleString() : ''))}</span>
                </div>
                <div class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-4 h-4 flex items-center justify-center opacity-0 group-hover/btn:opacity-100 cursor-pointer transition-opacity" data-action="remove-button" data-index="${index}">
                  <i data-lucide="x" class="w-2.5 h-2.5"></i>
                </div>
              </div>
            `).join('')}
            <div class="w-8 h-8 border-2 border-dashed border-gray-300 rounded-full flex items-center justify-center text-gray-400 hover:border-gray-500 hover:text-gray-500 cursor-pointer transition-all" data-action="add-button">
              <i data-lucide="plus" class="w-3 h-3"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  tiktok: (data) => `
     <div class="bg-black text-white w-[320px] h-[580px] rounded-xl overflow-hidden shadow-xl relative flex items-center justify-center font-sans mx-auto">
       ${withRemoval(`
        <div class="absolute inset-0 bg-gray-800 flex flex-col items-center justify-center text-gray-300 overflow-hidden cursor-pointer" data-editable data-editable-type="image">
           <div class="tiktok-image-fallback absolute inset-0 flex flex-col items-center justify-center bg-gray-800 text-gray-300">
              <i data-lucide="${data.icons.play}" class="w-16 h-16 opacity-30 mb-2" data-editable data-editable-type="icon" data-key="play"></i>
              <span class="text-sm font-medium">No image available</span>
           </div>
           ${data.image
             ? `<img src="${data.image}" class="w-full h-full object-cover opacity-80 relative z-[1]" alt="News Image" onerror="this.remove()" />`
             : ''
           }
        </div>
      `, 'image', data, 'absolute inset-0')}
       <div class="absolute right-2 bottom-20 flex flex-col items-center space-y-5 z-10">
        ${withRemoval(`
          <div class="w-12 h-12 rounded-full border-2 border-white overflow-hidden bg-gray-200 relative mb-2 cursor-pointer" data-editable data-editable-type="avatar">
             <img src="${data.avatar}" />
             <div class="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-pink-500 rounded-full w-5 h-5 flex items-center justify-center text-white text-xs font-bold border border-white">+</div>
          </div>
        `, 'avatar', data)}
        ${data.actionButtons.map((btn, index) => `
          <div class="relative group/btn flex flex-col items-center drop-shadow-md cursor-pointer" data-editable-container="action-button-${index}">
            <div data-editable data-editable-type="action-button" data-index="${index}" class="flex flex-col items-center">
              <i data-lucide="${btn.icon}" class="w-8 h-8 fill-transparent hover:fill-pink-500"></i>
              <span class="text-xs mt-1 font-semibold" data-editable data-editable-type="text" data-key="action-button-label" data-index="${index}">${btn.id === 'like' ? (data.likes >= 1000 ? (data.likes/1000).toFixed(1)+'K' : data.likes) : (btn.id === 'comment' ? (data.comments >= 1000 ? (data.comments/1000).toFixed(1)+'K' : data.comments) : (btn.id === 'share' ? (data.shares >= 1000 ? (data.shares/1000).toFixed(1)+'K' : data.shares) : btn.label))}</span>
            </div>
            <div class="absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-4 h-4 flex items-center justify-center opacity-0 group-hover/btn:opacity-100 cursor-pointer transition-opacity" data-action="remove-button" data-index="${index}">
              <i data-lucide="x" class="w-2.5 h-2.5"></i>
            </div>
          </div>
        `).join('')}
        <div class="w-8 h-8 border-2 border-dashed border-gray-400 rounded-full flex items-center justify-center text-gray-400 hover:border-white hover:text-white cursor-pointer transition-all" data-action="add-button">
          <i data-lucide="plus" class="w-4 h-4"></i>
        </div>
      </div>
      <div class="absolute bottom-4 left-4 right-16 z-10 drop-shadow-md">
        ${withRemoval(`<p class="font-bold text-[15px] mb-1 cursor-pointer" data-editable data-editable-type="text" data-key="username">${data.handle || data.username}</p>`, 'username', data)}
        ${withRemoval(`<p class="text-sm leading-snug line-clamp-2 cursor-pointer" data-editable data-editable-type="text" data-key="caption">${data.caption}</p>`, 'caption', data)}
        ${withRemoval(`
          <p class="text-sm font-medium flex items-center mt-2 cursor-pointer">
            <i data-lucide="${data.icons.music}" class="w-4 h-4 mr-2" data-editable data-editable-type="icon" data-key="music"></i> 
            <span data-editable data-editable-type="text" data-key="musicLabel">original sound - Sydney News</span>
          </p>
        `, 'music-info', data)}
        ${renderQuestionBlock(data, 'dark')}
      </div>
    </div>
  `
};

// --- 交互逻辑 ---

// 全局预览点击监听
previewContainer.addEventListener('click', (e) => {
  if (!getCurrentSurvey()) {
    return;
  }

  const target = e.target.closest('[data-editable], [data-action]');
  if (!target) return;

  const currentNews = surveyState.news[surveyState.currentNewsIndex];
  const currentData = currentNews.versions[surveyState.currentVersion];

  // 处理添加按钮
  if (target.getAttribute('data-action') === 'add-button') {
    currentData.actionButtons.push({
      id: 'custom-' + Date.now(),
      icon: 'star',
      label: 'New Button',
      active: true
    });
    renderAll();
    return;
  }

  // 处理移除按钮
  if (target.getAttribute('data-action') === 'remove-button') {
    const index = parseInt(target.getAttribute('data-index'));
    currentData.actionButtons.splice(index, 1);
    renderAll();
    return;
  }

  const type = target.getAttribute('data-editable-type');
  const key = target.getAttribute('data-key');
  const index = target.getAttribute('data-index');

  if (type === 'text') {
    handleTextEdit(target, key, currentData, index);
  } else if (type === 'icon' || type === 'action-button') {
    handleIconEdit(target, key, currentData, index);
  } else if (type === 'image') {
    imageUploadInput.click();
  } else if (type === 'avatar') {
    // 头像点击现在直接触发上传，和新闻图片一致
    avatarUploadInput.click();
  }

  // 处理元素移除
  if (target.getAttribute('data-action') === 'remove-element') {
    const key = target.getAttribute('data-key');
    currentData.hiddenElements[key] = true;
    renderAll();
    return;
  }

  // 处理元素恢复（目前仅针对图片占位符）
  if (target.getAttribute('data-action') === 'restore-element') {
    const key = target.getAttribute('data-key');
    delete currentData.hiddenElements[key];
    renderAll();
    return;
  }
});

// 处理文本编辑
function handleTextEdit(element, key, data, index = null) {
  // 获取原始值，如果是数字型字段，去掉逗号等格式化
  let originalValue = element.textContent;
  
  if (index !== null && key === 'action-button-label') {
    originalValue = data.actionButtons[index].label;
  } else if (['likes', 'comments', 'shares'].includes(key)) {
    // 尝试从 data 中直接获取原始数字，避免格式化带来的干扰
    originalValue = data[key].toString();
  }

  const input = document.createElement('textarea');
  input.className = 'edit-input-overlay';
  input.value = originalValue;
  
  // 定位
  const rect = element.getBoundingClientRect();
  input.style.top = `${rect.top + window.scrollY}px`;
  input.style.left = `${rect.left + window.scrollX}px`;
  input.style.width = `${Math.max(rect.width, 100)}px`;
  
  document.body.appendChild(input);
  input.focus();

  const save = () => {
    const newValue = input.value.trim();
    if (newValue !== originalValue) {
      if (index !== null && key === 'action-button-label') {
        data.actionButtons[index].label = newValue;
      } else if (['likes', 'comments', 'shares'].includes(key)) {
        // 处理 K/M 等单位（针对 TikTok）
        let numValue = newValue.toLowerCase();
        if (numValue.endsWith('k')) {
          data[key] = parseFloat(numValue) * 1000;
        } else if (numValue.endsWith('m')) {
          data[key] = parseFloat(numValue) * 1000000;
        } else {
          data[key] = parseInt(newValue.replace(/[^0-9.]/g, '')) || 0;
        }
      } else {
        data[key] = newValue;
      }
      renderAll();
    }
    input.remove();
  };

  input.addEventListener('blur', save);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      save();
    }
  });
}

// 处理图标编辑
let activeIconKey = null;
let activeIconIndex = null;
function handleIconEdit(element, key, data, index = null) {
  activeIconKey = key;
  activeIconIndex = index;

  const rect = element.getBoundingClientRect();
  // 确保弹窗不会超出屏幕右侧
  let left = rect.left + window.scrollX - 100;
  if (left + 240 > window.innerWidth) {
    left = window.innerWidth - 250;
  }

  iconPickerModal.style.top = `${rect.bottom + window.scrollY + 5}px`;
  iconPickerModal.style.left = `${left}px`;
  iconPickerModal.style.display = 'block';
  
  // 生成图标网格
  iconGrid.innerHTML = '';

  // 如果是头像编辑，增加一个“上传图片”的选项
  if (key === 'avatar-icon') {
    const uploadDiv = document.createElement('div');
    uploadDiv.className = 'col-span-5 mb-2';
    uploadDiv.innerHTML = `
      <button class="w-full flex items-center justify-center space-x-2 py-2 bg-blue-50 text-blue-600 rounded-lg text-xs font-bold hover:bg-blue-100 transition-colors">
        <i data-lucide="upload" class="w-4 h-4"></i>
        <span>Upload Custom Image</span>
      </button>
    `;
    uploadDiv.querySelector('button').addEventListener('click', () => {
      avatarUploadInput.click();
      iconPickerModal.style.display = 'none';
    });
    iconGrid.appendChild(uploadDiv);
  }

  availableIcons.forEach(iconName => {
    const div = document.createElement('div');
    div.className = 'icon-option';
    div.innerHTML = `<i data-lucide="${iconName}" class="w-5 h-5"></i>`;
    div.addEventListener('click', () => {
      if (activeIconIndex !== null) {
        // 处理动态按钮图标
        data.actionButtons[activeIconIndex].icon = iconName;
      } else if (activeIconKey === 'avatar-icon') {
        // 处理头像图标化
        data.avatar = `https://api.dicebear.com/7.x/shapes/svg?seed=${iconName}`;
      } else {
        // 处理固定图标
        data.icons[activeIconKey] = iconName;
      }
      iconPickerModal.style.display = 'none';
      renderAll();
    });
    iconGrid.appendChild(div);
  });

  lucide.createIcons({ scope: iconGrid });
}

closeIconPicker.addEventListener('click', () => {
  iconPickerModal.style.display = 'none';
});

// 点击外部关闭弹窗
document.addEventListener('mousedown', (e) => {
  if (iconPickerModal.style.display === 'block' && 
      !iconPickerModal.contains(e.target) && 
      !e.target.closest('[data-editable-type="icon"]')) {
    iconPickerModal.style.display = 'none';
  }
});

// 处理图片上传
imageUploadInput.addEventListener('change', (e) => {
  if (!getCurrentSurvey()) {
    imageUploadInput.value = '';
    return;
  }

  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      surveyState.news[surveyState.currentNewsIndex].versions[surveyState.currentVersion].image = event.target.result;
      renderAll();
    };
    reader.readAsDataURL(file);
  }
});

avatarUploadInput.addEventListener('change', (e) => {
  if (!getCurrentSurvey()) {
    avatarUploadInput.value = '';
    return;
  }

  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      surveyState.news[surveyState.currentNewsIndex].versions[surveyState.currentVersion].avatar = event.target.result;
      renderAll();
    };
    reader.readAsDataURL(file);
  }
});

// --- 渲染逻辑 ---
function renderNewsTabs() {
  newsTabsContainer.innerHTML = '';

  if (!getCurrentSurvey()) {
    return;
  }

  surveyState.news.forEach((news, index) => {
    const tabWrapper = document.createElement('div');
    tabWrapper.className = 'relative group';

    const tab = document.createElement('button');
    tab.className = `news-tab px-6 py-2 rounded-xl text-sm font-bold transition-all ${index === surveyState.currentNewsIndex ? 'active' : 'inactive'}`;
    tab.textContent = t('editor.newsTab', { number: index + 1 });
    tab.addEventListener('click', () => {
      surveyState.currentNewsIndex = index;
      renderAll();
    });
    
    // 删除按钮
    if (surveyState.news.length > 1) {
      const deleteBtn = document.createElement('div');
      deleteBtn.className = 'btn-delete-news flex items-center justify-center';
      deleteBtn.innerHTML = '<i data-lucide="x"></i>';
      deleteBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // 防止触发 tab 的点击事件
        surveyState.news.splice(index, 1);
        
        // 如果删除的是当前选中的新闻，或者删除后索引越界，更新 currentNewsIndex
        if (surveyState.currentNewsIndex >= surveyState.news.length) {
          surveyState.currentNewsIndex = surveyState.news.length - 1;
        } else if (index < surveyState.currentNewsIndex) {
          surveyState.currentNewsIndex--;
        }
        
        renderAll();
      });
      tab.appendChild(deleteBtn);
    }

    tabWrapper.appendChild(tab);
    newsTabsContainer.appendChild(tabWrapper);
  });

  // 添加 "+" 按钮
  const addBtn = document.createElement('button');
  addBtn.id = 'btn-add-news';
  addBtn.className = 'w-10 h-10 flex items-center justify-center rounded-xl border-2 border-dashed border-gray-300 text-gray-400 hover:border-gray-400 hover:text-gray-500 transition-all ml-2 shrink-0';
  addBtn.innerHTML = '<i data-lucide="plus" class="w-5 h-5"></i>';
  addBtn.addEventListener('click', () => {
    const currentPlatform = surveyState.news[surveyState.currentNewsIndex].versions[surveyState.currentVersion].platform;
    surveyState.news.push({
      link: '',
      versions: {
        'vA': createDefaultVersion(currentPlatform),
        'vB': createDefaultVersion(currentPlatform)
      }
    });
    surveyState.currentNewsIndex = surveyState.news.length - 1;
    renderAll();
  });
  newsTabsContainer.appendChild(addBtn);
  lucide.createIcons();
}

function getCurrentVersionData() {
  const currentNews = surveyState.news[surveyState.currentNewsIndex];
  return currentNews && currentNews.versions
    ? currentNews.versions[surveyState.currentVersion]
    : null;
}

function getCurrentQuestionBlock() {
  const currentData = getCurrentVersionData();
  if (!currentData) return null;

  currentData.questionBlock = normalizeQuestionBlock(currentData.questionBlock);
  return currentData.questionBlock;
}

function renderQuestionOptionEditor(option, index, totalOptions) {
  const label = String.fromCharCode(65 + index);
  const removeDisabled = totalOptions <= 2 ? 'disabled' : '';
  const removeClasses = totalOptions <= 2
    ? 'text-gray-300 cursor-not-allowed'
    : 'text-gray-400 hover:text-red-500';

  return `
    <div class="flex items-center gap-2">
      <span class="w-6 h-6 rounded-full bg-white border border-gray-200 flex items-center justify-center text-xs font-bold text-gray-500">${label}</span>
      <input
        type="text"
        data-question-option-index="${index}"
        value="${escapeHtml(option.label)}"
        class="flex-1 bg-white border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:border-gray-500"
      />
      <button
        type="button"
        data-action="remove-question-option"
        data-question-option-index="${index}"
        ${removeDisabled}
        class="w-8 h-8 flex items-center justify-center rounded-md ${removeClasses}"
      >
        <i data-lucide="x" class="w-4 h-4"></i>
      </button>
    </div>
  `;
}

function renderQuestionBlockEditor() {
  const questionBlock = getCurrentQuestionBlock();
  if (!questionBlock || !inputQuestionEnabled || !questionBlockControls) {
    return;
  }
  const currentData = getCurrentVersionData();
  const displayQuestionBlock = getTranslatedQuestionBlock(
    questionBlock,
    surveyState.currentNewsIndex,
    surveyState.currentVersion,
    currentData?.platform || 'instagram'
  );

  inputQuestionEnabled.checked = questionBlock.enabled;
  questionBlockControls.classList.toggle('hidden', !questionBlock.enabled);

  if (inputQuestionType) {
    inputQuestionType.value = questionBlock.type;
  }

  if (inputQuestionText && document.activeElement !== inputQuestionText) {
    inputQuestionText.value = displayQuestionBlock.questionText;
  }

  if (inputQuestionRequired) {
    inputQuestionRequired.checked = questionBlock.required;
  }

  if (questionOptionsList) {
    questionOptionsList.innerHTML = displayQuestionBlock.options
      .map((option, index) => renderQuestionOptionEditor(option, index, displayQuestionBlock.options.length))
      .join('');
    lucide.createIcons({ scope: questionOptionsList });
  }

  if (btnAddQuestionOption) {
    const isAtMax = questionBlock.options.length >= 4;
    btnAddQuestionOption.disabled = isAtMax;
    btnAddQuestionOption.classList.toggle('text-gray-300', isAtMax);
    btnAddQuestionOption.classList.toggle('cursor-not-allowed', isAtMax);
  }
}

function updateQuestionBlock(updater, shouldRenderEditor = false) {
  if (!getCurrentSurvey()) return;

  const questionBlock = getCurrentQuestionBlock();
  if (!questionBlock) return;

  updater(questionBlock);
  if (shouldRenderEditor) {
    renderQuestionBlockEditor();
  }
  renderPreview();
  saveAppStateToLocalStorage();
}

function getCurrentTranslationConfig() {
  const currentSurvey = getCurrentSurvey();
  if (!currentSurvey) return null;

  currentSurvey.translationConfig = normalizeTranslationConfig(currentSurvey.translationConfig);
  currentSurvey.translations = currentSurvey.translations && typeof currentSurvey.translations === 'object'
    ? currentSurvey.translations
    : {};
  return currentSurvey.translationConfig;
}

function renderTranslationStatus() {
  const currentSurvey = getCurrentSurvey();
  const config = getCurrentTranslationConfig();
  if (!translationStatusList || !currentSurvey || !config) return;

  if (config.targetLocales.length === 0) {
    translationStatusList.innerHTML = '<p class="text-xs text-gray-500">Select at least one target language before generating translations.</p>';
    return;
  }

  translationStatusList.innerHTML = config.targetLocales.map((locale) => {
    const translation = currentSurvey.translations[locale];
    const isReady = translation && translation.status === 'ready';
    const label = CONTENT_LOCALE_LABELS[locale] || locale;
    return `
      <div class="flex items-center justify-between gap-3 rounded-md bg-gray-50 border border-gray-100 px-3 py-2">
        <span class="text-xs font-bold text-gray-700">${escapeHtml(label)}</span>
        <span class="text-xs font-bold uppercase ${isReady ? 'text-emerald-600' : 'text-gray-400'}">${isReady ? 'Ready' : 'Not generated'}</span>
      </div>
    `;
  }).join('');
}

function renderTranslationEditor() {
  const config = getCurrentTranslationConfig();
  if (!config) return;

  if (inputSourceLocale) {
    inputSourceLocale.value = config.sourceLocale;
  }

  targetLocaleInputs.forEach((input) => {
    input.checked = config.targetLocales.includes(input.value);
    input.disabled = input.value === config.sourceLocale;
  });

  renderTranslationStatus();
}

function setDisabledState(element, disabled) {
  if (!element) return;

  element.disabled = false;
  element.classList.toggle('opacity-60', disabled);
  element.classList.toggle('cursor-not-allowed', disabled);

  if (disabled) {
    element.setAttribute('aria-disabled', 'true');
    element.dataset.noSurveyLocked = 'true';
    element.setAttribute('tabindex', '-1');

    if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
      element.readOnly = true;
    }
    return;
  }

  element.removeAttribute('aria-disabled');
  element.removeAttribute('tabindex');
  delete element.dataset.noSurveyLocked;

  if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
    element.readOnly = false;
  }
}

function updateEditorSurveyAvailability() {
  const hasSurvey = Boolean(getCurrentSurvey());
  if (noSurveyNotice) {
    noSurveyNotice.classList.toggle('hidden', hasSurvey);
  }

  [
    inputNewsLink,
    btnFetchNews,
    inputPlatform,
    inputQuestionEnabled,
    inputQuestionType,
    inputQuestionText,
    btnAddQuestionOption,
    inputQuestionRequired,
    inputSourceLocale,
    btnGenerateTranslations,
    btnGenerateCode,
    document.getElementById('btn-publish-survey')
  ].forEach((element) => setDisabledState(element, !hasSurvey));

  tabs.forEach((tab) => setDisabledState(tab, !hasSurvey));

  document.querySelectorAll('#news-tabs-container button, #question-options-list input, #question-options-list button, [data-target-locale]').forEach((element) => {
    setDisabledState(element, !hasSurvey);
  });
}

function updateTranslationConfig(updater) {
  const currentSurvey = getCurrentSurvey();
  const config = getCurrentTranslationConfig();
  if (!currentSurvey || !config) return;

  updater(config);
  currentSurvey.translationConfig = normalizeTranslationConfig(config);
  renderTranslationEditor();
  saveAppStateToLocalStorage();
}

function collectSurveyTranslationEntries(survey) {
  const entries = [
    { key: 'survey.title', text: survey.title || '' }
  ];

  (survey.news || []).forEach((news, newsIndex) => {
    Object.entries(news.versions || {}).forEach(([versionKey, version]) => {
      getPlatformVariantEntries(version).forEach(([platform, variant]) => {
        if (variant.caption) {
          entries.push({
            key: `news.${newsIndex}.${versionKey}.${platform}.caption`,
            text: variant.caption
          });
        }
        if (variant.likesLabel) {
          entries.push({
            key: `news.${newsIndex}.${versionKey}.${platform}.likesLabel`,
            text: variant.likesLabel
          });
        }
        if (variant.timeLabel) {
          entries.push({
            key: `news.${newsIndex}.${versionKey}.${platform}.timeLabel`,
            text: variant.timeLabel
          });
        }
        if (Array.isArray(variant.actionButtons)) {
          variant.actionButtons.forEach((button, buttonIndex) => {
            if (button && button.label) {
              entries.push({
                key: `news.${newsIndex}.${versionKey}.${platform}.action.${buttonIndex}.label`,
                text: button.label
              });
            }
          });
        }

        const questionBlock = normalizeQuestionBlock(variant.questionBlock);
        if (questionBlock.enabled) {
          entries.push({
            key: `news.${newsIndex}.${versionKey}.${platform}.question.text`,
            text: questionBlock.questionText
          });
          questionBlock.options.forEach((option, optionIndex) => {
            entries.push({
              key: `news.${newsIndex}.${versionKey}.${platform}.question.option.${optionIndex}`,
              text: option.label
            });
          });
        }
      });
    });
  });

  return entries.filter((entry) => entry.text.trim());
}

async function handleGenerateTranslationsClick() {
  const currentSurvey = getCurrentSurvey();
  const config = getCurrentTranslationConfig();
  if (!currentSurvey || !config) return;

  if (config.targetLocales.length === 0) {
    alert('Please select at least one target language.');
    return;
  }

  const originalText = btnGenerateTranslations ? btnGenerateTranslations.textContent : '';
  if (btnGenerateTranslations) {
    btnGenerateTranslations.disabled = true;
    btnGenerateTranslations.textContent = 'Generating...';
  }

  try {
    const response = await fetch(TRANSLATION_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        surveyId: currentSurvey.id,
        sourceLocale: config.sourceLocale,
        targetLocales: config.targetLocales,
        entries: collectSurveyTranslationEntries(currentSurvey)
      })
    });
    const result = await response.json();

    if (!response.ok || !result.success) {
      alert(result.error || 'Translation generation is not available yet.');
      return;
    }

    currentSurvey.translations = result.translations && typeof result.translations === 'object'
      ? result.translations
      : {};
    saveAppStateToLocalStorage();
    renderTranslationStatus();
  } catch (error) {
    console.error('Failed to generate translations:', error);
    alert('Translation service is unavailable. Please check the backend service.');
  } finally {
    if (btnGenerateTranslations) {
      btnGenerateTranslations.disabled = false;
      btnGenerateTranslations.textContent = originalText;
    }
  }
}

function renderEditor() {
  if (!getCurrentSurvey()) {
    inputNewsLink.value = '';
    inputPlatform.value = 'instagram';
    renderQuestionBlockEditor();
    renderInviteCode();
    updateEditorSurveyAvailability();
    return;
  }

  const currentNews = surveyState.news[surveyState.currentNewsIndex];
  const currentData = currentNews.versions[surveyState.currentVersion];
  
  inputNewsLink.value = currentNews.link || '';
  inputPlatform.value = currentData.platform;
  renderQuestionBlockEditor();
  renderTranslationEditor();
  renderInviteCode();
}

function renderPreview() {
  if (!getCurrentSurvey()) {
    previewBadgeName.textContent = '';
    previewNewsIndicator.textContent = '';
    previewBadgeName.classList.add('hidden');
    previewNewsIndicator.classList.add('hidden');
    previewContainer.innerHTML = `
      <div class="border border-dashed border-gray-300 rounded-lg bg-white p-8 text-center">
        <p class="text-sm font-semibold text-gray-900">${escapeHtml(t('editor.noSurveyTitle'))}</p>
        <p class="text-sm text-gray-500 mt-1">${escapeHtml(t('editor.noSurveyPreview'))}</p>
      </div>
    `;
    return;
  }

  const currentNews = surveyState.news[surveyState.currentNewsIndex];
  const currentData = getTranslatedVersionData(
    currentNews.versions[surveyState.currentVersion],
    surveyState.currentNewsIndex,
    surveyState.currentVersion
  );
  
  previewBadgeName.classList.remove('hidden');
  previewNewsIndicator.classList.remove('hidden');
  previewBadgeName.textContent = currentData.platform.toUpperCase();
  previewNewsIndicator.textContent = t('preview.newsIndicator', { number: surveyState.currentNewsIndex + 1 });
  
  if (templates[currentData.platform]) {
    previewContainer.innerHTML = templates[currentData.platform](currentData);
  }
  lucide.createIcons(); // 每次重新渲染 HTML 后，必须重新生成图标
}

function renderVersionTabs() {
  tabs.forEach(tab => {
    if (tab.getAttribute('data-version') === surveyState.currentVersion) {
      tab.classList.add('tab-active');
      tab.classList.remove('tab-inactive');
    } else {
      tab.classList.remove('tab-active');
      tab.classList.add('tab-inactive');
    }
  });
}

function renderInviteCode() {
  const currentSurvey = getCurrentSurvey();
  const inviteCode = currentSurvey ? currentSurvey.inviteCode : '';

  if (inviteCode) {
    displayInviteCode.textContent = inviteCode;
    displayInviteCode.classList.remove('hidden');
    btnGenerateCode.textContent = t('invite.regenerate');
  } else {
    displayInviteCode.textContent = '';
    displayInviteCode.classList.add('hidden');
    btnGenerateCode.textContent = t('invite.generate');
  }
}

function renderAll() {
  const hasSurvey = Boolean(getCurrentSurvey());
  renderSurveyTitle();
  renderVersionTabs();
  renderNewsTabs();
  renderEditor();
  renderPreview();
  updateEditorSurveyAvailability();
  if (hasSurvey) {
    saveAppStateToLocalStorage();
  }
}

// --- 事件监听绑定 ---

if (btnCreateSurveyEmptyState) {
  btnCreateSurveyEmptyState.addEventListener('click', handleNewSurveyClick);
}

// 4. 新闻链接真实抓取逻辑 (JS + Python Flask 架构)
btnFetchNews.addEventListener('click', async () => {
  if (!getCurrentSurvey()) {
    return;
  }

  const url = inputNewsLink.value.trim();
  if (!url) {
    alert(t('alert.newsLinkRequired'));
    return;
  }

  // 更新当前新闻的 link
  surveyState.news[surveyState.currentNewsIndex].link = url;
  saveAppStateToLocalStorage();

  // UI 变为加载状态
  const fetchNewsLabel = btnFetchNews.querySelector('[data-i18n]');
  const originalText = fetchNewsLabel ? fetchNewsLabel.textContent : btnFetchNews.innerText;
  if (fetchNewsLabel) {
    fetchNewsLabel.textContent = t('editor.fetching');
  } else {
    btnFetchNews.innerText = t('editor.fetching');
  }
  btnFetchNews.disabled = true;
  btnFetchNews.classList.add('opacity-75', 'cursor-not-allowed');

  try {
    // 调用 Flask 后端接口
    const response = await fetch('http://localhost:5001/api/scrape', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: url })
    });

    const result = await response.json();

    if (result.success) {
      // 将抓取到的数据同步到当前新闻的所有 Version
      const currentNews = surveyState.news[surveyState.currentNewsIndex];
      Object.keys(currentNews.versions).forEach(vKey => {
        updateVersionAcrossPlatformVariants(currentNews.versions[vKey], {
          caption: result.title,
          image: result.image
        });
      });

      // 更新 UI 视图
      renderEditor();
      renderPreview();
      saveAppStateToLocalStorage();
    } else {
      alert(t('alert.scrapingFailed', { error: result.error || 'Unknown error' }));
    }

  } catch (error) {
    console.error("Failed to fetch news data:", error);
    alert(t('alert.backendError'));
  } finally {
    // 恢复按钮状态
    if (fetchNewsLabel) {
      fetchNewsLabel.textContent = originalText;
    } else {
      btnFetchNews.innerText = originalText;
    }
    btnFetchNews.disabled = false;
    btnFetchNews.classList.remove('opacity-75', 'cursor-not-allowed');
  }
});

inputNewsLink.addEventListener('input', (e) => {
  if (!getCurrentSurvey()) {
    return;
  }

  surveyState.news[surveyState.currentNewsIndex].link = e.target.value;
  saveAppStateToLocalStorage();
});

inputPlatform.addEventListener('change', (e) => {
  if (!getCurrentSurvey()) {
    return;
  }

  switchVersionPlatform(
    surveyState.news[surveyState.currentNewsIndex].versions[surveyState.currentVersion],
    e.target.value
  );
  renderQuestionBlockEditor();
  renderPreview();
  saveAppStateToLocalStorage();
});

if (inputQuestionEnabled) {
  inputQuestionEnabled.addEventListener('change', (e) => {
    updateQuestionBlock((questionBlock) => {
      questionBlock.enabled = e.target.checked;
    }, true);
  });
}

if (inputQuestionType) {
  inputQuestionType.addEventListener('change', (e) => {
    updateQuestionBlock((questionBlock) => {
      questionBlock.type = e.target.value === 'multiple' ? 'multiple' : 'single';
    });
  });
}

if (inputQuestionText) {
  inputQuestionText.addEventListener('input', (e) => {
    updateQuestionBlock((questionBlock) => {
      questionBlock.questionText = e.target.value;
    });
  });
}

if (inputQuestionRequired) {
  inputQuestionRequired.addEventListener('change', (e) => {
    updateQuestionBlock((questionBlock) => {
      questionBlock.required = e.target.checked;
    });
  });
}

if (btnAddQuestionOption) {
  btnAddQuestionOption.addEventListener('click', () => {
    updateQuestionBlock((questionBlock) => {
      if (questionBlock.options.length >= 4) {
        return;
      }
      questionBlock.options.push({
        id: `option_${Date.now()}`,
        label: `Option ${questionBlock.options.length + 1}`
      });
    }, true);
  });
}

if (questionOptionsList) {
  questionOptionsList.addEventListener('input', (e) => {
    const optionInput = e.target.closest('[data-question-option-index]');
    if (!optionInput) return;

    const optionIndex = Number(optionInput.getAttribute('data-question-option-index'));
    updateQuestionBlock((questionBlock) => {
      if (questionBlock.options[optionIndex]) {
        questionBlock.options[optionIndex].label = optionInput.value;
      }
    });
  });

  questionOptionsList.addEventListener('click', (e) => {
    const removeButton = e.target.closest('[data-action="remove-question-option"]');
    if (!removeButton || removeButton.disabled) return;

    const optionIndex = Number(removeButton.getAttribute('data-question-option-index'));
    updateQuestionBlock((questionBlock) => {
      if (questionBlock.options.length > 2) {
        questionBlock.options.splice(optionIndex, 1);
      }
    }, true);
  });
}

if (inputSourceLocale) {
  inputSourceLocale.addEventListener('change', (e) => {
    updateTranslationConfig((config) => {
      config.sourceLocale = e.target.value;
      config.targetLocales = config.targetLocales.filter((locale) => locale !== e.target.value);
    });
  });
}

targetLocaleInputs.forEach((input) => {
  input.addEventListener('change', () => {
    updateTranslationConfig((config) => {
      config.targetLocales = Array.from(targetLocaleInputs)
        .filter((localeInput) => localeInput.checked && localeInput.value !== config.sourceLocale)
        .map((localeInput) => localeInput.value);
    });
  });
});

if (btnGenerateTranslations) {
  btnGenerateTranslations.addEventListener('click', handleGenerateTranslationsClick);
}

// 监听选项卡切换
tabs.forEach(tab => {
  tab.addEventListener('click', (e) => {
    if (!getCurrentSurvey()) {
      return;
    }

    const selectedVersion = e.target.getAttribute('data-version');
    if (selectedVersion === surveyState.currentVersion) return;

    const currentNews = surveyState.news[surveyState.currentNewsIndex];
    const currentPlatform = currentNews.versions[surveyState.currentVersion].platform;
    syncCurrentPlatformVariant(currentNews.versions[surveyState.currentVersion]);
    switchVersionPlatform(currentNews.versions[selectedVersion], currentPlatform);

    // 切换样式
    tabs.forEach(t => {
      t.classList.remove('tab-active');
      t.classList.add('tab-inactive');
    });
    e.target.classList.add('tab-active');
    e.target.classList.remove('tab-inactive');

    // 更新状态并重绘
    surveyState.currentVersion = selectedVersion;
    renderEditor();
    renderPreview();
    saveAppStateToLocalStorage();
  });
});

// --- 初始化执行 ---
initializeAppState();
ensureCreateSurveyButton();
bindNoSurveyEditGuard();
ensureDataExportNavigation();
applyStaticTranslations();
updateLanguageMenuState();
startParticipantGazeDataListeners();
bindPublishSurveyButton();
bindNewSurveyNavigation();
bindProfileNavigation();
bindHistoryNavigation();
bindDataExportNavigation();
bindResultsNavigation();
lucide.createIcons(); // 初始化页面中固定的图标 (如导航栏)
renderAll();
