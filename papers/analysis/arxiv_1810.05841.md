### arxiv:1810.05841v2 - Error estimation at the information reconciliation stage of quantum key distribution (2018, arXiv quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | irregular |
| 부호rate | 0.47~0.947 |
| 부호length | 4000~40000 |
| 연판정 | 무관 |
| 핵심기여 | 불규칙 LDPC·punctured/shortened 비트를 반영한 syndrome 기반 on-the-fly QBER(오류율) 추정 알고리즘 |
| HW설계 | X |
| 검증수준 | 실측 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | QKD reconciliation 전용 오류율 추정 문제로, NAND ECC에는 대응 개념(사전 QBER 추정)이 없음 |
| 추가확인 | 없음 (NAND binary LDPC ECC 이식 관점에서 활용점 없음) |

> 총평: QKD 정보조정 단계의 syndrome 기반 QBER 추정 논문으로 LDPC 디코더/부호설계 개선과 무관, NAND ECC 이식 가치 없음.

### B. 알고리즘 요약

1. 시스템: QKD 정보조정(information reconciliation). Alice/Bob의 sifted key를 irregular LDPC(`n`=4000~40000, rate 0.5~0.9 pool)로 조정, syndrome decoding으로 불일치 정정.
2. 문제: 조정 효율 `f = m / (n·h(q))`를 튜닝하려면 QBER `q`를 사전에 알아야 하나, 조정 전에는 미지 → 부정확 추정 시 효율 저하 또는 추가 통신 라운드 발생.
3. 모델: `k_A[i]`가 `k_B[i]`와 확률 `1-q`로 일치하는 BSC. syndrome `s_A = H·k_A (mod 2)`.
4. 핵심 기법: relative syndrome `Δs = s_A + s_B (mod 2)`의 각 비트를 Bernoulli 변수로 보고, 행별 차수 `d_c(i)`에 따른 crossover 확률 `p(q, d_c)`로 likelihood `L(q|Δs)` 구성 → ML 추정 `q_est = argmax L`.
5. 식 의미: irregular 코드는 행마다 `d_c(i)`가 달라 개별 crossover 확률을 곱한 likelihood가 필요 (기존 regular 전용 추정식 (6)의 일반화).
6. 확장: punctured 비트가 걸린 행(`A_i ∩ P ≠ ∅`)은 균등분포라 추정에서 제외, shortened 비트는 `d_c(i) = d_c - |A_i ∩ S|`로 유효 차수 보정.
7. 구현 디테일: 사전 QBER 분포를 두 sigmoid 곱 window `L_0(q)`로 반영해 outlier 억제, log-domain + Brent's method로 수치 최적화.
8. 최적화: 별도 학습 없음, 파라미터 `α1=α2=500, qmin=0.01, qmax=0.08` 고정.
9. 결과: 실 산업용 QKD 셋업에서 `n=40000` 시 syndrome 기반이 이전값 기반보다 정확, 두 추정 평균한 mixed 방식이 모든 frame length에서 최고 정확도 (accuracy 0.0015~0.0034).
10. 한계: 디코더/HW 없음, 오류율 "추정"만 다룸 (정정 성능 개선 아님), QKD 채널·프로토콜 전용.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| syndrome 기반 QBER 추정 | 대응 없음 | NAND ECC엔 사전 오류율 추정 단계·상대 syndrome 개념 없음 |
| irregular LDPC syndrome | 대응 없음 | Prime ECC는 고정 QC-LDPC(binary) 사용, 추정 로직 미대응 |

적용 가치: **낮음** — QKD reconciliation의 QBER 통계 추정 문제로 NAND binary LDPC 디코더/부호설계/HW 어느 레이어에도 이식 대상이 없음.

### D. JSON

```json
{
  "id": "arxiv:1810.05841v2",
  "title": "Error estimation at the information reconciliation stage of quantum key distribution",
  "year": 2018,
  "venue": "arXiv quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "irregular",
  "code_rate": "0.47~0.947",
  "code_length": "4000~40000",
  "soft_quant": "무관",
  "key_contribution": "불규칙 LDPC·punctured/shortened 비트를 반영한 syndrome 기반 on-the-fly QBER 추정 알고리즘",
  "hw_designed": "X",
  "verification": "실측",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "QKD reconciliation 전용 오류율 추정 문제로 NAND ECC에는 대응 개념 없음",
  "todo_check": "없음 (NAND binary LDPC ECC 이식 관점에서 활용점 없음)"
}
```
