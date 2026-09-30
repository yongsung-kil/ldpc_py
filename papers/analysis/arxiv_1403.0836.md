### arxiv:1403.0836v1 - Locally-Optimized Reweighted Belief Propagation for Decoding LDPC Codes with Finite-Length (2014, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 500 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 팩터그래프를 PEG 기반 서브그래프로 분할해 서브그래프별 reweighting parameter ρ를 오프라인 최적화하는 LOW-BP 디코딩 제안 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | X |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | AWGN·짧은 length(N=500) 코드에 대한 tanh 기반 sum-product 계열이며, 오프라인 최적화(최대 2700 recursion)와 온라인 reweighted message passing이 필요해 min-sum HW 구조와 직결되지 않음 |
| 추가확인 | ρ 값을 HW LLR 테이블/스케일링 팩터로 근사 이식 가능한지, min-sum 기반 재구현 시 성능 유지 여부 |

> 총평: 짧은 길이 저rate irregular LDPC에서 tree-reweighted BP의 오프라인 최적화로 waterfall 영역 0.4dB 개선을 보이나, sum-product(tanh) 기반·오프라인 학습 필요·NAND 무관 채널이라 Prime ECC(min-sum, 고rate QC-LDPC) 이식 실익 낮음.

### B. 알고리즘 요약

1. 대상은 rate 1/2, length N=500의 regular(column weight 4, row weight 6) 및 irregular LDPC, AWGN 채널.
2. 기존 표준 BP는 짧은 코드에서 short cycle/stopping set으로 수렴이 느리거나 실패하는 문제가 있고, TRW-BP/URW-BP/VFAP-BP 등 reweighting 기법도 factor appearance probability(FAP) ρ를 상수 또는 이진값으로 제약해 성능이 제한적.
3. 채널 모델은 표준 BPSK+AWGN, factor graph는 check node/variable node로 구성된 팩터그래프.
4. 핵심 기법: LOW-BP는 팩터그래프를 PEG(progressive edge growth) 기법으로 `T`개 서브그래프 `Gt(Vt,Et)`로 분할(disjoint 또는 RA 전략) 후, 서브그래프별 FAP 벡터 `ρt`를 conditional gradient method로 오프라인 최적화.
5. 온라인 복호 시 메시지 갱신식은 `Ψnm = λch,n + Σρm'Λm'n - (1-ρm)Λmn`(V2C), `Λmn = f⊞{ρmΨnm'} - (1-ρm)Ψnm`(C2V), `ρm=1`이면 표준 BP와 동일 — ρ가 short cycle의 메시지 과신을 억제.
6. 서브그래프 개수 `T`를 늘리면 오프라인 최적화는 빨라지지만(복잡도↓) BER 성능은 다소 저하되는 trade-off 존재.
7. 구현 디테일: 수치안정성을 위해 메시지는 LLR, `f⊞`는 Jacobian logarithm으로 계산(HW의 min-sum과 다른 sum-product 계열).
8. 최적화 절차: 오프라인 단계에서 1000개 codeword로 conditional gradient 기반 반복 최적화(regular ~800회, irregular ~2700회 recursion) 후 ρ 확정.
9. 결과: 표준 BP 대비 최대 0.4dB BER 개선(waterfall 영역), 기존 URW-BP/VFAP-BP 대비도 우위.
10. 한계: HW 미설계, iteration 수 감소 언급 없음(오히려 오프라인 최적화에 수백~수천 회 필요해 지연 증가), error-floor 영역 데이터 없음(BER 10^-8까지 waterfall만 관찰), 짧은 length·저rate 코드로 NAND 고rate 부호와 직접 비교 어려움.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Reweighted message passing (ρ 기반 C2V/V2C) | `decoder.cpp` `LDPC_Decoder()`, `C2V_Cal()` | min-sum이 아닌 tanh/Jacobian 기반 sum-product 변형으로, 구조적으로 다르나 iteration 루프 개념은 대응 |
| CN 연산 f⊞ (Jacobian logarithm) | `decoder.cpp` `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | Prime ECC는 min-sum 근사 사용, 논문은 정밀 tanh 근사라 직접 대응 어려움 |
| 오프라인 ρ 최적화(conditional gradient) | `ecc_data.h` `PARAM_LLR`, `decoder.cpp` `Get_VNU_Table_Idx()` | iteration별 LLR 테이블 개념과 유사하나, 논문은 SNR별 사전학습 파라미터로 min-sum scaling factor 튜닝에 참고 가능한 수준 |

적용 가치: **낮음** — sum-product(tanh) 계열 reweighting 기법으로 min-sum 기반 Prime ECC와 근본 연산이 다르고, 오프라인 최적화 비용(최대 2700회 반복)이 커 HW 친화적이지 않음. 단, "서브그래프별 파라미터 튜닝" 아이디어 자체는 min-sum scaling factor 최적화에 개념적으로만 참고 가능.

### D. JSON 블록

```json
{
  "id": "arxiv:1403.0836v1",
  "title": "Locally-Optimized Reweighted Belief Propagation for Decoding LDPC Codes with Finite-Length",
  "year": 2014,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": 500,
  "soft_quant": "soft-4bit+",
  "key_contribution": "팩터그래프를 PEG 기반 서브그래프로 분할해 서브그래프별 reweighting parameter ρ를 오프라인 최적화하는 LOW-BP 디코딩 제안",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "X",
  "latency": "악화",
  "recommend": "하",
  "caveat": "AWGN·짧은 length(N=500) 코드에 대한 tanh 기반 sum-product 계열이며, 오프라인 최적화(최대 2700 recursion)와 온라인 reweighted message passing이 필요해 min-sum HW 구조와 직결되지 않음",
  "todo_check": "ρ 값을 HW LLR 테이블/스케일링 팩터로 근사 이식 가능한지, min-sum 기반 재구현 시 성능 유지 여부"
}
```
