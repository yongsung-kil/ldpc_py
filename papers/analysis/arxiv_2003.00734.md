### arxiv:2003.00734v1 - Binary Representation for Non-binary LDPC Code with Decoder Design (2020, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 0.5~0.5355 |
| 부호length | 360~63000 |
| 연판정 | soft-4bit+ |
| 핵심기여 | non-binary LDPC를 binary 표현으로 변환할 때 발생하는 bit-level cycle을 제거하는 EPR-LDPC 구조와 전용 하이브리드 디코더 제안 |
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
| 한계,주의 | non-binary(GF(q)) LDPC 및 그 binary 표현 전용 이론으로 Prime ECC의 binary LDPC 설계·디코더와 근본 구조가 다름 |
| 추가확인 | 제안 디코더(hybrid hard-decision/hybrid parallel)의 HW 복잡도·게이트수는 본문에 미기재 |

> 총평: non-binary LDPC의 binary 표현·cycle 제거 이론 논문으로, non-binary 부호 특유의 구조(matrix label, companion matrix, GF(q) 심볼)에 강하게 결합되어 있어 NAND용 순수 binary LDPC ECC에 이식할 요소가 거의 없음.

### B. 알고리즘 요약

1. 대상은 GF(q)(q=2^p) 상의 non-binary LDPC 부호 C와 그 binary 표현 C̄(H를 companion matrix A로 치환해 얻는 등가 binary parity check matrix)이며, BSC/BEC/binary-input Gaussian channel을 다룸.
2. 문제: non-binary parity check matrix H가 symbol-level cycle-free여도, 이를 그대로 binary화한 H̄는 수많은 bit-level cycle을 가져 성능이 저하됨 (특히 length-4 cycle이 주요 원인).
3. 채널 모델: BSC(hard-decision), binary-input Gaussian channel(AWGN, BPSK), BEC 세 가지에 대해 각각 디코더를 설계.
4. 핵심 기법: **EPR(extended p-reducible)-LDPC** 구조. `Ψ_j^e`(extended generator matrix)와 매핑함수 `f_ω`를 이용해 non-zero column인 `Ω_i,j`를 구성, symbol-level cycle이 bit-level cycle로 전이되는 확률을 낮춤.
5. 핵심 식: `p4 = 1 - (q-2)/(q-1)`(길이-4 symbol cycle이 길이-4 bit cycle을 유발할 확률) — q(GF 크기)가 커질수록 이 확률이 줄어듦을 보여 EPR 구조의 근거를 제공.
6. 디코더 확장: BSC용 hybrid hard-decision decoder(Example 2)와 AWGN용 hybrid parallel decoder(Example 3, BP+hard-decision 교대 (µ,ν) 라운드)를 제안.
7. 구현 디테일: 디코딩 복잡도는 `O(ms)`, `ms=max{φ_e, ψ_e} < q`로, EMS(`O(nm log nm)`)나 QSPA(`O(q^2)`) 대비 낮춤. matrix label은 modified PEG 알고리즘으로 girth 최적화.
8. 최적화 절차: Corollary 5 기반 matrix label 최적화 + girth 제약을 만족하는 Ω_e 탐색(4단계 알고리즘, IV-C).
9. 결과: F16 rate-0.5, length-2048 부호에서 최적화된 non-binary cycle LDPC 대비 BER=10⁻⁴에서 최대 0.8dB 성능 이득, QSPA 대비 0.2dB 이내로 근접하면서 복잡도는 크게 감소.
10. 한계: 순수 시뮬레이션(이론 성능 곡선)만 제시, HW 구현/게이트카운트 없음. 부호 구조 자체가 GF(q) non-binary 심볼 표현에 종속적이라 binary LDPC 설계에 직접 이식 불가.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| non-binary→binary 표현 변환(companion matrix, EPR-LDPC 구조) | 대응 없음 | Prime ECC는 처음부터 binary QC-LDPC 전용으로, non-binary 심볼 표현 개념 자체가 불필요 |
| hybrid parallel decoder (BP + hard-decision 교대) | `decoder.cpp` `LDPC_Decoder()` 이터레이션 루프 | 개념적 유사성만 있음(반복 스케줄), 실제 alg.은 GF(q) simplex code 기반이라 직접 대응 어려움 |
| H-matrix girth/cycle 최적화(PEG 기반) | `ecc_top.cpp` `Load_PCM()` | Prime ECC의 QC-LDPC H-matrix도 girth 고려하나, 이 논문의 최적화는 non-binary matrix label 전용이라 재사용성 낮음 |
| BSC용 hard-decision 반복 디코더 | `decoder.cpp` `VN_Cal_HD()` | Prime ECC도 HD 디코더 보유하나 이 논문은 GF(q) simplex code bit-flip 방식으로 상이 |

적용 가치: **낮음** — non-binary(GF(q)) LDPC의 binary 표현·cycle 제거라는 특수 문제를 다루며 Prime ECC 판정 필터의 "non-binary LDPC 기법은 이식성 대체로 하" 기준에 해당.

### D. JSON 블록

```json
{
  "id": "arxiv:2003.00734v1",
  "title": "Binary Representation for Non-binary LDPC Code with Decoder Design",
  "year": 2020,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "360~63000",
  "soft_quant": "soft-4bit+",
  "key_contribution": "non-binary LDPC를 binary 표현으로 변환할 때 발생하는 bit-level cycle을 제거하는 EPR-LDPC 구조와 전용 하이브리드 디코더 제안",
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
  "caveat": "non-binary(GF(q)) LDPC 및 그 binary 표현 전용 이론으로 Prime ECC의 binary LDPC 설계·디코더와 근본 구조가 다름",
  "todo_check": "제안 디코더(hybrid hard-decision/hybrid parallel)의 HW 복잡도·게이트수는 본문에 미기재"
}
```
