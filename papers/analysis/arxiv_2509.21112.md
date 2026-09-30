### arxiv:2509.21112v3 - Adapt or Regress: Rate-Memory-Compatible Spatially-Coupled Codes (2026, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | SC-LDPC |
| 부호rate | 0.4167~0.7000 |
| 부호length | 6348~16240 |
| 연판정 | 무관 |
| 핵심기여 | 메모리 증가로 rate/메모리 호환되는 재구성형 이진 SC-LDPC(RMC-SC)를 gradient-descent(단주기 기댓값 최소화)+MCMC 분할/lifting으로 확률적 설계 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | SC-LDPC 대상이며 Prime ECC는 QC-LDPC 고정 - 부호설계 레이어 이식은 프로파일상 난이도 높음; HW 미설계, gate/throughput 미보고 |
| 추가확인 | 단주기 최소화 확률/GD 목적함수 정식화가 Prime ECC의 QC-LDPC PCM 구성(base+circulant)에 재적용 가능한지 - SC 구조 없이도 유효한지 |

> 총평: 데이터 스토리지/Flash를 명시 타깃한 이진 SC-LDPC 부호설계 논문으로 단주기 저감이 waterfall/error-floor 모두 개선하나, Prime ECC의 고정 QC-LDPC와 부호종류가 달라 직접 이식은 어렵다.

### B. 알고리즘 요약

1. 시스템/코드: 이진 protograph 기반 SC-LDPC. base matrix를 `m+1`개 component로 분할→coupling(길이 `L`)→lifting(`z×z` circulant). 실험: `(γ,κ,z,L)=(7,23,23,12)` rate 0.42~0.54 len 6348, `(7,35,29,16)` rate 0.61~0.70 len 16240.
2. 풀려는 문제: 한 시스템에서 채널/rate 변화(무선) 또는 device aging(스토리지) 시 여러 부호가 필요 - 재설계 없이 전환 가능한 rate-compatible 부호를 고성능으로.
3. 핵심 아이디어: rate compatibility를 **메모리 증가**로 달성(RMC-SC) → rate↓·memory↑가 동시에 성능↑(memory-compatible). 이전 stage 분포는 고정(`p`), 새 component 분포(`q`)만 최적화.
4. 핵심 기법 1단: protograph의 cycle-`2ℓ` candidate 기댓값을 `f(X)=Σp_jX^j`, `g(X)=Σq_jX^j` 다항식으로 표현. `E[cycle-2ℓ]=A_2ℓ[(r_f f+r_n g)^ℓ(r_f f(X⁻¹)+r_n g(X⁻¹))^ℓ]_0` (Theorem 1).
5. 핵심 식 의미: cycle이 partitioning 후에도 살아남을 조건 `ΣK(i_k,j_k)−K(i_k,j_{k+1})=0` (식4)을 확률화 - 상수항 계수가 예상 단주기 수.
6. 핵심 기법 2단: KKT/Lagrangian으로 cycle-6·cycle-8 가중합을 최소화하는 국소최적 `q`를 gradient-descent(RMC-GRADE, Alg.1)로 탐색. 결과는 U자형 분포.
7. 부수 트릭: rate 증분을 component 대신 row(또는 column) 추가로 하는 확장(Lemma 2, Remark 1)도 제시.
8. 최적화 절차: 유한길이는 MCMC(MC2, Alg.2)로 (i)분할행렬 K (ii)lifting행렬 T를 순차 국소최적화, cycle-4 전제거→cycle-6→cycle-8 순 제거.
9. 결과: SF-SC 대비 cycle-6 최대 100% 제거, cycle-8 최대 62.75% 감소; AWGN FER 최대 ≈3.73 orders 이득, BSC 최대 ≈4.92 orders; DE threshold 최대 14.55%↑; HW(엣지수) 54.88~55.28% 절감.
10. 한계: HW 미설계(gate/throughput 미보고), sum-product(FFT) 복호로 시뮬만; SC-LDPC 전용이라 QC-LDPC 코드베이스엔 부호종류 불일치.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SC-LDPC 부호구성(분할/coupling/lifting) | ecc_top.cpp `Load_PCM()` | 부호구조 로드 지점이나 Prime ECC는 QC-LDPC 고정 - SC-LDPC로 교체는 재검증 부담 큼(프로파일 §4 "높음") |
| lifting circulant power 설계 | encoder.cpp `Generate_PCM_encoding()` (간접) | QC-LDPC도 circulant shift 사용, 단주기 최소화 lifting 아이디어는 개념적 참고 가능 |
| 단주기 저감 → error-floor/waterfall 개선 | decoder.cpp `LDPC_Decoder()` (간접) | 복호 성능 개선의 원천(부호구조)이나 복호 알고리즘 자체는 변경 없음 |

적용 가치: **낮음** — 이진 스토리지 타깃 부호설계로 방향은 맞으나, Prime ECC의 고정 QC-LDPC와 부호종류(SC-LDPC)가 달라 부호설계 레이어 이식 난이도가 높고, 단주기 최소화 GD/MCMC 프레임워크를 QC-LDPC 구성에 재적용하려면 상당한 재작업이 필요하다.

### D. JSON 블록

```json
{
  "id": "arxiv:2509.21112v3",
  "title": "Adapt or Regress: Rate-Memory-Compatible Spatially-Coupled Codes",
  "year": 2026,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "SC-LDPC",
  "code_rate": "0.4167~0.7000",
  "code_length": "6348~16240",
  "soft_quant": "무관",
  "key_contribution": "메모리 증가로 rate/메모리 호환되는 재구성형 이진 SC-LDPC(RMC-SC)를 gradient-descent(단주기 기댓값 최소화)+MCMC 분할/lifting으로 확률적 설계",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "SC-LDPC 대상이며 Prime ECC는 QC-LDPC 고정 - 부호설계 레이어 이식은 프로파일상 난이도 높음; HW 미설계, gate/throughput 미보고",
  "todo_check": "단주기 최소화 확률/GD 목적함수 정식화가 Prime ECC의 QC-LDPC PCM 구성(base+circulant)에 재적용 가능한지 - SC 구조 없이도 유효한지"
}
```
