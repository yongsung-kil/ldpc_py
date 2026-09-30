### arxiv:1205.5729v2 - Blind Reconciliation (2013, Quantum Information and Computation)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | irregular |
| 부호rate | 0.5~0.8 |
| 부호length | 2000~10000 |
| 연판정 | 무관 |
| 핵심기여 | QKD 정보조정(information reconciliation)을 위해 사전 오류율 추정 없이 puncturing/shortening 비율을 반복적으로 조정하는 blind rate-adaptive LDPC 프로토콜 제안 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 채널이 BSC(양자키분배 특유의 오류모델), syndrome coding 기반 통신 프로토콜로 NAND read channel/디코더 HW와 목적 자체가 다름 |
| 추가확인 | Prime ECC는 오류정정 목적 디코더이고 이 논문은 협상형 syndrome 프로토콜이라 이식 대상 모듈 자체가 존재하지 않음 |

> 총평: QKD 정보조정을 위한 rate-adaptive/blind syndrome coding 프로토콜 논문으로, LDPC를 사용하지만 오류정정 디코더 자체보다는 통신 프로토콜(반복적 puncturing→shortening 전환)에 초점이 있어 NAND ECC 이식 가치가 없음.

### B. 알고리즘 요약

1. 시스템: QKD에서 Alice/Bob이 상관된 문자열 X, Y (BSC(ε) 특성)를 syndrome coding으로 일치시키는 information reconciliation 문제, 짧은 길이(`n=2×10^3`, 일부 `10^4`) LDPC 사용.
2. 풀려는 문제: 기존 rate-adaptive LDPC(순수 puncturing+shortening, 비대화형)는 짧은 코드에서 효율(efficiency) `f`가 나쁘고, Cascade는 상호작용이 많아 고속 QKD의 병목이 됨.
3. 핵심 모델: BSC(ε) 채널, 사전 오류율(QBER) 추정 없이 동작하는 "blind" 프로토콜, syndrome `s(x)=H·x`.
4. 핵심 기법: 코드 rate를 `puncturing`(비율 `π`)과 `shortening`(비율 `σ`)으로 동시에 조정, `δ=π+σ` 고정, rate `R=(R0-σ)/(1-π-σ)` (식 6).
5. blind 프로토콜: 1차 메시지는 전부 puncture(`p=d`) 상태로 syndrome만 전송, 실패 시 매 iteration마다 `Δ=d/t`개 심볼을 punctured→shortened로 전환해 재시도(최대 `t` iteration).
6. 평균 rate `R̂ = Σα_i·r_i` (식 8), `α_i`는 iteration i에서 정정 성공한 codeword 비율, 효율 `f̂_BSC(ε)=(1-R̂)/h(ε)`.
7. 부수 트릭: intentional puncturing 패턴(참고문헌 [26]) 사용, shortened 심볼은 무작위 선택; Gaussian approximation(observed channel)으로 FER을 빠르게 근사(density evolution 임계값 21개 사전 계산).
8. 부호 설계: PEG 계열(IPEG, low error-floor 지향) irregular LDPC, degree distribution λ(x)/ρ(x)를 rate별로(R=0.5/0.6/0.7/0.8) 최적화, edge/bit 비율 ≤6.06으로 HW 친화성 고려.
9. 결과: 최대 3회 iteration만으로도 최대interactive(Δ=1) 효율에 근접, δ=10%에서 2×10^3 bit 코드가 blind reconciliation에 적합함을 시뮬로 입증(구체적 efficiency 수치는 그래프 위주로 본문 서술 수치 제한적).
10. 한계: HW 구현은 "파이프라인으로 반복 가능"이라는 서술적 제안뿐이며 실제 회로 설계/합성 없음, decoder는 표준 sum-product 사용(신규 디코딩 알고리즘 아님), 목적이 QKD 통신 프로토콜이라 NAND 저장매체 오류정정과 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| syndrome coding 기반 blind reconciliation 프로토콜 | (대응 없음) | Prime ECC는 저장매체 오류정정 디코더로 QKD 협상 프로토콜과 목적 자체가 다름 |
| puncturing/shortening rate-adaptive | `encoder.cpp` (dual-diagonal 고정) | 개념적으로 유사하나 Prime ECC는 고정 rate 인코더로 rate-adaptive 미지원 |
| sum-product 디코더(표준) | `decoder.cpp` `LDPC_Decoder()` | Prime ECC는 이미 Min-Sum(HW 근사) 사용, sum-product는 오히려 역행 |
| irregular LDPC degree distribution 설계 | `ecc_top.cpp` `Load_PCM()` | Prime ECC는 QC-LDPC 고정 구조, irregular 설계와 직접 대응 없음 |

적용 가치: **낮음** — QKD 정보조정 프로토콜로 NAND ECC 디코더/HW 어느 레이어와도 목적·구조가 근본적으로 달라 이식 요소 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1205.5729v2",
  "title": "Blind Reconciliation",
  "year": 2013,
  "venue": "Quantum Information and Computation",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "irregular",
  "code_rate": "0.5~0.8",
  "code_length": "2000~10000",
  "soft_quant": "무관",
  "key_contribution": "QKD 정보조정(information reconciliation)을 위해 사전 오류율 추정 없이 puncturing/shortening 비율을 반복적으로 조정하는 blind rate-adaptive LDPC 프로토콜 제안",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "채널이 BSC(양자키분배 특유의 오류모델), syndrome coding 기반 통신 프로토콜로 NAND read channel/디코더 HW와 목적 자체가 다름",
  "todo_check": "Prime ECC는 오류정정 목적 디코더이고 이 논문은 협상형 syndrome 프로토콜이라 이식 대상 모듈 자체가 존재하지 않음"
}
```
