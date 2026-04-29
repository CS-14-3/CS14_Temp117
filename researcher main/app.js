// 初始化 Lucide 图标 
lucide.createIcons(); 

// 0. 用户与语言下拉菜单切换逻辑 (完全保留你原来的代码)
const userMenuBtn = document.getElementById('user-menu-btn'); 
const userDropdown = document.getElementById('user-dropdown'); 
const closeDropdownBtn = document.getElementById('close-dropdown-btn'); 

const langMenuBtn = document.getElementById('lang-menu-btn'); 
const langDropdown = document.getElementById('lang-dropdown'); 

// 切换用户菜单 
userMenuBtn.addEventListener('click', (e) => { 
  e.stopPropagation(); // 防止冒泡触发 document 的 click 
  userDropdown.classList.toggle('hidden'); 
  langDropdown.classList.add('hidden'); // 关闭语言菜单 
}); 

closeDropdownBtn.addEventListener('click', () => { 
  userDropdown.classList.add('hidden'); 
}); 

// 切换语言菜单 
langMenuBtn.addEventListener('click', (e) => { 
  e.stopPropagation(); 
  langDropdown.classList.toggle('hidden'); 
  userDropdown.classList.add('hidden'); // 关闭用户菜单 
}); 

// 点击外部区域关闭两个下拉菜单 
document.addEventListener('click', (e) => { 
  if (!userMenuBtn.contains(e.target) && !userDropdown.contains(e.target)) { 
    userDropdown.classList.add('hidden'); 
  } 
  if (!langMenuBtn.contains(e.target) && !langDropdown.contains(e.target)) { 
    langDropdown.classList.add('hidden'); 
  } 
}); 

// 4. 生成邀请码逻辑 (完全保留你原来的代码)
const btnGenerateCode = document.getElementById('btn-generate-code'); 
const displayInviteCode = document.getElementById('invite-code-display'); 
btnGenerateCode.addEventListener('click', () => { 
  const code = Math.random().toString(36).substring(2, 8).toUpperCase(); 
  displayInviteCode.textContent = code; 
  displayInviteCode.classList.remove('hidden'); 
  btnGenerateCode.textContent = 'Regenerate'; 
});

// ==============================================================
// === 以下为新增的 A/B 状态机与多平台预览逻辑 =====================
// ==============================================================

// 模拟的 A/B 版本数据状态
const surveyState = {
  currentVersion: 'vA',
  versions: {
    'vA': {
      platform: 'instagram',
      caption: 'This is a simulated news post caption. Researchers can edit this text in real-time on the left.',
      image: '', // 新增：图片数据状态
      likes: 1050,
      comments: 42,
      shares: 5
    },
    'vB': {
      platform: 'instagram',
      caption: 'Testing Version B with completely different variables and platform style.',
      image: '', // 新增：图片数据状态
      likes: 56,
      comments: 3,
      shares: 12
    }
  }
};

// DOM 获取 (更新版)
const tabs = document.querySelectorAll('.version-tab');
const inputNewsLink = document.getElementById('input-news-link');
const btnFetchNews = document.getElementById('btn-fetch-news');
const inputPlatform = document.getElementById('input-platform');
const inputCaption = document.getElementById('input-caption');
const inputLikes = document.getElementById('input-likes');
const inputComments = document.getElementById('input-comments');
const inputShares = document.getElementById('input-shares');

const previewContainer = document.getElementById('preview-container');
const previewBadgeName = document.getElementById('preview-badge-name');

