### arxiv:2501.14102v1 - 5G LDPC Linear Transformer for Channel Decoding (2025, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 5G-NR LDPC (protograph) |
| 부호rate | 0.5 |
| 부호length | 26~576 |
| 연판정 | soft-4bit+ |
| 핵심기여 | PCM을 self-attention 마스크로 넣은 완전미분가능 linear-attention transformer 디코더로 O(n) 복잡도 5G LDPC 복호 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | NN 전면 대체 디코더(GPU/Sionna, AWGN, 소형 PCM n=20~150), 1-iter BP만 능가·정식 BP 미비교, HW 미설계 |
| 추가확인 | 다반복 BP 대비 성능, 실수 LLR·GPU 의존성 제거 시 NAND HW에서 min-sum 대체 가능성 |

> 총평: 5G NR LDPC용 transformer(linear-attention) NN 디코더로 우리 min-sum QC-LDPC HW 파이프라인과 대응 모듈이 없어 이식성 낮음.

### B. 알고리즘 요약

1. 대상: 5G NR LDPC 및 regular LDPC, AWGN+QAM 채널, `rate=0.5`, 소형 블록 `(k,n)=(13,26)~(256,576)`, Sionna로 재현.
2. 문제: BP는 짧은/중간 블록에서 ML 성능 못 미치고, 일반 transformer 디코더는 코드 크기에 지수적 학습 복잡도(O(n^2))로 확장 불가.
3. 모델: 입력을 `X_nodes=[Λ(c); σ]` (LLR + syndrome `σ=Hc^T`) 연접으로 구성, 디코더 `De(X_nodes)`가 코드워드 추정.
4. 핵심 기법 1: PCM `H`를 self-attention mask로 주입(도메인 지식)해 Tanner-graph 구조를 attention에 반영.
5. 핵심 식: `Attention=softmax(QK^T/√dk)V` — attention을 완전연결 그래프로 보고 코드워드 원소 간 관계 학습.
6. 핵심 기법 2: Linformer식 linear attention — K,V를 저차원 `RN×K`(K≪N)로 사영해 score를 `RB×H×N×K`로 만들어 복잡도 `O(N^2)→O(N)`.
7. 구현 트릭: LLR은 `±20` 클리핑, mask division value=2, punctured 비트는 erasure(`ℓch=0`), shortened 비트는 known(`ℓch=∞`).
8. 학습: GPU에서 PCM shape별 약 6시간 학습, Eb/N0 8~15dB, lr 5e-3 cosine decay, linear transformer가 3배 빠르게 학습돼 더 많은 iteration 학습 가능.
9. 결과: regular transformer와 동등 BER, 1-iteration BP를 능가, 큰 블록에서도 BP 대비 경쟁력 있는 시간; GPU 메모리 한계로 대형 PCM 미검증.
10. 한계: NN 전면 대체(GPU 의존), 1-iteration BP만 기준(정식 다반복 BP 미비교), HW 미설계, AWGN/무선 채널 가정.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| transformer(NN) 디코더 전체 | 대응 없음 | 프로파일 §6에서 NN/딥러닝 디코더는 명시적 "대응 없음" |
| linear attention O(n) 복잡도 축소 | 대응 없음 | 우리 디코더는 min-sum message passing, attention 구조 무관 |
| LLR/syndrome 입력 구성 (`Λ(c)`, `σ`) | channel.cpp `Set_LLR_Th()`, `decoder.cpp` | LLR·syndrome 개념은 공유하나 float LLR·GPU 기반이라 HW 양자화와 상이 |
| 5G NR base graph lifting / PCM | ecc_top.cpp `Load_PCM()` | QC-lifting 개념 유사하나 5G-NR 부호로 우리 고정 QC-LDPC와 다름 |

적용 가치: 낮음 — NN(transformer) 전면 대체 디코더로 프로파일이 명시한 "대응 없음" 범주에 해당하고, GPU·float 기반이라 NAND용 bit-exact min-sum HW 시뮬레이터에 떼어 쓸 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2501.14102v1",
  "title": "5G LDPC Linear Transformer for Channel Decoding",
  "year": 2025,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "protograph",
  "code_rate": 0.5,
  "code_length": "26~576",
  "soft_quant": "soft-4bit+",
  "key_contribution": "PCM을 self-attention 마스크로 넣은 완전미분가능 linear-attention transformer 디코더로 O(n) 복잡도 5G LDPC 복호",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "NN 전면 대체 디코더(GPU/Sionna, AWGN, 소형 PCM n=20~150), 1-iter BP만 능가·정식 BP 미비교, HW 미설계",
  "todo_check": "다반복 BP 대비 성능, 실수 LLR·GPU 의존성 제거 시 NAND HW에서 min-sum 대체 가능성"
}
```
