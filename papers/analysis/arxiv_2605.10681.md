### arxiv:2605.10681v1 - Scalable Mamba-Based Message-Passing Neural Decoder for Error-Correcting Codes (2026, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | irregular |
| 부호rate | 0.75~0.83 |
| 부호length | 49~9984 |
| 연판정 | soft-4bit+ |
| 핵심기여 | attention을 Mamba SSM으로 대체해 Tanner-graph 메시지패싱 NN 디코더를 긴 부호로 선형 메모리 스케일링 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 NN(GPU FP32) 디코더로 HW 미설계·min-sum 대체 불가, non-NAND(AWGN/BPSK) 벤치마크 |
| 추가확인 | 없음 |

> 총평: attention-free NN 디코더로 학술적 스케일링 기여는 있으나 Prime ECC의 min-sum HW 파이프라인에 이식 불가.

### B. 알고리즘 요약

1. 시스템: 이진 선형블록부호(BCH/Polar/LDPC), BPSK, AWGN 채널. LDPC 예시 `(1056,880)` WiMAX, 5G BG1 rate 11/12로 `n=208~9984`.
2. 문제: ECCT/CrossMPT 등 attention 기반 NN 디코더는 attention map이 `O(n^2)`로 메모리·연산이 긴 부호에서 폭증.
3. 모델: syndrome-based 정식화 - 입력은 신뢰도 `my=|y|`와 부호화 syndrome `sy=τ(H·yb)`, 오류지시자 `ε` 복원.
4. 핵심기법1: VN 스트림 `M∈R^{n×d}`, CN 스트림 `S∈R^{(n-k)×d}` 유지하며 Tanner edge를 따라 CrossMPT식 교대 메시지패싱.
5. 핵심식: edge `(j,i)`마다 compact pairwise feature `φ=[m̃⊙s̃ ; m̃-s̃]`와 스칼라 score `f=w2ᵀ·SiLU(W1·φ)`를 softmax `α`로 정규화 - attention을 대체하는 국소 집계.
6. 핵심기법2: 각 스트림에 bidirectional Mamba(BiMamba) 블록 `Γ+λ·BiMamba(Γ)`으로 전역 장거리 전파를 선형시간에 수행.
7. 구현디테일: gated residual node update `ξ'=ξ+g⊙Δ`(GELU/sigmoid gate) + FFN, 출력head는 크기 무관 경량화(magnitude 스트림만).
8. 학습: 전부호 학습 불필요(선형성으로 all-zero codeword 학습), BCE loss로 오류지시자 예측, 파라미터 ~1.2M 정렬.
9. 결과: `(1056,880)`에서 CrossMPT 대비 0.45dB 이득 + 메모리 1.5배 절감, 긴 부호일수록 절감폭 증가(edge 수 `O(|E|)` 선형).
10. 한계: 순수 NN 디코더로 HW 미설계, GPU(H200 FP32) 시뮬만, min-sum/양자화 기반 NAND ECC와 접점 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Mamba/attention-free NN 디코더 백본 | 대응 없음 | NN 딥러닝 디코더는 Prime ECC의 min-sum HW 모델과 무관 |
| Tanner-graph 메시지패싱(VN/CN 교대) | decoder.cpp `LDPC_Decoder()`, `C2V_Cal()` | 개념적 대응이나 학습형 집계라 min-sum 루프에 이식 불가 |
| syndrome/채널 입력(my, sy) | channel.cpp `Set_LLR_Th()` | soft-info 개념만 유사, 양자화·threshold 재사용 불가 |

적용 가치: **낮음** - 순수 학습형 NN 디코더로 HW 미설계이며 Prime ECC의 min-sum bit-exact 파이프라인에 떼어 쓸 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2605.10681v1",
  "title": "Scalable Mamba-Based Message-Passing Neural Decoder for Error-Correcting Codes",
  "year": 2026,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "irregular",
  "code_rate": null,
  "code_length": "49~9984",
  "soft_quant": "soft-4bit+",
  "key_contribution": "attention을 Mamba SSM으로 대체해 Tanner-graph 메시지패싱 NN 디코더를 긴 부호로 선형 메모리 스케일링",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 NN(GPU FP32) 디코더로 HW 미설계·min-sum 대체 불가, non-NAND(AWGN/BPSK) 벤치마크",
  "todo_check": "없음"
}
```
