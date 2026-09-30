### arxiv:cond-mat/0508586v1 - Survey propagation at finite temperature: application to a Sourlas code as a toy model (2005, arXiv cond-mat.dis-nn)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 999~4998 |
| 연판정 | hard-1bit |
| 핵심기여 | 유한온도 survey propagation(1RSB cavity)으로 BP 실패 구간에서 retrieval state 복원, 동적천이 노이즈를 상향 |
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
| 한계,주의 | 비-LDPC Sourlas(3-spin) toy model·BSC, population dynamics(M=1024) 연산비 과대, proof-of-principle |
| 추가확인 | 실제 LDPC 코드로의 적용성(저자도 미래과제로 명시), HW 실현 가능성 |

> 총평: BP가 수렴 실패하는 임계노이즈 부근에서 1RSB survey propagation이 복호 성능을 회복함을 보인 통계역학 원리검증 — 비-LDPC·연산비 과대로 NAND ECC 이식가치 낮음.

### B. 알고리즘 요약

1. 대상: 유한연결(k=4) 3-spin Sourlas code(N=999, 4998), BSC 채널, 온도 β=5(Nishimori temperature 아래)에서 finite-temperature 복호.
2. 문제: 채널노이즈를 과소추정하면 Nishimori 온도 아래에서 replica symmetry breaking(RSB)이 발생, BP가 수렴 실패하거나 나쁜 marginal을 줌.
3. 모델: Ising 3-spin Hamiltonian `H=ΣJ_ν σσσ + Σθ_i σ_i`, biased Sourlas code(bias θ=1.5, c(0)=0.8), Boltzmann measure 기반 marginal `p(σ_i)`로 비트추론.
4. 핵심기법: 1-step RSB cavity method의 유한온도판을 단일 그래프 instance에 적용 — 링크마다 cavity field '분포' W(h)를 population dynamics로 반복, `e^{-mβΔF}` 재가중.
5. 핵심식: RSB 파라미터 m에 대한 일반화 자유에너지 `F(m)`을 `∂F(m)/∂m=0`으로 극대화해 평형상태(complexity=0) 선택.
6. 확장: cavity field 분포로 belief field 분포 `Ŵ(H)`를 구성, marginal `p(σ0)=½[1+σ0∫dH Ŵ(H)tanh(βH)]`.
7. 구현: N개 링크에 M=1024 field sample, 50 update(transient) + 50 update(관측), m=0~0.2 스윕 — 연산비 매우 큼.
8. 최적화: 자유에너지가 m 증가에 따라 상승하다 ferromagnetic 값으로 급락하는 지점 직후 최소 m을 최적으로 선택(BER 동시 급락).
9. 결과: pch=0.07/0.075에서 20/3개 instance 모두 retrieval state 복원(damped TABP·double-loop이 실패하는 instance 포함), 동적천이가 BP 대비 상향됨을 확인.
10. 한계: 비-LDPC Sourlas toy model, 연산비 과대, 저자가 "실용 알고리즘 아닌 원리검증"이라 명시, 실제 LDPC는 미검증.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| finite-T survey propagation 복호 | 대응 없음 | decoder.cpp `LDPC_Decoder()`는 min-sum HW 복호, 1RSB population dynamics와 계열 무관 |
| BSC 채널모델 | channel.cpp `Set_R_Offset()` | RBER/fixed-error는 BSC 유사하나 논문은 부호가 Sourlas라 직접 대응 안 됨 |
| Sourlas 3-spin 부호구조 | 대응 없음 | ecc_top.cpp `Load_PCM()`는 binary QC-LDPC 전용 |

적용 가치: **낮음** — 비-LDPC Sourlas code에 대한 연산비 과대한 통계역학 원리검증 복호기라 NAND binary QC-LDPC min-sum 엔진에 이식할 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:cond-mat/0508586v1",
  "title": "Survey propagation at finite temperature: application to a Sourlas code as a toy model",
  "year": 2005,
  "venue": "arXiv cond-mat.dis-nn",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "999~4998",
  "soft_quant": "hard-1bit",
  "key_contribution": "유한온도 survey propagation(1RSB cavity)으로 BP 실패 구간에서 retrieval state 복원, 동적천이 노이즈 상향",
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
  "caveat": "비-LDPC Sourlas(3-spin) toy model·BSC, population dynamics(M=1024) 연산비 과대, proof-of-principle",
  "todo_check": "실제 LDPC 코드로의 적용성(저자도 미래과제로 명시), HW 실현 가능성"
}
```
