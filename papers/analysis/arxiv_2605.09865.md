### arxiv:2605.09865v1 - A Global Coding Scheme for OFDM over Finite Fields (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.89~0.955 |
| 부호length | 7921~16129 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 다중 사용자 스트림을 GFT로 결합해 GF(2^s) 위 global QC-LDPC를 만들고 이를 s개 병렬 이진 소프트결정 디코더(MSA)로 분해 복호함 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 다중 사용자 OFDM/무선 통신(AWGNC) 맥락의 부호 구성법으로 NAND 단일 채널 ECC와 목적·채널 모델이 다름 |
| 추가확인 | 논문이 부수적으로 언급한 "cyclic LDPC 기반 base code" 확장(결론부)이 NAND용 짧은 QC-LDPC 설계에 참고될 수 있는지 |

> 총평: 다중접속(FFMA/OFDM) 시스템을 위한 부호 구성 이론 논문으로, 결과물이 QC-LDPC 구조를 갖지만 NAND ECC 이식 관점에서는 표준 min-sum 디코딩과 시뮬레이션 검증뿐이라 이식 가치가 낮음.

### B. 알고리즘 요약

1. 시스템: 소수 길이 `n`의 cyclic code `C`와 그 Hadamard equivalent `n-1`개, SPC code 1개를 "부반송파"로 사용해 `ns`개 독립 이진 스트림을 GF(2^s) 위에서 다중화(FF-OFDM).
2. 풀려는 문제: 다중 사용자 통신에서 코딩과 다중화를 분리 설계하면 협력 이득을 얻지 못하고, GF(2^s) 전체를 비이진 디코더로 처리하면 복잡도가 지수적으로 폭증.
3. 핵심 가정: AWGNC 채널, BPSK 변조, 다중경로 페이딩은 다루지 않음(향후 과제로 명시).
4. 핵심 기법: 각 그룹의 `s`개 이진 부호어를 `ck = uk,0 + uk,1*α + ... + uk,s-1*α^(s-1)`로 GF(2^s) 합성 후, Vandermonde 행렬 `V`(GFT)로 전역 결합해 `cglobal` 생성.
5. 핵심 식: `Hglobal = CPM(B)`(식 19) — 전역 검사행렬이 base code 검사행렬 `B`의 CPM-dispersion과 동일함을 증명, 이는 부분기하(partial geometry)의 line-point incidence matrix로 girth≥6 보장.
6. 확장(Binary Decomposition Theorem, 정리 1): `v`가 GF(2^s) 위 전역 부호어일 필요충분조건은 `s`개 이진 성분벡터 각각이 동일한 `Hglobal`(GF(2) 행렬)의 null space에 속하는 것.
7. 구현 디테일: 이를 통해 단일 비이진 디코더 대신 `s`개의 독립적 이진 소프트결정 디코더(scaled MSA, scaling factor 0.625~0.75)를 완전 병렬로 구동.
8. 최적화 절차: 별도 학습/최적화 없음(대수적 구성 + 고정 스케일링 팩터 MSA).
9. 결과: (127,113) BCH 기반 예제에서 WER 10^-5 기준 독립 MLD 대비 1dB, BM-HDDA 대비 3.7dB 이득; (16129,15372) 이진 QC-LDPC는 BER 10^-15까지 error floor 없음; 반복당 amortized 복잡도 `Navg = 3mn/(ns)*ns = 3mn`으로 선형.
10. 한계: HW 미설계, AWGNC 전용(다중경로 페이딩 미고려), 다중 사용자 OFDM 응용에 특화되어 NAND 단일 스트림 ECC와는 문제 설정이 다름.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 전역 QC-LDPC 부호구성 (partial geometry 기반 CPM(B)) | `ecc_top.cpp` `Load_PCM()` | H-matrix를 부분기하로 새로 설계하는 것은 특정 QC-LDPC 고정된 Prime ECC에 재검증 부담이 큼 |
| Scaled Min-Sum 반복복호 | `decoder.cpp` `LDPC_Decoder()`, `CNU_Update_New_Mag()` | 이미 보유한 표준 min-sum과 동일 계열, 신규성 없음 |
| Binary Decomposition Theorem(비이진→이진 병렬 분해) | 대응 없음 | Prime ECC는 애초에 binary LDPC 전용이라 비이진 GF(2^s) 분해 자체가 불필요 |
| 다중 사용자 GFT 다중화/역다중화 | 대응 없음 | NAND ECC는 단일 채널·단일 스트림 구조로 다중접속 다중화 개념이 대응되지 않음 |

> 적용 가치: **낮음** — 결과 부호가 QC-LDPC 형태이나 본 논문의 핵심 기여(GFT 기반 다중 사용자 결합, 비이진 분해 정리)는 NAND의 단일 채널 binary LDPC ECC 설계·복호와 직접 연결되지 않으며, 사용된 디코더도 표준 scaled MSA로 Prime ECC가 이미 보유한 기법과 중복됨.

### D. JSON 블록

```json
{
  "id": "arxiv:2605.09865v1",
  "title": "A Global Coding Scheme for OFDM over Finite Fields",
  "year": 2026,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": "0.89~0.955",
  "code_length": "7921~16129",
  "soft_quant": "soft-4bit+",
  "key_contribution": "다중 사용자 스트림을 GFT로 결합해 GF(2^s) 위 global QC-LDPC를 만들고 이를 s개 병렬 이진 소프트결정 디코더(MSA)로 분해 복호함",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "다중 사용자 OFDM/무선 통신(AWGNC) 맥락의 부호 구성법으로 NAND 단일 채널 ECC와 목적·채널 모델이 다름",
  "todo_check": "논문이 부수적으로 언급한 cyclic LDPC 기반 base code 확장이 NAND용 짧은 QC-LDPC 설계에 참고될 수 있는지"
}
```
