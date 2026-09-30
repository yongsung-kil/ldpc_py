### arxiv:2511.02951v1 - List Decoding and New Bicycle Code Constructions for Quantum LDPC Codes (2025, arXiv/cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.044~0.137 |
| 부호length | 124~560 |
| 연판정 | 무관 |
| 핵심기여 | Tanner-subtree 유래 중복 parity-check 다중 basis로 병렬 BP 리스트 디코딩(MBBP-LD)+빈도-가중 결정규칙으로 trapping set 완화, 선형복잡도 유지하며 BP-OSD 대비 LER 최대 40% 감소 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | 부분 |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | 양자 CSS(BB/UB) 부호·syndrome 디코딩 전용, BSC/depolarizing 채널 파이썬 시뮬뿐(HW 없음). 다중 BP 인스턴스 병렬화라 단일 z=32 pipeline HW에 그대로 이식 부적합 |
| 추가확인 | subtree 기반 중복 basis + FWS 결정규칙 아이디어가 NAND binary QC-LDPC의 error-floor(trapping set) 완화에 단독 이식 가능한지, 다중 basis 병렬의 HW 비용 |

> 총평: trapping set 완화용 다중 basis BP 리스트 디코딩은 개념적으로 흥미로우나, 양자 CSS 부호 대상·다중 BP 병렬·HW 미설계라 NAND binary QC-LDPC 이식성은 낮음(post-processing 컨셉만 참고).

### B. 알고리즘 요약

1. 대상: QLDPC CSS 부호(대표 bivariate bicycle `[[144,12,12]]`, `[[288,12,18]]`), syndrome 기반 디코딩, BSC 독립 X-error 및 depolarizing 채널.
2. 문제: 표준 BP-OSD는 OSD 단계가 최악 `O(n^3)`로 n 증가 시 비실용적, 반면 순수 BP는 QLDPC 특유의 dense 짧은 cycle·small trapping set에 취약.
3. 핵심 알고리즘 MBBP-LD: 동일 부호의 서로 다른 중복 parity-check 표현 `H^(t)=[H; H_t]` 여러 개에 BP를 병렬 실행, 각 표현이 다른 디코딩 궤적을 유도해 trapping set/짧은 cycle 영향을 교란.
4. 중복 basis 생성: Tanner 그래프의 maximal subtree collection(BFS 순회, Algorithm 2)으로 check node를 partition해 well-distributed layering 구성. subtree는 tree라 BP가 exact, ML 디코딩 보존(추가 제약 없음).
5. subtree 크기 bound(Lemma 2): check-regular degree w에 대해 `|t| ≤ (|Vv|-1)/(w-1)`, w=6 GB 부호는 `|t| ≤ 0.4|Vc|`.
6. 결정 규칙 FWS(Frequency-Weighted Scoring): `argmax_e |{e'∈L: e'=e}|/(wH(e)+1)` — 여러 인스턴스가 반복 산출한 후보를 보상하고 고weight error를 페널티, 기존 LMS 대비 성능 향상.
7. UB 부호 구성: GB 부호에서 Frobenius identity로 `b(x)=a(x)^{2^ℓ}`를 두어 a(x)의 Hamming weight(=row weight w) 보존, 탐색공간을 `O(n^w)`→`O(n^{w/2})`로 축소(w=6,8 저weight parity check).
8. 복잡도: 병렬 스케줄 하 `O(n)` 유지, `T_MBBP-LD = O((1+γ)T_BP-Serial)` (w=6에서 `O(1.4·T_BP-Serial)`). min-sum(정규화 β=0.875 또는 serial β=0) 사용.
9. 결과: `[[144,12,12]]`에서 BP-OSD 대비 LER 최대 40% 감소, p∈[0.03,0.10] 전 구간 우위, 병렬 시 선형 디코더 수준 latency(런타임 표 II). UB `[[126,12/14]]` 부호가 coprime BB 대비 소폭 개선.
10. 한계: 파이썬(MacBook M3, ThreadPoolExecutor) 시뮬뿐, HW 미설계, 양자 CSS·syndrome 디코딩 특화, 채널이 BSC/depolarizing.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| BP min-sum(정규화 β) 메시지 갱신 | decoder.cpp `LDPC_Decoder()`, `CNU_Update_New_Mag()` | 동일 min-sum 계열이나 우리도 이미 보유(중복), 여기선 tanh/min-sum 혼용·양자 syndrome 맥락 |
| 중복 parity-check basis(subtree) 리스트 디코딩(post-processing) | 대응 없음 | 우리 조기종료는 CRC 기반, 다중 basis 병렬 BP post-processing 개념은 코드베이스에 상응 모듈 없음 |
| trapping set/error-floor 완화 | corner.cpp (수렴실패 추적, 개념적 인접) | 우리는 수렴실패 추적만, 다중 basis로 error-floor 개선하는 후처리 대응 없음 |
| UB/GB 부호(circulant) 구성 | ecc_top.cpp `Load_PCM()` | 우리는 고정 binary QC-LDPC(circulant shift), 양자 CSS bicycle 부호구성은 직접 대응 없음 |

적용 가치: **낮음** — 양자 CSS(BB/UB) 부호의 syndrome 디코더로 부호·채널이 NAND binary QC-LDPC와 상이하고 HW 미설계·다중 BP 병렬 구조라 그대로 이식 불가. 다만 "중복 parity-check basis + 빈도가중 결정규칙으로 trapping set 완화"라는 후처리 컨셉은 우리 error-floor 대책 아이디어로만 참고 여지 있음.

### D. JSON 블록

```json
{
  "id": "arxiv:2511.02951v1",
  "title": "List Decoding and New Bicycle Code Constructions for Quantum LDPC Codes",
  "year": 2025,
  "venue": "arXiv/cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "124~560",
  "soft_quant": "무관",
  "key_contribution": "Tanner-subtree 유래 중복 parity-check 다중 basis 병렬 BP 리스트 디코딩(MBBP-LD)+빈도-가중 결정규칙으로 trapping set 완화, 선형복잡도 유지하며 BP-OSD 대비 LER 최대 40% 감소",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "부분",
  "latency": "개선",
  "recommend": "하",
  "caveat": "양자 CSS(BB/UB) 부호·syndrome 디코딩 전용, BSC/depolarizing 파이썬 시뮬뿐(HW 없음). 다중 BP 인스턴스 병렬화라 단일 z=32 pipeline HW에 그대로 이식 부적합",
  "todo_check": "subtree 기반 중복 basis + FWS 결정규칙의 NAND binary QC-LDPC error-floor(trapping set) 완화 단독 이식 가능성, 다중 basis 병렬의 HW 비용"
}
```