// 多平台 UI 模板 (更新：支持动态渲染抓取到的图片)
const templates = {
  instagram: (data) => `
    <div class="bg-white border border-gray-200 rounded-lg shadow-sm w-full">
      <div class="flex items-center justify-between p-3 border-b border-gray-100">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-yellow-400 to-fuchsia-600 p-0.5">
            <div class="w-full h-full rounded-full bg-white p-0.5">
              <div class="w-full h-full rounded-full bg-gray-200 overflow-hidden">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="avatar" />
              </div>
            </div>
          </div>
          <div class="flex flex-col">
            <span class="text-sm font-semibold">sydney_news_hub</span>
            <span class="text-xs text-gray-500">Sydney, Australia</span>
          </div>
        </div>
        <i data-lucide="more-horizontal" class="text-gray-600 cursor-pointer w-5 h-5"></i>
      </div>
      <div class="aspect-square bg-gray-100 flex items-center justify-center relative group overflow-hidden">
        ${data.image 
          ? `<img src="${data.image}" class="w-full h-full object-cover" alt="News Image" />`
          : `<div class="text-gray-400 text-sm flex flex-col items-center">
              <i data-lucide="image" class="w-12 h-12 mb-2 opacity-50"></i>
              <span>[News Image Preview]</span> 
             </div>`
        }
      </div>
      <div class="p-3">
        <div class="flex items-center justify-between mb-2">
          <div class="flex space-x-4">
            <i data-lucide="heart" class="w-6 h-6 hover:text-gray-500 cursor-pointer"></i>
            <i data-lucide="message-circle" class="w-6 h-6 hover:text-gray-500 cursor-pointer"></i>
            <i data-lucide="send" class="w-6 h-6 hover:text-gray-500 cursor-pointer"></i>
          </div>
          <i data-lucide="bookmark" class="w-6 h-6 hover:text-gray-500 cursor-pointer"></i>
        </div>
        <div class="text-sm font-semibold mb-2">
          <span id="preview-likes">${data.likes.toLocaleString()}</span> likes 
        </div>
        <div class="text-sm leading-relaxed mb-2">
          <span class="font-semibold mr-2">sydney_news_hub</span>
          <span id="preview-caption">${data.caption}</span> 
        </div>
        <div class="text-sm text-gray-500 cursor-pointer">
          View all <span id="preview-comments">${data.comments.toLocaleString()}</span> comments 
        </div>
        <div class="text-[10px] text-gray-400 mt-2 uppercase">1 hour ago</div>
      </div>
      <div class="p-3 border-t border-gray-100 flex items-center justify-between hidden md:flex">
        <div class="flex items-center space-x-3">
          <div class="text-xl">☺</div>
          <span class="text-sm text-gray-400">Add a comment...</span> 
        </div>
        <button class="text-sky-500 font-semibold text-sm opacity-50">Post</button>
      </div>
    </div>
  `,
  facebook: (data) => `
    <div class="bg-white border border-gray-200 rounded-xl shadow-sm w-full">
      <div class="p-4 flex items-center space-x-2">
        <div class="w-10 h-10 rounded-full bg-gray-200 overflow-hidden shrink-0">
           <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" />
        </div>
        <div>
          <p class="font-bold text-sm leading-tight text-gray-900">Sydney News Hub</p>
          <p class="text-xs text-gray-500 flex items-center">2 hrs · <i data-lucide="globe" class="w-3 h-3 ml-1"></i></p>
        </div>
      </div>
      <div class="px-4 pb-3 text-sm text-gray-800">${data.caption}</div>
      <div class="w-full aspect-video bg-gray-100 flex flex-col items-center justify-center border-y border-gray-200 text-gray-400 overflow-hidden">
        ${data.image
          ? `<img src="${data.image}" class="w-full h-full object-cover" alt="News Image" />`
          : `<i data-lucide="image" class="w-12 h-12 mb-2 opacity-50"></i>
             <span class="text-sm">[News Image Preview]</span>`
        }
      </div>
      <div class="px-4 py-2 flex justify-between items-center text-xs text-gray-500 border-b border-gray-200">
        <div class="flex items-center"><div class="bg-blue-500 text-white rounded-full p-1 mr-1 w-5 h-5 flex items-center justify-center"><i data-lucide="thumbs-up" class="w-3 h-3"></i></div> ${data.likes.toLocaleString()}</div>
        <div>${data.comments.toLocaleString()} comments · ${data.shares.toLocaleString()} shares</div>
      </div>
      <div class="px-4 py-1 flex justify-between">
        <button class="flex-1 flex items-center justify-center space-x-2 py-2 text-gray-600 hover:bg-gray-100 rounded-lg text-sm font-medium"><i data-lucide="thumbs-up" class="w-5 h-5"></i><span>Like</span></button>
        <button class="flex-1 flex items-center justify-center space-x-2 py-2 text-gray-600 hover:bg-gray-100 rounded-lg text-sm font-medium"><i data-lucide="message-square" class="w-5 h-5"></i><span>Comment</span></button>
        <button class="flex-1 flex items-center justify-center space-x-2 py-2 text-gray-600 hover:bg-gray-100 rounded-lg text-sm font-medium"><i data-lucide="share-2" class="w-5 h-5"></i><span>Share</span></button>
      </div>
    </div>
  `,
  x: (data) => `
    <div class="bg-white border border-gray-200 shadow-sm w-full p-4">
      <div class="flex space-x-3">
        <div class="w-12 h-12 rounded-full bg-gray-200 overflow-hidden shrink-0">
           <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" />
        </div>
        <div class="flex-1">
          <div class="flex items-center text-sm">
            <span class="font-bold text-gray-900 mr-1">Sydney News Hub</span>
            <i data-lucide="badge-check" class="w-4 h-4 text-blue-500 mr-1"></i>
            <span class="text-gray-500">@sydneynews · 2h</span>
          </div>
          <p class="text-[15px] text-gray-900 mt-1 mb-3">${data.caption}</p>
          <div class="w-full aspect-video bg-gray-100 rounded-2xl border border-gray-200 flex flex-col items-center justify-center text-gray-400 overflow-hidden">
             ${data.image
               ? `<img src="${data.image}" class="w-full h-full object-cover" alt="News Image" />`
               : `<i data-lucide="image" class="w-10 h-10 mb-2 opacity-50"></i>
                  <span class="text-sm">[News Image Preview]</span>`
             }
          </div>
          <div class="flex justify-between mt-3 text-gray-500 max-w-md">
            <div class="flex items-center space-x-2 hover:text-blue-500 cursor-pointer"><i data-lucide="message-circle" class="w-4 h-4"></i><span class="text-xs">${data.comments.toLocaleString()}</span></div>
            <div class="flex items-center space-x-2 hover:text-green-500 cursor-pointer"><i data-lucide="repeat-2" class="w-4 h-4"></i><span class="text-xs">${data.shares.toLocaleString()}</span></div>
            <div class="flex items-center space-x-2 hover:text-pink-500 cursor-pointer"><i data-lucide="heart" class="w-4 h-4"></i><span class="text-xs">${data.likes.toLocaleString()}</span></div>
            <div class="flex items-center space-x-2 hover:text-blue-500 cursor-pointer"><i data-lucide="bar-chart-2" class="w-4 h-4"></i><span class="text-xs">12K</span></div>
          </div>
        </div>
      </div>
    </div>
  `,
  tiktok: (data) => `
    <div class="bg-black text-white w-[320px] h-[580px] rounded-xl overflow-hidden shadow-xl relative flex items-center justify-center font-sans mx-auto">
      <div class="absolute inset-0 bg-gray-800 flex flex-col items-center justify-center text-gray-500 overflow-hidden">
         ${data.image
           ? `<img src="${data.image}" class="w-full h-full object-cover opacity-80" alt="News Image" />`
           : `<i data-lucide="play-circle" class="w-16 h-16 opacity-30 mb-2"></i>
              <span class="text-sm font-medium">Video Placeholder</span>`
         }
      </div>
      <div class="absolute right-2 bottom-20 flex flex-col items-center space-y-5 z-10">
        <div class="w-12 h-12 rounded-full border-2 border-white overflow-hidden bg-gray-200 relative mb-2">
           <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" />
           <div class="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-pink-500 rounded-full w-5 h-5 flex items-center justify-center text-white text-xs font-bold border border-white">+</div>
        </div>
        <div class="flex flex-col items-center drop-shadow-md cursor-pointer"><i data-lucide="heart" class="w-8 h-8 fill-transparent hover:fill-pink-500"></i><span class="text-xs mt-1 font-semibold">${data.likes >= 1000 ? (data.likes/1000).toFixed(1)+'K' : data.likes}</span></div>
        <div class="flex flex-col items-center drop-shadow-md cursor-pointer"><i data-lucide="message-circle" class="w-8 h-8 fill-white text-black"></i><span class="text-xs mt-1 font-semibold">${data.comments >= 1000 ? (data.comments/1000).toFixed(1)+'K' : data.comments}</span></div>
        <div class="flex flex-col items-center drop-shadow-md cursor-pointer"><i data-lucide="bookmark" class="w-8 h-8 text-white"></i><span class="text-xs mt-1 font-semibold">Save</span></div>
        <div class="flex flex-col items-center drop-shadow-md cursor-pointer"><i data-lucide="forward" class="w-8 h-8 fill-white text-white"></i><span class="text-xs mt-1 font-semibold">${data.shares}</span></div>
      </div>
      <div class="absolute bottom-4 left-4 right-16 z-10 drop-shadow-md">
        <p class="font-bold text-[15px] mb-1">@sydney_news_hub</p>
        <p class="text-sm leading-snug line-clamp-2">${data.caption}</p>
        <p class="text-sm font-medium flex items-center mt-2"><i data-lucide="music" class="w-4 h-4 mr-2"></i> original sound - Sydney News</p>
      </div>
    </div>
  `
};

