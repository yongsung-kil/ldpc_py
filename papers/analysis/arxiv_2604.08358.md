### arxiv:2604.08358v1 - Scalable Neural Decoders for Practical Fault-Tolerant Quantum Computation (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호length | 72~144785(surface: d^2, BB: 72~288) |
| 부호rate | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 코드의 기하학적 규칙성(국소성/이동등변성/방향성)을 이용한 CNN 기반 신경망 디코더(Cascade)로 quantum surface/BB code에서 BP+OSD 대비 최대 4000배 낮은 논리 오류율 달성 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | N/A |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | 양자 안정자 코드(surface code/BB code)의 spacetime syndrome, degenerate error, logical equivalence class 판정 문제이며 classical binary NAND LDPC의 hard/soft decision decoding 문제와 근본적으로 다름 |
| 추가확인 | 신경망 디코더의 국소성/이동등변성/방향성 설계 원칙이 classical QC-LDPC의 protograph 반복구조에 CNN 기반 디코더로 이식 가능한지 여부 (단, HW 미구현·GPU 추론 전제) |

> 총평: quantum error correction(surface/BB code)용 CNN 신경망 디코더로 waterfall 영역 논리오류율을 크게 개선했으나, 대상이 quantum stabilizer code이고 GPU 기반 미구현 하드웨어 추정치뿐이라 NAND classical binary LDPC ECC 이식 관점의 적용 가치는 낮음.

### B. 알고리즘 요약

1. 대상은 surface code와 Bivariate Bicycle(BB) quantum LDPC code(예: [[144,12,12]] Gross code)이며, 반복적 stabilizer 측정으로 얻은 spacetime syndrome에서 logical error class를 추론하는 문제.
2. 기존 BP는 quantum degeneracy로 인한 trapping set 때문에 수렴 실패가 잦고, BP+OSD/Tesseract 등 정확한 방법은 실시간 사용에 너무 느려 정확도-속도 trade-off가 존재.
3. 채널모델은 circuit-level depolarizing noise이며, 논리 오류율 `P_L ≈ Σ_w N(w) p^w`(가중치 w의 최소 실패모드 개수 N(w))로 모델링.
4. 핵심 기법: Cascade라는 CNN 디코더로, 코드의 국소성(locality)·이동등변성(translation equivariance)·방향성(anisotropy) 3가지 기하학적 성질을 만족하는 학습된 convolution을 BP의 고정된 message-passing 규칙 대신 사용.
5. 핵심 식 `h_v^(l+1) = Σ_{u∈N(v)} W_{δ(u,v)}^(l) h_u^(l) + W_self^(l) h_v^(l)` — 상대위치 δ에 따라 가중치를 공유하는 convolution으로 위치별 동일 규칙 적용.
6. 확장: surface code는 표준 3D convolution(3×3×3 커널), BB code는 torus 위 check-to-check를 check→data→check 2단계 bipartite convolution으로 분해해 커널 크기를 5배 축소.
7. 구현 디테일: bottleneck residual block(H→H/4→H), FP8 post-training quantization(정확도 손실 없음, ~16배 면적/전력 절감), depthwise convolution으로 추가 4배 절감(총 ~60배).
8. 학습 절차: Stim으로 온더플라이 데이터 생성, binary cross-entropy loss, Muon/Lion 옵티마이저, 저노이즈→목표노이즈로 점진 annealing하는 3단계 커리큘럼(grokking 유사 현상 회피).
9. 결과: Gross code에서 BP+OSD 대비 ~4000배, Relay 대비 ~17배 낮은 논리오류율(p=0.1%에서 P_L~10^-10), waterfall 지수 `P_L~p^11` vs distance-limited floor `P_L~p^6.4`, 처리량은 기존 대비 3,000~100,000배(GPU 추론 기준).
10. 한계: 실제 HW(FPGA/ASIC) 미구현이며 roofline 추정치일 뿐, GPU 추론 지연(~40µs/cycle)이 초전도 큐빗 예산(~1µs)에는 미달, 신경망 디코더 특유의 systematic misclassification floor 위험(경험적으로는 관측 안 됨).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| CNN 기반 message-passing 디코더(Cascade) | 대응 없음 (NN/딥러닝 디코더는 모듈 지도에 "대응 없음" 명시) | Prime ECC는 min-sum 기반 결정론적 C++ 디코더이며 학습형 신경망 디코더 자체가 이식 범위 밖 |
| BP trapping set / 4-cycle 유사 수렴 실패 | `decoder.cpp` `LDPC_Decoder()` | quantum degeneracy로 인한 trapping set 논의는 개념적으로만 classical BP trapping set과 유사하나 원인(양자 안정자 대칭성)이 달라 직접 대응 어려움 |
| waterfall/error-floor 두 영역 구조 분석 | `decoder.cpp` (error-floor 관련 일반론) | 최소 weight 실패모드 개수 분포로 waterfall/floor를 설명하는 프레임은 classical LDPC error-floor 분석과 유사한 개념이나, 본 논문 자체는 quantum 특유의 실패모드 계산에 의존 |

> 적용 가치: 낮음 — 핵심 기여(quantum stabilizer code 전용 CNN 디코더, GPU/미구현 FPGA 추정치)가 classical binary QC-LDPC의 min-sum 디코더 구조와 판정 문제 자체가 다르며, Prime ECC 모듈 지도상 "대응 없음"(NN/딥러닝 디코더)에 명시적으로 해당.

### D. JSON 블록

```json
{
  "id": "arxiv:2604.08358v1",
  "title": "Scalable Neural Decoders for Practical Fault-Tolerant Quantum Computation",
  "year": 2026,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "72~288(BB code), d^2(surface code)",
  "soft_quant": "무관",
  "key_contribution": "코드의 기하학적 규칙성을 이용한 CNN 기반 신경망 디코더(Cascade)로 quantum surface/BB code에서 BP+OSD 대비 최대 4000배 낮은 논리 오류율 달성",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "N/A",
  "latency": "개선",
  "recommend": "하",
  "caveat": "양자 안정자 코드의 spacetime syndrome, degenerate error, logical equivalence class 판정 문제로 classical binary NAND LDPC의 decoding 문제와 근본적으로 다름",
  "todo_check": "국소성/이동등변성/방향성 CNN 디코더 설계 원칙이 classical QC-LDPC protograph 구조에 이식 가능한지 확인 (HW 미구현 전제)"
}
```
