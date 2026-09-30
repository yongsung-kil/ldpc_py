### arxiv:0704.2258v2 - On the Hardness of Approximating Stopping and Trapping Sets (2008, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | LDPC/선형블록코드 Tanner graph의 stopping/trapping set 최소크기를 근사하는 문제가 NP-hard임을 다수 디코더(ER/ZP/GA/AWGN)에 대해 증명 |
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
| 한계,주의 | 순수 계산복잡도(NP-hardness/근사불가능성) 증명 논문으로 실제 디코딩 알고리즘·수치결과·HW 요소 없음 |
| 추가확인 | 없음 |

> 총평: stopping/trapping set 열거 기반 error-floor 추정 기법의 이론적 한계(근사 불가능성)를 증명하는 계산복잡도 논문으로 NAND ECC 실무 이식 가치 없음.

### B. 알고리즘 요약

1. 대상은 선형 블록코드(및 LDPC 코드) Tanner graph에서 정의되는 stopping set(BEC, edge-removal 디코더 실패조건), ZP/GA trapping set(BSC, bit-flipping/Gallager-A 디코더), AWGN (a,b)-trapping set/elementary/majority trapping set 등 여러 실패 집합 구조.
2. 문제의식은 error-floor 높이를 추정하는 기존 기법들이 "가장 작은 stopping/trapping set을 열거"하는 방식에 의존하는데, 이 최소집합 탐색(근사 포함)이 계산적으로 다루기 어려운지 규명하는 것.
3. 핵심 가정/모델은 별도 채널 노이즈 모델이 아니라 각 디코더(ER-BEC, ZP-BSC, Gallager A-BSC, sum-product-AWGN)별로 정의된 "디코더가 실패하는 정점 부분집합" 조합 구조를 그래프 이론적으로 정의.
4. 핵심 기법은 각 문제(MinStop, MinCStop, MinTrapZP, MinTrapGA, MinTrapAWGN, MinTrapAWGN-elem, MinTrapAWGN-maj)를 Minimum Set Cover / Minimum Distance(MinCodeword) / Maximum 3-Dimensional Matching 등 이미 알려진 NP-hard 문제로부터 다항시간 환원(reduction)하여 근사불가능성을 증명.
5. 핵심 결과 예: MinStop은 `c log N` 인수 내 근사가 NP-hard(Theorem 1), MinTrapZP/GA/AWGN은 상수 인수 근사조차 `RP=NP`가 아니면 불가능(Theorem 2~4).
6. LDPC(희소 H, 열/행 차수 상수 bound)로 제한된 클래스에서도 동일 하드니스가 성립함을 별도 환원으로 재증명(Section 5, Theorem 8~10) — 일반 코드뿐 아니라 실제 LDPC에도 적용됨을 보임.
7. 부수적으로 MinCStop(cover stopping set)에 대해서는 `O(log n)` 근사를 주는 그리디 다항시간 알고리즘을 제시(MinHitSet 환원 경유), 유일하게 실행 가능한 근사 결과.
8. Fixed-Parameter Tractability(FPT) 분석: 최소 stopping/trapping set 크기 `κ`가 작을 때는(고정 파라미터) 다항시간 해법이 존재함을 보이고 복잡도 상한(`κ` 지수, `n` 선형)을 제시(Theorem 11, 12).
9. 결과 시사점: `κ`(최소 실패집합 크기)가 10~15 이하인 "좋은 코드"에서는 기존 열거법이 실용적으로 동작하지만, 그 이상에서는 열거 기반 error-floor 추정이 이론적으로 정확도를 보증할 수 없음(Corollary 6).
10. 한계: 실제 디코딩 알고리즘·시뮬레이션·HW 구현 전무, 순수 그래프 환원/복잡도 증명이며 NAND 채널이나 특정 코드 구성법과 무관한 범용 이론 결과.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| stopping/trapping set 근사 하드니스 증명 | 대응 없음 | 순수 이론 결과이며 Prime ECC의 min-sum 디코더 구현과 직접 대응되는 모듈 없음 |
| error-floor 추정 기법의 이론적 한계 논의 | `decoder.cpp` `LDPC_Decoder()` | error-floor는 언급되나 구체적 개선 알고리즘/파라미터가 아니라 추정기법의 계산복잡도 한계만 다룸 |
| LDPC H-matrix 열/행 차수 제약 하 하드니스(Section 5) | `ecc_top.cpp` `Load_PCM()` | H-matrix 구조를 다루지만 부호 구성법이 아닌 계산복잡도 분석이라 실질 이식 요소 없음 |

> 적용 가치: 낮음 — trapping/stopping set 근사의 계산복잡도 이론 논문으로 알고리즘·수치·HW 요소가 전무해 Prime ECC 이식 요소 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:0704.2258v2",
  "title": "On the Hardness of Approximating Stopping and Trapping Sets",
  "year": 2008,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "LDPC/선형블록코드 Tanner graph의 stopping/trapping set 최소크기를 근사하는 문제가 NP-hard임을 다수 디코더(ER/ZP/GA/AWGN)에 대해 증명",
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
  "caveat": "순수 계산복잡도(NP-hardness/근사불가능성) 증명 논문으로 실제 디코딩 알고리즘·수치결과·HW 요소 없음",
  "todo_check": "없음"
}
```
