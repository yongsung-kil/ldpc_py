### arxiv:2604.12332v2 - Turán-Theoretic Bounds on Several Elementary Trapping Sets in LDPC Codes (2026, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | Turán 수 기반 ETS 크기 하한 유도 + 특정 short-cycle/8-cycle 구조 배제로 error-floor 개선 QC-LDPC 구성 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | variable-regular(γ 고정) girth 6/8 가정에 국한, HW 미설계·rate/length 미확정, base matrix 재설계 부담 큼 |
| 추가확인 | Prime ECC의 실제 base matrix에서 T1/T2/T3·8-cycle 공유 구조 존재 여부 및 배제 시 재검증 비용 |

> 총평: error-floor를 부호구조(ETS 배제)로 낮추는 이론+구성법으로 방향은 유효하나, 특정 QC-LDPC 고정 코드베이스에 재적용하려면 base matrix 재설계·재검증 부담이 커 이식성 중.

### B. 알고리즘 요약

1. 대상: variable-regular QC-LDPC(circulant permutation matrix, lifting `p`), girth `g=6` 또는 `g=8`, VN degree `dL(v)=γ`.
2. 문제: iterative decoding의 error floor는 elementary trapping set(ETS)이 주원인이며, 최소 ETS 크기를 크게 만들면 floor가 낮아진다.
3. 모델: (a,b)-ETS를 VN graph `GVN`로 사상(`|VVN|=a`, `|EVN|=(aγ-b)/2`), Butler-Siegel 선형 상태공간 모델의 system matrix `Asys` 스펙트럴 반경 `ρ`로 유해도 정량화.
4. 핵심기법 1단: 유해 구조(θ(2,2,2), θ(1,3,3), D(4,4;0) 및 chord 달린 short cycle G1/G2/G3)의 Turán 수 `ex(n,H)` 상·정확값을 유도.
5. 핵심식: girth 8·γ 조건에서 `b ≥ aγ − a(√(24a−23)−1)/4` (Theorem 6) — 8-cycle이 공통 VN을 공유하지 않으면 ETS의 b 하한이 커져 소형 ETS가 배제됨.
6. 확장: girth 6에서 T1/T2/T3-free 조건별 `b ≥ aγ − (a²+a)/2` 등 3개 하한(Theorem 7)과 γ=3,4,5 최소 크기표(Corollary 1~3).
7. 구현 디테일: 하한만으로 소형 ETS 비존재를 증명해 열거(enumeration) 복잡도를 낮추는 설계 지침 제공.
8. 최적화: QC-PEG-CYCLE 알고리즘으로 cycle 간 거리를 늘려 유해 구조를 배제하는 두 코드 C1(4,8-regular, girth6, lift35), C2(4,7-regular, girth8, lift77) 구성.
9. 결과: nauty로 전수 열거한 ETS 집합에서 구조 배제 클래스의 ρ mean/median이 항상 더 작음(Table II/III), FER 곡선에서 PEG/GCD 등 대비 error floor 개선(Fig.7/8, 구체 수치는 그림에만 존재→미상).
10. 한계: 순수 이론+시뮬, HW 미설계, variable-regular·특정 girth 가정, rate/length는 예시 코드에만 국한.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| ETS 배제 QC-LDPC base matrix 구성 | ecc_top.cpp Load_PCM() | H-matrix 설계 단계 반영 필요, 고정 QC-LDPC 재설계·재검증 부담 |
| error-floor 개선(구조적) | decoder.cpp LDPC_Decoder() | 디코더 알고리즘 무변경, 부호구조로만 floor 개선이라 코드 대응은 간접 |
| 8-cycle/short-cycle chord 구조 배제 규칙 | 대응 없음 | 부호설계 제약이며 실행코드 모듈에 직접 대응 없음 |
| ETS 스펙트럴 반경(ρ) 유해도 지표 | 대응 없음 | 분석 지표일 뿐 런타임 모듈 없음 |
```

적용 가치: **중간** — error-floor를 min-sum 변형 없이 부호구조로 낮추는 검증된 지침이지만, Prime ECC의 고정 base matrix(`matrix_sel`) 재설계·재검증 비용이 커 즉시 이식은 어렵고 차기 부호설계 가이드로만 유효.

### D. JSON 블록

```json
{
  "id": "arxiv:2604.12332v2",
  "title": "Turán-Theoretic Bounds on Several Elementary Trapping Sets in LDPC Codes",
  "year": 2026,
  "venue": "arXiv cs.IT",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": null,
  "soft_quant": "무관",
  "key_contribution": "Turán 수 기반 ETS 크기 하한 유도 + short-cycle/8-cycle 구조 배제로 error-floor 개선 QC-LDPC 구성",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "variable-regular·girth 6/8 가정 국한, HW 미설계·rate/length 미확정, base matrix 재설계 부담 큼",
  "todo_check": "Prime ECC 실제 base matrix의 T1/T2/T3·8-cycle 공유 구조 존재 여부 및 배제 시 재검증 비용"
}
```
