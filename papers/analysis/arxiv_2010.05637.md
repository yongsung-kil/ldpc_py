### arxiv:2010.05637v2 - Learning to Decode: Reinforcement Learning for Decoding of Sparse Graph-Based Channel Codes (2020, NeurIPS 2020)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 미상 |
| 부호length | 196 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 클러스터 기반 Q-learning으로 sequential CN scheduling 정책을 학습해 flooding/기존 NS 대비 BER과 메시지 전달 횟수(복잡도)를 동시에 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 없음 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | 오프라인 Q-learning 학습(고정 H 전용, ℓmax=25, n=196 짧은 코드) 및 순차(sequential) CN 스케줄링이라 완전병렬 HW 구조와 상충 |
| 추가확인 | 학습된 정책을 고정 H-matrix가 아닌 QC-LDPC 다양한 rate/length에 재학습 없이 일반화 가능한지 |

> 총평: 순차(sequential) CN 스케줄링 기반 RL 최적화로, flooding 병렬 아키텍처를 쓰는 NAND LDPC HW 디코더에는 구조적으로 이식이 어려움.

### B. 알고리즘 요약

1. 대상: (j,k)-regular 및 array-based(AB-) LDPC 짧은 코드(`n=196`), BP 반복복호를 flooding이 아닌 순차(sequential) CN 스케줄링으로 수행.
2. 문제: 기존 node-wise scheduling(NS)은 residual `r_{a→v}=|m'_{a→v}-m_{a→v}|` 실시간 계산 비용이 커서 flooding보다 연산량이 큼.
3. 채널 모델: AWGN, `y_i=(-1)^{x_i}+z`, `z~N(0,σ²)`, 채널 LLR `L_i`.
4. 핵심 기법: CN 스케줄링을 m-armed bandit MDP로 모델링, Q-learning으로 action-value function 학습. 상태는 CN별 quantized soft syndrome `s_ℓ(j)=g_M(ŝ_ℓ(j))`.
5. 핵심 식: `Q_{ℓ+1}(s_u,a_u)=(1-α)Q_ℓ(s_u,a_u)+α[R_ℓ+β max Q_ℓ(...)]` — 상태공간 폭발을 막기 위해 CN을 크기 `z`의 클러스터로 묶어 클러스터별 별도 상태/행동공간 사용.
6. 확장 기법: cluster-connecting set(CCS) 정의 후, 클러스터 내부 short cycle(κ-cycle, 예 κ=6)을 최대화하는 방향으로 클러스터를 구성(MQO)해 클러스터 간 의존성(상태공간 결합)을 최소화.
7. 구현 디테일: CN 상태는 M-level scalar quantization(`M=4`)로 이산화, ε-greedy 행동선택(`ε=0.6`).
8. 학습 절차: 클러스터별 Q-learning을 `|L|=1.25×10^6` 채널 샘플에 대해 `ℓ_max=25` 반복으로 학습(`α=0.1, β=0.9, z=7`).
9. 결과: (3,7) AB-LDPC/(3,6)-regular, `n=196`에서 MQO가 flooding·MGI·NS·MQC·MQR 대비 BER 최저, SNR 0.5dB 기준 평균 CN→VN 메시지 수 264(367) vs flooding 27040(27913)로 대폭 감소.
10. 한계: 순수 시뮬레이션(HW 미설계), 매우 짧은 코드 길이(196)에서만 검증, 순차 스케줄링 특성상 flooding 기반 완전병렬 HW와 근본적으로 다른 아키텍처 요구.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 순차 CN 스케줄링(Q-learning 기반) | 대응 없음 | Prime ECC는 flooding 기반 병렬 pipeline(`decoder.cpp`)이며 순차 스케줄링 구조 자체가 없음 |
| CN 상태 quantization / soft syndrome | `channel.cpp` `Set_LLR_Th()` | 개념적으로 LLR quantization과 유사하나 스케줄링 목적이 달라 직접 이식 어려움 |
| 반복 메시지 감소(조기 수렴) | `partial_CRC.cpp` `partial_crc_HW_T4()` | 목적(반복 수 감소)은 유사하나 메커니즘(조기종료 vs 스케줄링 학습)은 무관 |

> 적용 가치: 낮음 — 순차 스케줄링과 오프라인 RL 학습이 Prime ECC의 flooding 기반 완전병렬 pipeline HW 구조와 근본적으로 상충하며, 짧은 코드(n=196)에서만 검증되어 NAND급 QC-LDPC로의 확장성도 미확인.

### D. JSON 블록

```json
{
  "id": "arxiv:2010.05637v2",
  "title": "Learning to Decode: Reinforcement Learning for Decoding of Sparse Graph-Based Channel Codes",
  "year": 2020,
  "venue": "NeurIPS 2020",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": null,
  "code_length": "196",
  "soft_quant": "soft-4bit+",
  "key_contribution": "클러스터 기반 Q-learning으로 sequential CN scheduling 정책을 학습해 flooding/기존 NS 대비 BER과 메시지 전달 횟수(복잡도)를 동시에 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "없음",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "하",
  "caveat": "오프라인 Q-learning 학습(고정 H 전용, ℓmax=25, n=196 짧은 코드) 및 순차(sequential) CN 스케줄링이라 완전병렬 HW 구조와 상충",
  "todo_check": "학습된 정책을 고정 H-matrix가 아닌 QC-LDPC 다양한 rate/length에 재학습 없이 일반화 가능한지"
}
```
