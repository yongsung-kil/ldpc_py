### arxiv:1403.0847v2 - Knowledge-Aided Reweighted Belief Propagation LDPC Decoding using Regular and Irregular Designs (2014, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 500 |
| 연판정 | soft-4bit+ |
| 핵심기여 | cycle-counting 알고리즘으로 check node별 length-g cycle 개수를 구해, 짧은 cycle 밀도가 높은 check node만 선택적으로 reweight하는 VFAP-BP 제안 (O(gN) 저복잡도) |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | tanh(sum-product) 기반 C2V 연산이라 min-sum HW와 직접 대응 안 되며, 짧은 length(N=500) 저rate(1/2) AWGN 코드로 NAND 고rate QC-LDPC와 code 구조가 다름 |
| 추가확인 | check-node별 cycle count 기반 선택적 reweight를 min-sum scaling factor 차등 적용으로 변환 시 HW 오버헤드·성능 유지 여부 |

> 총평: 코드별 사전 계산한 short cycle 통계로 check node를 선택적으로 reweight해 수렴 iteration을 실측 단축(저복잡도 O(gN))한 점은 흥미로우나, sum-product 기반·저rate 짧은 코드 실험이라 Prime ECC(min-sum, 고rate QC-LDPC) 직접 이식은 재검증 부담이 큼.

### B. 알고리즘 요약

1. 대상은 rate 1/2, length N=500의 PEG 설계 regular(VN degree 4, CN degree 6) 및 irregular LDPC, AWGN 채널.
2. 짧은 길이 코드에서 표준 BP는 short cycle로 수렴이 느리거나 실패하며, 무선통신은 저지연이 중요한데 기존 reweighting(TRW-BP, URW-BP)은 전역 상수 ρ만 써서 asymmetric(irregular) 그래프에 부적합.
3. 채널은 표준 BPSK+AWGN, `L(xj)=2yj/σ²`.
4. 핵심 기법: cycle counting 알고리즘(lollipop walk 재귀식 (10)-(15))으로 그래프 girth `g`와 각 check node `Ci`를 지나는 length-g cycle 개수 `si`를 계산, 평균 `μg`보다 `si`가 크면 해당 check node에 `ρi=ρv=2/n̄D`(축소된 reweight), 작으면 `ρi=1`(표준 BP) 적용.
5. 메시지 갱신식 `Ψji = L(xj) + Σρi'Λi'j - (1-ρi)Λij`(V2C, C2V는 표준 tanh 기반 `Λij=2tanh⁻¹(Πtanh(Ψj'i/2))` 그대로) — short cycle이 몰린 check node만 선택적으로 메시지 과신을 억제.
6. 확장/2단 기법 없음, 대신 계산복잡도가 기존 global optimization `O(M²N)` 대비 `O(gN)`으로 대폭 감소.
7. 구현 디테일: `ρv=2/n̄D`는 평균 connectivity 기반 폐형(closed-form) 추정치로 온라인 최적화 없이 즉시 계산 가능(오프라인 학습 불필요, 앞선 LOW-BP 논문과 차별점).
8. 학습 절차: 사전에 cycle counting으로 `g`, `si`, `μg`를 1회 계산해 ρ 벡터 결정(오프라인이지만 반복 최적화가 아닌 폐형 계산).
9. 결과: regular 코드에서 URW-BP·표준BP 대비 저SNR(2dB)에서 수렴 속도 개선, irregular 코드에서 URW-BP는 2dB에서 수렴 실패하지만 VFAP-BP는 표준BP를 iteration 수와 무관하게 일관되게 상회.
10. 한계: HW 미설계, error-floor 데이터 없음(BER 10^-6~10^-7까지 waterfall 위주), 짧은 length·저rate 코드라 NAND 고rate 부호와 규모 차이 큼, sum-product(tanh) 연산이라 min-sum HW 이식 시 재설계 필요.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Check-node별 선택적 reweight(VFAP-BP 메시지 갱신) | `decoder.cpp` `LDPC_Decoder()`, `C2V_Cal()` | iteration 루프 내 CN별 파라미터 차등 적용 아이디어는 대응되나 tanh 기반이라 연산 자체는 상이 |
| CN 연산 (2tanh⁻¹ Π tanh) | `decoder.cpp` `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | Prime ECC는 min-sum 근사, 논문은 정밀 sum-product라 직접 대응 어려움 |
| Cycle-count 기반 오프라인 ρ 결정 (폐형식) | `ecc_data.h` `PARAM_LLR`, `decoder.cpp` `Get_VNU_Table_Idx()` | 코드 구조(H-matrix) 기반 사전 통계로 CN별 scaling factor를 차등화하는 아이디어로 LLR 테이블 설계에 개념적 참고 가능 |
| 짧은 cycle 위치 파악(lollipop walk 카운팅) | `ecc_top.cpp` `Load_PCM()` | H-matrix 설계/분석 단계에서 trapping set 위치 파악에 참고 가능 |

적용 가치: **중간** — check node 단위로 cycle 밀집도를 폐형 계산해 선택적으로 reweight하는 저복잡도(O(gN)) 아이디어는 min-sum scaling factor를 CN 위치별로 차등화하는 방식으로 개념 이식 가능성이 있으나, sum-product 기반 실험·저rate 짧은 코드라 실제 min-sum HW 재검증 부담이 크고 정량적 gatecount/throughput 데이터가 없어 하드웨어 관점 판단은 불가.

### D. JSON 블록

```json
{
  "id": "arxiv:1403.0847v2",
  "title": "Knowledge-Aided Reweighted Belief Propagation LDPC Decoding using Regular and Irregular Designs",
  "year": 2014,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": 500,
  "soft_quant": "soft-4bit+",
  "key_contribution": "cycle-counting 알고리즘으로 check node별 length-g cycle 개수를 구해, 짧은 cycle 밀도가 높은 check node만 선택적으로 reweight하는 VFAP-BP 제안 (O(gN) 저복잡도)",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "중",
  "caveat": "tanh(sum-product) 기반 C2V 연산이라 min-sum HW와 직접 대응 안 되며, 짧은 length(N=500) 저rate(1/2) AWGN 코드로 NAND 고rate QC-LDPC와 code 구조가 다름",
  "todo_check": "check-node별 cycle count 기반 선택적 reweight를 min-sum scaling factor 차등 적용으로 변환 시 HW 오버헤드·성능 유지 여부"
}
```
