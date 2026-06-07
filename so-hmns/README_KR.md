# SO-HMNS: 자율 최적화 하이퍼 매니폴드 정규화 시스템

[![DOI](https://zenodo.org)](https://doi.org)
[![Python Version](https://shields.io)](https://python.org)
[![Framework](https://shields.io)](https://pytorch.org)

본 프로젝트는 고차원 매니폴드 환경에서 비선형 데이터 분포를 동적으로 정규화하고 과적합을 방지하는 **자율 최적화 하이퍼 매니폴드 정규화 시스템(SO-HMNS)**의 공식 PyTorch 구현체입니다. 기존 기계학습 이론들이 가졌던 기하학적 차원 충돌 및 열역학적 수렴 특이점을 수학적으로 완전히 교정하여 설계되었습니다.

> 🌐 **English Documentation**: 영문 명세는 [README.md](./README.md)를 참조하십시오.

---

## 🏆 핵심 수학적 돌파구 및 해결된 논리 공백

### 1. 고차원 매니폴드 곡률 계산의 차원 오류 수정
- **기존 문제**: 고차원 매니폴드를 다루면서 2차원 표면(Surface)에서만 정의되는 스칼라 가우스 곡률(K)과 평균 곡률(H)을 대입하여 차원 충돌 및 위상 붕괴가 발생했습니다.
- **해결 방안**: 데이터 기반 매니폴드 공간에서 차원 불변성을 보장하는 **대칭 정규화된 그래프 라플라시안(\(L_{\text{sym}}\))**의 디리클레 에너지를 도입하여 매니폴드의 기하학적 매끈함을 엄밀하게 보존합니다.

### 2. 열역학 자유 에너지 분모 특이점(발산) 제거
- **기존 문제**: 시스템의 상태 에너지를 미분하는 과정에서 자유 에너지 \(F_m \to 0\)인 물리적 평형 상태에 도달할 때, 학습률이 무한대로 발산(\(\eta_m \to \infty\))하며 연산 그래프가 파괴되는 치명적인 결함이 있었습니다.
- **해결 방안**: 통계역학적 **볼츠만 가중치 지수 감쇄 모델**을 도입하여, 어떠한 상태 변화 경로에서도 학습률이 항상 유한한 범위(\(\eta_m \in (0, M]\)) 내에서만 움직이도록 수치적 안정성을 확보했습니다.

### 3. 정보 밀도(KLD)와 매니폴드 위상 구조의 선형 연결
- **기존 문제**: 원본 공간의 확률 밀도 분포와 저차원 정규화 공간의 기하학적 구조 간에 명확한 수학적 연결 고리가 누락되어 연산 단절이 존재했습니다.
- **해결 방안**: 원본 데이터 공간의 가우시안 커널 분포(P)와 하이퍼 매니폴드 공간의 코시(Student-t) 분포(Q)를 **쿨백-라이블러 발산(KLD)** 목적함수로 결합하여 완벽한 위상학적 전사(Mapping)를 이끌어냅니다.

### 4. 다중 목적함수 간섭(GradNorm) 최적화
- **기존 문제**: 주 작업 손실 함수와 매니폴드 제어 손실 함수가 고정된 가중치 하에서 서로의 역전파 그래디언트를 상쇄(Gradient Cancellation)하거나 격렬하게 진동했습니다.
- **해결 방안**: 오차 역전파 그래프 외부에서 실시간으로 각 태스크의 그래디언트 L₂-노름 비율의 균형을 맞추는 **GradNorm 동적 가중치 알고리즘**을 임베딩하여 다중 목적함수 최적화 수렴성을 보장했습니다.

---

## 📁 프로젝트 파일 구조

```text
so-hmns/
├── README.md               # 영문 메인 설명서
├── README_KR.md            # 한국어 설명서 (본 파일)
├── requirements.txt         # 필수 종속성 라이브러리 목록
├── proof.tex               # 학회 제출용 LaTeX 완전무결성 증명서
├── main.py                 # 시스템 전체 연산 검증 파이프라인 데모
└── sohmns/
    ├── __init__.py
    ├── core.py             # GradNorm 및 볼츠만 감쇄 기반 최적화 엔진 코어
    └── utils.py            # 고차원 그래프 라플라시안 스펙트럼 연산 모듈
```

---

## 🚀 시작하기 및 실행 방법

### 의존성 설치
본 패키지는 PC 환경뿐만 아니라 안드로이드 Termux 리눅스(`aarch64`) 환경의 파이토치 구동계와도 완벽하게 호환되도록 최적화되어 있습니다:
```bash
git clone https://github.com
cd so-hmns
pip install -r requirements.txt
```

### 데모 루프 실행
통합 정규화 엔진이 실시간으로 동적 가중치와 학습률을 제어하는 연산 결과를 모니터링하려면 다음 스크립트를 실행하십시오:
```bash
python main.py
```

---

## 📊 통합 엔진 정상 구동 로그 예시
`main.py` 파이프라인을 가동하면 GradNorm 역전파 튜플 제어기가 수동 하이퍼파라미터 튜닝 없이도 실시간으로 황금 가중치 밸런스를 찾아냅니다:
```text
=== SO-HMNS Engine Integrity Check ===
1. Fused Comprehensive Loss (L_total): 4.9596
2. Thermodynamic Bounded Learning Rate (eta_m): 0.000838
3. Dynamic Manifold Balance Scale (lambdas): [0.9039, 1.1561]
```

---

## 📜 공식 학술 인용 양식 (BibTeX)

본 연구에서 확립한 고차원 매니폴드 검증 수식 및 LaTeX 증명 데이터를 학술 논문, 인공지능 연구 프레임워크, 또는 오픈소스 프로젝트에 인용할 경우 Zenodo에 영구 아카이빙된 아래의 공식 고유 식별자(DOI) 주소를 사용하여 인용해 주시기 바랍니다:

```bibtex
@software{choi_so_hmns_2026,
  author       = {Choi, Ryujin},
  title        = {Self-Optimizing Hyper-Manifold Normalization Systems (SO-HMNS)},
  month        = jun,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.0.0},
  doi          = {10.5281/zenodo.20579901},
  url          = {https://doi.org}
}
```
