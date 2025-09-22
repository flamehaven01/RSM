# Flamehaven Initiative - 학술 포털 설계

## 🏛️ flamehaven-papers.github.io

### 메인 포털 구조

```
flamehaven-papers.github.io/
├── index.html                 # 메인 랜딩
├── projects/                  # 개별 프로젝트 페이지
│   ├── rsm-ontology/
│   ├── arr-medic/
│   ├── kairos-compressor/
│   ├── drift-ontology-ethics/
│   └── astra-nova-forge/
├── research/
│   ├── themes/               # 연구 테마별 분류
│   │   ├── symbolic-ai/
│   │   ├── medical-ai/
│   │   ├── ethics-ai/
│   │   └── compression/
│   ├── timeline/             # 시간순 연구 히스토리
│   └── collaborations/       # 협력 프로젝트
├── team/
│   ├── researchers/          # 연구진 소개
│   ├── advisors/            # 자문단
│   └── contributors/        # 기여자들
├── resources/
│   ├── datasets/            # 공개 데이터셋
│   ├── tools/               # 연구 도구들
│   ├── templates/           # 논문 템플릿
│   └── guidelines/          # 연구 가이드라인
├── blog/                    # 연구 블로그
├── news/                    # 뉴스 & 업데이트
└── api/                     # 메타데이터 API
```

## 🎯 메인 랜딩 페이지

### 히어로 섹션
```html
<section class="hero flamehaven-gradient">
    <div class="container">
        <div class="hero-content">
            <div class="logo-section">
                <img src="assets/images/flamehaven-logo-full.svg" alt="Flamehaven Initiative">
            </div>
            <h1 class="main-title">Flamehaven Initiative</h1>
            <p class="subtitle">Advancing AI Research Through<br>
               <span class="highlight">Sovereign Intelligence</span> &
               <span class="highlight">Ethical Innovation</span></p>
            <div class="stats-row">
                <div class="stat">
                    <span class="number">{{TOTAL_PAPERS}}</span>
                    <span class="label">Research Papers</span>
                </div>
                <div class="stat">
                    <span class="number">{{TOTAL_CITATIONS}}</span>
                    <span class="label">Citations</span>
                </div>
                <div class="stat">
                    <span class="number">{{ACTIVE_PROJECTS}}</span>
                    <span class="label">Active Projects</span>
                </div>
            </div>
        </div>
    </div>
</section>
```

### 핵심 연구 영역
```html
<section class="research-domains">
    <div class="container">
        <h2>Research Domains</h2>
        <div class="domains-grid">
            <div class="domain-card">
                <div class="icon">🧠</div>
                <h3>Symbolic AI</h3>
                <p>Machine-executable ontologies and interpretive frameworks</p>
                <div class="projects-count">{{SYMBOLIC_AI_COUNT}} projects</div>
            </div>
            <div class="domain-card">
                <div class="icon">⚕️</div>
                <h3>Medical AI</h3>
                <p>Drug interaction prediction and healthcare applications</p>
                <div class="projects-count">{{MEDICAL_AI_COUNT}} projects</div>
            </div>
            <div class="domain-card">
                <div class="icon">🛡️</div>
                <h3>AI Ethics</h3>
                <p>Drift prevention and ethical AGI development</p>
                <div class="projects-count">{{ETHICS_AI_COUNT}} projects</div>
            </div>
            <div class="domain-card">
                <div class="icon">🗜️</div>
                <h3>Compression</h3>
                <p>Gravitas-aware multimodal compression systems</p>
                <div class="projects-count">{{COMPRESSION_COUNT}} projects</div>
            </div>
        </div>
    </div>
</section>
```

## 📑 프로젝트 카탈로그

### 동적 프로젝트 그리드
```html
<section class="projects-catalog">
    <div class="container">
        <div class="catalog-header">
            <h2>Research Projects</h2>
            <div class="filters">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="published">Published</button>
                <button class="filter-btn" data-filter="preprint">Preprint</button>
                <button class="filter-btn" data-filter="in-progress">In Progress</button>
            </div>
        </div>

        <div class="projects-grid" id="projects-grid">
            <!-- 동적으로 생성될 프로젝트 카드들 -->
        </div>
    </div>
</section>
```

### 프로젝트 카드 템플릿
```html
<div class="project-card" data-status="{{STATUS}}" data-year="{{YEAR}}">
    <div class="project-image">
        <img src="{{PROJECT_IMAGE}}" alt="{{PROJECT_TITLE}}">
        <div class="status-badge status-{{STATUS}}">{{STATUS}}</div>
    </div>
    <div class="project-content">
        <h3 class="project-title">{{PROJECT_TITLE}}</h3>
        <p class="project-description">{{SHORT_DESCRIPTION}}</p>
        <div class="project-meta">
            <span class="venue">{{VENUE}} {{YEAR}}</span>
            <div class="metrics">
                <span class="metric">
                    <i class="icon-star"></i>{{GITHUB_STARS}}
                </span>
                <span class="metric">
                    <i class="icon-eye"></i>{{DEMO_VISITS}}
                </span>
            </div>
        </div>
        <div class="project-links">
            <a href="{{PAPER_URL}}" class="btn btn-sm">Paper</a>
            <a href="{{DEMO_URL}}" class="btn btn-sm btn-outline">Demo</a>
            <a href="{{CODE_URL}}" class="btn btn-sm btn-outline">Code</a>
        </div>
    </div>
</div>
```

