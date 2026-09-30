### arxiv:1902.01212v2 - Model-Based Detector for SSDs in the Presence of Inter-cell Interference (2019, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 직접 |
| 대상 | other |
| 부호종류 | 미상 |
| 부호rate | 0.89 |
| 부호length | 9216 |
| 연판정 | soft-2~3bit |
| 핵심기여 | 공통 aggressor로 인한 인접셀 상관을 FSMC로 모델링해 sum-product로 soft LLR을 계산, ICI 완화 |
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
| 추천도 | 중 |
| 한계,주의 | 채널 파라미터 완전 지식 가정, 양자화 시 이득 급감(99.7%->14.1%), MLC(q=4) 전용 모델 |
| 추가확인 | 반복 검출/복호(MaxOut=10) 시 LDPC 디코더 호출 횟수가 NAND latency에 미치는 영향, binary SLC 확장 가능성 |

> 총평: LDPC 디코더 자체가 아닌 앞단 soft-detector(채널 LLR 생성)를 개선하는 논문으로, Prime ECC의 channel/LLR 모듈에 간접 이식 가능하나 디코더/부호설계에는 직접 대응 없음.

### B. 알고리즘 요약

1. 대상 시스템: MLC(`q=4`) NAND, ABL + full-sequence WL 프로그래밍, rate-0.89/length-9216 LDPC + soft 복호.
2. 문제: 기존 채널 모델은 셀을 i.i.d.로 가정해 ICI를 독립 잡음 처리 -> 인접 victim 셀 간 상관을 무시.
3. 핵심 가정: victim 셀은 다음 WL의 3개 이웃으로부터만 ICI를 받고(`γv`, `γd`), 공통 aggressor가 인접 셀을 상관시킴.
4. 핵심 기법 1단: 셀 상태 `Si=(X^a_{i-1},X^a_i,X^a_{i+1})`를 aggressor 입력으로 정의 -> 채널이 FSMC로 환원, `p(y_i|x_i,s_i)=N(v x_i+ψ(s_i), σ²+θ²(s_i))`.
5. 핵심 식 의미: FSMC로 보면 인접 상태가 2성분 공유하는 Markov chain이 되어, 지수적 `q^n` 혼합 대신 tractable factor graph로 표현.
6. 핵심 기법 2단: factor graph(tree)에 sum-product를 forward/backward 1회 실행(Algorithm 1)해 각 셀 posterior `p(x_i|y)`를 정확히 계산, 복잡도 `O(n)`.
7. 부수 트릭: posterior를 LLR로 매핑해 soft-LDPC에 전달; LSB/MSB 페이지에 3/6 read reference로 상호정보 최대화 양자화(Kurkoski-Yagi) 적용.
8. 확장(양자화 대책): 검출<->복호 사이 outer iteration(`MaxOut=10`, `MaxIn=20`)으로 decoder posterior를 detector prior로 되먹임(iterative receiver).
9. 결과: 미양자화 시 강한 diagonal coupling에서 coded BER 최대 99.99% 감소; 양자화 시 14.1%로 급감하나 iterative scheme으로 ICI-limited 영역에서 수 order 회복.
10. 한계: HW 미설계, 시뮬만, 채널 파라미터 완전 지식 가정, MLC 전용 모델(binary 확장 미검증).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| soft LLR 생성 / soft-read threshold | channel.cpp `Set_R_Offset()`, `Set_LLR_Th()` | FSMC 기반 posterior->LLR을 채널 LLR 생성부로 대체/보강 가능 |
| 상호정보 최대화 양자화 테이블 | channel.cpp + `PARAM_LLR` (LLR 테이블) | LSB/MSB read reference 양자화가 LLR 파라미터 설계에 대응 |
| sum-product FSMC detector 알고리즘 | 대응 없음 | 앞단 detector이며 LDPC 디코더 루프(min-sum) 밖 -- 구조적 대응 없음 |
| 검출<->복호 outer iteration | 대응 없음 | Prime ECC는 단일 디코더 루프 구조, 외부 detector 되먹임 경로 없음 |

적용 가치: **중간** -- 디코더/부호 자체가 아니라 채널 soft-input 정확도를 높이는 기법이라 channel/LLR 모듈에 이식 여지는 있으나, ICI 완화 detector가 별도 앞단 블록이고 채널 파라미터 완전 지식·MLC 가정이 NAND 실측 적용의 장벽이다.

### D. JSON 블록

```json
{
  "id": "arxiv:1902.01212v2",
  "title": "Model-Based Detector for SSDs in the Presence of Inter-cell Interference",
  "year": 2019,
  "venue": "arXiv cs.IT",
  "portability": "중",
  "nand_relevance": "직접",
  "target": "other",
  "code_type": "미상",
  "code_rate": 0.89,
  "code_length": "9216",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "공통 aggressor로 인한 인접셀 상관을 FSMC로 모델링해 sum-product로 soft LLR을 계산, ICI 완화",
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
  "recommend": "중",
  "caveat": "채널 파라미터 완전 지식 가정, 양자화 시 이득 급감(99.7%->14.1%), MLC(q=4) 전용 모델",
  "todo_check": "반복 검출/복호(MaxOut=10) 시 LDPC 디코더 호출 횟수가 NAND latency에 미치는 영향, binary SLC 확장 가능성"
}
```
