### arxiv:2411.19092v2 - Neural Window Decoder for SC-LDPC Codes (2026, IEEE (arXiv preprint, cs.LG))

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | SC-LDPC |
| 부호rate | 미상 |
| 부호length | 20000 |
| 연판정 | 무관 |
| 핵심기여 | SC-LDPC window decoder에 학습형 CN 가중치·damping을 도입한 최초 neural window decoder(target-specific 학습+neural 비균일 스케줄+EP-resilient 적응) |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | SC-LDPC/window decoding 구조 전제 - block QC-LDPC(Prime ECC)에 그대로 이식 불가, neural 가중치 학습 파이프라인 필요 |
| 추가확인 | target-specific 학습·비균일 스케줄 아이디어를 window 구조 없이 block QC-LDPC min-sum 가중치/스케줄에 재해석 가능한지 |

> 총평: SC-LDPC window decoder 전용 neural min-sum 기법으로 NAND block QC-LDPC로의 직접 이식성은 낮으나, 학습형 가중치·CN skip 스케줄 개념은 참고 가치 있음.

### B. 알고리즘 요약 (10줄 내외)

1. 대상은 protograph 기반 `(3,6)-regular SC-LDPC` 부호(`Ln=20000`, `L=100`, `z=100`)를 window decoding(`W`, target `T`)으로 복호하는 시스템.
2. 문제: 기존 WD는 고정가중, 비균일 스케줄은 online BER 추정 오버헤드, EP(error propagation) 취약 - 성능/복잡도/EP 3측면 개선 필요.
3. 채널은 AWGN, 복호는 neural min-sum(`m_c→v = w_c^(ℓ)·∏sgn·min|m_v→c|`)로 CN 메시지에 학습 가중치 `w_C^(ℓ)`를 곱함.
4. 핵심1 target-specific 학습: 손실을 window 앞 `T`개 target VN에만 한정(`L_T`) → 신경망 구조적 pruning, 가중치/노드 대폭 감소.
5. 의미: window마다 구조 반복 → 단일 window만 학습해도 전체 chain 재사용, 긴 부호 학습 불가 문제 회피.
6. 핵심2 neural 비균일 스케줄: 학습형 damping `γ_C^(ℓ)`로 CN 업데이트 중요도 정량화, target 도달 경로수로 정규화한 schedule importance로 낮은 CN skip.
7. 트릭: damping은 스케줄 결정에만 쓰고 실제 복호는 plain NWD로 수행(추가 메모리/런타임 오버헤드 제거).
8. 핵심3 adaptive NWD: EP 시나리오용 EP-resilient 가중치를 boosting learning으로 학습, 이전 window의 UCN(unsatisfied CN) 검출 시 전환.
9. 결과: WD 대비 FER 3배 개선(또는 복잡도 45% 감소), target-specific이 WD보다 낮은 복잡도로 FER 3배↓, adaptive가 EP 확률 0.781→0.642, BLER 35%↓.
10. 한계: HW 미설계(연산량은 Horowitz energy model 계산뿐), SC-LDPC/window 구조 전제, AWGN 시뮬만.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| neural min-sum CN 가중치 `w_C^(ℓ)` | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | min-sum CN 연산 위치는 대응하나 학습 가중치 개념 자체는 우리에 없음 |
| iteration별 가중치/스케줄 | decoder.cpp `Get_VNU_Table_Idx()`, ecc_data.h `PARAM_LLR` | iteration 구간별 테이블 구조는 유사하나 window 스케줄은 대응 없음 |
| UCN 기반 조기검출/전환 | partial_CRC.cpp `partial_crc_HW_T4()`, full_CRC.cpp | 조기종료용 parity 검사와 유사 아이디어이나 window 간 전환 개념은 대응 없음 |
| CN update skip(비균일 스케줄) | GT.cpp `Make_GT_HW()` | edge 축소(graph thinning)와 목적 유사하나 SC-LDPC window 전용이라 직접 이식 불가 |
| SC-LDPC 부호구조/window | 대응 없음 | Prime ECC는 block QC-LDPC 고정, SC-LDPC 미지원 |
| neural/딥러닝 디코더 학습 | 대응 없음 | NN 기반 학습 파이프라인 부재 |

적용 가치: **낮음** - SC-LDPC window decoding 구조에 밀착된 neural 기법이라 block binary QC-LDPC인 Prime ECC에 직접 이식 불가하며, 우리가 이미 보유한 min-sum/조기종료와 상당 부분 중복된다.

### D. JSON 블록

```json
{
  "id": "arxiv:2411.19092v2",
  "title": "Neural Window Decoder for SC-LDPC Codes",
  "year": 2026,
  "venue": "IEEE (arXiv preprint, cs.LG)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "SC-LDPC",
  "code_rate": null,
  "code_length": "20000",
  "soft_quant": "무관",
  "key_contribution": "SC-LDPC window decoder에 학습형 CN 가중치·damping을 도입한 최초 neural window decoder(target-specific 학습+neural 비균일 스케줄+EP-resilient 적응)",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "하",
  "caveat": "SC-LDPC/window decoding 구조 전제 - block QC-LDPC(Prime ECC)에 그대로 이식 불가, neural 가중치 학습 파이프라인 필요",
  "todo_check": "target-specific 학습·비균일 스케줄 아이디어를 window 구조 없이 block QC-LDPC min-sum 가중치/스케줄에 재해석 가능한지"
}
```
