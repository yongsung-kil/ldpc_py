### arxiv:0911.3262v1 - Moderate-Density Parity-Check Codes (2009, arXiv / submitted to IEEE Trans. Commun.)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 0.72~0.83 |
| 부호length | 127~129 |
| 연판정 | 무관 |
| 핵심기여 | idempotent/cyclotomic coset로 moderate-density cyclic 부호 구성 + automorphism group 기반 Auto-Diversity(AD) BP 디코더로 동급 BCH 대비 0.75~1 dB 이득·복잡도 감소 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | 짧은(n≈127) moderate-density cyclic 부호 + cyclic automorphism 의존 AD 디코더 → 긴 고rate QC-LDPC(NAND)에 부호·디코더 모두 부적합, moderate-density라 sparse min-sum HW와 상충 |
| 추가확인 | NAND 4KB QC-LDPC엔 cyclic automorphism 다양성이 없어 AD 적용 불가(구조적 비호환) |

> 총평: 짧은 고rate cyclic moderate-density 부호와 automorphism 다양성 디코더로 BCH 대체가 목표 — NAND 장블록 QC-LDPC + min-sum과 부호·디코더 양면 모두 비호환.

### B. 알고리즘 요약

1. 시스템: AWGN + BPSK, LLR `L=(2/σ²)y` 입력, 짧은/중간 블록 binary cyclic 부호(n≈127~129, rate 0.72~0.83).
2. 문제: 짧고 고rate인 구조적 LDPC는 sparse H와 큰 min-distance를 동시 만족하기 어려움 → 밀도 제약을 완화한 부호 필요.
3. 모델: cyclic code를 `Rn=F2[x]/(xⁿ−1)`의 ideal로 보고, idempotent `E(x)=E(x²)`와 2-cyclotomic coset `Cs`로 부호 생성.
4. 핵심 기법1(부호설계): bounded-weight idempotent를 cyclotomic coset로 탐색(Alg.1)해 moderate-density parity-check `i*dual(x)`를 구성, primitive idempotent 수로 rate/밀도 조절.
5. 식 의미: `idual(x)=1+xⁿi(x⁻¹)`로 dual 부호 idempotent를 얻어 H를 n−k cyclic shift로 생성 → 부호가 cyclic이라 shift-register 인코딩 가능.
6. 핵심 기법2(디코더): Auto-Diversity(AD) 디코더 — 여분 parity-check(m≈n/2)로 BP 수행, 미수렴 시 automorphism `σ∈Aut(C)`로 H 열을 순열(`σ⁻¹SI`) 후 재복호, 최대 `Nds` diversity stage.
7. 구현 디테일: 미수렴 시 least-metric selector(LMS)로 codeword 추정, redundant parity-check 최소화(m≈n/2).
8. 최적화 절차: GAP/GUAVA/MAGMA로 idempotent·min-distance·weight distribution 계산(오프라인 부호탐색).
9. 결과: MDPC(127,92)/(129,100)/(127,106)가 동급 BCH 대비 BER=1e-4서 0.9~1 dB, FER=1e-3서 0.75 dB 이득, 복잡도 10~60% 감소, BER=1e-5까지 평균 <3 iteration.
10. 한계: HW 미설계·AWGN 시뮬만, 매우 짧은 블록(127), moderate-density(sparse LDPC보다 dense), AD는 순차 diversity stage(최대 Nds=30) 의존.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Auto-Diversity BP 디코더(automorphism 순열 + 재복호) | decoder.cpp `LDPC_Decoder()` | Prime ECC는 min-sum 단일 스케줄, cyclic automorphism 기반 다양성 개념이 없어 비대응 |
| moderate-density cyclic 부호 구성(idempotent/cyclotomic) | ecc_top.cpp `Load_PCM()` | 부호 계열(cyclic moderate-density)이 QC-LDPC와 다르고 dense해 이식 불가 |
| least-metric selector / redundant parity-check | 대응 없음 | 다양성 재복호·LMS는 Prime ECC HW 파이프라인과 무관 |

적용 가치: **낮음** — cyclic automorphism 다양성 디코더와 short moderate-density 부호는 NAND용 장블록 sparse QC-LDPC + min-sum(Prime ECC)과 부호·디코더 양면에서 구조적으로 비호환.

### D. JSON 블록

```json
{
  "id": "arxiv:0911.3262v1",
  "title": "Moderate-Density Parity-Check Codes",
  "year": 2009,
  "venue": "arXiv (submitted to IEEE Trans. Commun.)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "127~129",
  "soft_quant": "무관",
  "key_contribution": "idempotent/cyclotomic coset로 moderate-density cyclic 부호 구성 + automorphism group 기반 Auto-Diversity(AD) BP 디코더로 동급 BCH 대비 0.75~1 dB 이득·복잡도 감소",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "악화",
  "recommend": "하",
  "caveat": "짧은(n≈127) moderate-density cyclic 부호 + cyclic automorphism 의존 AD 디코더 → 긴 고rate QC-LDPC(NAND)에 부호·디코더 모두 부적합, moderate-density라 sparse min-sum HW와 상충",
  "todo_check": "NAND 4KB QC-LDPC엔 cyclic automorphism 다양성이 없어 AD 적용 불가(구조적 비호환)"
}
```
