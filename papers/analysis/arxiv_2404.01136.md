### arxiv:2404.01136v2 - Density Evolution Analysis of Generalized Low-density Parity-check Codes under a Posteriori Probability Decoder (2024, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 3000~3500 |
| 연판정 | soft-4bit+ |
| 핵심기여 | GLDPC를 APP 디코더로 DE 확장(대칭/집중/단조 증명), message-invariant subcode 정의, Gaussian mixture 근사로 threshold 정밀도 향상 |
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
| 한계,주의 | GLDPC(SPC 대신 Hamming/BCH 블록 subcode)+APP 디코더는 우리 binary QC-LDPC min-sum 구조와 부호·디코더 모두 상이, 점근(n→∞) 이론 위주 |
| 추가확인 | GC node subcode/APP 디코더 도입 시 HW 복잡도·latency와 error-floor 실측 (본문은 threshold·BLER 시뮬만) |

> 총평: GLDPC의 DE 이론 확장 + Gaussian mixture threshold 근사가 핵심으로, 부호설계 도구·분석법이 NAND binary QC-LDPC min-sum 파이프라인과 직접 접점 없음(이식성 하). GA→GMA 정밀화 아이디어만 참고 가치.

### B. 알고리즘 요약

1. 대상: `(C,J,K,t)` GLDPC ensemble — check node 중 비율 `t`를 subcode `C`의 GC(generalized constraint) node로, 나머지 `1-t`는 SPC로 둔 Tanner graph (variable degree `J`, check degree `K`).
2. 문제: GLDPC를 APP 디코더로 쓸 때 BEC 외 BI-AWGN 등 넓은 채널에서 성능분석 부재, APP 계산 복잡도 큼.
3. DE 확장: GLDPC+APP 디코더에 대해 concentration/symmetry/monotonicity 성립 증명 → 무한길이 성능을 cycle-free tree에서 all-zero(all-one) codeword로 분석 가능, 채널 threshold 존재 보장.
4. Extended symmetry: 기존 채널/VN/SPC 대칭에 GC node symmetry(식21) 추가 — subcode codeword `(b1..bK)`의 부호가 GC 메시지맵에서 인수분해됨(Lemma1,2).
5. Message-invariant subcode(정의3): GC→각 연결 VN 메시지 전달식이 permutation `πi`만 다르고 구조 동일한 subcode. Hamming/RM/extended-BCH 등이 해당 → 분석·복호 대폭 단순화.
6. BEC DE: subcode별 erasure 재귀식 유도(식30,31 for `(6,3)`-shortened Hamming `C1`, `(7,4)` Hamming `C2`), `ε_{l+1}=ε0(t·eC + (1-t)·eS)^{J-1}` (식33).
7. BI-AWGN DE: L-density 재귀(식34). GC node 출력밀도 `Φ_GC`를 Monte Carlo로 구함.
8. Gaussian approx(GA): mean만 추적(식36)하나 `t∈(0,1)`에서 큰 오차(예 `(C1,2,6,0.5)`에서 4.91 dB).
9. Gaussian mixture approx(GMA): VN 출력을 GC/SPC mean 두 성분 혼합으로 근사(식38,39) → threshold 오차 대폭 축소(대개 <0.2 dB), LDPC irregular check에도 적용(2.38→0.15 dB).
10. 결과: 적절한 `t`(BI-AWGN에서 C1 t=0.8, C2 t=0.85)로 base LDPC 대비 gap-to-capacity 감소, 동일 rate LDPC 대비 BLER 약 0.4~1 dB 개선(길이 3000/3500, 최대 iter 20/50). HW 미설계.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| GLDPC 부호구조(GC node=블록 subcode) | 대응 없음 | Prime ECC는 SPC 기반 binary QC-LDPC PCM, GC node/subcode 개념 없음 |
| APP 디코더 (GC node 메시지) | 대응 없음 | `decoder.cpp` `LDPC_Decoder()`는 min-sum SPC CN 연산, APP subcode 복호 미대응 |
| DE / Gaussian mixture threshold 근사 | 대응 없음 | 부호설계·성능해석 이론 도구로, 코드베이스에 DE 모듈 없음 |
| C2V/V2C tanh 메시지 갱신(식5,6) | decoder.cpp `C2V_Cal()` | 개념만 공통, 본문은 full-tanh SPA/APP이고 우리 엔진은 min-sum |

적용 가치: **낮음** — GLDPC(subcode GC node)+APP 디코더 + DE 이론 확장 논문으로, NAND binary QC-LDPC min-sum 부호설계/디코더/HW(§6 모듈)에 떼어 쓸 접점이 없음. GMA threshold 정밀화 아이디어만 간접 참고 가능.

### D. JSON 블록

```json
{
  "id": "arxiv:2404.01136v2",
  "title": "Density Evolution Analysis of Generalized Low-density Parity-check Codes under a Posteriori Probability Decoder",
  "year": 2024,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": "미상",
  "code_length": "3000~3500",
  "soft_quant": "soft-4bit+",
  "key_contribution": "GLDPC를 APP 디코더로 DE 확장(대칭/집중/단조 증명), message-invariant subcode 정의, Gaussian mixture 근사로 threshold 정밀도 향상",
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
  "caveat": "GLDPC(SPC 대신 Hamming/BCH 블록 subcode)+APP 디코더는 우리 binary QC-LDPC min-sum 구조와 부호·디코더 모두 상이, 점근(n→∞) 이론 위주",
  "todo_check": "GC node subcode/APP 디코더 도입 시 HW 복잡도·latency와 error-floor 실측 (본문은 threshold·BLER 시뮬만)"
}
```
