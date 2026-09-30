### arxiv:1204.2577v1 - Reduced-Complexity Column-Layered Decoding and Implementation for LDPC Codes (2012, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5~0.875 |
| 부호length | 2304~4096 |
| 연판정 | soft-4bit+ |
| 핵심기여 | Min-Sum 기반 column-layered decoding의 중복 계산을 재구성·근사(3-min)로 최대 90%까지 절감하고 relaxed pipelining으로 고속화 |
| HW설계 | O |
| 검증수준 | ASIC합성 |
| 복잡도 | 6.755mm^2@0.13um |
| 병렬화 | 완전병렬 |
| Throughput | 3.928Gbps |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | column-layered 구조 전제(각 check node가 block column당 이웃 1개)라 Prime ECC의 row-layered/HCU 구조와 스케줄링 방식이 근본적으로 다름 |
| 추가확인 | 3-min 근사가 Prime ECC의 min1/min2 기반 CNU와 결합 가능한지, VN degree 17 구조에서 정렬벡터 길이 3 근사의 성능 손실 재검증 필요 |

> 총평: column-layered 스케줄링에 특화된 min-sum 근사·파이프라이닝 기법으로, row-layered 기반인 Prime ECC 3.1과 스케줄링 패러다임이 달라 직접 이식보다는 CNU 정렬-벡터 근사 아이디어 정도만 참고 가능.

### B. 알고리즘 요약

1. (N,K) binary LDPC, 부호는 G개 block column으로 분할되는 QC-LDPC 구조(예: (4096,3584) (4,32)-regular), N0..NG-1 그룹.
2. Column-layered decoding은 기존에도 있었으나 원 알고리즘은 매 layer마다 나머지 전체 block column에 대해 check node 연산을 반복해 계산량이 TPMP/row-layered보다 훨씬 큼.
3. Min-Sum을 column-layered에 최초로 결합하고, 알고리즘 재구성으로 연속 layer 간 `m_c^(g)`(check node에 모인 메시지 크기 정렬벡터)를 증분 갱신.
4. 핵심 변수: 정렬벡터 `m_c^(g)`(오름차순), 부호곱 `S_c^(g)`. `R_cv = S~_c^(g) × m1`로 check-to-variable 메시지 계산 (식 4-7).
5. `L_cv = I_v + α·Σ R_mv`, `L_v = I_v + α·Σ R_mv` (식 2,3), scaling factor `α=0.75`로 VLSI 친화적 근사.
6. 정렬벡터 길이를 3으로 제한하는 "three-min" 근사, 추가로 3번째 비교를 생략하는 "simplified three-min"으로 CNU 비교기 수를 `d_c-2`에서 2개로 축소(최대 90%대 절감, (4,32) 코드 기준 93%).
7. Relaxed pipelining: `m_c^(g-1)`을 `m_c^(g-1+P)`의 근사치로 사용해 P사이클 지연 허용, `Get R_cv` 컴포넌트로 layer g+P 메시지 선계산.
8. 별도 학습/최적화 절차 없음(수치 시뮬레이션만).
9. (4096,3584) (4,32) QC-LDPC 기준 10 iteration에서 388MHz 클록으로 throughput 3.928Gbps, 0.13um 6.755mm^2, simplified three-min은 표준 대비 0.02dB 성능 손실.
10. row-layered 대비 CNU 구조가 간단해지나 column-layered 고유의 loop(CNUa-CNUb, Get_Rcv-VNU) 구조 의존; error-floor/정정능력 개선은 다루지 않고 순수 구현 복잡도·throughput 최적화에 국한.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Min-Sum CN 정렬벡터 근사(3-min) | `decoder.cpp` `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | min1/min2 기반 CNU와 유사 아이디어이나 3-min 확장은 column-layered 전용 정렬벡터 구조 |
| column-layered 스케줄링/pipeline | `decoder.cpp` `LDPC_Decoder()` | Prime ECC는 row 단위(z_sb=32) 병렬 구조로 스케줄링 패러다임 상이, 직접 대응 어려움 |
| scaling factor α=0.75 근사 | `ecc_data.h` `PARAM_LLR` | 유사 개념(정규화 min-sum)이나 이미 자체 양자화 테이블 보유 |
| relaxed pipelining(Get_Rcv) | `decoder.cpp` pipeline 6-stage (col_M1/Z/P1~P4) | 이미 6-stage 파이프라인 보유, 신규 기법 아님 |
| 인코딩/부호설계 | (대응 없음) | 논문은 인코더·H-matrix 설계 다루지 않음 |

적용 가치: **낮음** — column-layered 전용 스케줄링·정렬벡터 근사로 이미 min-sum/HCU/파이프라인을 보유한 row-layered 기반 Prime ECC와 구조적으로 상이하며, 정정능력 개선도 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1204.2577v1",
  "title": "Reduced-Complexity Column-Layered Decoding and Implementation for LDPC Codes",
  "year": 2012,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": "0.5~0.875",
  "code_length": "2304~4096",
  "soft_quant": "soft-4bit+",
  "key_contribution": "Min-Sum 기반 column-layered decoding의 중복 계산을 재구성·근사(3-min)로 최대 90%까지 절감하고 relaxed pipelining으로 고속화",
  "hw_designed": "O",
  "verification": "ASIC합성",
  "complexity": "6.755mm^2@0.13um",
  "parallelism": "완전병렬",
  "throughput_gbps": 3.928,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "중",
  "caveat": "column-layered 구조 전제(각 check node가 block column당 이웃 1개)라 Prime ECC의 row-layered/HCU 구조와 스케줄링 방식이 근본적으로 다름",
  "todo_check": "3-min 근사가 Prime ECC의 min1/min2 기반 CNU와 결합 가능한지, VN degree 17 구조에서 정렬벡터 길이 3 근사의 성능 손실 재검증 필요"
}
```