## 🔍 검색 & 필터링

### 고급 검색 기능
```javascript
class FlamehavenProjectSearch {
    constructor() {
        this.projects = [];
        this.filteredProjects = [];
        this.initSearch();
    }

    async loadProjects() {
        const response = await fetch('/api/projects.json');
        this.projects = await response.json();
        this.filteredProjects = [...this.projects];
        this.renderProjects();
    }

    search(query) {
        this.filteredProjects = this.projects.filter(project => {
            return project.title.toLowerCase().includes(query.toLowerCase()) ||
                   project.description.toLowerCase().includes(query.toLowerCase()) ||
                   project.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()));
        });
        this.renderProjects();
    }

    filterByStatus(status) {
        if (status === 'all') {
            this.filteredProjects = [...this.projects];
        } else {
            this.filteredProjects = this.projects.filter(p => p.status === status);
        }
        this.renderProjects();
    }

    renderProjects() {
        const grid = document.getElementById('projects-grid');
        grid.innerHTML = this.filteredProjects.map(project =>
            this.createProjectCard(project)
        ).join('');
    }
}
```

## 📊 연구 대시보드

### 메트릭스 시각화
```html
<section class="research-dashboard">
    <div class="container">
        <h2>Research Impact</h2>
        <div class="dashboard-grid">
            <div class="metric-card">
                <h3>Publication Timeline</h3>
                <canvas id="publicationChart"></canvas>
            </div>
            <div class="metric-card">
                <h3>Citation Growth</h3>
                <canvas id="citationChart"></canvas>
            </div>
            <div class="metric-card">
                <h3>Demo Usage</h3>
                <canvas id="demoChart"></canvas>
            </div>
            <div class="metric-card">
                <h3>Research Domains</h3>
                <canvas id="domainsChart"></canvas>
            </div>
        </div>
    </div>
</section>
```

## 🤝 팀 & 협력

### 연구진 소개
```html
<section class="team-section">
    <div class="container">
        <h2>Research Team</h2>
        <div class="team-grid">
            <div class="team-member">
                <div class="member-photo">
                    <img src="{{PHOTO_URL}}" alt="{{NAME}}">
                </div>
                <h3>{{NAME}}</h3>
                <p class="role">{{ROLE}}</p>
                <p class="expertise">{{EXPERTISE}}</p>
                <div class="social-links">
                    <a href="{{GITHUB}}"><i class="icon-github"></i></a>
                    <a href="{{SCHOLAR}}"><i class="icon-scholar"></i></a>
                    <a href="{{TWITTER}}"><i class="icon-twitter"></i></a>
                </div>
            </div>
        </div>
    </div>
</section>
```

## 📡 API & 데이터

### 프로젝트 메타데이터 API
```json
{
    "flamehaven_projects": [
        {
            "id": "rsm-ontology-2025",
            "title": "Resonant Structures of Meaning",
            "short_title": "RSM",
            "description": "A Machine-Executable Ontology for Interpretive AI",
            "status": "published",
            "venue": "arXiv",
            "year": 2025,
            "authors": ["Flamehaven Team"],
            "tags": ["symbolic-ai", "ontology", "interpretability"],
            "urls": {
                "paper": "https://rsm-ontology.github.io/paper/paper.pdf",
                "demo": "https://rsm-ontology.github.io/demo/",
                "code": "https://github.com/flamehaven/rsm-implementation",
                "project_site": "https://rsm-ontology.github.io/"
            },
            "metrics": {
                "github_stars": 150,
                "demo_visits": 2500,
                "paper_downloads": 800,
                "citations": 12
            },
            "research_domain": "symbolic-ai",
            "featured": true
        }
    ],
    "meta": {
        "total_projects": 8,
        "total_citations": 156,
        "total_demo_visits": 15000,
        "last_updated": "2025-09-22T07:50:48Z"
    }
}
```

## 🚀 배포 & 자동화

### CI/CD 파이프라인
```yaml
name: Deploy Flamehaven Portal
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'  # 매일 06:00 업데이트

jobs:
  update-metrics:
    runs-on: ubuntu-latest
    steps:
    - name: Fetch GitHub metrics
      run: |
        # GitHub API로 각 프로젝트의 스타, 포크 수 업데이트
        python scripts/update_metrics.py

    - name: Update citations
      run: |
        # Google Scholar API로 인용 수 업데이트
        python scripts/update_citations.py

    - name: Generate project data
      run: |
        # 모든 프로젝트 메타데이터 생성
        python scripts/generate_project_data.py

  deploy:
    needs: update-metrics
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./dist
```

이렇게 구축하면 Flamehaven이 학술적으로 매우 전문적이고 접근성 높은 브랜드로 자리잡을 수 있을 것 같습니다! 🔥