### arxiv:1501.04394v1 - Band Splitting Permutations for Spatially Coupled LDPC Codes Enhancing Burst Erasure Immunity (2015, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | (l,r,L) SC-code의 base matrix에 band splitting permutation(열 치환)을 적용해 burst erasure 정정 가능 길이를 L에 비례하도록 개선. |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | erasure 채널(BEC) 및 erasure-BP 전용 이론으로, NAND의 binary LDPC hard/soft error 정정 및 min-sum 복호와 무관. |
| 추가확인 | 없음 |

> 총평: BEC 상의 burst erasure 정정을 위한 SC-LDPC 열 치환 구성법으로 NAND binary LDPC ECC와 접점이 없다.

### B. 알고리즘 요약 (10줄 내외)

1. 대상은 (l, r, L) SC-code (protograph 기반 spatially coupled LDPC), 채널은 memoryless/burst erasure channel(BEC), 복호는 erasure belief propagation(erasure-BP).
2. 기존 (l, r, L) SC-code는 memoryless erasure에는 강하지만 burst erasure에는 취약(연속 소실 시 양쪽에서 전파되는 reliability wave가 끊김).
3. 채널 모델은 단일 burst erasure(연속된 소실 심볼 1개)만 발생한다고 가정.
4. 핵심 기법: base matrix `B(l,r,L)`에 band splitting permutation(BSP) `σ_{k,L}`을 적용해 동일 block에 속한 열들을 최대한 멀리 재배치하는 block interleaver(interleaving depth `k=r/l`).
5. 핵심 식: `Wmax(H) = Span(H) - 1`, permuted 코드에서 `(L-1)M < Wmax(H) < (L+1)M` (Thm 3) — span(최소 stopping set 길이)이 burst 정정 가능 길이를 결정.
6. 확장: irreducible stopping set은 항상 동일 block 내 두 열의 쌍(Thm 2)이라는 구조적 성질을 이용해 BSP 설계.
7. 부수 트릭: lift-up factor `M`으로 base matrix를 실제 PCM으로 확장(순열행렬 대입), non-permuted 대비 `λmax`가 `1/k`(대신 기존은 `L→∞`에서 0)로 수렴함을 증명.
8. 최적화 절차 없음(닫힌 형태 permutation 정의 + 정리 증명).
9. 결과: `(3,6,128)` SC-code에서 permuted `λmax=0.496` > BP threshold `0.488`; 무작위 치환보다 월등히 높은 `λmax` 히스토그램(M=40, 1000 샘플).
10. 한계: BEC/erasure-BP 전용 이론 결과이며 실제 HW 미설계, AWGN/NAND read-noise 채널이나 min-sum soft-decision 복호와는 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Base matrix 열 치환(BSP) | `ecc_top.cpp` `Load_PCM()` | H-matrix 구조 변경 관점에서만 형식적으로 대응, 실질적 이식 대상 아님 |
| erasure-BP 복호 | 대응 없음 | Prime ECC는 hard/soft LLR min-sum 복호(binary AWGN/RBER 채널)만 지원, erasure 채널 미지원 |
| burst erasure 정정 이론 | 대응 없음 | NAND 채널은 burst erasure가 아닌 bit-flip/RBER 오류 모델 |

> 적용 가치: 낮음 — erasure 채널·erasure-BP 전용 이론 구성법으로 NAND binary LDPC의 부호설계/디코더/HW 어디에도 직접 이식할 요소가 없음.

### D. JSON 블록 (DB 적재용)

```json
{
  "id": "arxiv:1501.04394v1",
  "title": "Band Splitting Permutations for Spatially Coupled LDPC Codes Enhancing Burst Erasure Immunity",
  "year": 2015,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "(l,r,L) SC-code의 base matrix에 band splitting permutation(열 치환)을 적용해 burst erasure 정정 가능 길이를 L에 비례하도록 개선.",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "erasure 채널(BEC) 및 erasure-BP 전용 이론으로, NAND의 binary LDPC hard/soft error 정정 및 min-sum 복호와 무관.",
  "todo_check": "없음"
}
```
