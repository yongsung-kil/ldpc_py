### arxiv:0705.1345v1 - Degree Optimization and Stability Condition for the Min-Sum Decoder (2007, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | code-design |
| 부호종류 | irregular |
| 부호rate | 0.3~0.9 |
| 부호length | 미상 |
| 연판정 | soft-4bit+ |
| 핵심기여 | Min-Sum 복호의 안정 조건 유도(BP와 동일 형태) 및 EXIT chart 기반 degree distribution 최적화로 MS 전용 코드 설계 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | asymptotic(무한 block length) density evolution 기반 이론 분석으로 유한길이/HW 실측 없음. scaled min-sum(α=1.25)은 이미 보유 기법과 중복 |
| 추가확인 | scaled min-sum의 α 최적화가 Prime ECC의 magnitude 양자화 테이블 설계에 참고 가능한지 확인 |

> 총평: Min-Sum 자체의 안정성·최적 degree distribution을 다루는 순수 이론 논문으로, MS 전용 코드 설계 통찰은 유효하나 HW/유한길이 검증이 전혀 없어 즉시 이식성은 중간 수준.

### B. 알고리즘 요약

1. BMS(binary memoryless symmetric) 채널, 특히 biAWGN 채널에서 무한 block length LDPC 앙상블(λ(x), ρ(x))의 Min-Sum(MS) 복호를 density evolution으로 분석.
2. 문제: BP(sum-product)는 안정조건·degree distribution 최적화가 잘 연구됐지만 MS는 상대적으로 미해결 상태 — MS 전용 최적 코드 설계와 안정성 조건이 불명확.
3. 채널모델: check-to-bit 갱신은 `L_b = (1/α)·sign(prod)·min|L|` (α=1이면 표준 MS, α>1이면 scaled/modified MS), all-zero codeword 가정 density evolution.
4. 핵심 결과 1 (안정조건): `B(a_ch)·λ'(0)·ρ'(1) < 1` (Bhattacharyya parameter 기반)이면 밀도가 error-free density로 수렴 — 이는 BP의 안정조건(Richardson-Urbanke)과 형태가 동일함을 증명.
5. 이 조건이 필요충분에 가까운 이유: Bhattacharyya parameter `B(a)=∫a(x)e^{-x/2}dx`가 variable node convolution에서 multiplicative하기 때문(Lemma 3: `B(c) ≤ B(a)+B(b)`).
6. 핵심 기법 2단: EXIT chart 기반 반복적 degree distribution 최적화(선형계획법) — 이전 스텝의 실제 density evolution 출력을 이용해 λ(x)/ρ(x)를 번갈아 갱신, MS 안정조건(9)을 LP 제약으로 포함.
7. 구현 디테일: λ 최적화 시 `-δ ≤ λ_i - λ_old,i ≤ δ` 로 한 스텝 변화폭 제한, EXIT 곡선 간극을 β로 조절해 실제 density evolution 수렴을 매 스텝 확인.
8. 학습/최적화 절차: EXIT chart + density evolution 결합 LP 반복(2 서브스텝: λ 고정 ρ 최적화 → ρ 고정 λ 최적화), rate 증가가 멈추면 종료.
9. 결과: MS 최적화 코드는 rate 0.3에서 capacity 대비 gap 1dB, rate 0.9에서 0.4dB(단조 감소). Scaled MS(α=1.25)는 gap이 0.75dB~0.2dB로 다소 개선. BP용 코드를 MS로 복호하면 gap이 0.97dB 더 나쁨(rate 0.5 비교).
10. 한계: 무한 block length 점근 분석뿐이며 유한길이 코드·HW 구현·실측 전혀 없음. Variable node 측 밀도 대칭성 증명은 미해결로 남겨둠(open question).

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Min-Sum 안정조건(수렴 보장) | decoder.cpp `LDPC_Decoder()` | 참고용 이론적 배경, 코드 구현체엔 직접 반영 요소 없음 |
| Scaled Min-Sum (α 스케일) | decoder.cpp `CNU_Update_New_Mag()` | Prime ECC의 magnitude 양자화 테이블과 유사 개념이나 논문은 이론적 α값 산출뿐, 이미 보유 기법과 중복 |
| MS 전용 degree distribution 최적화 | ecc_top.cpp `Load_PCM()` | 부호설계(H-matrix) 레이어, Prime ECC는 QC-LDPC 고정구조라 무한길이 irregular 앙상블 최적화 결과를 그대로 이식하기 어려움 |
```

> 적용 가치: 낮음 — MS 복호의 이론적 한계와 안정조건을 규명한 학술적 가치는 있으나, 무한길이 점근 분석이며 HW/유한길이 실증이 없어 Prime ECC(유한길이 QC-LDPC, HW bit-exact)에 직접 이식할 구체적 산출물이 부족함.

### D. JSON 블록

```json
{
  "id": "arxiv:0705.1345v1",
  "title": "Degree Optimization and Stability Condition for the Min-Sum Decoder",
  "year": 2007,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "code-design",
  "code_type": "irregular",
  "code_rate": "0.3~0.9",
  "code_length": null,
  "soft_quant": "soft-4bit+",
  "key_contribution": "Min-Sum 복호의 안정 조건 유도(BP와 동일 형태) 및 EXIT chart 기반 degree distribution 최적화로 MS 전용 코드 설계",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "asymptotic(무한 block length) density evolution 기반 이론 분석으로 유한길이/HW 실측 없음. scaled min-sum(α=1.25)은 이미 보유 기법과 중복",
  "todo_check": "scaled min-sum의 α 최적화가 Prime ECC의 magnitude 양자화 테이블 설계에 참고 가능한지 확인"
}
```
