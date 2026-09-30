### arxiv:1903.04656v3 - Deep Log-Likelihood Ratio Quantization (2019, EUSIPCO)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 미상 |
| 부호rate | 0.5 |
| 부호length | 648 |
| 연판정 | soft-4bit+ |
| 핵심기여 | deep autoencoder로 LLR을 3차원 sufficient-statistic 잠재공간으로 압축·양자화(2.7x 압축, <0.1dB 손실) |
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
| 한계,주의 | 무선 fading+256-QAM 수신 버퍼 압축 타깃, NN 재학습 필요·채널분포 취약, NAND read/LDPC 디코더 무관 |
| 추가확인 | 3-sufficient-statistic 압축 개념이 NAND soft-read LLR 저장 버퍼에 적용 가능한지(NAND는 QAM/fading 없음) |

> 총평: 무선 fading 수신단 LLR 저장버퍼 압축용 딥러닝 오토인코더로, NAND binary LDPC 디코더/부호설계와 무관하여 이식성 하.

### B. 알고리즘 요약

1. 시스템: SISO uncorrelated Rayleigh fading 채널 + 256-QAM, 표준 rate-1/2 LDPC(`N=648`, WiFi 802.11), 수신단 LLR 저장 압축이 목표.
2. 문제: 메모리 제약 수신기에서 LLR/soft-bit를 최소 bit로 저장해야 하며, 순진한 scalar 양자화는 압축률이 낮음.
3. 핵심 관찰: memoryless 채널에서 LLR은 `(G, r̃r, r̃i)` 3개 sufficient statistic으로 완전 복원 가능(`G=|h|^2/σn^2`가 순시 SNR).
4. 핵심 기법: deep autoencoder를 학습해 soft-bit 벡터 `Λi=tanh(Li/2)`를 잠재차원 3의 `z=(z1,z2,z3)`로 압축, decoder(또는 LUT)로 복원.
5. 잠재공간 양자화: `z`를 `[-δ,δ]`(δ=0.8) saturation 후 `Nb`-bit uniform 양자화 `Q(x)`, 학습 시엔 Gaussian noise layer로 양자화 잡음을 미분가능하게 근사.
6. 손실함수: 저(불확실) LLR을 더 정확히 복원하도록 가중 제곱오차 `Σ|Λj-Λ̃j|^2/(|Λj|+ε)`, encoder/decoder 마지막층 `tanh`로 `[-1,1]^3` 제약.
7. 구현: 6 hidden layer(f/g 각 3), 중간층 폭 O(K)=4K, ReLU(마지막 제외 tanh), Adadelta 학습, 여러 SNR 데이터 concat(별도 SNR 추정 불필요).
8. 결과(single): 12 vs 32 bit, 15 vs 40 bit 저장으로 <0.1 dB 손실, 약 2.7x 압축(오토인코더 자체 0.15 dB 손실 존재).
9. 결과(HARQ 2-Tx, equal gain combining `Li=L̃i(1)+Li(2)`): 15 bit로 32 bit와 거의 동일, 2.13x 압축; 9 bit면 1.77x(hard-output 근접).
10. 한계: 채널분포(h) 바뀌면 전체 재학습 필요, HW 미설계·시뮬 전용, 무선 QAM/fading 특화(NAND soft-read와 다른 세팅).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| LLR 양자화/저장(잠재공간) | channel.cpp `Set_LLR_Th()`, `Set_R_Offset()` | 우리는 iteration별 LLR threshold 테이블 기반, autoencoder 압축과 접근 상이 |
| soft-bit 표현 / LLR 계산 | ecc_data.h `PARAM_LLR` | LLR 파라미터 저장부에 개념적으로만 닿음 |
| deep autoencoder(NN) 압축 | 대응 없음 | Prime ECC는 NN/딥러닝 디코더·압축 미보유 |
| 256-QAM/fading 채널 모델 | 대응 없음 | NAND는 QAM/fading 없음, AWGN/RBER만 |

적용 가치: **낮음** — sufficient-statistic 압축 아이디어는 흥미로우나 무선 fading+QAM 수신 버퍼 압축 전용이고 NN 재학습·채널분포 의존이 커서 NAND binary QC-LDPC ECC 파이프라인에 이식 가치 낮음.

### D. JSON 블록

```json
{
  "id": "arxiv:1903.04656v3",
  "title": "Deep Log-Likelihood Ratio Quantization",
  "year": 2019,
  "venue": "EUSIPCO",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "미상",
  "code_rate": 0.5,
  "code_length": "648",
  "soft_quant": "soft-4bit+",
  "key_contribution": "deep autoencoder로 LLR을 3차원 sufficient-statistic 잠재공간으로 압축·양자화(2.7x 압축, <0.1dB 손실)",
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
  "caveat": "무선 fading+256-QAM 수신 버퍼 압축 타깃, NN 재학습 필요·채널분포 취약, NAND read/LDPC 디코더 무관",
  "todo_check": "3-sufficient-statistic 압축 개념이 NAND soft-read LLR 저장 버퍼에 적용 가능한지(NAND는 QAM/fading 없음)"
}
```
