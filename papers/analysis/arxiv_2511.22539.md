### arxiv:2511.22539v1 - TransCoder: A Neural-Enhancement Framework for Channel Codes (2025, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 0.3~0.83 |
| 부호length | 31~512 |
| 연판정 | soft-4bit+ |
| 핵심기여 | transformer 기반 code-adaptive 신경 인코더/디코더 모듈로 기존 ECC의 BLER를 향상(TransCoder) |
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
| 한계,주의 | 송신단 신경 인코더가 실수 심볼 생성(BPSK/QPSK 무선 AWGN 전제) - NAND는 송신단 심볼 shaping 불가로 인코더 이식 불가; 신경망 학습 필요 |
| 추가확인 | 인코더 없이 수신단 refinement decoder만 min-sum LDPC에 결합 시 BLER 이득 여부 |

> 총평: 무선 AWGN 채널에서 송수신 양단에 transformer 신경 모듈을 덧붙여 기존 ECC의 BLER를 개선하는 프레임워크로, 송신 심볼 shaping과 신경망 학습을 전제해 NAND binary QC-LDPC ECC에는 이식 불가.

### B. 알고리즘 요약

1. 시스템: AWGN 무선 채널, BPSK/QPSK 변조, 기존 선형블록부호(LDPC/BCH/Polar/Turbo) `C(n,k)` 구조를 **유지**하면서 성능만 향상.
2. 문제: 완전 신경 디코더(ECCT/CrossMPT)는 BER는 개선하나 복잡도·메모리 폭증, BLER 이득은 미미 - 실용 배치 곤란.
3. 핵심기법: transformer encoder 기반 `block attention` 모듈을 송신단 신경 인코더 `E_T`(codeword→실수심볼 `s∈R^n`)와 수신단 디코더 `D_T`·refinement `D_Trf`로 삽입, 기존 채널 디코더는 파이프라인 내부에 유지.
4. 반복복호: `D_Trf`가 채널출력 `y`와 채널디코더의 soft estimate `x`를 함께 입력받아 block-wise 확률 갱신, `r`회 refinement 루프.
5. 메시지 변환: `f_m2d`로 block 확률→bit LLR, `f_d2m`으로 soft estimate를 [-1,1]로 역변환하여 채널출력과 정렬.
6. 정규화: index별 power normalization + 학습 벡터 `w`로 심볼 power 재할당(평균전력 제약 (2) 충족).
7. 손실: end-to-end BCE(`L_CD`)에 더해 BP 디코더용 soft parity-check 정규화 손실 `L_H`(syndrome 기반 multi-label) 결합.
8. 학습: AWGN Eb/N0 [2,8]dB 균등샘플, backprop 가능한 채널디코더 통해 end-to-end 학습(polar SC는 신경 근사기 사용).
9. 결과: LDPC(384,192)에서 BP-20·CrossMPT 대비 BLER 10^-5에서 1dB 이득; TransCoder 모듈 10~15k params(ECCT 1.2M), FLOPs·복잡도 ECCT 대비 2 orders 낮음; 긴 부호(>64)·저rate에서 강점.
10. 한계: 시뮬(RTX A6000)뿐, HW 미설계; 송신단 실수심볼 생성·신경망 학습 전제, 무선 AWGN·BPSK 특화.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 송신단 신경 인코더 `E_T`(실수심볼 생성) | 대응 없음 | NAND는 송신단 심볼 shaping/변조 없음, BPSK 전제 부적합 |
| 수신단 transformer 신경 디코더 `D_T`/`D_Trf` | 대응 없음 | NN 디코더는 프로파일상 "대응 없음"(min-sum 대체 불가) |
| 채널 디코더 반복복호 결합 | `decoder.cpp` `LDPC_Decoder()` | 개념상 iteration 루프에 닿으나 실제 결합은 NN 학습·실수 LLR 전제라 이식성 없음 |

적용 가치: **낮음** - transformer 신경 모듈을 송수신 양단에 덧붙이고 학습을 요구하는 접근이라 §5 판정필터의 "NN 전면 대체=낮음"에 해당, NAND binary QC-LDPC HW 디코더에는 떼어 쓸 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2511.22539v1",
  "title": "TransCoder: A Neural-Enhancement Framework for Channel Codes",
  "year": 2025,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "31~512",
  "soft_quant": "soft-4bit+",
  "key_contribution": "transformer 기반 code-adaptive 신경 인코더/디코더 모듈로 기존 ECC의 BLER를 향상(TransCoder)",
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
  "caveat": "송신단 신경 인코더가 실수 심볼 생성(BPSK/QPSK 무선 AWGN 전제) - NAND는 송신단 심볼 shaping 불가로 인코더 이식 불가; 신경망 학습 필요",
  "todo_check": "인코더 없이 수신단 refinement decoder만 min-sum LDPC에 결합 시 BLER 이득 여부"
}
```