// --- 渲染逻辑 ---
function renderEditor() {
  const currentData = surveyState.versions[surveyState.currentVersion];
  inputPlatform.value = currentData.platform;
  inputCaption.value = currentData.caption;
  inputLikes.value = currentData.likes;
  inputComments.value = currentData.comments;
  inputShares.value = currentData.shares;
}

function renderPreview() {
  const currentData = surveyState.versions[surveyState.currentVersion];
  previewBadgeName.textContent = currentData.platform.toUpperCase();
  if (templates[currentData.platform]) {
    previewContainer.innerHTML = templates[currentData.platform](currentData);
  }
  lucide.createIcons(); // 每次重新渲染 HTML 后，必须重新生成图标
}

// --- 事件监听绑定 ---

// 4. 新闻链接真实抓取逻辑 (JS + Python Flask 架构)
btnFetchNews.addEventListener('click', async () => {
  const url = inputNewsLink.value.trim();
  if (!url) {
    alert("Please paste a news link first.");
    return;
  }

  // UI 变为加载状态
  const originalText = btnFetchNews.innerText;
  btnFetchNews.innerText = 'Fetching...';
  btnFetchNews.disabled = true;
  btnFetchNews.classList.add('opacity-75', 'cursor-not-allowed');

  try {
    const API_BASE = window.API_BASE || "";

    // 调用 Flask 后端接口
    const response = await fetch(`${API_BASE}/api/scrape`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: url })
    });

    const result = await response.json();

    if (result.success) {
      // 将抓取到的数据同步到所有 Version (全局属性)
      Object.keys(surveyState.versions).forEach(vKey => {
        surveyState.versions[vKey].caption = result.title;
        surveyState.versions[vKey].image = result.image;
      });

      // 更新 UI 视图
      renderEditor();
      renderPreview();
    } else {
      alert("Scraping failed: " + (result.error || "Unknown error"));
    }

  } catch (error) {
    console.error("Failed to fetch news data:", error);
    alert("Backend service error. Please make sure the scraping API service is running.");
  } finally {
    // 恢复按钮状态
    btnFetchNews.innerText = originalText;
    btnFetchNews.disabled = false;
    btnFetchNews.classList.remove('opacity-75', 'cursor-not-allowed');
  }
});

