### arxiv:2605.10433v1 - Syndrome Adaptive Gain Control for Min-Sum Decoding of Quantum LDPC Codes (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 126 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 불만족 stabilizer 비율(syndrome ratio)을 피드백으로 CN 스케일링 계수를 반복마다 온라인으로 자기보정하는 SAGMS min-sum 변형 제안 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | GF(4) 양자 stabilizer 코드(QLDPC) 전용 설계로, 부호와 신드롬 정의가 binary NAND LDPC와 근본적으로 다름(대상은 CN degree 10~16의 밀집 그래프) |
| 추가확인 | syndrome ratio(불만족 체크 비율) 기반 gain 스케줄링 아이디어를 GF(2) binary min-sum의 offset/normalized 스케일링과 결합해 NAND 디코더에 재구현 가능한지 |

> 총평: 양자 LDPC(QLDPC) min-sum 디코더의 스케일링 계수를 오프라인 최적화 없이 신드롬 비율로 온라인 적응시키는 기법으로, 핵심 아이디어(수렴 거리 기반 gain 스케줄링)는 개념적으로 흥미롭지만 GF(4) stabilizer 코드 특유의 설계라 NAND binary LDPC로의 직접 이식은 재해석·재검증이 필요함.

### B. 알고리즘 요약

1. 대상 코드: `[[n,k]]` QLDPC(generalized bicycle 계열), 검사행렬 `H ∈ GF(4)^(m×n)`, depolarizing 채널에서 Pauli 오류 `{I,X,Y,Z}` 발생.
2. 풀려는 문제: BP4(GF(4) belief propagation)는 `log`, `tanh` 등 초월함수 필요로 HW 비용 크고, 기존 Min-Sum(MS)은 CN 출력 크기를 체계적으로 과대추정하며, 고정 스케일링(SMS)은 코드·노이즈별 오프라인 최적화가 필요.
3. 핵심 가정: CN degree `dc`가 커지고 노이즈 수준이 불확실(mismatch)할수록 고정 스케일 `α`의 성능 열화가 커짐(Proposition 1).
4. 핵심 기법: 매 반복 `ℓ`에서 불만족 stabilizer 비율(syndrome ratio) `γ(ℓ) = ||s̃(ℓ)||_0 / |S|`를 계산해 CN 출력 스케일 `α_eff(ℓ)`를 `αmax - (αmax-αmin)*γ(ℓ)` (불만족 CN엔 `ηunsat` 추가 부스트)로 실시간 조정.
5. 핵심 식(9): BP4와 MS를 일치시키는 최적 스케일 `α* ≈ 1 - ln(dc-1)/L0`가 CN degree `dc`에 대해 단조 감소함을 증명, 즉 고정 `α`는 `dc`가 변하면 갈수록 불일치가 커짐(식 10, 스케일 페널티 `Δα`).
6. 확장: `αmax = α*(L0)`을 수렴점에서의 이론적 상한(gain ceiling)으로 두고, `γ(ℓ)→0`(수렴 근접)일 때 `α_eff→αmax`, `γ(ℓ)→1`(수렴 실패)일 때 `α_eff→αmin`으로 자기보정(Corollary 1).
7. 구현 디테일: `γ(ℓ)`는 이미 조기종료용으로 계산되는 잔여 syndrome의 popcount(이진 adder tree, `O(m)`)로 거의 무비용 계산 가능, 파이프라이닝으로 throughput 영향 미미.
8. 최적화 절차: 오프라인 코드별/노이즈별 파라미터 튜닝 불필요 — `αmin, αmax, ηunsat` 3개 파라미터만 고정하면 여러 CN degree/노이즈에 걸쳐 재사용 가능함을 실험으로 검증.
9. 결과: `[[126,28]]` GB 코드에서 `ε=0.01, ℓmax=8` 기준 SAGMS FER `3.9×10^-5` (SMS `4.6×10^-5`, BP4 `4.0×10^-4`, 약 10배 개선); `ℓmax=4`에서 SAGMS가 BP4 `ℓmax=8`과 동등 성능(반복수 절반); CN당 연산 `C_SAGMS=2dc+3` vs `C_BP4=22dc-13`.
10. 한계: 양자 stabilizer 코드(GF(4), depolarizing 채널) 전용 설계·시뮬레이션(FPGA/ASIC 미검증)이며, 검증된 코드가 `[[126,28]]`, `[[126,20]]` 두 개뿐이고 CN degree가 10~16으로 NAND LDPC보다 훨씬 밀집.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Syndrome ratio 기반 CN 스케일 온라인 적응(SAGMS) | `decoder.cpp` `CNU_Update_New_Mag()` | min-sum CN 스케일링 로직에 불만족 신드롬 비율 피드백을 추가하는 형태로 이식 검토 가능(파라미터 재보정 필요) |
| 반복별 스케일/threshold 테이블 | `ecc_data.h` `PARAM_LLR`, `decoder.cpp` `Get_VNU_Table_Idx()` | 기존 "iteration 구간별 LLR threshold 테이블"과 유사한 목적(적응형 LLR)이나, 본 논문은 syndrome 비율 기반 동적 계산이라 정적 테이블 대비 이식 시 재설계 필요 |
| 조기종료(불만족 syndrome 개수 계산) | `partial_CRC.cpp` `partial_crc_HW_T4()` | 잔여 syndrome popcount 활용 아이디어가 조기종료 로직과 공유 가능한 연산(HW 재사용 여지) |
| GF(4) 양자 stabilizer 신드롬/degeneracy 처리 | 대응 없음 | Prime ECC는 binary LDPC 전용이라 GF(4) Pauli 대칭·degeneracy 개념 자체가 대응되지 않음 |

> 적용 가치: **중간** — 핵심 아이디어인 "신드롬 불만족 비율을 온라인 피드백으로 min-sum 스케일 계수를 조정"은 개념적으로 Prime ECC의 min-sum CN 업데이트에 이식 가능하나, 원 설계가 GF(4) 양자코드/조밀 그래프 특화라 binary NAND QC-LDPC(성긴 그래프, CN degree 작음)에서도 동일 이득이 재현되는지 별도 검증 필요.

### D. JSON 블록

```json
{
  "id": "arxiv:2605.10433v1",
  "title": "Syndrome Adaptive Gain Control for Min-Sum Decoding of Quantum LDPC Codes",
  "year": 2026,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "126",
  "soft_quant": "soft-4bit+",
  "key_contribution": "불만족 stabilizer 비율(syndrome ratio)을 피드백으로 CN 스케일링 계수를 반복마다 온라인으로 자기보정하는 SAGMS min-sum 변형 제안",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "중",
  "caveat": "GF(4) 양자 stabilizer 코드(QLDPC) 전용 설계로, 부호와 신드롬 정의가 binary NAND LDPC와 근본적으로 다름(대상은 CN degree 10~16의 밀집 그래프)",
  "todo_check": "syndrome ratio(불만족 체크 비율) 기반 gain 스케줄링 아이디어를 GF(2) binary min-sum의 offset/normalized 스케일링과 결합해 NAND 디코더에 재구현 가능한지"
}
```
