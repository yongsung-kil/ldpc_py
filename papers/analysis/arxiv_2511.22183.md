### arxiv:2511.22183v1 - Constructions of block MDS LDPC codes from punctured circulant matrices (2025, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.83~0.955 |
| 부호length | 1584~45012 |
| 연판정 | soft-2~3bit |
| 핵심기여 | punctured circulant matrix로 block MDS 성질과 4-cycle 부재를 동시 만족하는 binary QC-LDPC 대수적 구성 |
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
| 추천도 | 중 |
| 한계,주의 | 대수적 구성뿐(HW 미설계); N은 odd prime·2가 원시근이어야 하는 수론적 제약, girth 6 수준 |
| 추가확인 | error-floor 영역 성능·girth와 최소거리 관계, dual-diagonal 인코딩 적용 가능 여부 |

> 총평: block MDS 성질을 갖는 binary QC-LDPC 부호를 punctured circulant matrix로 대수적 구성, 동일 rate/length 대비 random-error 정정 개선 - 고rate binary QC-LDPC 부호설계로 이식 여지는 있으나 특정 QC 고정된 Prime ECC에 대한 재검증 부담 큼.

### B. 알고리즘 요약

1. 목표: block MDS 성질(burst 정정 최적)과 4-cycle 부재(random 정정 우수)를 **동시** 만족하는 QC-LDPC 부호를 대수적으로 구성.
2. 문제: Blaum-Roth(BR) MDS array code는 parity-check에 4-cycle 다발; Fossorier CPM-QC는 MDS array가 아님 - 둘 다 동시 만족 불가.
3. 구성1(CPM 기반, binary 가능): Vandermonde 형 `V(I_N,P_N,...,P_N^{N-1};r)`을 puncturing하여 block MDS + 4-cycle-free 부호(Theorem 6). `N`은 odd prime, `q`가 mod `N` 원시근 요구.
4. 핵심식: puncturing 후 gcd 조건(`gcd(a_i(x)-a_j(x), x^N-1)=x-1`)으로 MDS array 성질 보장(Lemma 5), 부호길이 `N(N-1)`, rate `(N-r)/N`.
5. 불가능성: binary block MDS CPM-QC LDPC(4-cycle-free)는 **존재하지 않음**을 증명 - binary는 puncturing 필수.
6. 구성2(CSM 기반): non-binary 전용, puncturing 불필요, scaling matrix `S`로 4-cycle 회피(Theorem 9), Schur's formula 없이 Vandermonde 형으로 단순화.
7. 구성3(CM(t), t>1, char2): column weight>1 circulant을 Moore 형으로 사용, `Δ(Index)`가 N-modular Golomb ruler면 4-cycle 회피(Lemma 11~13).
8. CM(t) Moore determinant 공식(Lemma 14)과 t>1일 때 4-cycle 회피 충분조건 제시; 주 관심은 CM(2), r=2(고rate).
9. 결과: Example 17(2856,2380 rate0.833 girth6)·18(45012,42108 rate0.935)·19(1944,1620 rate0.83)에서 Xiao[38]·Li[17]·IEEE 802.11n 부호 대비 SNR>4dB 구간 BER/BLER 우수; Example 7(rate0.955)은 PEG random 대비 열화 거의 없음.
10. 한계: 순수 대수 구성·시뮬(AWGN, sum-product, max iter 50)뿐; HW·양자화·NAND 채널 미고려, girth는 6 수준.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| block MDS binary QC-LDPC H-matrix 구성 | `ecc_top.cpp` `Load_PCM()` | 새 base matrix/circulant 구조 로드 지점이나 Prime ECC는 특정 QC 고정, 재검증 부담 |
| 4-cycle-free/girth 보장 부호설계 | 대응 없음 | Prime ECC 프로파일에 부호 girth 최적화 모듈 명시 없음(H-matrix 종속) |
| 인코딩(punctured QC 효율 인코딩 [5,20]) | `encoder.cpp` `Generate_PCM_encoding()` | Prime ECC는 dual-diagonal 고정, punctured 구성과 인코딩 방식 상이 |

적용 가치: **중간** - 고rate binary QC-LDPC 부호설계 관점에서 관심 대상(waterfall 개선)이나, Prime ECC의 QC-LDPC/dual-diagonal이 고정되어 있어 H-matrix 교체는 §4 이식난이도 "높음"이며 burst 정정·QKD 지향이라 NAND random-error 이득은 재검증 필요.

### D. JSON 블록

```json
{
  "id": "arxiv:2511.22183v1",
  "title": "Constructions of block MDS LDPC codes from punctured circulant matrices",
  "year": 2025,
  "venue": "arXiv cs.IT",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "1584~45012",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "punctured circulant matrix로 block MDS 성질과 4-cycle 부재를 동시 만족하는 binary QC-LDPC 대수적 구성",
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
  "recommend": "중",
  "caveat": "대수적 구성뿐(HW 미설계); N은 odd prime·2가 원시근이어야 하는 수론적 제약, girth 6 수준",
  "todo_check": "error-floor 영역 성능·girth와 최소거리 관계, dual-diagonal 인코딩 적용 가능 여부"
}
```
