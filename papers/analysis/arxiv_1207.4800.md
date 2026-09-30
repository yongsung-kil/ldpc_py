### arxiv:1207.4800v1 - Finite Alphabet Iterative Decoders, Part I: Decoding Beyond Belief Propagation on BSC (2012, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 상 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.5~0.833 |
| 부호length | 155~5184 |
| 연판정 | soft-2~3bit |
| 핵심기여 | BP/min-sum을 근사하지 않는 유한 알파벳(3비트) 변수노드 갱신 맵(FAID)을 trapping-set 기반으로 설계해 error floor에서 floating-point BP를 능가 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 상 |
| 한계,주의 | column-weight-3 코드에 한정된 설계이며 FAID의 variable-node 갱신 맵은 code-independent 후보군에서 code별 브루트포스 시뮬레이션으로 최종 선택해야 함(온라인 자동 설계 아님) |
| 추가확인 | 3비트(7-level) LUT 기반 Φv를 z=32 lifting 및 HCU/GT 파이프라인 구조에 이식 시 CN 연산(min-sum과 동일 Φc)은 그대로 두고 VN LUT만 교체 가능한지 검증 필요 |

> 총평: check-node는 기존 min-sum과 동일하게 두고 variable-node update만 trapping-set 인지형 유한알파벳 LUT로 교체하는 구조라, 3비트 soft-info를 쓰는 Prime ECC 3.1 VN 갱신 로직에 최소침습적으로 이식 가능한 매우 이식성 높은 error-floor 개선 기법.

### B. 알고리즘 요약

1. 대상: BSC(binary symmetric channel) 위의 column-weight-3 (regular dv=3) binary LDPC 코드, rate 0.5~0.833, length 155~5184 다양한 실제 코드로 검증.
2. 문제: BP는 loopy graph에서 trapping set 때문에 error floor가 발생하고, 기존 양자화 디코더들은 BP를 근사(density evolution 기준 최적화)할 뿐이라 유한정밀도에서도 floor 문제가 남음.
3. 핵심 가정: 채널은 BSC, 메시지는 log-likelihood/확률의 양자화 값이 아니라 `M={-Ls,...,-L1,0,L1,...,Ls}` 유한 알파벳(`Ns=2s+1` 레벨) 자체 값.
4. 핵심 기법(FAID): check-node 갱신 `Φc`는 기존 min-sum과 동일(`Φc = sgn(mj) · min|mj|`), variable-node 갱신 `Φv(yi,m1,...,mdv-1) = Q(Σmj + ωi·yi)`로 정의, `Q(x)`는 threshold 집합 `T={Ti}`로 non-linear quantization.
5. 핵심 식의 의미: 가중치 `ωi`가 입력 메시지들의 비선형 조합(NLT, non-linear-threshold)을 결정 - 같은 합(sum)이라도 다른 조합이면 다른 출력을 낼 수 있어, BP/min-sum이 tree로 취급하는 loopy 이웃 구조(trapping set)를 variable node가 인지하도록 설계.
6. 확장: column-weight-3 코드에서 Φv는 2차원 LUT `[li,j]`로 표현 가능하며, 대칭(symmetry)·lexicographic ordering 제약을 만족하는 class-A FAID는 symmetric plane partition과 1:1 대응(Ns=7일 때 후보 5억 3천만 개).
7. 부수 트릭: "noisy trapping set" 개념(TS의 degree-1 check node에 초기화 벡터 Θ를 흘려 이웃 영향을 근사) + "noisy critical number"로 특정 TS에 대한 FAID의 정정 능력을 코드-독립적으로 평가.
8. 선택 절차: 사전 정의된 good/bad FAID 집합(Fg, Fb) 대비 도미넌스 기반 비용함수 `C~(Dk)`로 후보군 Fc를 스크리닝(브루트포스 아님, 휴리스틱 사전선별 후 코드별 시뮬레이션으로 최종 확정).
9. 결과: (155,64) Tanner code 및 (2388,1793), (504,252), (5184,4322) 등 다양한 실제 코드에서 7-level(3비트) NLT FAID가 FER 10^-5 부근부터 floating-point BP를 능가, waterfall 손실은 미미.
10. 한계: column-weight-3 코드로 범위 한정, HW 구현/합성 없이 시뮬레이션 결과만 제시, 최적 FAID는 코드마다 후보군에서 재선택 필요(완전 범용 단일 맵 아님).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| VN 갱신 함수 Φv (유한알파벳 LUT, error-floor 개선) | `decoder.cpp` `VN_Cal_HD()` 등(HD/2SD/3SD), `decoder.h` `Get_VNU_*` | Prime ECC의 3SD(3비트) VN 처리 로직과 동일 정밀도대에서 LUT 교체로 직접 대응 가능 |
| CN min-sum 연산 Φc (기존과 동일 유지) | `decoder.cpp` `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | 변경 없이 그대로 사용되는 부분이라 이식 시 리스크 낮음 |
| iteration별 threshold 테이블 T={Ti} | `ecc_data.h` `PARAM_LLR`, `decoder.cpp` `Get_VNU_Table_Idx()` | 기존 적응형 LLR 테이블 구조와 유사한 형태로 threshold 삽입 가능 |
| trapping-set 기반 코드별 FAID 선택(오프라인 튜닝) | 대응 없음 | Prime ECC에는 코드별 offline TS 분석/LUT 선택 파이프라인이 없어 신규 튜닝 절차 필요 |

> 적용 가치: 높음 - CN 로직은 그대로 두고 VN LUT만 교체하는 최소침습 구조이며, Prime ECC가 이미 지원하는 soft-2~3bit 정밀도에 그대로 맞아 error-floor 개선을 저비용으로 시도할 수 있음.

### D. JSON 블록

```json
{
  "id": "arxiv:1207.4800v1",
  "title": "Finite Alphabet Iterative Decoders, Part I: Decoding Beyond Belief Propagation on BSC",
  "year": 2012,
  "venue": "arXiv",
  "portability": "상",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": "0.5~0.833",
  "code_length": "155~5184",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "BP/min-sum을 근사하지 않는 유한 알파벳(3비트) 변수노드 갱신 맵(FAID)을 trapping-set 기반으로 설계해 error floor에서 floating-point BP를 능가",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "상",
  "caveat": "column-weight-3 코드에 한정된 설계이며 FAID의 variable-node 갱신 맵은 code-independent 후보군에서 code별 브루트포스 시뮬레이션으로 최종 선택해야 함(온라인 자동 설계 아님)",
  "todo_check": "3비트(7-level) LUT 기반 Φv를 z=32 lifting 및 HCU/GT 파이프라인 구조에 이식 시 CN 연산(min-sum과 동일 Φc)은 그대로 두고 VN LUT만 교체 가능한지 검증 필요"
}
```
