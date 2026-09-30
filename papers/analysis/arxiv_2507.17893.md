### arxiv:2507.17893v2 - Action-List Reinforcement Learning Syndrome Decoding for Binary Linear Block Codes (2025, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.41 |
| 부호length | 155 |
| 연판정 | hard-1bit |
| 핵심기여 | DQN 기반 syndrome bit-flipping RL 복호 + action-list(beam) + 기존 복호기 실패 영역 보정하는 feedback + automorphism 활용 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | BSC hard-decision·짧은/저rate 코드 전용, DQN 추론(NN+beam 탐색)이라 NAND HW min-sum 파이프라인 이식 부담 큼 |
| 추가확인 | soft-read(2SD/3SD) 및 고rate NAND QC-LDPC로의 일반화·상태공간 폭증 여부, feedback을 min-sum 뒤단 post-processing으로 근사 가능한지 |

> 총평: BSC 하드판정 짧은 코드용 DQN RL bit-flipping/feedback 복호로 error-floor를 개선하나, NN 추론·beam 탐색 기반이라 고rate NAND soft-read min-sum HW에 그대로 이식 곤란.

### B. 알고리즘 요약

1. 대상: binary linear block code(주로 QC-LDPC, Tanner `(155,64,20)` 및 random `(24,6,10)`), BSC 하드판정 채널 `y=(1-2c)+z`, `z~Bernoulli(ρ)`.
2. 문제: 짧은/저rate 코드에서 BP·OSD 성능이 ML에 못 미침 → 복호를 MDP로 보고 RL로 최적 bit-flip 정책 학습.
3. MDP 정의: 상태 = 신드롬(`s0=yH^T`), 행동 = 뒤집을 비트 `A={1..n}`, 전이 `s'=s+h_ca`(결정적), 종단 = 전영 신드롬, 보상 `R=-1/L(+1 if 종단)`으로 최소 flip 유도.
4. Truncated MDP: 코드워드 주변 반경 `w` Hamming ball `B(w)`로 상태를 `Σ_{i=0}^w C(n,i)`로 축소(bounded-distance decoding에 대응), 경계밖 전이엔 `-1` 페널티.
5. Q-learning/DQN: `Q(s,a)` 업데이트(식6), 복잡도 `O(|S|·|A|^2)=O(n^2·2^{n-k})`; DQN은 은닉층 512뉴런 NN + replay memory + target network로 근사.
6. 유한지평 보상 분석: `Q(j)=γ^{j-1}r-(1-γ^j)/(1-γ)p`, γ 조절로 원거리 상태 학습성 vs 초기 상태 구분성 트레이드오프.
7. Action-list decoding(핵심): DQN Q-value 상위 `k`개 행동으로 beam search, `Q(s_l,a)>v_i` 조건 개선 경로만 확장·상위 `k` pruning(`Dmax` 깊이). 진동 수렴실패 완화, list size↑ 시 성능↑.
8. Feedback decoder: 기존 복호기 Φ(예: bit-flipping)의 실패영역 `R_Φ^f` 신드롬만 대상으로 RL block 학습, `D`회 순차 적용해 correctable region 확장. 정정능력 하한 정리 제시.
9. Automorphism: QC-LDPC(circulant `p×p`, `p` 소수) 자기동형군(가법 `Z_p`+승법 부분군)으로 신드롬 대칭 이용, Burnside/Booth로 unique state 수 축소·다양성 확보.
10. 결과·한계: Tanner code에서 list=5+automorphism이 BDD(radius10)에 근접, feedback이 error-floor FER 개선. 단 HW 미설계·시뮬만, BSC 하드판정·짧은 코드 전용, `w≥4`에서 상태공간 폭증.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| DQN syndrome bit-flipping 복호 | 대응 없음 | Prime ECC는 min-sum 메시지 패싱이며 NN/RL 복호 미보유 |
| Feedback 복호(실패영역 후처리) | decoder.cpp `LDPC_Decoder()` 이터레이션 루프 | 개념상 조기종료 후 post-processing과 유사하나 RL block 이식은 별개 |
| action-list(beam) 탐색 | 대응 없음 | min-sum 파이프라인에 리스트/beam 탐색 구조 없음 |
| QC-LDPC automorphism 활용 | ecc_top.cpp `Load_PCM()` (H-matrix) | 우리 부호도 QC지만 특정 H 고정·자기동형 재배치 미지원 |

적용 가치: **낮음** — DQN NN 추론과 beam 탐색에 의존하는 BSC 하드판정 복호라, 고rate NAND soft-read min-sum HW 파이프라인(Prime ECC 3.1)에는 error-floor 개선 아이디어(feedback post-processing)만 개념적 참고 가치가 있고 직접 이식은 어렵다.

### D. JSON 블록

```json
{
  "id": "arxiv:2507.17893v2",
  "title": "Action-List Reinforcement Learning Syndrome Decoding for Binary Linear Block Codes",
  "year": 2025,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": 0.41,
  "code_length": "155",
  "soft_quant": "hard-1bit",
  "key_contribution": "DQN 기반 syndrome bit-flipping RL 복호 + action-list(beam) + 기존 복호기 실패 영역 보정하는 feedback + automorphism 활용",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "악화",
  "recommend": "하",
  "caveat": "BSC hard-decision·짧은/저rate 코드 전용, DQN 추론(NN+beam 탐색)이라 NAND HW min-sum 파이프라인 이식 부담 큼",
  "todo_check": "soft-read(2SD/3SD) 및 고rate NAND QC-LDPC로의 일반화·상태공간 폭증 여부, feedback을 min-sum 뒤단 post-processing으로 근사 가능한지"
}
```
