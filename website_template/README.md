# 🔥 Flamehaven Academic Website Ecosystem

ResearchCodeBench 스타일의 완전한 학술 웹사이트 시스템이 구축되었습니다!

## 📚 구성 요소

### 1. **개별 논문 사이트 템플릿**
- `flamehaven_paper_template.md` - 표준 논문 사이트 구조
- `rsm_project_site/` - RSM 프로젝트 완전 구현 사례
- 인터랙티브 데모, 실험 결과 시각화, BibTeX 관리

### 2. **Flamehaven 메인 포털 설계**
- `flamehaven_main_portal.md` - 중앙 집중식 논문 포털
- 모든 프로젝트 카탈로그와 메트릭스 대시보드
- 자동화된 업데이트 시스템

### 3. **브랜드 디자인 시스템**
- Flamehaven 고유 컬러 팔레트 (`#FF6B35`, `#1A1A2E`)
- 학술적 타이포그래피 (Inter + Source Serif Pro)
- 반응형 컴포넌트 라이브러리

## 🚀 즉시 시작하기

### GitHub Pages로 RSM 사이트 배포
```bash
# 1. 새 레포 생성
git clone https://github.com/yourusername/rsm-ontology.github.io.git
cd rsm-ontology.github.io

# 2. 템플릿 복사
cp -r website_template/rsm_project_site/* .

# 3. 배포
git add .
git commit -m "Launch RSM project site"
git push origin main

# 결과: https://yourusername.github.io/rsm-ontology 접속 가능
```

### Flamehaven 메인 포털 구축
```bash
# 1. 메인 포털 레포 생성
git clone https://github.com/flamehaven/flamehaven-papers.github.io.git
cd flamehaven-papers.github.io

# 2. 포털 구조 생성 (flamehaven_main_portal.md 참조)
mkdir -p projects research team resources api
```

## 🎯 핵심 기능들

### ✅ 완전 구현된 기능
- **인터랙티브 RSM 데모**: 실시간 symbolic reasoning
- **실험 결과 대시보드**: 5개 핵심 실험 데이터 시각화
- **학술적 레이아웃**: 논문 메타데이터, BibTeX, 다운로드
- **반응형 디자인**: 모바일/데스크톱 완벽 지원
- **분석 추적**: Google Analytics 통합

### 🔄 자동화 파이프라인
- GitHub Actions로 자동 배포
- 메트릭스 실시간 업데이트 (스타, 다운로드 수)
- 논문별 방문자 추적 및 사용 패턴 분석

## 📊 예상 효과

### 학술적 브랜딩
- **전문성**: ResearchCodeBench 수준의 학술적 완성도
- **접근성**: 인터랙티브 데모로 논문 이해도 향상
- **신뢰성**: 완전한 재현성과 검증 가능한 결과

### 연구 영향력
- **가시성**: 검색 엔진 최적화와 소셜 공유
- **참여도**: 라이브 데모로 연구자 engagement 증가
- **인용률**: 쉬운 접근성으로 인용 빈도 향상

## 🔗 연동 시스템

### 개별 논문 → 메인 포털
```javascript
// 각 논문 사이트에서 메인 포털로 메트릭스 전송
fetch('https://flamehaven-papers.github.io/api/update-metrics', {
    method: 'POST',
    body: JSON.stringify({
        project_id: 'rsm-ontology-2025',
        demo_visits: getDemoVisits(),
        paper_downloads: getPaperDownloads()
    })
});
```

### 통합 검색 및 발견
- 모든 Flamehaven 논문의 통합 검색
- 태그 기반 연구 분야별 필터링
- 시간순/인기순 정렬

## 🎨 브랜드 일관성

### 모든 사이트 공통 요소
- Flamehaven 로고와 네비게이션
- 일관된 컬러 스키마와 타이포그래피
- 표준화된 논문 메타데이터 형식
- 통일된 CTA (Call-to-Action) 버튼

## 📈 확장성

### 새 논문 추가 프로세스
1. 표준 템플릿으로 개별 사이트 생성
2. 실험 데이터 JSON 업로드
3. 메인 포털에 자동 등록
4. 크로스 레퍼런스 링크 생성

이 시스템으로 Flamehaven이 학술 AI 연구의 브랜드 리더로 자리잡을 수 있을 것입니다! 🔥