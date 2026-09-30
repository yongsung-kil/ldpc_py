### arxiv:1407.5136v1 - Rate-Compatible LDPC Codes Based on Puncturing and Extension Techniques for Short Block Lengths (2014, arXiv (cs.IT))

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | irregular |
| 부호rate | 0.1~0.9 |
| 부호length | 700~2000 |
| 연판정 | 무관 |
| 핵심기여 | cycle-counting/ACE 메트릭 기반 puncturing 3종과 extension 2종을 제안해, 짧은/중간 블록길이 irregular LDPC의 rate-compatible 패밀리를 짧은 사이클을 깨는 방식으로 구성 |
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
| 한계,주의 | 단일 고정 rate·고정 코드가 아닌 hybrid ARQ용 가변rate(puncturing/extension) 부호설계로, NAND ECC의 고정 고rate QC-LDPC 구조와 목적이 다름. HW 구현·복잡도 분석 없음 |
| 추가확인 | ACE 기반 puncturing/extension 아이디어를 고정 rate QC-LDPC의 H-matrix 설계 단계(정정능력 개선용 짧은사이클 최소화)에 부분 응용 가능한지 |

> 총평: 채널 적응형(hybrid ARQ) rate-compatible LDPC 코드 구성법 논문으로, AWGN 무선통신의 가변 rate 시나리오를 겨냥해 NAND 고정 고rate QC-LDPC ECC와는 목적·적용 환경이 다름.

### B. 알고리즘 요약 (10줄 내외)

1. 시스템: AWGN 채널, hybrid ARQ/FEC 시나리오. irregular LDPC 코드 A(N=1000, R=0.5)/코드 B(N=2000, R=0.4)/코드 C(N=1000, R=0.5)를 mother code로 사용, rate 0.1~0.9 범위의 rate-compatible(RC) 코드 패밀리 생성.
2. 문제: 채널 상태에 따라 다른 rate 코드를 매번 재설계하는 것은 비현실적이므로, 하나의 mother code에서 puncturing(고rate화)/extension(저rate화)으로 RC 코드 패밀리를 구성.
3. 가정: 짧은 사이클(short cycle)이 반복복호 성능을 저해한다는 전제 하에, 사이클 분포(cycle-counting) 또는 ACE(Extrinsic Message Degree) 메트릭으로 puncturing/extension 위치를 선정.
4. 핵심 기법 1(puncturing 3종): CC-based(사이클 카운팅 알고리즘으로 girth-length 사이클 많은 변수노드 우선 펑처), ACE-based(`α_sj = min{α_g, α_g2, α_g4}` 최솟값 변수노드 우선 펑처, 식 2·3), SIM-based(다수 랜덤 패턴 중 exhaustive search로 최소 평균 BER 선택, 식 4).
5. 핵심 식 의미: ACE 값이 클수록 사이클이 그래프 나머지와 singly-connected 되어 있어 stopping/trapping set 형성 확률이 낮음 → 낮은 ACE 값 노드부터 펑처하면 성능 저하 최소화.
6. 핵심 기법 2(extension 2종): B×B 서브행렬 `h_ext`를 S개 후보 중 CC-based(최대 girth·최소 사이클수) 또는 ACE-based(최대 평균 ACE 스펙트럼) 기준으로 선택해 다단계(level)로 parity-check 행렬을 확장(그림 1), dual-diagonal형 구조로 fast linear-time 인코딩 유지.
7. 부수 디테일: mother code는 improved PEG(ACE-PEG) 알고리즘으로 생성, 사이클 카운팅은 message-passing 기반 저복잡도 알고리즘(O(g|E|²)) 사용.
8. 최적화 절차: 없음(DE로 mother code degree distribution만 도출, 이후는 조합적 탐색/그리디 선택).
9. 결과: ACE-based puncturing이 unpunctured 코드 대비 BER 10⁻⁶에서 0.2dB 이내 성능차, CC-based extension은 기존 기법[24] 대비 우수, RC-LDPC 시스템 throughput이 AWGN 용량에 근접(Fig.8).
10. 한계: BP(로그영역) 표준 디코더만 사용, HW 설계·게이트카운트·throughput(Gbps) 분석 없음, 목적이 채널적응 가변rate(ARQ)로 NAND의 고정 고rate ECC와 상이.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| ACE 메트릭 기반 짧은 사이클 최소화 puncturing/extension | `ecc_top.cpp` `Load_PCM()` | H-matrix 설계 단계 아이디어이나 Prime ECC는 특정 고rate QC-LDPC 고정, rate-compatible 목적 자체가 대응 없음 |
| PEG 기반 mother code 생성 | `ecc_top.cpp` `Load_PCM()` | 부호구조 로드 지점과 연관되나 이식은 H-matrix 전면 재설계 수준(난이도 높음) |
| rate-compatible 가변 puncturing/extension 프레임워크 | 대응 없음 | Prime ECC는 고정 rate 단일 부호, hybrid ARQ 가변rate 개념 자체가 대상 밖 |
| 표준 BP(log-domain) 디코더 | `decoder.cpp` `LDPC_Decoder()` | 이미 보유한 min-sum과 유사하나 본 논문은 디코더 자체 개선 없이 표준 BP만 사용 |

> 적용 가치: 낮음 — 부호설계는 순수 QC-LDPC 구성법(ACE PEG)이 아닌 irregular RC-LDPC(puncturing/extension) 프레임워크로, Prime ECC의 고정 rate/고정 구조와 목적이 다르고 이식 시 H-matrix 재설계 부담이 크며 표준 교과서 수준 재사용에 가까움.

### D. JSON 블록 (DB 적재용)

```json
{
  "id": "arxiv:1407.5136v1",
  "title": "Rate-Compatible LDPC Codes Based on Puncturing and Extension Techniques for Short Block Lengths",
  "year": 2014,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "irregular",
  "code_rate": "0.1~0.9",
  "code_length": "700~2000",
  "soft_quant": "무관",
  "key_contribution": "cycle-counting/ACE 메트릭 기반 puncturing 3종과 extension 2종으로 짧은 사이클을 깨는 rate-compatible irregular LDPC 코드 패밀리 구성",
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
  "caveat": "hybrid ARQ용 가변rate(puncturing/extension) 부호설계로 NAND ECC의 고정 고rate QC-LDPC 구조와 목적이 다름, HW 구현/복잡도 분석 없음",
  "todo_check": "ACE 기반 짧은사이클 최소화 아이디어를 고정 rate QC-LDPC의 H-matrix 설계 단계에 부분 응용 가능한지 확인 필요"
}
```
