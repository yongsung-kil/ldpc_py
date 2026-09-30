### arxiv:1202.1348v2 - Selecting Two-Bit Bit Flipping Algorithms for Collective Error Correction (2012, arXiv (ISIT-style))

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.75 |
| 부호length | 732 |
| 연판정 | hard-1bit |
| 핵심기여 | trapping set profile 기반 재귀적 열거로, 서로 다른 에러패턴을 교정하는 Two-Bit Bit Flipping(TBF) 알고리즘 집합을 선택해 병렬 구동하는 절차 제시 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | hard-decision bit-flipping 계열이라 soft-info 기반 min-sum 디코더와 결합 구조가 이질적이며, 다중 알고리즘 병렬 실행 시 게이트 비용이 알고리즘 수에 비례해 증가 |
| 추가확인 | 저자들의 후속 저널판(TBFA1/TBFA2 상세)과 실제 게이트카운트 수치 확인 필요 |

> 총평: hard-decision 2-bit bit-flipping 알고리즘을 trapping-set 다양성 기준으로 다중 선택해 error-floor를 낮추는 이론적 절차로, NAND LDPC 디코더 자체보다는 저복잡도 후처리/보조 디코더 설계에 참고할 만한 간접 이식 소재.

### B. 알고리즘 요약 (10줄 내외)

1. (dv, dc)-regular LDPC를 BSC 상에서 hard-decision Two-Bit Bit Flipping(TBF) 알고리즘 `F = (f, l_m^F, Δv, Δc)`로 복호하는 문제를 다룸.
2. TBF는 기존 serial/parallel bit-flipping보다 variable node에 1비트, check node에 1비트를 추가해 상태 메모리를 부여, 저복잡도를 유지하면서 error floor를 낮추려 함.
3. variable node 상태는 `Av={0s,0w,1w,1s}`(strong/weak zero/one), check node 상태는 `Ac={0p,0n,1p,1n}`(이전/새로 satisfied/unsatisfied)로 정의.
4. 핵심 문제는 TBF 알고리즘이 다수(예: dv=3일 때 최대 2^81) 존재하여 좋은 알고리즘 및 알고리즘 조합을 고르는 절차가 없다는 점.
5. 핵심 기여는 "trapping set"을 TBF 알고리즘 관점에서 재정의하고, 초기 오류 variable node 집합 `I`를 확장해가며 재귀적으로 trapping set profile `E_I^r(F)`를 구성하는 절차(Section IV-B) 제시.
6. 선택 기준(Proposition 3): trapping set profile 내 최소 variable node 수 `n_min^{I,F}`가 클수록 임의 Tanner 그래프가 그 trapping set을 포함할 확률이 낮아지므로, `n_min^{I,F}`가 큰 알고리즘을 선호.
7. 다중 알고리즘 선택(Section V-C)은 개별적으로 우수하면서 trapping set profile이 서로 다른(complementary) 알고리즘들을 병렬 배치해 개별 알고리즘이 실패하는 에러패턴을 서로 보완.
8. 별도 학습/최적화 절차는 없고, 제약조건(f의 대칭성/기약성)으로 탐색 공간을 줄인 뒤 trapping set profile을 전수 열거해 완전탐색으로 알고리즘 조합을 선정.
9. 결과: dv=3, girth-8 코드에서 21,962,496개 알고리즘 중 360,162개가 weight-3 오류를 모두 교정, 여기서 35개를 선택해 병렬 구동 시 (155,64) Tanner 코드와 (732, R=0.75) QC 코드 C732에서 error-floor 기울기가 SPA(최대 100 iteration)와 근접하거나 상회.
10. 한계: 시뮬레이션(FER 곡선)만 제시, HW 미설계(게이트카운트는 6비트 가산기/비교기와의 정성적 비교뿐), hard-decision 전용이라 soft-read 활용 불가, 코드 girth/구조 의존적 가정.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| TBF 알고리즘 (hard 2-bit bit-flipping) | `decoder.cpp` `LDPC_Decoder()`, `VN_Cal_HD()` | Prime ECC는 min-sum soft 디코더가 주력이나 HD(hard-decision) 모드 존재, bit-flipping 계열은 별도 알고리즘이라 직접 대응 약함 |
| trapping set profile 기반 알고리즘 선택/조합 | 대응 없음 | error-floor 대책이지만 Prime ECC는 min-sum + partial-CRC 조기종료 구조로 다중 알고리즘 병렬 선택 개념이 없음 |
| 병렬 다중 알고리즘 디코더 구조 | 대응 없음 | 여러 개의 독립 알고리즘을 동시에 돌리는 구조는 Prime ECC의 단일 파이프라인(GT/HCU) 구조와 상이 |

적용 가치: **낮음** — hard-decision bit-flipping 계열 이론 연구로 Prime ECC의 soft min-sum 기반 QC-LDPC 구조와 이질적이며, 코드 대응 모듈이 거의 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1202.1348v2",
  "title": "Selecting Two-Bit Bit Flipping Algorithms for Collective Error Correction",
  "year": 2012,
  "venue": "arXiv (ISIT-style)",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": 0.75,
  "code_length": 732,
  "soft_quant": "hard-1bit",
  "key_contribution": "trapping set profile 기반 재귀적 열거로 서로 다른 에러패턴을 교정하는 TBF 알고리즘 집합을 선택해 병렬 구동하는 절차 제시",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "hard-decision bit-flipping 계열이라 soft-info 기반 min-sum 디코더와 결합 구조가 이질적이며, 다중 알고리즘 병렬 실행 시 게이트 비용이 알고리즘 수에 비례해 증가",
  "todo_check": "저자들의 후속 저널판(TBFA1/TBFA2 상세)과 실제 게이트카운트 수치 확인 필요"
}
```
