### arxiv_cond-mat_0401170v1 - Error-correcting codes on scale-free networks (2004, arXiv cond-mat.stat-mech)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | 변수노드 차수분포를 멱함수 `p(k)=C(k+α)^-γ`(γ≈2)로 두는 scale-free LDPC 부호설계 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | BEC(소거채널) 전용 검증, AWGN/NAND 미검증, 유한장·HW 언급 없음 |
| 추가확인 | γ≈2 멱함수 분포가 NAND용 고rate QC-LDPC 부호에도 이득 있는지(BEC 외 채널) |

> 총평: 고성능 LDPC의 차수분포가 멱함수라는 관찰에서 scale-free 차수분포로 BEC threshold를 Tornado 대비 개선한 부호설계 논문. QC 구조·HW·AWGN 무관해 NAND 이식성 낮음.

### B. 알고리즘 요약

1. 대상: 이분그래프 기반 irregular LDPC, BEC 위에서 BP 복호, 예시 rate `R=0.5`.
2. 문제: capacity-achieving 차수분포 구조에 대한 이해가 부족하고, 대부분 수치최적화에 의존.
3. 관찰: 세계기록급 LDPC(Chung et al., AWGN, γ≈2.14)와 Tornado(BEC, γ≈2.02)의 변수노드 차수분포가 멱함수 `p(k)∼k^-γ`(γ≈2)에 잘 맞음.
4. 핵심기법: scale-free 생성함수를 `p(k)=C(k+α)^-γ`로 두고(식 3), `k≥2`부터 시작(degree-1 제거), 체크노드는 인접 두 정수 차수로 제한(`F(x)=bx^i+(1-b)x^{i+1}`).
5. 최적화 변수: `α`, `γ` 두 파라미터만으로 성능 극대화(direction set method).
6. 평가식: BEC density evolution `x_l = x0·λ(1-ρ(1-x_{l-1}))`(식 4), threshold `δ*`가 `1-R`에 근접할수록 우수.
7. 확장: 저차수(k=2,3)에 가중치 `w2,w3` 추가(식 5)로 멱함수 이탈 허용 → threshold 추가 개선.
8. 비교군: 지수·가우시안 차수분포는 threshold가 각각 0.465 부근으로 수렴, 멱함수보다 열등.
9. 결과: `dmax`≲1000에서 Tornado 대비 δ* 우수(예 dmax=610: SFN 0.49920 vs Tornado 0.49918), 평균차수 `k̄`도 작고 수렴 iteration도 적음(작은 그래프 지름 `d∼ln ln N` 논증).
10. 한계: BEC 전용 검증, AWGN/NAND 실험 없음, 유한장 성능·QC 구조·HW 구현 전무.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 멱함수 변수노드 차수분포 설계 | `ecc_top.cpp` `Load_PCM()` (개념상 H-matrix/부호구조) | 부호설계 레이어이나 QC-LDPC 고정 구조·고rate와 정합 안 됨, 재검증 부담 큼 |
| BEC density evolution threshold | 대응 없음 | Prime ECC는 AWGN/RBER 기반, 소거채널 threshold 미사용 |
| BP(erasure) 복호 iteration | `decoder.cpp` `LDPC_Decoder()` (개념 대응) | 소거채널 BP이라 min-sum HD/2SD/3SD 파이프라인과 직접 접점 없음 |

적용 가치: **낮음** — irregular 차수분포 부호설계라 우리 고정 QC-LDPC(z=32, 고rate) 구조와 어긋나고, 검증도 BEC 한정이라 NAND soft-read/AWGN 환경 이득이 불확실.

### D. JSON 블록

```json
{
  "id": "arxiv:cond-mat/0401170v1",
  "title": "Error-correcting codes on scale-free networks",
  "year": 2004,
  "venue": "arXiv (cond-mat.stat-mech)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "변수노드 차수분포를 멱함수 p(k)=C(k+α)^-γ(γ≈2)로 두는 scale-free LDPC 부호설계",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "BEC(소거채널) 전용 검증, AWGN/NAND 미검증, 유한장·HW 언급 없음",
  "todo_check": "γ≈2 멱함수 분포가 NAND용 고rate QC-LDPC 부호에도 이득 있는지(BEC 외 채널)"
}
```
