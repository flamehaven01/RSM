# Flamehaven Academic Paper Website Template

## 📋 표준 구조

```
paper-project.github.io/
├── index.html                 # 메인 랜딩 페이지
├── assets/
│   ├── css/
│   │   ├── flamehaven.css    # Flamehaven 브랜드 스타일
│   │   └── paper.css         # 논문별 커스텀
│   ├── js/
│   │   ├── demo.js           # 인터랙티브 데모
│   │   └── analytics.js      # 방문자 추적
│   └── images/
│       ├── logo/             # Flamehaven 로고
│       ├── figures/          # 논문 그림들
│       └── screenshots/      # 데모 스크린샷
├── paper/
│   ├── paper.pdf            # 논문 PDF
│   ├── supplementary.pdf    # 보충 자료
│   └── bibtex.txt          # BibTeX 인용
├── code/
│   ├── demo/               # 라이브 데모
│   ├── experiments/        # 실험 재현 코드
│   └── download/           # 다운로드 링크
├── data/
│   ├── datasets/           # 데이터셋
│   ├── results/            # 실험 결과
│   └── api/                # 데이터 API
└── docs/
    ├── installation.md     # 설치 가이드
    ├── tutorial.md         # 사용법 튜토리얼
    └── api.md              # API 문서
```

## 🎨 Flamehaven 브랜드 디자인

### 컬러 팔레트
```css
:root {
    --flamehaven-primary: #FF6B35;    /* 플레임 오렌지 */
    --flamehaven-secondary: #1A1A2E;  /* 딥 네이비 */
    --flamehaven-accent: #16213E;     /* 아카데믹 블루 */
    --flamehaven-light: #EAEAEA;      /* 라이트 그레이 */
    --flamehaven-text: #2C2C2C;       /* 다크 그레이 */
}
```

### 타이포그래피
```css
.flamehaven-title {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    color: var(--flamehaven-primary);
}

.academic-text {
    font-family: 'Source Serif Pro', serif;
    line-height: 1.7;
    text-align: justify;
}
```

## 📱 반응형 레이아웃

### 헤더 구조
```html
<header class="flamehaven-header">
    <div class="container">
        <div class="logo">
            <img src="assets/images/logo/flamehaven-logo.svg" alt="Flamehaven">
        </div>
        <nav class="main-nav">
            <a href="#abstract">Abstract</a>
            <a href="#demo">Demo</a>
            <a href="#results">Results</a>
            <a href="#code">Code</a>
            <a href="#paper">Paper</a>
        </nav>
    </div>
</header>
```

### 메인 히어로 섹션
```html
<section class="hero">
    <div class="container">
        <h1 class="paper-title">{{PAPER_TITLE}}</h1>
        <div class="authors">
            <span class="author flamehaven-author">{{AUTHORS}}</span>
            <span class="affiliation">Flamehaven Initiative</span>
        </div>
        <div class="paper-meta">
            <span class="venue">{{VENUE}} {{YEAR}}</span>
            <span class="status">{{STATUS}}</span>
        </div>
        <div class="action-buttons">
            <a href="paper/paper.pdf" class="btn btn-primary">Read Paper</a>
            <a href="#demo" class="btn btn-secondary">Try Demo</a>
            <a href="code/" class="btn btn-outline">View Code</a>
        </div>
    </div>
</section>
```

## 🔬 표준 섹션들

### 1. Abstract
```html
<section id="abstract" class="section">
    <div class="container">
        <h2>Abstract</h2>
        <div class="abstract-text academic-text">
            {{ABSTRACT_CONTENT}}
        </div>
    </div>
</section>
```

### 2. 인터랙티브 데모
```html
<section id="demo" class="section demo-section">
    <div class="container">
        <h2>Interactive Demo</h2>
        <div class="demo-container">
            <div class="demo-controls">
                <!-- 입력 컨트롤들 -->
            </div>
            <div class="demo-results">
                <!-- 결과 시각화 -->
            </div>
        </div>
    </div>
</section>
```

### 3. 실험 결과
```html
<section id="results" class="section">
    <div class="container">
        <h2>Experimental Results</h2>
        <div class="results-grid">
            <div class="result-card">
                <h3>{{EXPERIMENT_NAME}}</h3>
                <div class="metrics">
                    <!-- 핵심 지표들 -->
                </div>
                <div class="visualization">
                    <!-- 차트/그래프 -->
                </div>
            </div>
        </div>
    </div>
</section>
```

### 4. 코드 & 재현성
```html
<section id="code" class="section">
    <div class="container">
        <h2>Code & Reproducibility</h2>
        <div class="code-blocks">
            <div class="installation">
                <h3>Quick Start</h3>
                <pre><code>pip install {{PACKAGE_NAME}}
python demo.py</code></pre>
            </div>
            <div class="links">
                <a href="{{GITHUB_REPO}}" class="btn">GitHub Repository</a>
                <a href="{{COLAB_LINK}}" class="btn">Open in Colab</a>
                <a href="{{HUGGINGFACE}}" class="btn">Hugging Face Space</a>
            </div>
        </div>
    </div>
</section>
```

## 📊 분석 및 추적

### Google Analytics 통합
```javascript
// 논문별 방문자 추적
gtag('config', 'GA_MEASUREMENT_ID', {
    custom_map: {
        'paper_title': '{{PAPER_TITLE}}',
        'flamehaven_project': '{{PROJECT_NAME}}'
    }
});

// 데모 사용 추적
function trackDemoUsage(demoType, inputData) {
    gtag('event', 'demo_usage', {
        'paper_title': '{{PAPER_TITLE}}',
        'demo_type': demoType,
        'user_input': JSON.stringify(inputData)
    });
}
```

## 🔗 메인 포털 연동

### 메타데이터 API
```json
{
    "paper_id": "rsm-ontology-2025",
    "title": "Resonant Structures of Meaning: A Machine-Executable Ontology for Interpretive AI",
    "authors": ["Flamehaven Team"],
    "venue": "arXiv",
    "year": 2025,
    "status": "published",
    "demo_url": "https://rsm-ontology.github.io/demo/",
    "paper_url": "https://rsm-ontology.github.io/paper/paper.pdf",
    "code_url": "https://github.com/flamehaven/rsm-implementation",
    "tags": ["symbolic-ai", "ontology", "interpretability"],
    "metrics": {
        "github_stars": 150,
        "demo_visits": 2500,
        "paper_downloads": 800
    }
}
```

## 🚀 자동화 파이프라인

### GitHub Actions 워크플로우
```yaml
name: Deploy Flamehaven Paper Site
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    - name: Install dependencies
      run: npm install
    - name: Build site
      run: npm run build
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./dist
```

이 템플릿을 사용하면 Flamehaven의 모든 논문이 일관된 브랜딩과 높은 접근성을 가질 수 있습니다!