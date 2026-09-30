### arxiv:2004.06875v1 - On Cyclic Polar Codes and the Burst Erasure Performance of Spatially-Coupled LDPC Codes (2015, Texas A&M M.S. Thesis / arXiv 2020)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 랜덤 규칙 (dv,dc,w,L,M) SC-LDPC 앙상블의 burst-erasure 채널(BEC 기반) 블록소거확률에 대한 타이트한 하한을 stopping-set 개수로 유도 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | Binary Erasure Channel(BEC) 상 stopping-set 이론 분석 전용이며 AWGN/NAND read-noise 채널이나 soft-decision 디코딩과 무관 |
| 추가확인 | 본문은 이 논문의 두 독립 파트(2장 cyclic polar codes, 3장 SC-LDPC burst erasure) 중 LDPC 관련 3장만을 근거로 판정함 |

> 총평: 순수 확률·조합론 기반 BEC 상 SC-LDPC 앙상블 성능(stopping set) 이론 분석 논문으로, NAND 고전 binary LDPC ECC(디코더/HW) 이식 가치는 낮음.

### B. 알고리즘 요약

1. 대상은 규칙적 `(dv, dc, w, L, M)` 랜덤 SC-LDPC 앙상블(코드율 `r = 1 - dv/dc - δ`, `δ=O(w/L)`)이며 채널은 이진소거채널(BEC) 및 그 변형인 burst-erasure 채널.
2. 기존 SC-LDPC 연구는 AWGN/BEC 하 threshold saturation에 집중했고, 실제 응용(슬롯 ALOHA 충돌, block-fading, 편광의존손실 등)에서 발생하는 연속된 burst 소거에 대한 유한장 성능 분석이 부족함이 문제의식.
3. 채널 모델은 두 가지: 한 spatial position(SP)의 M개 VN 전체를 소거하는 SPBC(Single Position Burst Channel)와, 임의 시작점·길이의 연속 소거를 모델링하는 RBC(Random Burst Channel, `RBC(ℓ,s,b)`).
4. 핵심 기법은 BP(peeling) 디코더 실패의 지배적 원인인 size-2 stopping set 개수(`N_S2P`, SP당 평균)를 통해 `P_B^SPBC`의 하한을 유도.
5. `P_B^SPBC = Prob[최소 1개 stopping set 존재]`이며, 이는 size-2 stopping set 발생 확률의 조합적 계산으로 근사되고 M이 커질수록 하한이 tight해짐.
6. RBC로 확장 시 결합된 SP 간 size-2 stopping set 분포(타입 벡터 `t=(t0,...,t_{w-1})` 기반)를 이용해 burst 길이 `b`에 대한 근사식을 유도.
7. BEC 상 error floor는 `N_H2`(전체 그래프의 size-2 stopping set 개수)의 분포(포아송 근사)로 특성화.
8. 확장(expurgation) 기법: 코드 생성 시 size-2 stopping set이 없는 그래프만 채택하여(minimal stopping set size 증가) `P_B^SPBC`를 수 자릿수 개선.
9. 결과: dv를 1 늘리면 성능이 `M^{-dv}` 수준으로 개선됨을 Monte-Carlo로 확인했으나(수치 곡선은 그림 위주라 본문 확정치 없음), 모든 결과는 Monte-Carlo 시뮬레이션으로 검증.
10. 한계: 결과는 모두 BEC(소거)/이론 해석 한정이며 HW 설계, AWGN soft-decision, iterative min-sum 디코더 구현은 다루지 않음. dv≥3, w≥dv 조건에서만 bound가 tight.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| BEC 상 stopping-set 기반 burst-erasure 성능 분석 | 대응 없음 | Prime ECC는 binary QC-LDPC 고정 부호이며 채널도 AWGN/RBER/fixed-error(`channel.cpp`)로, 순수 BEC 랜덤 앙상블 이론과 직접 대응 모듈 없음 |
| 랜덤 규칙 (dv,dc,w,L,M) SC-LDPC 앙상블 구성/확장(expurgation) | `ecc_top.cpp` `Load_PCM()` | Prime ECC는 특정 QC-LDPC H-matrix 고정, 랜덤 앙상블 재구성은 이식 난이도 높음(§4 표) |
| 소거채널(peeling BP) 디코딩 | 대응 없음 | Prime ECC 디코더는 min-sum 기반 hard/soft LLR 디코딩(`decoder.cpp`)이며 소거채널 peeling 디코더와 무관 |

> 적용 가치: **낮음** — BEC 전용 이론 분석이며 NAND ECC가 겪는 AWGN/read-noise soft-decision 환경과 채널 모델이 다르고, 부호구성도 특정 QC-LDPC 고정인 Prime ECC와 직접 연결점이 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2004.06875v1",
  "title": "On Cyclic Polar Codes and the Burst Erasure Performance of Spatially-Coupled LDPC Codes",
  "year": 2015,
  "venue": "Texas A&M M.S. Thesis (arXiv 2020)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "랜덤 규칙 (dv,dc,w,L,M) SC-LDPC 앙상블의 burst-erasure 채널(BEC 기반) 블록소거확률에 대한 타이트한 하한을 stopping-set 개수로 유도",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "Binary Erasure Channel(BEC) 상 stopping-set 이론 분석 전용이며 AWGN/NAND read-noise 채널이나 soft-decision 디코딩과 무관",
  "todo_check": "본문은 이 논문의 두 독립 파트(2장 cyclic polar codes, 3장 SC-LDPC burst erasure) 중 LDPC 관련 3장만을 근거로 판정함"
}
```