inputPlatform.addEventListener('change', (e) => {
  surveyState.versions[surveyState.currentVersion].platform = e.target.value;
  renderPreview();
});
inputCaption.addEventListener('input', (e) => {
  surveyState.versions[surveyState.currentVersion].caption = e.target.value;
  renderPreview();
});
inputLikes.addEventListener('input', (e) => {
  surveyState.versions[surveyState.currentVersion].likes = parseInt(e.target.value) || 0;
  renderPreview();
});
inputComments.addEventListener('input', (e) => {
  surveyState.versions[surveyState.currentVersion].comments = parseInt(e.target.value) || 0;
  renderPreview();
});
inputShares.addEventListener('input', (e) => {
  surveyState.versions[surveyState.currentVersion].shares = parseInt(e.target.value) || 0;
  renderPreview();
});

// 监听选项卡切换
tabs.forEach(tab => {
  tab.addEventListener('click', (e) => {
    const selectedVersion = e.target.getAttribute('data-version');
    if (selectedVersion === surveyState.currentVersion) return;

    // 新增逻辑：切换版本时，让目标版本的平台风格与当前版本保持一致
    surveyState.versions[selectedVersion].platform = surveyState.versions[surveyState.currentVersion].platform;

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
  });
});

// --- 初始化执行 ---
lucide.createIcons(); // 初始化页面中固定的图标 (如导航栏)
renderEditor();
renderPreview();