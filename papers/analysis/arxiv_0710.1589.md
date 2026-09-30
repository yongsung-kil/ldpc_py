### arxiv:0710.1589v1 - Fast Reliability-based Algorithm of Finding Minimum-weight Codewords for LDPC Codes (2007, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 기타 |
| 부호rate | 0.5~0.5 |
| 부호length | 96~1008 |
| 연판정 | soft-4bit+ |
| 핵심기여 | serial BP-OSD 기반 신뢰도 재처리로 LDPC 코드의 최소 가중치 코드워드(dm)를 실험적으로 탐색하는 오프라인 분석 알고리즘 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 실제 디코더/부호설계 개선이 아니라 offline 코드 분석(최소거리 추정) 도구, 실시간 디코딩 파이프라인과 무관 |
| 추가확인 | 코드 설계 단계에서 error-floor 예측(union bound 추정)용으로 활용 가치가 있는지 여부(Prime ECC H-matrix 설계/검증 단계 참고용) |

> 총평: LDPC 코드의 최소 가중치 코드워드를 실험적으로 찾는 오프라인 분석 기법으로, 디코더/부호 설계 자체를 개선하는 논문이 아니라 코드 평가 도구이므로 이식 대상이 아님.

### B. 알고리즘 요약

1. 시스템: binary `(N,K)` LDPC 코드, BPSK 변조 후 AWGN 채널(`σ` 표준편차) 전송, all-zero 코드워드 송신 가정, 목적은 최소거리 `dm`에 해당하는 최소 가중치 코드워드 탐색.
2. 문제: 선형코드의 최소거리 `dm` 계산은 NP-hard이며, union bound 추정에 필요한 최소 가중치 코드워드를 다항시간에 찾을 기존 기법이 부족.
3. 가정: 신뢰도가 낮은 두 오류패턴의 모듈로-2 합이 서포트 크기가 작을수록 최소 가중치 코드워드일 확률이 높다는 conjecture(경험적 가정).
4. 핵심 기법: standard BP `Im`회 반복 후 OSD(ordered statistic decoding) 재처리를 결합한 serial BP-OSD. 신뢰도 `ri = Σ_j α^(Im-j) l_i^j` (본 논문은 `α=1`)로 비트별 신뢰도를 정의, 신뢰도 오름차순 정렬로 최소신뢰기저(LRB)를 구성.
5. 핵심 식: `H2 e2 = [H21 H22][e21 e22]' = s` → 시스템 형태로 변환해 `e12 = H21⁻¹H22 e22 + H21⁻¹ s`로 오류패턴 재구성(order-p OSD, 정보집합 내 최대 p비트 오류 후보 조합).
6. 확장: 신드롬이 all-zero면 가장 가벼운 비영 오류패턴이 곧 후보 코드워드, 비영 신드롬이면 최경량 오류패턴과 나머지 후보들의 모듈로-2 합으로 코드워드 생성.
7. 부수 트릭: `Im`(최대 반복횟수)과 `σ`를 시뮬레이션으로 튜닝 — `σ`는 표준 BP로는 초기 반복에서 거의 성공 못하되 `Im` 반복 후에는 near-MLD 성능을 보이도록 설정.
8. 학습/최적화 절차: 다수 코드워드(`Lc`개) 전송 반복 → 매 전송마다 order-2 OSD 재처리로 후보 코드워드 갱신 → 최종 생존한 최경량 코드워드를 `dm` 추정치로 채택.
9. 결과: `C3(1008,504)` 코드에서 기존 기법([11], Stern 알고리즘 기반) 대비 훨씬 적은 계산자원으로 `dm=30, 다중도=1` 추정(복잡도 `Lc·O(N³)`, `Lc=10⁴` vs 기존 `r=10⁷`), 처리시간 0.01~140시간(코드 길이에 비례 급증).
10. 한계: 실시간 디코더/부호설계 알고리즘이 아닌 오프라인 코드 분석 도구, order-p=2로 제한되어 긴 코드일수록 tracking 성능 저하, HW 미설계, 순수 시뮬레이션.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| serial BP-OSD 기반 최소 가중치 코드워드 탐색 (offline 분석) | 대응 없음 | 실시간 디코딩/부호설계 모듈이 아닌 코드 평가용 오프라인 도구로 Prime ECC 런타임 모듈에 대응 없음 |
| 비트 신뢰도 정의(`ri`, LLR 누적) | `decoder.cpp` `VN_Cal_HD()` 등 (참고용) | 신뢰도 계산 방식 자체는 LLR 누적과 유사하나 본 논문 목적은 디코딩이 아닌 코드워드 탐색이라 직접 대응 아님 |

> 적용 가치: 낮음 — 디코더나 부호 자체를 개선하는 것이 아니라 코드의 최소거리를 실험적으로 추정하는 오프라인 분석 알고리즘이라 Prime ECC 런타임 이식 대상이 아님.

### D. JSON 블록

```json
{
  "id": "arxiv:0710.1589v1",
  "title": "Fast Reliability-based Algorithm of Finding Minimum-weight Codewords for LDPC Codes",
  "year": 2007,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "기타",
  "code_rate": 0.5,
  "code_length": "96~1008",
  "soft_quant": "soft-4bit+",
  "key_contribution": "serial BP-OSD 기반 신뢰도 재처리로 LDPC 코드의 최소 가중치 코드워드(dm)를 실험적으로 탐색하는 오프라인 분석 알고리즘",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "실제 디코더/부호설계 개선이 아니라 offline 코드 분석(최소거리 추정) 도구, 실시간 디코딩 파이프라인과 무관",
  "todo_check": "코드 설계 단계에서 error-floor 예측(union bound 추정)용으로 활용 가치가 있는지 여부(Prime ECC H-matrix 설계/검증 단계 참고용)"
}
```
