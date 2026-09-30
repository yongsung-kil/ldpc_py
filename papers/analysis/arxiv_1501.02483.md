### arxiv:1501.02483v3 - Design of LDPC Codes Robust to Noisy Message-Passing Decoding (2015, arXiv (IEEE Trans. Commun. 관련))

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 10000 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 디코더 내부 노이즈(아날로그 VLSI 회로/양자화 유래)를 메시지에 더해지는 AWGN으로 모델링하고, 2차원(평균+분산) density evolution과 noisy EXIT chart 분석으로 이 노이즈에 강건한 irregular LDPC 차수분포를 설계 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 아날로그 VLSI soft-gate 디코더(analog transistor circuit)의 연속값 내부 노이즈를 대상으로 하며, Prime ECC 같은 디지털 고정소수점 양자화 min-sum 회로의 노이즈(결정론적 라운딩)와 노이즈 모델 자체가 다름 |
| 추가확인 | 디지털 min-sum 회로의 quantization 오차를 이 논문의 AWGN 내부노이즈 모델로 근사할 수 있는지, 가능하다면 강건 차수분포 설계 방법론이 Prime ECC의 고정 QC-LDPC 구조에도 재현 가능한지 |

> 총평: 아날로그 VLSI 디코더의 내부 회로 노이즈를 채널 노이즈처럼 다루는 확장 density evolution/EXIT 프레임워크는 이론적으로 흥미로우나, 대상이 analog soft-gate 회로이고 검증도 rate 0.5 무한장 앙상블/유한장(N=10^4) 시뮬에 그쳐 Prime ECC의 디지털 고rate QC-LDPC 이식성은 낮음.

### B. 알고리즘 요약

1. 채널은 AWGN(BPSK), 코드는 regular `(dv,dc)=(3,6)` 및 irregular LDPC, rate `r=0.5`, 유한장 검증은 `N=10^4~10^3` 수준.
2. 문제의식: sum-product 디코더를 디지털(양자화) 또는 아날로그(soft-gate VLSI) 회로로 구현하면 노드 간 교환 메시지(LLR)에 내부 노이즈가 실려 성능 저하가 발생, 이를 채널처럼 다뤄 강건하게 설계하고 싶음.
3. 핵심 가정: variable/check node 출력 메시지에 각각 독립 i.i.d. AWGN `n_i, ν_j ~ N(0, σ_d^2)`가 더해짐(`μ_i(l)=u_i(l)+n_i`, `γ_j(l)=v_j(l)+ν_j`).
4. 핵심 기법 1단: 노이즈 있는 디코더는 "consistency"(분산=2×평균) 가정이 깨지므로, 메시지 밀도의 평균 `m`과 분산 `σ²`을 동시에 추적하는 2차원 density evolution을 유도(`(7)`,`(11)`,`(17)`,`(19)-(21)`).
5. 핵심 식: check node DE `f(m_u,σ_u²)=f(m_v,σ_v²+σ_d²)^{dc-1}` — 이 식이 내부노이즈 `σ_d²`를 check node 갱신에 직접 반영해 문턱값(threshold) 열화를 정량화.
6. 핵심 기법 2단: consistency가 깨져 기존 J-function 기반 EXIT 계산이 불가하므로, 노이즈를 포함한 실제 mutual information을 몬테카를로 시뮬로 계산하는 "noisy EXIT curve" 알고리즘(Algorithm 1, NVND/NCND)을 제안.
7. 부수 트릭: 각 노드를 독립적으로 시뮬레이션하고 consistency를 입력 단계에서만 임시 가정(step 6)해 근사 정확도를 확보.
8. 최적화 절차(Algorithm 2): check 차수분포를 두 연속 차수(`αx^{dc-1}+(1-α)x^{dc}`)로 제한하고, 주어진 `σ_d²`에서 SNR 문턱값을 점진적으로 낮춰가며 `IE,NVND ≻ IA,NCND` 제약을 만족하는 variable 차수분포 `λ(x)`를 탐색.
9. 결과: `σ_d²=1`일 때 무노이즈 대비 SNR 문턱값 약 2.5dB 열화; 설계된 Code A(`σ_d²=0.5` 대상)가 기존 노이즈없는 최적 코드([29] 코드) 대비 노이즈 하 성능 우수(도달 SNR 개선, waterfall 영역).
10. 한계: 아날로그 soft-gate VLSI 회로 또는 단순 AWGN 근사 양자화 노이즈만 다루며, HW gatecount/throughput/디지털 min-sum 구현 세부는 전혀 없고 최대 iteration 80회 시뮬 수준.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 내부 디코더 노이즈(AWGN) 모델 | `decoder.cpp` `LDPC_Decoder()`, `CNU_Update_New_Mag()` | Prime ECC는 고정소수점 양자화 min-sum이라 결정론적 라운딩 오차이며, 이 논문의 연속 AWGN 노이즈 모델과 성격이 다름 — 직접 대응 어려움 |
| 노이즈 강건 차수분포 설계(Algorithm 2) | `ecc_top.cpp` `Load_PCM()` | H-matrix/차수분포를 바꾸는 부호설계 영역이나, 이 논문은 rate 0.5 랜덤 irregular 앙상블 대상으로 Prime ECC의 고정 QC-LDPC(rate~0.9) 재검증 부담 큼 |
| 2차원(평균+분산) density evolution | 대응 없음 | Prime ECC는 시뮬레이터이지 부호설계 최적화 툴이 아니므로 DE 분석 자체가 대응되는 모듈 없음 |

> 적용 가치: 낮음 — 대상이 아날로그 VLSI 회로 노이즈이고 rate 0.5 랜덤 앙상블 이론 검증 수준이라, Prime ECC의 디지털 고정소수점 min-sum·고rate QC-LDPC 구조와 노이즈 모델·부호 스펙 모두 괴리가 큼.

### D. JSON 블록

```json
{
  "id": "arxiv:1501.02483v3",
  "title": "Design of LDPC Codes Robust to Noisy Message-Passing Decoding",
  "year": 2015,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": 10000,
  "soft_quant": "soft-4bit+",
  "key_contribution": "디코더 내부 노이즈를 AWGN으로 모델링하고 2차원 density evolution + noisy EXIT chart로 이에 강건한 irregular LDPC 차수분포를 설계",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "아날로그 VLSI soft-gate 디코더의 연속값 내부 노이즈를 대상으로 하며, 디지털 고정소수점 min-sum 회로의 결정론적 양자화 오차와 노이즈 모델이 다름",
  "todo_check": "디지털 min-sum 회로의 quantization 오차를 이 논문의 AWGN 내부노이즈 모델로 근사할 수 있는지, 강건 차수분포 설계가 Prime ECC 고정 QC-LDPC에 재현 가능한지"
}
```
