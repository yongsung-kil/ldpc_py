### arxiv:1407.0521v2 - Lowering the error floor of Gallager codes: a statistical-mechanical view (2014, arXiv (J. Stat. Mech. 관련))

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | irregular |
| 부호rate | 0.77 |
| 부호length | 1057 |
| 연판정 | soft-4bit+ |
| 핵심기여 | BP의 effective-field 업데이트를 damping factor `1-γ`로 완화(PDBP/PD′BP)하여 min-sum 계열 디코더의 trapping-set 수렴 실패를 줄이고 error floor를 낮춤 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | 부분 |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | 단일 소형 코드(N=1057, BSC 채널)로만 검증, HW 설계·복잡도·AWGN 실측은 미제시 |
| 추가확인 | γ 최적값 탐색 비용과 irregular 코드에서의 bit-dependent damping 일반화 가능성 |

> 총평: min-sum BP의 effective-field 갱신에 damping factor를 도입해 trapping set을 줄이는 저복잡도 알고리즘 변형으로, 구현 단순성은 매력적이나 검증이 소형 BSC 코드 시뮬레이션에 국한됨.

### B. 알고리즘 요약 (10줄 내외)

1. Gallager LDPC 코드의 BP 복호를 multispin Ising 모델의 Bethe-Peierls 근사와 동일시하고, BSC 채널(N=1057, rate≈0.77, almost-regular n=3/m=13)에서 실험.
2. 표준 BP/min-sum은 trapping set으로 인해 수렴 실패 또는 비-codeword로의 수렴이 발생해 error floor를 유발.
3. min-sum 근사(`18`식, β→∞ 극한)를 기본으로 하며, 채널은 단순 BSC(bit-flip 확률 x)로 가정.
4. 핵심 기법: effective field 업데이트 `h_i := h_i + (1-γ)Δ_i` (`22`식)로, damping parameter `γ∈[0,1)`를 도입해 BP 갱신폭을 감쇠.
5. `Δ_i`를 두 가지 방식으로 정의(`20`, `21`식)하면 PDBP(식 23, 기존 BP와의 convex combination)와 PD′BP 두 변종이 생성되며 둘 다 BP fixed point는 보존.
6. 이론적으로 damping은 double-loop 최적화 알고리즘(Heskes-Albers-Kappen)의 근사로 해석 가능, 정규 코드에서 수렴 충분조건(`33`식, γ≥0.638)을 rule-of-thumb로 제시.
7. HW 친화적 요소: 병렬(parallel) 업데이트 스케줄만 사용(RSBP의 순차 업데이트는 병렬화 어려움으로 배제), 추가 연산은 스칼라 곱셈 1회 수준으로 낮은 오버헤드.
8. 최적화 절차: γ를 스윕하며 weight-3 오류패턴 전수조사로 수렴에 필요한 최대 반복수(ν̂3)를 최소화하는 값 탐색(PDBP: γ=0.83, PD′BP: γ=0.35).
9. 결과: BP는 N3=5180(오류플로어 원인 weight-3 패턴)에서 plateau, PDBP/PD′BP/DMBP는 N3=0 달성(asymptotic slope 3→4), PD′BP가 최소 반복수(ν̂3=20)로 가장 우수.
10. 한계: 단일 소형 코드·BSC 채널에서만 검증(AWGN·대형 코드는 unpublished 예비결과 언급뿐), HW 구현/게이트카운트/throughput 분석 없음, irregular 코드로의 일반화는 향후 과제로 남김.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| min-sum 기반 BP 디코딩 루프 | `decoder.cpp` `LDPC_Decoder()`, `C2V_Cal()` | 반복 루프 구조 동일, damping 변형 적용 지점 |
| effective field damping (γ 완화) | `decoder.cpp` `VN_Cal_HD()` 등 VN 업데이트 | VN 갱신식에 damping factor 추가하는 형태로 이식 가능성 있으나 검증 부담 |
| iteration별 파라미터(γ) 테이블 | `ecc_data.h` `PARAM_LLR`, `decoder.cpp` `Get_VNU_Table_Idx()` | γ를 iteration-dependent LLR threshold처럼 테이블화 가능 |
| trapping-set 감소를 통한 error-floor 개선 | `decoder.cpp` `LDPC_Decoder()` 이터레이션 루프 | 목적(=error floor 개선)은 일치하나 본 논문은 BSC/소형코드 한정, Prime ECC의 NAND 채널·고rate QC-LDPC 재검증 필요 |
| CN min-sum 연산 자체 | `decoder.cpp` `CNU_Update_New_Mag()` | 논문도 min-sum(§3.1 식18) 사용, 이미 보유 기법과 중복 |

> 적용 가치: 중간 — VN effective-field 갱신에 damping factor를 추가하는 것은 구현이 단순(곱셈 1회)하여 낮은 난이도로 이식 가능하지만, 검증이 소형 BSC 코드에 국한되어 NAND 고rate QC-LDPC·soft-read 환경에서의 효과는 별도 재검증이 필요.

### D. JSON 블록 (DB 적재용)

```json
{
  "id": "arxiv:1407.0521v2",
  "title": "Lowering the error floor of Gallager codes: a statistical-mechanical view",
  "year": 2014,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "irregular",
  "code_rate": 0.77,
  "code_length": 1057,
  "soft_quant": "soft-4bit+",
  "key_contribution": "BP effective-field 업데이트에 damping factor(1-γ)를 도입한 PDBP/PD'BP로 min-sum 계열 디코더의 trapping-set 기반 error floor를 낮춤",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "부분",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "단일 소형 코드(N=1057, BSC 채널)로만 검증, HW 설계·복잡도·AWGN 실측 미제시",
  "todo_check": "γ 최적값 탐색 비용과 irregular 코드에서의 bit-dependent damping 일반화 가능성 확인 필요"
}
```
