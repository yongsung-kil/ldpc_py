### arxiv:2603.10192v1 - Learning to Decode Quantum LDPC Codes Via Belief Propagation (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호length | 144~882 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 순차(sequential) VN 스케줄링 순서를 Q-learning으로 학습해 BP 수렴성/FER을 개선하는 RL-SVNS 디코더를 제안하고, 잔여 신드롬 기반 국소 상태와 2차 이웃만 갱신하는 incremental 구현으로 추론 비용을 절감 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 없음 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | 대상 코드가 quantum(CSS/QLDPC, non-binary Pauli 4元) 특화이고 degeneracy 등 quantum 고유 문제가 핵심 동기라 부호설계 자체는 이식 불가; 스케줄링/incremental update 아이디어만 분리 이식 필요 |
| 추가확인 | Q-table 크기가 `2^Amax`(VN degree 기반) 스케일이라 NAND QC-LDPC의 VN degree(17)·col-block(129) 규모에서 상태공간이 실용적인지, 그리고 offline 학습된 정책이 다양한 H-matrix/degree 분포에 일반화되는지 확인 필요 |

> 총평: Quantum LDPC 전용 논문이지만 핵심 아이디어인 "학습된 순차 VN 스케줄(RL-SVNS)"과 잔여 신드롬 기반 국소/incremental 상태 갱신 기법은 classical binary LDPC의 shuffled/sequential decoding 스케줄 최적화에 개념적으로 이식 가능해 중간 수준의 관심 가치가 있음.

### B. 알고리즘 요약

