### arxiv:2503.03936v3 - Construction and Decoding of Quantum Margulis Codes (2026, Quantum)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 240~642 |
| 연판정 | 무관 |
| 핵심기여 | 비Abelian 군(SL(2,Zp)) 기반 2BGA 양자 Margulis 부호로 Tanner 그래프 대칭을 깨 OSD 없이 min-sum만으로 error-floor 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | CSS 양자부호(qubit degeneracy/qTS) 전용이라 고전 binary NAND LDPC에는 개념 부적합, circuit-level 노이즈에선 여전히 OSD 필요 |
| 추가확인 | "그래프 대칭↓ = MP 디코딩 향상" 원리가 고전 LDPC trapping-set 회피 부호설계에 재활용 가능한지 |

> 총평: 양자 LDPC 전용 부호설계/디코딩 논문으로 NAND binary LDPC 직접 이식은 불가하나, 그래프 비대칭으로 MS 수렴을 돕는다는 정성적 통찰만 참고 가치.

### B. 알고리즘 요약

1. 대상은 유한 길이 `[n=240,642]` 양자 CSS LDPC 부호(QLDPC), 채널은 code-capacity(depolarizing ϵ) 및 circuit-level noise.
2. 기존 BB(bivariate bicycle) 양자부호는 error degeneracy로 인해 min-sum이 진동·미수렴, 효과적 정정에 O(n^3) OSD 후처리가 필수인 것이 문제.
3. 핵심 관찰: 부호를 만드는 군 `G`가 Tanner 그래프 automorphism의 부분군이 되어, Abelian군이면 모든 체크노드 이웃이 동형 → 대칭 stabilizer(qTS)에서 MP가 진동.
4. 제안: `G=SL(2,Zp)`(비Abelian) 기반 2BGA(two-block group algebra) 프레임워크로 고전 Margulis 부호를 양자로 확장, `HX=[A B]`, `HZ=[B^T A^T]`.
5. 비Abelian군이면 Theorem 1 조건(생성집합이 정규부분군)이 거의 안 성립 → 그래프 대칭이 깨져 대칭 stabilizer에서도 nMS가 비대칭 메시지로 수렴.
6. girth 제어 알고리즘(Algorithm 1/2): 루트에서 트리를 층별 확장하며 4-cycle·6-cycle을 유발하는 생성원을 교체, girth ≥ 6(n=240) 또는 8(n=642) 보장.
7. 디코더는 flooding(완전병렬) 스케줄 nMS, 정규화 계수 `β=0.875`, 최대 반복 300(n=240)/700(n=642).
8. 검증: 대칭 stabilizer에 반무게 오류 주입 후 추정오류 무게 `Wk`와 Bethe free-entropy 궤적으로 BB는 국소최소 정체, Margulis는 수렴함을 시각화.
9. 결과: code-capacity에서 nMS만으로 logical error rate 약 `10^-8`(n=240,k=2) 달성, BB보다 error floor 우수, 복잡도 O(n^3)→O(n).
10. 한계: circuit-level noise에선 확장 Tanner 그래프의 짧은 사이클·불규칙 차수로 nMS 이점 소멸, 다시 BPOSD 필요. HW 미설계, 시뮬만.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| nMS(정규화 min-sum) 디코더 | decoder.cpp `LDPC_Decoder()`, `C2V_Cal()` | Min-Sum 자체는 이미 보유, 정규화 β 개념만 부분 참고 |
| 2BGA/Margulis H-matrix 구성 | ecc_top.cpp `Load_PCM()` | 양자 CSS 이중블록 구조라 binary QC-LDPC 로더와 개념 불일치, 직접 이식 불가 |
| girth 제어 부호 생성 | 대응 없음 | Prime ECC는 QC-LDPC 고정, 생성원 탐색 구성법 미보유 |
| qTS/대칭 stabilizer 회피 | 대응 없음 | 고전 trapping-set 개선 개념과 유사하나 양자 degeneracy 전용 |

적용 가치: **낮음** — 양자 CSS LDPC 전용 부호이며 HW 미설계·code-capacity 시뮬뿐이라 NAND binary QC-LDPC에 떼어 쓸 요소가 사실상 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2503.03936v3",
  "title": "Construction and Decoding of Quantum Margulis Codes",
  "year": 2026,
  "venue": "Quantum",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "240~642",
  "soft_quant": "무관",
  "key_contribution": "비Abelian 군(SL(2,Zp)) 기반 2BGA 양자 Margulis 부호로 Tanner 그래프 대칭을 깨 OSD 없이 min-sum만으로 error-floor 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "하",
  "caveat": "CSS 양자부호(qubit degeneracy/qTS) 전용이라 고전 binary NAND LDPC에는 개념 부적합, circuit-level 노이즈에선 여전히 OSD 필요",
  "todo_check": "그래프 대칭↓ = MP 디코딩 향상 원리가 고전 LDPC trapping-set 회피 부호설계에 재활용 가능한지"
}
```
