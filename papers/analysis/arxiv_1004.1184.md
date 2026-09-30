### arxiv:1004.1184v1 - Circulant Arrays on Cyclic Subgroups of Finite Fields: Rank Analysis and Construction of Quasi-Cyclic LDPC Codes (2010, arXiv/cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.653~0.9571 |
| 부호length | 225~64386 |
| 연판정 | 무관 |
| 핵심기여 | 유한체 순환부분군 기반 RC-제약 QC-LDPC 부호족 구성 + parity-check 행렬 rank 조합식 유도 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | O |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | AWGN/SPA 시뮬만, HW 미설계, 부호 길이/rate가 GF(q) 인수분해에 종속되어 자유도 제한 |
| 추가확인 | 우리 고rate(0.9급) QC-LDPC와 length/z=32 정합 여부, min-sum(SPA 아님)에서의 수렴속도 재확인 |

> 총평: 순환부분군 기반 대수적 QC-LDPC 구성법 - 고rate(0.87~0.96) 대칭 부호와 빠른 수렴이 NAND ECC와 결이 맞으나 우리 고정 부호 재설계·검증 부담으로 이식성 중.

### B. 알고리즘 요약

1. 대상: 유한체 GF(q) 순환부분군 기반 binary QC-LDPC 부호족 구성(girth≥6), 예제 rate 0.653/0.8752/0.9183/0.9571 등 고rate 다수.
2. 문제: 랜덤/PEG 대비 구조적(대수적) QC-LDPC로 wire routing 단순·부분병렬 복호가 가능한 고성능 부호를 계통적으로 얻고자 함.
3. 모델: RC-constraint(두 행/열이 1을 공유하는 위치 ≤1) → girth≥6 보장, (γ,ρ)-정규시 `d_min ≥ γ+1`.
4. 핵심기법: `q-1=cn`(c,n 서로소), `β=α^c`,`δ=α^n`로 두 순환부분군 G1,G2 정의; `W_i,j` 항목 `δ^{j-i}β^k - β^l`로 RD-constrained base matrix W 구성(식3,4).
5. 핵심식: RD-constraint(임의 두 행이 최소 n-1 위치서 상이)를 만족하면 `(q-1)`-fold CPM array dispersion H가 RC-constraint 만족 → 유효 QC-LDPC.
6. 확장: H의 `γ×ρ` 부분배열 H(γ,ρ)로 rate≥(ρ-γ)/ρ 부호족 생성; masking(`M=Z∘H`)으로 비정규·저밀도화하여 최적 차수분포 근사.
7. 구현 디테일: CPM 기반이라 shift-register 인코딩·부분병렬 복호 친화; masking으로 short cycle 감소·girth 증가.
8. 최적화(rank 분석): 특성 2 GF(2^m)에서 `rank(M)=Σ rank(G^∘l)`(정리3), Pascal 삼각형 홀수 개수 `λ_l=2^{w(l)}` 이용해 `rank(H(γ,·))` 조합식 유도(정리4,5) → 실제 부호 dimension/redundancy 계산.
9. 결과: (12096,10587) rate0.8752 BER 1e-8서 Shannon 1dB; (3969,3645) rate0.9183, (16129,15437) rate0.9571 모두 PEG 랜덤부호 상회; full-array 부호는 IBMPDA(정수덧셈+이진논리)로 SPA 대비 0.6dB로 복잡도 대폭 감소, OSMLGD로 31에러 정정.
10. 한계: AWGN/SPA 시뮬만, HW 미설계, 길이·rate가 GF(q) 인수분해에 종속.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 순환부분군 기반 QC-LDPC H-matrix 구성 | `ecc_top.cpp` `Load_PCM()` + H-matrix | 고rate binary QC-LDPC 부호 재설계 소스로 활용 가능(부호 교체 부담) |
| CPM 배열/circulant 구조 | `ecc_data.h` `PCM_b` (base+shift) | 우리 base+circulant shift 표현과 동형 - 구조적 호환 |
| SPA/iterative message passing 복호 | `decoder.cpp` `LDPC_Decoder()`, `C2V_Cal()` | 우리는 min-sum 근사(SPA 아님) - 수렴속도 이점 재검증 필요 |
| 부분병렬/wire routing 단순화 | 디코더 HW 모델 (z=32, HCU, GT) | QC 구조의 라우팅 이점은 이미 우리도 활용 |
| OSMLGD/IBMPDA 저복잡도 복호 | 대응 없음 | min-sum/majority-logic 계열 별도 - 현 구조와 상이 |

적용 가치: 중간 - 고rate 대수적 QC-LDPC 부호와 rank 기반 dimension 설계가 NAND ECC 부호설계에 참고 가치가 있으나, Prime ECC의 고정 H-matrix를 교체·재검증해야 하고 SPA 기준 결과라 min-sum 이식 검증이 추가로 필요.

### D. JSON 블록

```json
{
  "id": "arxiv:1004.1184v1",
  "title": "Circulant Arrays on Cyclic Subgroups of Finite Fields: Rank Analysis and Construction of Quasi-Cyclic LDPC Codes",
  "year": 2010,
  "venue": "arXiv/cs.IT",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "225~64386",
  "soft_quant": "무관",
  "key_contribution": "유한체 순환부분군 기반 RC-제약 QC-LDPC 부호족 구성 + parity-check 행렬 rank 조합식 유도",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "O",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "AWGN/SPA 시뮬만, HW 미설계, 부호 길이/rate가 GF(q) 인수분해에 종속되어 자유도 제한",
  "todo_check": "우리 고rate(0.9급) QC-LDPC와 length/z=32 정합 여부, min-sum(SPA 아님)에서의 수렴속도 재확인"
}
```
