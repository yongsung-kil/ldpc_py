### arxiv_1104.1457v1 - High-Rate Short-Block LDPC Codes for Iterative Decoding with Applications to High-Density Magnetic Recording Channels (2011, arXiv [cs.IT])

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | regular |
| 부호rate | 0.94~0.978 |
| 부호length | 561~2080 |
| 연판정 | soft-2~3bit |
| 핵심기여 | 조합설계(Steiner) 기반 Triangle/SPC 고rate·단블록 LDPC로 TPC/SPC 대비 절반 길이·복잡도 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 자기채널 특화, dH=3로 minimum distance 낮음, HW 미설계·시뮬만 |
| 추가확인 | interleaving gain이 NAND 채널(무 ISI)에서도 성립하는지 |

> 총평: 자기기록 채널용 조합설계 고rate LDPC 구성법으로 NAND binary QC-LDPC와 부호구조·채널 모두 상이해 이식성 낮음.

### B. 알고리즘 요약

1. 시스템: SISO 등화기(BCJR) + 내부 고rate LDPC(T/SPC) + 외부 RS/BCH의 반복 수신기, 고밀도 수직 자기기록 채널.
2. 문제: 고속(4Gb/s+) 반복 수신기의 높은 구현 복잡도와 error-floor, 짧은 섹터에 맞는 고rate·저복잡 LDPC 필요.
3. 채널 모델: microtrack 모델, transition jitter noise(i.i.d. 가우시안) + 전자 noise, 밀도 `D=PW50/T`.
4. 핵심 기법: 조합설계(combinatorial design)의 incidence matrix 전치를 `H`로 사용, 2D-T/SPC(N)를 (N-1,2,2)-Steiner-system에서 유도.
5. 부호 파라미터: `dH=3`, length `n=N(N+1)/2`, rate `R=(N-1)/(N+1)`, check `N+1`, 열가중치 γ=2로 length-4 cycle 없음(λ=1).
6. 확장: M차원 T/SPC로 일반화 가능(`dH=M+1`), 본 논문은 2D에 집중.
7. 구현 디테일: min-sum 근사 SPA 2 iteration만 수행, random-design interleaver 결합.
8. 복잡도: edge 수 `Ne=N(N+1)` (T/SPC) vs `2N^2` (TPC/SPC) → 메모리·상호연결 약 1/2.
9. 결과: rate 0.94/0.969에서 lT=2nT interleaver로 TPC/SPC 대비 최대 0.3dB SNR gain(BER=1e-4), 섹터당 오류분포는 TPC/SPC와 유사.
10. 한계: HW 미설계·시뮬만, minimum distance 낮음(dH=3), 자기기록 채널·SISO 등화기 가정에 종속.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| T/SPC H-matrix 조합설계 구성 | `ecc_top.cpp` `Load_PCM()` | 부호구조가 QC-LDPC 아님(Steiner triangular), 직접 로드 불가 |
| min-sum SPA 반복 복호 | `decoder.cpp` `LDPC_Decoder()`, `C2V_Cal()` | min-sum은 이미 보유, 중복 |
| SISO 등화기(BCJR) 연동 | 대응 없음 | Prime ECC는 NAND 채널로 등화기 없음 |

적용 가치: **낮음** — 자기기록 전용 조합설계 부호로 Prime ECC의 QC-LDPC·NAND 채널과 부호구조/채널 모두 정합되지 않고 복호기법(min-sum)은 이미 보유.

### D. JSON 블록

```json
{
  "id": "arxiv:1104.1457v1",
  "title": "High-Rate Short-Block LDPC Codes for Iterative Decoding with Applications to High-Density Magnetic Recording Channels",
  "year": 2011,
  "venue": "arXiv [cs.IT]",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "regular",
  "code_rate": "0.94~0.978",
  "code_length": "561~2080",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "조합설계(Steiner) 기반 Triangle/SPC 고rate·단블록 LDPC로 TPC/SPC 대비 절반 길이·복잡도",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "자기채널 특화, dH=3로 minimum distance 낮음, HW 미설계·시뮬만",
  "todo_check": "interleaving gain이 NAND 채널(무 ISI)에서도 성립하는지"
}
```
