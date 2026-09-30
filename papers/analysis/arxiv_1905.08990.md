### arxiv:1905.08990v1 - MIST: A Novel Training Strategy for Low-latency Scalable Neural Net Decoders (2019, arXiv eess.SP)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5 |
| 부호length | 100~1000 |
| 연판정 | 무관 |
| 핵심기여 | CNN 신경망 디코더 + Mixed-SNR 독립샘플 훈련(MIST)으로 RNN 대비 8배 낮은 latency |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | 신경망 전면 대체 디코더, 소프트 BP보다 성능 낮고 NAND/HW 설계 전무 |
| 추가확인 | 없음 (신경망 디코더는 Prime ECC의 min-sum 구조와 무관) |

> 총평: 5G mmWave 대상 CNN 신경망 디코더로 min-sum 기반 NAND binary QC-LDPC에 이식할 요소가 없다.

### B. 알고리즘 요약

1. AWGN + BPSK 채널, rate `1/2` regular LDPC `(10,20)` 및 rate `1/2` 컨볼루션 부호(`(5,7)` octal), blocklength `n=100/200/1000`을 대상으로 한다.
2. 기존 RNN(Bi-GRU) 신경망 디코더는 near-optimal이지만 decoding latency가 커 실사용이 어렵고, CNN은 빠르지만 성능이 낮다는 통설을 깨는 것이 목표다.
3. 채널 모델은 `y = b + z` (z는 공분산 `σ²Iₙ`의 zero-mean 가우시안), 학습으로 `f(y)=arg max P(m|y)` 근사.
4. 핵심 기법: 1D CNN 3-layer(Conv+BatchNorm ×3 + Dense sigmoid)로 디코더를 대체, 출력 posterior를 양자화해 메시지 비트 복원.
5. 핵심 훈련기법 MIST: 매 iteration마다 codeword를 Monte-Carlo로 즉석 생성(고정 데이터셋 X)하여 과적합 회피, blocklength 1000에서도 전체 dataword의 1% 미만으로 학습.
6. MIST 확장: 각 배치 샘플의 SNR을 집합 `S`에서 균등 랜덤 샘플링해 광범위 SNR에 강건한 단일 디코더 확보.
7. 구현 디테일: kernel size 3→24, 각 층 커널 (10,50,50), ReLU, zero-padding, dropout 불필요(과적합 없음). loss는 `L(m,p̂)`=MSE.
8. 최적화: Adam, 초기 learning rate `10⁻³`, hyperparameter는 validation 없이 loss값으로 직접 튜닝.
9. 결과: 컨볼루션은 hard Viterbi/RNN과 동등, LDPC는 bit-flipping을 능가(단 BP보다는 열세). RNN 대비 latency 8배 감소(`n=1000`에서 170Kbps→1.25Mbps).
10. 한계: 고정채널에서 soft BP/unquantized Viterbi에 못 미치고, HW 미설계·시뮬만·NAND 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| CNN 신경망 디코더 (min-sum 전면 대체) | 대응 없음 | Prime ECC는 min-sum message-passing 기반, NN 디코더와 구조 불일치 |
| MIST 랜덤 SNR 훈련 | 대응 없음 | 학습 기반, bit-exact HW 시뮬과 무관 |
| posterior 양자화 출력 | 대응 없음 | 신경망 출력 양자화로 LLR 테이블과 성격 다름 |

적용 가치: **낮음** — NN 전면 대체 디코더이자 5G 무선 특화로 Prime ECC의 binary QC-LDPC min-sum 이식 대상이 전혀 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1905.08990v1",
  "title": "MIST: A Novel Training Strategy for Low-latency Scalable Neural Net Decoders",
  "year": 2019,
  "venue": "arXiv eess.SP",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": 0.5,
  "code_length": "100~1000",
  "soft_quant": "무관",
  "key_contribution": "CNN 신경망 디코더 + Mixed-SNR 독립샘플 훈련(MIST)으로 RNN 대비 8배 낮은 latency",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "개선",
  "recommend": "하",
  "caveat": "신경망 전면 대체 디코더, 소프트 BP보다 성능 낮고 NAND/HW 설계 전무",
  "todo_check": "없음 (신경망 디코더는 Prime ECC의 min-sum 구조와 무관)"
}
```
