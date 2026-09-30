### arxiv:2408.12154v1 - Binary codes from subset inclusion matrices (2024, arXiv math.CO)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 0.71~0.79 |
| 부호length | 2310~27720 |
| 연판정 | hard-1bit |
| 핵심기여 | Wilson subset-inclusion 행렬 `W_{t,n,k}` 기반 binary 부호의 최소거리 정확값(t<=3) 규명 및 circulant lifting으로 QC-LDPC 구성 |
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
| 한계,주의 | 최소거리 이론(design/ILP)이 주내용, 디코딩 성능은 MacKay 랜덤부호와 "유사"할 뿐 이득 없음 |
| 추가확인 | Wilson 행렬 rate/degree가 Prime ECC 고rate(~0.9)·VN degree 17·z=32와 맞출 수 있는지 |

### B. 알고리즘 요약

1. 대상: t-subset 대 k-subset inclusion 행렬 `W_{t,n,k}`를 parity-check로 쓰는 binary 선형부호 `C_{t,n,k}` (n은 k에 선형 의존, 충분히 큰 n).
2. 문제: 이 부호족의 최소거리 `d_{t,n,k}`를 t<=3에 대해 정확히 결정 (기존엔 `t+2 <= d <= 2^{t+1}` 범위만 알려짐).
3. 핵심 대응: 부호의 nonzero codeword ↔ binary t-(n,k)-design(임의 t-subset이 짝수 블록에 포함) 1:1 대응(Prop.1), 최소거리=최소 블록수.
4. 핵심 기법 1단: design 구성법 4종(Subsets/Doubling/Generalized Pasch/Hadamard 2-(7,4,2))으로 블록수 상한 유도.
5. 핵심 식 의미: 하한은 derivative design `(D_i)'`가 (t-1)-design임을 이용한 재귀부등식 `d_{t,n,k} >= d_{t-1,n-1,k-1}+1`(식7·8) + Lucas 정리로 parity 판정.
6. 핵심 기법 2단: even-k의 3-design 최소블록수는 reduced incidence 행렬에 대한 **정수선형계획(ILP)** + MAGMA canonical-graph 동형제거 탐색으로 확정(Thm6).
7. 구현 디테일: C# 프로그램이 base(mother) 행렬에서 4-/6-cycle 없는 exponent 행렬(식3·4)을 랜덤+greedy 순서로 산출해 QC-LDPC 생성.
8. 학습/최적화: 없음(조합론+ILP 완전탐색), NN 무관.
9. 결과: `d_{t,n,k}` 정확값 표(Thm1~6), lift QC-LDPC 3종(len 2310/27720, dim 1816/19801) 생성; layered min-sum(AWGN)·multi-GDBF(BSC)에서 MacKay 랜덤부호와 **유사** 성능(우위 아님).
10. 한계: 순수 부호구성·최소거리 이론, HW/양자화/throughput 무설계, 디코딩 이득 미입증, rate/degree가 우리 고rate ECC 스펙과 불일치 가능.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Wilson 행렬 → circulant lifting QC-LDPC 구성 | ecc_top.cpp `Load_PCM()` | H-matrix 후보 생성법이나 우리 부호 스펙(고rate·VN degree 17·z=32)과 정합 미확인, 재검증 부담 큼 |
| exponent 행렬 4-/6-cycle 회피(식3·4) | 대응 없음 | girth 확보는 표준 QC 설계지만 우리 코드에 고정 H가 이미 존재 |
| layered min-sum / GDBF 디코딩 | decoder.cpp `LDPC_Decoder()` | 이미 min-sum 보유, 논문은 디코더 개선 없이 부호만 테스트 |

적용 가치: **낮음** — 최소거리 이론이 주된 기여이고 디코딩 성능은 랜덤부호 수준(이득 없음), 산출 부호를 우리 고rate QC-LDPC 스펙에 맞추는 재검증 비용이 이득을 초과.

### D. JSON 블록

```json
{
  "id": "arxiv:2408.12154v1",
  "title": "Binary codes from subset inclusion matrices",
  "year": 2024,
  "venue": "arXiv (math.CO) preprint",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": "0.71~0.79",
  "code_length": "2310~27720",
  "soft_quant": "hard-1bit",
  "key_contribution": "Wilson subset-inclusion 행렬 W_{t,n,k} 기반 binary 부호의 최소거리 정확값(t<=3) 규명 및 circulant lifting으로 QC-LDPC 구성",
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
  "caveat": "최소거리 이론(design/ILP)이 주내용, 디코딩 성능은 MacKay 랜덤부호와 유사할 뿐 이득 없음",
  "todo_check": "Wilson 행렬 rate/degree가 Prime ECC 고rate(~0.9)·VN degree 17·z=32와 맞출 수 있는지"
}
```