1. 대상은 CSS/stabilizer QLDPC 코드(예: [[882,24,d]], [[144,12,12]] bivariate bicycle 등)로, X-only Pauli 채널과 depolarizing(4元 Pauli) 채널 모두 다루며 표준 flooding BP는 quantum degeneracy와 Tanner graph 내 짧은 cycle 때문에 수렴이 잘 안 되는 문제가 있다.
2. 풀려는 문제: 기존 sequential/shuffled BP(SVNS)는 순서를 고정/무작위로 정하지만 최적 갱신 순서는 신드롬 인스턴스마다 다르므로, 이를 매번 적응적으로 정하는 정책이 필요하다.
3. VN 스케줄링을 국소·신드롬 기반 상태를 갖는 Markov decision process로 정식화: 잔여 불일치 벡터 `δ = s ⊕ (H1·ê)`에서 VN `v_i`의 이웃 체크만으로 국소 상태 `σ_i`(비트마스크 정수, 이웃 체크의 unsatisfied 여부)를 정의.
4. Q-learning agent가 매 BP iteration 내에서 remaining VN 집합 중 `argmax Q(σ_i,i)`로 다음 갱신 VN을 선택(schedule-without-replacement)하며, 보상은 `r_t=(w_before-w_after)/A_a` + 신드롬 완전 일치 시 종료 보너스 +1로 정의(SVNS 메시지 갱신식 자체는 표준 BP tanh-product 그대로 유지).
5. Lemma 1: 한 VN의 hard decision이 뒤집히면 그 이웃 체크의 잔여 불일치 비트만 뒤집힌다는 성질을 이용해, 상태·우선순위 갱신을 "2차 이웃"(flip된 체크의 이웃 VN들)으로 국한하는 incremental 구현을 제안.
6. HW/구현 친화 트릭: edge-indexed adjacency array(CSR 유사 구조)로 이웃 순회 O(degree)화, CN별 tanh-product를 캐싱(`P_j=∏x_k`)해 재계산 방지, XOR 기반 O(1) 국소 상태 갱신(`σ_{i_k}←σ_{i_k}⊕β(k)`), max-heap 기반 O(log|R|) greedy VN 선택.
7. 확장(2단): depolarizing 채널(4元 Pauli I/X/Y/Z)에서는 HX/HZ 두 그래프에 대해 LLR 스트림 2개를 유지하는 quaternary-coupled SVNS(RL-QSVNS)로 확장, 상태는 두 잔여 마스크를 결합한 정수(`σ_i=σ_i^X+2^Amax·σ_i^Z`)로 정의.
8. 학습 절차: px(또는 depolarizing p)를 훈련 그리드 {0.03~0.07}에서 샘플링해 episode당 최대 Imax=100 BP iteration 동안 tabular Q-learning(`α=0.1, γ=0.9`, ε-greedy 선형감쇠) 수행, 총 Emax=10^5 episode.
9. 결과: [[882,24,d]] 코드에서 RL-SVNS가 flooding BP·random SVNS 대비 FER 2자릿수 이상 개선, 평균 iteration 수도 저px 영역에서 크게 감소하며 시뮬 범위 내 error-floor 미관측; BPGD와 결합한 RL-QSVNS-GD는 표준 QBPGD 대비 decimation 단계 수를 유의하게 줄임.
10. 한계: 대상이 quantum CSS 코드(4元 Pauli, degeneracy)에 특화되어 부호 자체·채널 모델은 NAND binary LDPC와 근본적으로 다르며, HW 구현/합성 없이 순수 소프트웨어 시뮬레이션(Q-table 기반 tabular RL)에 그침; Q-table 크기가 VN degree에 지수적으로 커 대규모/고차수 그래프로의 확장성은 불명.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 학습된 순차(sequential) VN 스케줄링(RL-SVNS) | `decoder.cpp` `LDPC_Decoder()`, `C2V_Cal()` | 현재 Dual-Update(even/odd 교대)는 고정 스케줄이며, 논문의 적응형 순차 스케줄 아이디어는 스케줄링 레이어 개선 후보이나 quantum 특화 학습 프레임워크라 이식 난이도는 낮음~중 |
| 잔여 신드롬 기반 국소 상태·incremental 갱신(2차 이웃만 갱신, XOR 트릭) | `decoder.cpp` `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | 조기 수렴/redundant 연산 축소 아이디어로 min-sum 반복 루프에 참고 가능하나 코드 자체 수정 없이는 직접 대응 없음 |
| CN tanh-product 캐싱 | 대응 없음 | Prime ECC는 min-sum(비-tanh) 기반이라 직접 대응 없음 |
| Non-binary/quaternary Pauli 채널 모델, degeneracy 처리 | 대응 없음 | binary LDPC 전용 코드베이스와 무관 |

적용 가치: 중간 — quantum 특화 채널·부호 자체는 이식 불가하지만, "학습 기반 적응형 순차 스케줄"과 "국소/incremental 상태 갱신" 아이디어는 Prime ECC의 반복 루프(Dual-Update 스케줄) 개선 검토 대상으로 참고 가치 있음.

### D. JSON 블록

```json
{
  "id": "arxiv:2603.10192v1",
  "title": "Learning to Decode Quantum LDPC Codes Via Belief Propagation",
  "year": 2026,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "144~882",
  "soft_quant": "soft-4bit+",
  "key_contribution": "순차(sequential) VN 스케줄링 순서를 Q-learning으로 학습해 BP 수렴성/FER을 개선하는 RL-SVNS 디코더를 제안하고, 잔여 신드롬 기반 국소 상태와 2차 이웃만 갱신하는 incremental 구현으로 추론 비용을 절감",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "없음",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "중",
  "caveat": "대상 코드가 quantum(CSS/QLDPC, non-binary Pauli 4元) 특화이고 degeneracy 등 quantum 고유 문제가 핵심 동기라 부호설계 자체는 이식 불가; 스케줄링/incremental update 아이디어만 분리 이식 필요",
  "todo_check": "Q-table 크기가 2^Amax(VN degree 기반) 스케일이라 NAND QC-LDPC의 VN degree(17)·col-block(129) 규모에서 상태공간이 실용적인지, 그리고 offline 학습된 정책이 다양한 H-matrix/degree 분포에 일반화되는지 확인 필요"
}
```
