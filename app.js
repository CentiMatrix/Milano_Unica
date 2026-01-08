// Milano Unica 42nd Edition 手绘逛展指南 - 主逻辑 (双语版)

// ===== 多语言配置 =====
const I18N = {
    zh: {
        'subtitle': '手绘逛展指南 · Milano 2026',
        'brands-count': '加载中...',
        'categories-count': '加载中...',
        'curated': '精选推荐',
        'quick-nav': '逛展路线导航',
        'nav-subtitle': '按展区快速定位品牌',
        'footer-tip': '逛展愉快，记得带好舒适的鞋子！',
        'pros': '核心优势 (Advantage)',
        'cons': '潜在短板 (Disadvantage)',
        'price-range': '价格参考 (Price)',
        'recommended-for': 'B2B 价值策略 (Strategy)',
        'visit-website': '🔗 访问官网',
        'brands': '个品牌',
        'loading-error': '🔧 数据加载失败，请检查 data/brands.json 文件',
        'search-placeholder': '搜索品牌、展位或关键词...',
        'no-results': '🔍 未找到匹配的品牌',
        'booth-label': '展位',
        'clients': '服务客户 (Clients)',
        'product-type': '产品类型 (Product Type)',
    },
    en: {
        'subtitle': 'Hand-drawn Exhibition Guide · Milano 2026',
        'brands-count': 'Loading...',
        'categories-count': 'Loading...',
        'curated': 'Curated Picks',
        'quick-nav': 'Route Navigation',
        'nav-subtitle': 'Locate brands by area',
        'footer-tip': 'Enjoy the show! Remember to wear comfortable shoes.',
        'pros': 'Key Advantages',
        'cons': 'Potential Drawbacks',
        'price-range': 'Price Range',
        'recommended-for': 'Strategy',
        'visit-website': '🔗 Visit Website',
        'brands': 'Brands',
        'loading-error': '🔧 Failed to load data, please check data/brands.json',
        'search-placeholder': 'Search brands, booths, or keywords...',
        'no-results': '🔍 No matching brands found',
        'booth-label': 'Booth',
        'clients': 'Key Clients',
        'product-type': 'Product Type',
    }
};

const CATEGORY_I18N = {
    zh: {
        IDE: 'Ideabiella', SHI: 'Shirt Avenue', MOD: 'Moda In Fabrics'
    },
    en: {
        IDE: 'Ideabiella', SHI: 'Shirt Avenue', MOD: 'Moda In Fabrics'
    }
};

let currentLang = 'zh';
let brandsData = null;
let searchQuery = '';

// 品类排序与图标
const CATEGORY_ORDER = ['IDE', 'SHI', 'MOD'];
const CATEGORY_ICONS = {
    IDE: '🧶', SHI: '👕', MOD: '🧵'
};

// 加载数据
async function loadBrandsData() {
    try {
        const response = await fetch('data/brands.json');
        if (!response.ok) throw new Error('数据加载失败');
        return await response.json();
    } catch (error) {
        console.error('加载品牌数据出错:', error);
        return null;
    }
}

// 渲染星级
function renderStars(count) {
    return '⭐'.repeat(count);
}

// 获取文本
function t(key) {
    return I18N[currentLang][key] || key;
}

// 生成品牌卡片 HTML
function createBrandCard(brand) {
    const prosHtml = brand.pros?.length
        ? `<ul class="pros-list">${brand.pros.map(p => `<li>${p.title}</li>`).join('')}</ul>`
        : '';

    const consHtml = brand.cons?.length
        ? `<ul class="cons-list">${brand.cons.map(c => `<li>${c.title}</li>`).join('')}</ul>`
        : '';

    // 修复价格显示 Bug：处理字符串数组
    const pricesHtml = brand.prices?.length
        ? brand.prices.map(p => {
            if (typeof p === 'string') return `<div>${p}</div>`;
            return `<div>${p.item || ''}: ${p.range || ''}</div>`;
        }).join('')
        : '';

    return `
        <article class="brand-card" onclick="this.classList.toggle('expanded')">
            <div class="brand-header">
                <h3 class="brand-name">${brand.name}</h3>
                <span class="brand-stars">${renderStars(brand.stars)}</span>
            </div>
            <p class="brand-tagline">${brand.tagline || ''}</p>
            <div class="brand-meta">
                ${brand.stand ? `<span class="brand-stand">📍 ${brand.stand}</span>` : ''}
                ${brand.style ? `<span class="brand-style">${brand.style.split(',')[0]}</span>` : ''}
            </div>
            <div class="brand-details">
                <div class="detail-grid">
                    ${(prosHtml || consHtml) ? `
                        <div class="detail-section full-width">
                            <div class="pros-cons-container">
                                ${prosHtml ? `<div class="pros-box"><div class="detail-label">${t('pros')}</div>${prosHtml}</div>` : ''}
                                ${consHtml ? `<div class="cons-box"><div class="detail-label">${t('cons')}</div>${consHtml}</div>` : ''}
                            </div>
                        </div>
                    ` : ''}
                    
                    <div class="detail-section">
                        <div class="detail-label">${t('price-range')}</div>
                        <div class="detail-content price-tag">${pricesHtml || 'TBD'}</div>
                    </div>

                    ${brand.recommended ? `
                        <div class="detail-section">
                            <div class="detail-label">${t('recommended-for')}</div>
                            <div class="detail-content strategy-text">${brand.recommended}</div>
                        </div>
                    ` : ''}

                    ${brand.clients ? `
                        <div class="detail-section">
                            <div class="detail-label">${t('clients')}</div>
                            <div class="detail-content clients-text">${brand.clients}</div>
                        </div>
                    ` : ''}

                    ${brand.product_type ? `
                        <div class="detail-section full-width">
                            <div class="detail-label">${t('product-type')}</div>
                            <div class="detail-content product-text">${brand.product_type}</div>
                        </div>
                    ` : ''}
                </div>
                
                ${brand.website ? `
                    <div class="detail-footer">
                        <a href="${brand.website}" target="_blank" rel="noopener" class="brand-link">
                            ${t('visit-website')}
                        </a>
                    </div>
                ` : ''}
            </div>
        </article>
    `;
}

