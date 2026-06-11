# JB Silver Connect — 백엔드 아키텍처 가이드 (as-built)

> 노년층(60세+) 대상 AI 시니어 안심 금융 플랫폼.
> 헥사고날(Ports & Adapters) + 클린 + DDD + SOLID. **참조 repo `com.ragwatson/minseok` 패턴**을 따른다.
> 데모 단계는 Mock 어댑터로 동작하며, 운영 전환 시 Mock만 실구현으로 교체한다 (유스케이스·도메인 변경 0).

## 실행 / 검증

```bash
# 모두 cloud.solidbob/ (= 저장소 루트, jb 패키지의 부모)에서 실행
cd cloud.solidbob
python3 -m venv .venv && .venv/bin/pip install -r jb/requirements.txt

# 반드시 venv의 python -m 으로 실행 (전역 uvicorn 사용 시 --reload subprocess가 jb를 못 찾음)
.venv/bin/python -m uvicorn jb.main:app --reload   # → http://127.0.0.1:8000/docs
.venv/bin/python -m pytest jb/tests -q             # 도메인 + 유스케이스 테스트
.venv/bin/lint-imports                              # 헥사고날 레이어 계약 (setup.cfg)
```

## 의존성 규칙 (절대)

> 의존성은 항상 바깥에서 안으로만. 안쪽은 바깥을 절대 모른다.

```
adapter  →  app  →  domain  →  shared_kernel
(dependencies = 컨텍스트별 조립 루트, 레이어링 밖에서 모두 와이어링)
core = cross-context 공용 외부 포트/어댑터 (LLM, Account)
```

| 레이어 | 폴더 | 책임 | import 가능 |
|--------|------|------|-------------|
| domain | `apps/<ctx>/domain/` | 엔티티·VO·이벤트·도메인서비스 | `shared_kernel`만 |
| app | `apps/<ctx>/app/` | 유스케이스(인터랙터)·입출력 포트·DTO | `domain`, `core.ports`, `shared_kernel` |
| adapter | `apps/<ctx>/adapter/` | FastAPI 라우터·스키마·Mock 구현체 | `app`, `domain` |
| dependencies | `apps/<ctx>/dependencies/` | DI 조립(Depends provider) | 모두 (조립 루트) |
| core | `core/` | 공용 포트·LLM/Account 어댑터·DI | `shared_kernel` |
| shared_kernel | `shared_kernel/` | 공용 도메인 VO(Money·UserId)·DomainEvent | 없음 (의존 0) |

`lint-imports`가 `adapter > app > domain` 방향과 `shared_kernel` 독립성을 빌드 단계에서 강제한다.

## 디렉토리 (as-built)

```
cloud.solidbob/
├── setup.cfg                         # import-linter 계약 + pytest 설정
├── .venv/
└── jb/
    ├── main.py                       # FastAPI 앱, 6개 라우터 등록 (prefix /api/v1) + CORS
    ├── requirements.txt
    ├── .env.example
    ├── shared_kernel/
    │   ├── value_objects.py          # Money, UserId
    │   └── domain_event.py           # DomainEvent 베이스
    ├── core/
    │   ├── config.py                 # Settings (env)
    │   ├── di.py                     # get_llm() 폴백체인, get_account_query()
    │   ├── ports/                    # LlmPort, AccountQueryPort (cross-context)
    │   ├── llm/                      # Gemini / Groq / Mock / Fallback 어댑터
    │   └── account/                  # MockAccountQuery
    ├── apps/<ctx>/                   # 6 컨텍스트: savings reservation phishing briefing branch report
    │   ├── domain/{entities, value_objects, events, services}
    │   ├── app/{dtos, ports/input, ports/output, use_cases}
    │   ├── adapter/{inbound/api/v1, inbound/api/schemas, outbound/mock}
    │   └── dependencies/<ctx>_provider.py
    └── tests/{domain, application}
```

## 6개 컨텍스트 (1 유스케이스씩, as-built)

| 컨텍스트 | 엔드포인트 | 유스케이스 | 핵심 도메인 규칙 | 주입 포트 |
|---|---|---|---|---|
| savings | `POST /api/v1/savings/propose` | ProposeSavings | `accept()` 없이 이동 이벤트 0 (확증형) | AccountQuery, Llm, SavingsRepository |
| reservation | `POST /api/v1/reservation/tickets` | CreateReservation | 생성 시 번호표 발권 이벤트 | TicketDispenser |
| phishing | `POST /api/v1/phishing/check` | CheckPhishing | RiskLevel **다형**(Safe/Warning/Danger), 분기 없음 | Llm |
| briefing | `POST /api/v1/briefing/daily` | GenerateBriefing | 잔액+날씨+음성 합성 | AccountQuery, Weather, Llm, Tts |
| branch | `POST /api/v1/branch/nearby` | FindNearbyBranches | 거리순 정렬 `list[Branch]` | Map |
| report | `POST /api/v1/report/interest` | GetInterestReport | `takewhile`로 연속 이자 streak | ReportRepository |

## 코딩 규칙 (엄격 — 위반 코드 금지)

| 금지 | 대신 |
|---|---|
| `@staticmethod` | 인스턴스 메서드 / 모듈 함수 |
| `@property` | 명시적 행위 메서드 (`expected_monthly_interest()`) |
| `list[dict]` / `dict[str, Any]` | 타입 있는 VO/DTO 리스트 (`list[BranchView]`) |
| 타입/상태 분기 `if-else` / `switch` | 다형성(포트 구현체/Strategy), dict 디스패치 |
| ✅ 허용 | 가드절·불변조건(`if amount < 0: raise`), 단일 조건 조기반환 |

## 명명 규칙 (참조 repo 패턴)

- 유스케이스 포트(인): `<동작>UseCase` (`ProposeSavingsUseCase`)
- 유스케이스 구현: `<동작>Interactor` (`ProposeSavingsInteractor`)
- 아웃바운드 포트: `<역할>Port` (`LlmPort`, `MapPort`)
- 어댑터: `<기술><역할>Adapter` (`GeminiAdapter`, `MockMapAdapter`)
- DI provider: `<ctx>_provider.py`의 `get_<usecase>_use_case()`
- 도메인 이벤트: 과거형 (`ReservationCreated`, `SavingsProposalAccepted`)

## 다음 단계 (미구현)

- 프론트엔드 `www/` (React + Vite, 시니어 UX 규칙)
- 실 어댑터: Gemini/Groq 키 연결, Supabase 영속성, 카카오 지도, 기상청 날씨, gTTS
- savings 외 컨텍스트 테스트 보강
```
