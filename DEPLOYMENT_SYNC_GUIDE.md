# 🔄 HF-GitHub 동기화 가이드

## ⚠️ 문제 상황
- **HF Space**: 실시간 업데이트, 사용자 피드백 반영
- **GitHub**: 소스 코드 관리, 버전 히스토리
- **결과**: 두 저장소 간 코드 차이 발생

## 🛠️ 해결 방안

### **방법 1: 수동 동기화 (즉시 사용 가능)**

#### GitHub → HF 동기화
```bash
# 1. 최신 GitHub 코드를 HF로 복사
python D:/Sanctum/RSM_Implementation/sync_to_hf.py github-to-hf

# 2. 또는 수동 복사
cp RSM_Implementation/huggingface_deployment/* rms-simulator/
cd rms-simulator
git add .
git commit -m "Sync from GitHub"
git push
```

#### HF → GitHub 동기화
```bash
# 1. HF 변경사항을 GitHub로 복사
cp rms-simulator/app.py RSM_Implementation/huggingface_deployment/
cp rms-simulator/requirements.txt RSM_Implementation/huggingface_deployment/

# 2. GitHub에 커밋
cd RSM_Implementation
git add .
git commit -m "Sync from HF Space"
git push
```

### **방법 2: 자동화된 동기화 (GitHub Actions)**

#### Setup
1. GitHub 저장소에 `.github/workflows/sync-hf-space.yml` 추가 (이미 생성됨)
2. HF Token을 GitHub Secrets에 추가:
   - GitHub → Settings → Secrets → Actions
   - Name: `HF_TOKEN`
   - Value: [Hugging Face Access Token]

#### 사용법
- **GitHub → HF**: 코드 push시 자동 동기화
- **HF → GitHub**: Manual trigger로 PR 생성

### **방법 3: 단일 소스 관리 (권장)**

#### 원칙
1. **GitHub를 마스터로 설정**
   - 모든 개발은 GitHub에서 진행
   - HF는 배포용으로만 사용

2. **개발 워크플로우**
   ```
   GitHub (개발) → 테스트 → HF Space (배포) → 모니터링
   ```

3. **긴급 수정시**
   ```
   HF에서 핫픽스 → 즉시 GitHub로 역동기화 → 정식 릴리즈
   ```

## 🔧 도구 및 스크립트

### **동기화 확인 명령어**
```bash
# 차이점 확인
python sync_to_hf.py check

# GitHub → HF 동기화
python sync_to_hf.py github-to-hf

# HF → GitHub 차이점 보고
python sync_to_hf.py hf-to-github
```

### **자동화 스크립트 활용**
- `sync_to_hf.py`: 양방향 동기화 도구
- `.github/workflows/sync-hf-space.yml`: CI/CD 자동화
- 파일 수정 시간 기반 충돌 감지

## 📊 버전 관리 전략

### **태깅 시스템**
```bash
# GitHub에서 버전 태그
git tag -a v2.3.0 -m "Add visualizations"
git push origin v2.3.0

# HF Space 버전 동기화
git tag -a hf-v2.3.0 -m "HF deployment v2.3.0"
```

### **브랜치 전략**
- `main`: 안정화된 코드
- `development`: 개발 중인 기능
- `hf-hotfix`: HF 긴급 수정용

## 🚨 비상 상황 대처

### **HF Space 다운 시**
1. GitHub에서 로컬 서버 실행
2. `python app.py` 로 임시 데모 제공
3. HF 복구 후 즉시 동기화

### **GitHub 장애 시**
1. HF Space에서 직접 수정
2. 복구 후 즉시 역동기화 필수
3. 변경 사항 문서화

## ✅ 체크리스트

### **매 배포 후 확인사항**
- [ ] GitHub와 HF 코드 버전 일치
- [ ] HF Space 빌드 성공 확인
- [ ] 주요 기능 테스트 통과
- [ ] 버전 태그 생성 및 릴리즈 노트 작성

### **주간 점검사항**
- [ ] 동기화 상태 확인 (`sync_to_hf.py check`)
- [ ] HF Space 성능 모니터링
- [ ] 사용자 피드백 GitHub 이슈로 전환
- [ ] 백업 및 히스토리 정리

## 🎯 장기 목표

1. **완전 자동화**: GitHub 커밋 → 자동 HF 배포
2. **모니터링 대시보드**: 실시간 동기화 상태 추적
3. **롤백 시스템**: 문제 발생시 즉시 이전 버전 복구
4. **다중 환경**: dev/staging/prod HF Spaces 분리