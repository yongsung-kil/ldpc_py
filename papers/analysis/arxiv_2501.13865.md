### arxiv:2501.13865v1 - Threshold Selection for Iterative Decoding of (v, w)-regular Binary Codes (extended version) (2025, arXiv/ISIT 2025)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.5 |
| 부호length | 200~13323 |
| 연판정 | hard-1bit |
| 핵심기여 | 2-iteration bit-flipping 디코더의 syndrome weight 분포·DFR 폐형 모델로 iteration별 최적 threshold 도출 |
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
| 한계,주의 | 암호(BIKE/LEDAcrypt)용 (v,w)-regular LDPC/MDPC 대상, 2-iteration hard bit-flipping 한정, NAND soft-LDPC와 채널·목표 상이 |
| 추가확인 | th(1)(y)·th(2)(z0,z1) 룩업 방식이 min-sum 기반 우리 디코더에 개념 이식 가능한지, 고rate에서의 유효성 |

> 총평: 암호용 bit-flipping 디코더 DFR 폐형 모델·threshold 최적화 이론 논문으로 NAND용 min-sum QC-LDPC와 결이 달라 직접 이식 가치 낮음.

### B. 알고리즘 요약

1. 대상은 `(v,w)-regular` binary sparse code (LDPC/MDPC), `rate=1-v/w`, 실험은 주로 `k/n=1/2`, `n=200~13323`, `v=7~71`.
2. 문제: 병렬 hard-decision bit-flipping 디코더의 threshold를 어떻게 골라야 DFR(Decoding Failure Rate)을 최소화하는가 (BIKE/LEDAcrypt 암호 보안수준 직결).
3. 모델: `H`의 각 행을 길이 n·weight w의 균일 랜덤 벡터로 가정, 첫 iteration 후 discrepancy 비트를 `(a,b)=(e_i, d_i)` 4개 클래스 `J_{a,b}`로 분할.
4. 핵심 기법 1: 첫 iteration 후 syndrome weight `wt(s(1))`의 분포를 비균질 Markov process로 폐형 유도 (`Z0`=만족→불만족 전이 수, `Z1`=계속 불만족 수, `z0+z1=wt(s(1))`).
5. 핵심 식: `Pr(E(iter)=d)=Σ_y Pr(E(iter)=d|Wt=y)Pr(Wt=y)` — syndrome weight y로 조건화해 discrepancy weight 분포를 계산.
6. 핵심 기법 2: 2번째 iteration DFR `DFR(y,ϵ01,ϵ11,z0,z1)`를 pflip|00/01/10/11로 폐형화, 이를 최소화하는 `th(1)(y)`, `th(2)(y,z0,z1)`를 pointwise argmin으로 결정.
7. 구현 트릭: joint 최적화를 first/second iteration 분리 최적화로 쪼개 복잡도(`r^3 n t`)를 낮춰 노트북에서 암호급 파라미터 계산 가능, threshold는 소형 테이블로 tabulate.
8. 학습/최적화: 별도 학습 없음, DFR 모델에 대한 결정론적 argmin 스위프.
9. 결과: majority threshold 대비 DFR ~10^3배 개선, leftover discrepancy는 BIKE-flip 대비 ~3·10^2배, majority 대비 >5·10^3배 감소; 10^8 decode 회귀 최적 threshold와 성능 일치.
10. 한계: HW 미설계, 2-iteration만 모델링, 순수 시뮬/이론, 채널이 fixed-weight error(암호)로 NAND RBER·soft-read와 무관.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| bit-flipping 디코딩 루프 | decoder.cpp `LDPC_Decoder()` | 개념상 이터레이션 루프에 대응하나 우리는 min-sum(연판정)이라 알고리즘 상이 |
| syndrome-weight 의존 threshold 선택 | 대응 없음 | 우리 디코더는 LLR threshold 테이블(`PARAM_LLR`) 기반이지 upc-threshold 방식 아님 |
| DFR 폐형 모델 / error-floor 추정 | 대응 없음 | 시뮬레이터엔 해석적 DFR 모델 없음 (corner.cpp는 수렴실패 추적만) |
| iteration별 threshold 테이블 tabulate | decoder.cpp `Get_VNU_Table_Idx()`, `ecc_data.h` `PARAM_LLR` | 개념적 유사(구간별 테이블)이나 대상 물리량이 다름 |

적용 가치: 낮음 — 대상이 암호용 hard-decision bit-flipping (v,w)-regular LDPC/MDPC로, NAND용 soft min-sum QC-LDPC와 디코더 알고리즘·채널이 근본적으로 달라 threshold 폐형 모델을 직접 떼어 쓸 수 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2501.13865v1",
  "title": "Threshold Selection for Iterative Decoding of (v, w)-regular Binary Codes (extended version)",
  "year": 2025,
  "venue": "arXiv/ISIT 2025",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": 0.5,
  "code_length": "200~13323",
  "soft_quant": "hard-1bit",
  "key_contribution": "2-iteration bit-flipping 디코더의 syndrome weight 분포·DFR 폐형 모델로 iteration별 최적 threshold 도출",
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
  "caveat": "암호(BIKE/LEDAcrypt)용 (v,w)-regular LDPC/MDPC 대상, 2-iteration hard bit-flipping 한정, NAND soft-LDPC와 채널·목표 상이",
  "todo_check": "th(1)(y)·th(2)(z0,z1) 룩업 방식이 min-sum 기반 우리 디코더에 개념 이식 가능한지, 고rate에서의 유효성"
}
```
