### arxiv:2507.00591v1 - Construction of LDPC convolutional codes with large girth from Latin squares (2025, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | SC-LDPC |
| 부호rate | 0.5 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 직교 Latin square + 다단계 lifting으로 girth 6~12의 compact SC-LDPC convolutional/block 부호 명시적 구성 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | SC-LDPC(convolutional) 구조·rate 1/2 고정, girth/거리 이론 증명만이고 BER 시뮬·복호·HW 전무, Prime ECC 고rate binary QC-LDPC block과 비정합 |
| 추가확인 | girth 향상이 실제 message-passing BER/error-floor에 미치는 이득(시뮬 없음), 고rate·NAND 블록길이로의 적용 가능성 |

> 총평: Latin square 기반 large-girth SC-LDPC convolutional 부호의 순수 구성·이론 논문으로, 복호·시뮬·HW가 없고 rate 1/2 convolutional 구조라 NAND용 고rate binary QC-LDPC block 이식성 하.

### B. 알고리즘 요약

1. 대상: `F2` 위 binary (시변/시불변) LDPC convolutional 부호(SC-LDPC) 및 LDPC block 부호, 예제 `(2p, p)` rate 1/2.
2. 문제: message-passing 성능을 위해 Tanner graph girth를 키우되 저장 효율(compact 표현)도 확보.
3. 도구: 소수 `p`에 대한 pairwise orthogonal Latin square `Lr(a,b)=b-r(a-1) mod p`와 그 permutation incidence matrix `Qr^i`.
4. girth-6 구성: `H0(t)=[Q | Ip]`, `Hi(t)=[Q | 0]` 형태 sliding parity-check matrix로 (2p,p) 시변 convolutional code `C0`, period `p-1`.
5. 핵심논거: 4-cycle 존재는 `(r1-r2)(a2-a1)≡0 mod p` 모순으로 배제, girth ≥ 6 증명(Theorem 4).
6. lifting으로 girth 확장: 각 원소를 `p×p` 블록으로 치환(`Qr^i→Qr^{ra}` 등)해 `Cm`(girth 8, m≥1), `C̃m`(girth 10 m≥2, girth 12 m≥3) 구성.
7. 핵심보조정리: cycle 길이 `2ℓ`이면 대응 `r_i`가 Vandermonde 행렬 비특이성으로 짝을 이뤄야 함(Lemma 1)→짧은 cycle 배제.
8. 거리성질: `d^c_j = min{j,µ}+2`, `d_free = µ+2`; 밀도는 `o(n)`, `p` 커질수록 밀도↓·거리↑(Theorem 7).
9. block 부호: [16]의 Latin square 기반 block code의 6-cycle을 4단계 Fan-sum 치환으로 제거해 girth 8 달성, 크기 `25m(2m+1)^2 × 25m^2(2m+1)^2`.
10. 한계: 순수 구성·이론(증명)만, 복호 알고리즘·BER 시뮬·HW 전무, rate 1/2 convolutional 중심.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Latin square 기반 H-matrix / lifting 구성 | ecc_top.cpp `Load_PCM()` | Prime ECC는 고정 QC-LDPC block 사용, SC-LDPC convolutional 구성은 대응 없음에 가까움 |
| girth 최적화(cycle 제거) | 대응 없음 | Prime ECC에 girth 최적화/그래프 구성 모듈 없음(고정 PCM) |
| SC-LDPC convolutional 복호 | 대응 없음 | Prime ECC 디코더는 block QC-LDPC 전용, convolutional 미지원 |

적용 가치: **낮음** — 복호·시뮬·HW가 없는 순수 SC-LDPC convolutional 구성 이론이며, Prime ECC의 고rate binary QC-LDPC block 구조와 부호족·rate가 달라 직접 이식 근거가 부족하다.

### D. JSON 블록

```json
{
  "id": "arxiv:2507.00591v1",
  "title": "Construction of LDPC convolutional codes with large girth from Latin squares",
  "year": 2025,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "SC-LDPC",
  "code_rate": 0.5,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "직교 Latin square + 다단계 lifting으로 girth 6~12의 compact SC-LDPC convolutional/block 부호 명시적 구성",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "SC-LDPC(convolutional) 구조·rate 1/2 고정, girth/거리 이론 증명만이고 BER 시뮬·복호·HW 전무, Prime ECC 고rate binary QC-LDPC block과 비정합",
  "todo_check": "girth 향상이 실제 message-passing BER/error-floor에 미치는 이득(시뮬 없음), 고rate·NAND 블록길이로의 적용 가능성"
}
```
