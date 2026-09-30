### arxiv:1904.02703v3 - Degenerate Quantum LDPC Codes With Good Finite Length Performance (2021, Quantum)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 46~7938 |
| 연판정 | 무관 |
| 핵심기여 | BP 실패 시 신뢰도기반 정보집합으로 OSD 후처리(BP-OSD)하여 WER 최대 5자릿수 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | X |
| latency | 악화 |
| 추천도 | 하 |
| 한계,주의 | 양자 CSS/비바이너리 GF(4) BP 대상, O(n^3) OSD 후처리는 NAND HW 예산에 부적합 |
| 추가확인 | OSD-0 신뢰도정렬+가우스소거 아이디어를 고전 binary error-floor 후처리로 축소 이식 가능성만 검토 |

> 총평: 양자 LDPC용 BP-OSD 후처리 논문으로 NAND binary QC-LDPC와 채널·부호·복잡도 모두 상이, 이식성 하.

### B. 알고리즘 요약

1. 대상은 depolarizing 채널의 중간길이 양자 LDPC(QLDPC) CSS/비CSS 부호(`[[n,k,d]]`, n=46~7938), 목표는 short 코드길이에서의 실전 정정성능.
2. 표준 BP 디코더는 QLDPC의 불가피한 4-cycle과 다수 degenerate error로 성능이 최적과 크게 벌어짐 → 후처리로 보강.
3. 채널모델: 각 qubit i.i.d. Pauli 오류 `P(Ei=X)=P(Ei=Y)=P(Ei=Z)=p/3`, syndrome 디코딩(전송 codeword 아닌 syndrome `s`만 관측).
4. 핵심기법: BP가 syndrome을 못 맞추면 BP soft-decision으로 각 위치 신뢰도 `ρi=max(pi,E)` 계산, 가장 신뢰높은 information set `I`를 그리디로 선택.
5. `I` 밖(가장 불신뢰) w비트를 모두 2^w 뒤집어 `He=s` 만족하는 오류벡터 후보 생성, 최소 무게(depolarizing은 symplectic weight `|·|Sp`) 후보 선택.
6. 확장: order-w qOSD = 비바이너리 GF(4) BP 뒤에 OSD를 붙인 버전, CSS+독립 X/Z 오류면 X/Z 성분 분리해 표준 OSD 병렬 적용.
7. 구현 디테일: OSD-0(w=0)만으로도 대부분 충분, 복잡도 `O(n^3)`(일반 `O(n^3+n^2 w)`), 가우스소거 조기중단으로 full elimination 회피.
8. BP는 normalized min-sum(정규화계수 0.625, layered 스케줄, max iter 32)로 근사.
9. 결과: 코드 B1에서 BP 대비 WER 최대 5자릿수 개선, [[1270,28]] GHP 부호가 near-optimal MPS 디코더의 [[1201,1,25]] surface code보다 우수. 신규 GB/GHP 부호구성·차원공식 제시.
10. 한계: 양자 채널·비바이너리 BP·syndrome 디코딩 전제, HW 미설계·순수 시뮬, `O(n^3)` 후처리로 latency 악화.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 비바이너리(GF4) BP / syndrome 디코딩 | 대응 없음 | Prime ECC는 binary min-sum 전용, 양자 syndrome 디코딩 없음 |
| OSD 후처리(신뢰도정렬+가우스소거) | 대응 없음 | 후처리 error-floor 모듈 부재, `O(n^3)` HW 부적합 |
| BP soft-decision 신뢰도 기반 정렬 | decoder.cpp `Get_VNU_Table_Idx()` (원리상 유사, 직접이식 아님) | LLR/신뢰도 개념만 대응, 알고리즘 상이 |
| QC-LDPC circulant 구조 | ecc_top.cpp `Load_PCM()` | QC 구조 공유하나 부호는 양자 CSS로 재사용 불가 |
| normalized min-sum(0.625) BP 근사 | decoder.cpp `CNU_Update_New_Mag()` | min-sum은 이미 보유, 신규성 없음 |

적용 가치: **낮음** — 양자 QLDPC/비바이너리 BP + `O(n^3)` OSD 후처리로 NAND binary QC-LDPC HW 디코더에 떼어 쓸 요소가 사실상 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1904.02703v3",
  "title": "Degenerate Quantum LDPC Codes With Good Finite Length Performance",
  "year": 2021,
  "venue": "Quantum",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": "미상",
  "code_length": "46~7938",
  "soft_quant": "무관",
  "key_contribution": "BP 실패 시 신뢰도기반 정보집합으로 OSD 후처리(BP-OSD)하여 WER 최대 5자릿수 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "X",
  "latency": "악화",
  "recommend": "하",
  "caveat": "양자 CSS/비바이너리 GF(4) BP 대상, O(n^3) OSD 후처리는 NAND HW 예산에 부적합",
  "todo_check": "OSD-0 신뢰도정렬+가우스소거 아이디어를 고전 binary error-floor 후처리로 축소 이식 가능성만 검토"
}
```
