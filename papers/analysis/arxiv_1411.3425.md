### arxiv:1411.3425v1 - Novel LDPC Decoder via MLP Neural Networks (2014, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.05~0.05 |
| 부호length | 20~60 |
| 연판정 | soft-4bit+ |
| 핵심기여 | LDPC Tanner graph 구조를 그대로 2-layer MLP 신경망으로 매핑, XOR 함수를 미분 가능 형태로 표현해 gradient descent로 입력벡터(수신 심볼) 자체를 반복 갱신하는 새로운 디코딩 방식 제안 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 극히 짧은 코드(N=20, N=60)만 시뮬, SPA(full sum-product) 대비 곱셈 연산수 기준 복잡도 비교뿐 HW 구현·양자화·확장성 전혀 검증 안 됨 |
| 추가확인 | 실제 NAND급 길이(수천~수만 bit) QC-LDPC로 확장 시 학습(gradient descent) 수렴성과 지연이 어떻게 되는지 본문에 없음 |

> 총평: Tanner graph를 MLP로 재구성해 gradient descent로 디코딩하는 개념 증명 수준 논문으로, 극소형 코드 시뮬만 있고 min-sum 기반 HW 디코더와 근본적으로 다른 패러다임(딥러닝 전면 대체)이라 Prime ECC 이식 가치는 낮음.

### B. 알고리즘 요약

1. 대상은 (20,1,2), (60,1,3) 표기의 매우 짧은 정규(regular) LDPC 코드; 채널·rate 명시 없음(예제 코드 rate 극저, 사실상 toy 예제).
2. 기존 SPA(sum-product)는 근사 최적이나 곱셈 연산이 많아 복잡도가 높다는 문제의식에서, 반복적 최적화 구조를 신경망으로 대체하고자 함.
3. 채널/노이즈 모델은 별도 정의 없이 수신벡터 `r`을 신경망 입력으로 그대로 사용.
4. 핵심 기법: Tanner graph를 그대로 2-layer MLP로 매핑 — layer 1(입력)=variable node, layer 2(출력)=check node, 출력층 activation은 analog XOR 함수 `x⊕y = x(1-y)+y(1-x)`의 다변수 확장(`(12)`식).
5. 핵심 식은 SSE 손실 `E = (1/2)Σ o_j^2`(check node 출력이 0에 가까워지도록)이며, 이 손실의 gradient를 입력벡터(수신 심볼) `c_i`에 역전파해 반복 갱신(`(14)`,`(16)`).
6. 미분 가능한 XOR의 편미분 `∂o_j/∂c_i = ∏(1-2c_l)`을 Lemma로 유도(`(17)`,`(25)`)해 gradient 계산 가능하게 함.
7. 부수 트릭: 학습 대상은 신경망 가중치가 아니라 "입력벡터 자체"이며, 매 반복마다 갱신된 입력을 0/1로 유클리드 거리 기준 매핑해 추정 코드워드로 사용.
8. 최적화 절차는 gradient descent(학습률 `η` 선택이 성능 좌우), 별도 학습 데이터셋/오프라인 훈련 없음(온라인 반복만).
9. 결과: SPA 대비 곱셈수 기준 복잡도가 예제1(N=20)에서 160→80, 예제2(N=60)에서 540→320로 감소(약 2배↓), BER은 SPA와 근접.
10. 한계: 극소형 코드 2개 예제뿐, HW/게이트/양자화 미검토, 코드 길이·H밀도 증가 시 복잡도 격차가 선형/제곱으로 커진다고만 언급되고 실측 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| MLP 기반 신경망 디코더 전체 | 대응 없음 | 프로파일 §6에 "NN/딥러닝 디코더는 대응 없음"으로 명시된 이질적 패러다임 |
| gradient descent 기반 입력벡터 갱신 | 대응 없음 | min-sum 기반 message passing(`decoder.cpp` `LDPC_Decoder()`)과 연산 구조 자체가 다름 |
| SSE 기반 복잡도(곱셈수) 비교 | 대응 없음 | HW gatecount/throughput 등 실제 구현 지표와 무관한 이론적 지표 |

> 적용 가치: 낮음 — 신경망 전면 대체 디코더로 Prime ECC의 min-sum/HCU/pipeline HW 구조와 이질적이며, 검증도 극소형 코드(N≤60) 시뮬에 그침.

### D. JSON 블록

```json
{
  "id": "arxiv:1411.3425v1",
  "title": "Novel LDPC Decoder via MLP Neural Networks",
  "year": 2014,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "20~60",
  "soft_quant": "soft-4bit+",
  "key_contribution": "LDPC Tanner graph를 2-layer MLP로 매핑하고 미분 가능 XOR로 gradient descent 기반 반복 디코딩을 제안",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "극히 짧은 코드(N=20, N=60)만 시뮬, HW 구현·양자화·확장성 전혀 검증 안 됨",
  "todo_check": "실제 NAND급 길이 QC-LDPC로 확장 시 gradient descent 수렴성과 지연이 어떻게 되는지 본문에 없음"
}
```
