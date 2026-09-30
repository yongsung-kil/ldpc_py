### arxiv:2605.14170v1 - Multiple-Bases Belief Propagation List Decoding for Quantum LDPC Codes (2026, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 144~882 |
| 연판정 | soft-4bit+ |
| 핵심기여 | Tanner graph의 cycle-free maximal subtree 분해로 구조화된 redundant parity-check(augmented H) 여러 개를 만들고 병렬 BP + frequency-weighted list decision(fDM)으로 trapping-set 영향을 완화 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | QLDPC CSS 코드(stabilizer, binary symmetric channel, X-error 전용) 대상 실험으로 원조 classical MBBP[14][15]도 high-density cyclic code 대상이라 NAND용 저밀도 QC-LDPC에서 subtree redundancy 이득이 재현될지 불확실 |
| 추가확인 | Tanner graph 부분트리 기반 augmented parity-check(H(t)=[H;Ht]) 구성을 Prime ECC의 base QC-LDPC(z=32, girth 6+)에 적용 시 추가 행으로 인한 하드웨어/파이프라인 오버헤드가 감수할 만한 수준인지 |

> 총평: 여러 개의 구조화된(트리 기반) redundant parity-check 표현을 병렬 BP로 동시에 돌리고 다수결/해밍weight 기반으로 최종 후보를 뽑는 리스트 디코딩 기법으로, 초선형 후처리(OSD) 없이 BP-급 latency를 유지하면서 오류율을 개선하는 아이디어는 개념적으로 이식 가능하나 QLDPC 특화 실험이라 binary NAND LDPC 재현성은 미검증.

### B. 알고리즘 요약

1. 대상: `[[n,k,d]]` QLDPC CSS 코드(bivariate bicycle `[[144,12,12]]`, `[[288,12,18]]`, B1 `[[882,24]]`), binary symmetric channel에서 X-type 오류만 고려.
2. 풀려는 문제: 표준 BP는 QLDPC의 degeneracy·short cycle·trapping set으로 성능 저하되고, BP-OSD(`O(n^3)`)나 BPGD(`O(n^2)`) 같은 후처리 기반 개선책은 초선형 복잡도·큰 반복 오버헤드를 요구.
3. 핵심 가정: Tanner graph의 cycle-free 부분구조(subtree) 위에서는 BP가 정확(exact)하다는 성질을 이용, 서로 다른 subtree 분해가 서로 다른 수렴 경로를 유도한다고 가정.
4. 핵심 기법: 검사노드 순열 `π`마다 Tanner graph를 cycle-free maximal subtree 집합 `T={t1,...,t|T|}`로 분할(Algorithm 2, BFS로 사이클 생기지 않는 한 확장), 각 subtree `t`의 서브행렬 `Ht`로 증강행렬 `H(t)=[H; Ht]`(식 4) 구성.
5. 핵심 식: subtree 크기 상한 `|t| ≤ (|Vv|-1)/(w-1)` (Lemma 1), weight-6 GB코드에서 `|t| ≤ 0.4|Vc|`로 증강 행 수가 상수배 이내로 제한됨을 보장 → 복잡도/latency가 표준 BP와 같은 오더(`O(Kmax|Vv|)`) 유지.
6. 확장(list decision): 각 `H(t)`에서 병렬 BP(정규화 min-sum, `α=0.875`) 실행 후 수렴한 추정치들을 후보 리스트 `L`로 모아 Frequency-Weighted Scoring `fDM(L)=argmax |{e'=e}|/(w_H(e)+1)` 규칙으로 최종 오류 벡터 선택.
7. 구현 디테일: 무작위 행 중복(APC[16][17])이 아닌 결정론적 subtree 기반 구성이 핵심 차별점이며, 표 II에서 subtree 기반이 동일 조건 random 대비 LER 2.5~9.4% 낮음을 확인.
8. 최적화 절차: 별도 학습 없음. 순열 `π`을 바꿔가며 여러 subtree 분할(=여러 BP 인스턴스)을 생성하는 조합적 구성.
9. 결과: `[[288,12,18]]` 코드에서 BP-OSD 대비 LER 최대 49% 감소, BPGD 대비 최대 36% 감소; `[[882,24]]` B1 코드에서 BP-OSD 대비 91%+ 감소(`p=0.04`)이며 평균 반복수는 BPGD(21.7) 대비 MBBP-LD(14.4)로 더 적음(vs BP-OSD 43.03, MBBP-LD 81.31 at p=0.08, 같은 오더 유지).
10. 한계: HW 미설계·시뮬레이션뿐이며, QLDPC stabilizer 코드·binary symmetric channel(X-error 단독) 가정에 한정, subtree 분해·리스트 크기가 늘수록 병렬 BP 인스턴스 수와 하드웨어 자원이 비례 증가.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Subtree 기반 augmented parity-check(H(t)=[H;Ht]) 구성 | `ecc_top.cpp` `Load_PCM()` | 기존 H-matrix에 추가 redundant 행을 삽입하는 구조 변경이라 QC-LDPC 고정 PCM(`PCM_b`) 재검증 부담 큼 |
| 병렬 다중 BP 인스턴스 + list decision(fDM) | `decoder.cpp` `LDPC_Decoder()` | 여러 디코더 인스턴스를 병렬 실행하고 결과를 다수결/해밍weight로 선택하는 구조는 Prime ECC의 단일 디코더 파이프라인과 다른 아키텍처(HW 자원 다중화 필요) |
| 정규화 min-sum(normalized MSA, α=0.875) | `decoder.cpp` `CNU_Update_New_Mag()` | 이미 보유한 min-sum/scaling 기법과 동일 계열, 신규성 없음 |
| Trapping-set 완화(구조화된 redundancy로 다양한 수렴 경로 유도) | `decoder.cpp` `LDPC_Decoder()` 이터레이션 루프 | error-floor 유발 trapping set 대응이라는 목적은 Prime ECC의 관심사(§5)와 일치, subtree 구성 로직은 신규 추가 필요 |

> 적용 가치: **중간** — "cycle-free subtree 기반 redundant parity-check + 병렬 BP + 리스트 선택"이라는 구조는 trapping-set/error-floor 대응이라는 Prime ECC 관심 영역과 맞닿아 있으나, 여러 디코더 인스턴스를 병렬 하드웨어로 두는 구조적 변경과 QC-LDPC 고정 PCM에 subtree 증강 행을 추가하는 재설계 부담이 커서 직접 이식보다는 아이디어 차용 수준.

### D. JSON 블록

```json
{
  "id": "arxiv:2605.14170v1",
  "title": "Multiple-Bases Belief Propagation List Decoding for Quantum LDPC Codes",
  "year": 2026,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "144~882",
  "soft_quant": "soft-4bit+",
  "key_contribution": "Tanner graph의 cycle-free maximal subtree 분해로 구조화된 redundant parity-check(augmented H) 여러 개를 만들고 병렬 BP + frequency-weighted list decision(fDM)으로 trapping-set 영향을 완화",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "중",
  "caveat": "QLDPC CSS 코드(stabilizer, binary symmetric channel, X-error 전용) 대상 실험으로 원조 classical MBBP도 high-density cyclic code 대상이라 NAND용 저밀도 QC-LDPC에서 subtree redundancy 이득이 재현될지 불확실",
  "todo_check": "Tanner graph 부분트리 기반 augmented parity-check(H(t)=[H;Ht]) 구성을 Prime ECC의 base QC-LDPC(z=32, girth 6+)에 적용 시 추가 행으로 인한 하드웨어/파이프라인 오버헤드가 감수할 만한 수준인지"
}
```
