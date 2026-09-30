### arxiv:2605.06547v2 - Affine Subcode Ensemble Decoding for Degeneracy-Aware Quantum Error Correction (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호length | 46~128 |
| 부호rate | 미상 |
| 연판정 | 무관 |
| 핵심기여 | stabilizer code의 degeneracy set을 분할하는 선형독립 행("splitter")을 check matrix에 부가해 앙상블 경로마다 다른 부분 degeneracy set을 병렬 탐색하는 aSCED(affine subcode ensemble decoding) 기법 제안 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | quantum stabilizer code(F4 기반 BP4, degeneracy set) 전제라 binary classical LDPC의 syndrome decoding 문제와 근본 구조가 다름; HW 미설계, Imax 최대 200회 등 real-time 제약 미고려 |
| 추가확인 | 기반 기법인 classical aSCED[32](Mandelbaum et al., 2604.06889)가 순수 binary linear block code용으로 개발되었는지, 그 원 논문이 NAND QC-LDPC에 더 직접 이식 가능한지 확인 필요 |

> 총평: quantum stabilizer code의 degeneracy 문제에 특화된 앙상블 디코딩 기법으로, 기반 아이디어(앙상블+overcomplete check matrix)는 고전 코딩이론에서 유래했으나 본 논문 자체는 quantum 설정(BP4, degeneracy set) 전용이라 NAND binary LDPC 이식성은 낮음.

### B. 알고리즘 요약

1. 대상은 stabilizer 기반 quantum LDPC 코드(toric code, generalized bicycle code)이며 depolarizing 채널에서 X/Y/Z Pauli 오류를 다룸.
2. 문제는 stabilizer code의 degeneracy(같은 syndrome에 대응하는 여러 오류가 논리적으로 동등)가 BP 디코딩의 수렴(oscillation)을 방해하는 현상.
3. 핵심 가정: 오류 `e`를 `E⊕S⊕L` 직합 분해로 detectable(`ε`)/trivial undetectable(`σ`)/logical(`λ`) 성분으로 분리하고, coset `D_{λ,ε} = λ+ε+S`로 정의되는 degeneracy set 개념 도입.
4. 핵심 기법: check matrix `H`에 선형독립인 추가 행("splitter") `Δ`개를 부가하면 각 degeneracy set이 `2^Δ`개의 균등 크기 부분집합으로 분할됨(Theorem 1).
5. `aSCED`(affine subcode ensemble decoding)는 `K=L·2^Δ`개의 병렬 BP4(quaternary BP) 경로를 운용, 각 경로가 서로 다른 확장 syndrome `z_δ=(z, g_δ)`로 부분 degeneracy set만 탐색해 최종적으로 최소 weight 추정치를 선택.
6. 확장으로 overcomplete check matrix(`H^(ℓ)_oc = M H^(ℓ)`)를 각 경로에 적용해(OBP4) 짧은 4-cycle을 줄이고 수렴성을 더 개선.
7. 부수 트릭: splitter 행은 낮은 weight(4~6)로 생성해 Tanner graph에 추가 4-cycle을 만들지 않도록 [25, Algorithm 1] 사용.
8. 별도 학습/최적화 절차 없음 (Monte-Carlo 시뮬레이션 기반 파라미터 튜닝: `Δ`, `L` 조합 비교).
9. 결과: `[[46,2,9]]` GB 코드에서 OBP4-aSCED64가 Type I(비수렴) 실패를 전 구간에서 0으로 제거; `[[128,2,8]]` toric code에서 K=64,256일 때 MWPM/correlated MWPM보다 낮은 LER 달성.
10. 한계: 순수 시뮬레이션(HW 미설계), 최대 반복수 최대 200(OBP4-aSCED 조합에서), depolarizing 채널만 가정하고 회로 수준 fault-tolerant 시나리오는 향후 과제.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| BP4(quaternary BP) 디코딩 알고리즘 | `decoder.cpp` `LDPC_Decoder()` | 대응 없음 - F4 기반 stabilizer syndrome decoding이며 binary min-sum과 메시지 구조가 다름 |
| 앙상블 디코딩(K개 병렬 경로 + 최소weight 선택) | 대응 없음 | Prime ECC는 단일 디코더 구조; 앙상블 개념 자체는 일반 BP에 적용 가능하나 코드 내 대응 모듈 없음 |
| overcomplete check matrix (중복 parity 추가) | `ecc_top.cpp` `Load_PCM()` | 개념적으로 redundant row 추가는 H-matrix 로드/구성과 연관되나, degeneracy set 분할이라는 quantum 특유 목적과는 무관 |
| splitter 행 생성(4-cycle 회피) | 대응 없음 | Tanner graph short-cycle 제거라는 목표는 일반적이나 구현은 quantum 특유 논문[25] 알고리즘 기반 |

적용 가치: 낮음 - degeneracy set, stabilizer syndrome decoding은 quantum 특유 개념으로 NAND binary QC-LDPC 부호/디코더에 직접 대응되지 않음. 다만 "앙상블+overcomplete matrix로 수렴성 개선"이라는 상위 아이디어 자체는 참고용 [32] classical aSCED 원 논문을 별도로 검토할 가치는 있음.

### D. JSON 블록

```json
{
  "id": "arxiv:2605.06547v2",
  "title": "Affine Subcode Ensemble Decoding for Degeneracy-Aware Quantum Error Correction",
  "year": 2026,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "46~128",
  "soft_quant": "무관",
  "key_contribution": "stabilizer code의 degeneracy set을 분할하는 선형독립 행(splitter)을 check matrix에 부가해 앙상블 경로마다 다른 부분 degeneracy set을 병렬 탐색하는 aSCED 기법 제안",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "quantum stabilizer code(F4 기반 BP4, degeneracy set) 전제라 binary classical LDPC의 syndrome decoding 문제와 근본 구조가 다름; HW 미설계, Imax 최대 200회 등 real-time 제약 미고려",
  "todo_check": "기반 기법인 classical aSCED[32](Mandelbaum et al., 2604.06889)가 순수 binary linear block code용으로 개발되었는지, 그 원 논문이 NAND QC-LDPC에 더 직접 이식 가능한지 확인 필요"
}
```