// 过滤品牌
function filterBrands() {
    if (!brandsData) return null;
    if (!searchQuery) return brandsData;

    const query = searchQuery.toLowerCase();
    const filtered = {};

    Object.entries(brandsData).forEach(([code, category]) => {
        const matchedBrands = category.brands.filter(brand => {
            return brand.name.toLowerCase().includes(query) ||
                (brand.stand && brand.stand.toLowerCase().includes(query)) ||
                (brand.tagline && brand.tagline.toLowerCase().includes(query)) ||
                (brand.recommended && brand.recommended.toLowerCase().includes(query));
        });

        if (matchedBrands.length > 0) {
            filtered[code] = { ...category, brands: matchedBrands };
        }
    });

    return filtered;
}

// 渲染内容
function renderContent() {
    const displayData = filterBrands();
    const contentEl = document.getElementById('content');

    if (!displayData || Object.keys(displayData).length === 0) {
        contentEl.innerHTML = `
            <div class="no-results">
                <p>${t('no-results')}</p>
            </div>
        `;
        return;
    }

    const sortedEntries = Object.entries(displayData)
        .sort((a, b) => CATEGORY_ORDER.indexOf(a[0]) - CATEGORY_ORDER.indexOf(b[0]));

    const contentHtml = sortedEntries
        .map(([code, categoryData]) => {
            const { brands } = categoryData;
            const categoryName = CATEGORY_I18N[currentLang][code];
            const categoryNameEn = CATEGORY_I18N.en[code];
            const icon = CATEGORY_ICONS[code];
            const brandsHtml = brands.map(createBrandCard).join('');

            return `
                <section class="category-section" id="cat-${code}">
                    <div class="category-header">
                        <div class="category-icon">${icon}</div>
                        <h2 class="category-title">${categoryName}${currentLang === 'zh' ? ' · ' + categoryNameEn : ''}</h2>
                        <span class="category-count">${brands.length} ${t('brands')}</span>
                    </div>
                    <div class="brands-grid">
                        ${brandsHtml}
                    </div>
                </section>
            `;
        })
        .join('');

    contentEl.innerHTML = contentHtml;
}

// 生成导航链接
function renderNav() {
    const navLinksEl = document.getElementById('navLinks');
    if (!brandsData) return;

    navLinksEl.innerHTML = Object.keys(brandsData)
        .sort((a, b) => CATEGORY_ORDER.indexOf(a) - CATEGORY_ORDER.indexOf(b))
        .map(code => {
            const icon = CATEGORY_ICONS[code];
            const name = CATEGORY_I18N[currentLang][code];
            return `<a href="#cat-${code}" class="nav-link">${icon} ${name}</a>`;
        })
        .join('');
}

// 更新静态 i18n 文本
function updateStaticTexts() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (I18N[currentLang][key]) {
            el.textContent = I18N[currentLang][key];
        }
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.dataset.i18nPlaceholder;
        if (I18N[currentLang][key]) {
            el.placeholder = I18N[currentLang][key];
        }
    });

    document.documentElement.lang = currentLang === 'zh' ? 'zh-CN' : 'en';
}

// 切换语言
function switchLanguage(lang) {
    currentLang = lang;
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });
    localStorage.setItem('mu-guide-lang', lang);
    updateStaticTexts();
    renderContent();
    renderNav();
}

// 初始化
async function initApp() {
    const savedLang = localStorage.getItem('mu-guide-lang');
    if (savedLang && I18N[savedLang]) {
        currentLang = savedLang;
    }

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === currentLang);
        btn.addEventListener('click', () => switchLanguage(btn.dataset.lang));
    });

    // 搜索监听
    const searchInput = document.getElementById('brandSearch');
    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value;
        renderContent();
    });

    brandsData = await loadBrandsData();

    if (!brandsData) {
        document.getElementById('content').innerHTML = `<div class="error-msg">${t('loading-error')}</div>`;
        return;
    }

    // 更新总数
    const totalBrands = Object.values(brandsData).reduce((sum, c) => sum + c.brands.length, 0);
    const totalCategories = Object.keys(brandsData).length;
    I18N.zh['brands-count'] = `${totalBrands} 个品牌`;
    I18N.zh['categories-count'] = `${totalCategories} 个品类`;
    I18N.en['brands-count'] = `${totalBrands} Brands`;
    I18N.en['categories-count'] = `${totalCategories} Categories`;

    updateStaticTexts();
    renderNav();
    renderContent();
}

document.addEventListener('DOMContentLoaded', initApp);
