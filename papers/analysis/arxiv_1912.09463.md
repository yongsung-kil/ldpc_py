### arxiv:1912.09463v1 - Finite State Markov Modeling of Fading Channels Towards Decoding of LDPC Codes (2010, M.Tech thesis IIT Delhi)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.33~0.5 |
| 부호length | 2000~4000 |
| 연판정 | soft-2~3bit |
| 핵심기여 | Markov(GEC) 메모리 채널에서 sum-product에 BCJR형 helper block과 Baum-Welch 채널추정을 결합해 버스트 오류 정정 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | X |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | 채널 메모리(버스트) 가정 특화 - NAND는 대체로 메모리없는 오류모델, full-tanh sum-product·BCJR forward-backward로 HW 부담 큼 |
| 추가확인 | NAND read 오류가 상관성(버스트)을 가지는 상황이 있는지, 있다면 helper LLR 개념만 차용 가능한지 |

> 총평: Markov 메모리 채널 특화 sum-product+BCJR helper 디코더로 버스트 채널에선 이득이 있으나 메모리없는 NAND binary QC-LDPC 이식성은 낮음.

### B. 알고리즘 요약

1. 시스템: regular LDPC((2,4) rate 1/2, (4,6) rate 1/3), N=2000~4000, 2-state Gilbert-Elliott(GEC) Markov 노이즈 채널(good/bad 상태, bit-flip 잡음), 50 iteration.
2. 문제: 실채널 오류는 독립이 아니라 버스트로 발생 - 기존 memoryless sum-product는 채널 메모리를 활용 못해 버스트 정정 능력 미달.
3. 모델: 가법 잡음 `y = x ⊕ z`, `z`는 2-state MM(good/bad) 출력. 상태전이 `p(i|j)`, 상태별 오류확률 `q_{i←j}`.
4. 핵심 기법 1단(helper block): sum-product 결과 잠정어 `ĉ`로부터 상태 정보를 이용해 각 bit의 helper LLR `HΛ(dk)`를 계산(식 3.4), 이를 sum-product 입력 extrinsic으로 되먹임(turbo 원리).
5. 핵심 식: joint prob `ζ(i,m)=αk(i,m)·βk(m)`(식 3.9) - forward `α`/backward `β` 재귀(식 3.10/3.11)로 상태별 APP 계산(BCJR/forward-backward).
6. 핵심 기법 2단(Gallager 확률적 복호 재해석): 상태정보를 넣은 likelihood ratio(식 4.4)로 Gallager의 옛 probabilistic decoding을 side-information 버전으로 확장.
7. 부수: 상태별 오류확률 대비(contrast)가 클수록 상태 구분이 쉬워 이득 증가.
8. 학습/추정: 채널 파라미터(전이·오류확률) 미지 시 Baum-Welch(EM)로 온라인 추정(식 3.16~3.26).
9. 결과: helper block sum-product > 기본 sum-product, Gallager+side-info가 세 기법 중 최고 BER; 근사 DE(식 4.13)로 성공복호 영역(decoding region) 도출.
10. 한계: 채널 메모리(버스트) 가정 특화, HW 미설계, gate/throughput 없음, full-tanh sum-product + BCJR forward-backward로 연산 부담 큼, 부호설계는 미논의.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| sum-product LDPC 복호 루프 | decoder.cpp `LDPC_Decoder()` | Prime ECC는 tanh SPA 아닌 min-sum - 계열이 다름(대응 약함) |
| helper block LLR / 채널 상태 LLR | channel.cpp `Set_LLR_Th()`, `Set_R_Offset()` | 채널 LLR 생성부에 닿으나 GEC 상태모델은 우리 채널에 없음 |
| BCJR forward-backward / Baum-Welch 채널추정 | 대응 없음 | Prime ECC에 상태추정·EM 모듈 없음 |
| 근사 Density Evolution 부호영역 | 대응 없음 | 부호설계/DE 도구 미보유 |

적용 가치: 낮음 - 버스트(메모리) 채널 전제의 상태추정 helper가 핵심인데 NAND는 대체로 메모리없는 오류모델이고 Prime ECC는 min-sum 기반이라 이식 경로가 약하다.

### D. JSON 블록

```json
{
  "id": "arxiv:1912.09463v1",
  "title": "Finite State Markov Modeling of Fading Channels Towards Decoding of LDPC Codes",
  "year": 2010,
  "venue": "M.Tech thesis, IIT Delhi",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": null,
  "code_length": "2000~4000",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "Markov(GEC) 메모리 채널에서 sum-product에 BCJR형 helper block과 Baum-Welch 채널추정을 결합해 버스트 오류 정정",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "X",
  "latency": "악화",
  "recommend": "하",
  "caveat": "채널 메모리(버스트) 가정 특화 - NAND는 대체로 메모리없는 오류모델, full-tanh sum-product·BCJR forward-backward로 HW 부담 큼",
  "todo_check": "NAND read 오류가 상관성(버스트)을 가지는 상황이 있는지, 있다면 helper LLR 개념만 차용 가능한지"
}
```
