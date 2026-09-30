### arxiv:2507.16326v1 - Hourglass Sorting: A novel parallel sorting algorithm and its implementation (2025, arXiv cs.AR)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | 미상 |
| 부호rate | 미상 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | PISO 스킴 병렬 정렬기(hourglass): 첫 출력 `log(n)`, 전체 `n+log(n)`, HW `O(n)`, 클록이 n에 무관 |
| HW설계 | O |
| 검증수준 | FPGA |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 정렬 가속기일 뿐이며 quantum LDPC BP-OSD 전용, binary LDPC 복호 알고리즘/부호설계와 무관 |
| 추가확인 | Prime ECC는 min-sum 기반이라 OSD용 대량 정렬 단계 자체가 없음 - 적용처 부재 |

> 총평: NAND binary LDPC ECC와 무관한 quantum LDPC BP-OSD용 PISO 정렬 HW로, Prime ECC 3.1에 이식 대상 없음.

### B. 알고리즘 요약

1. 문제: quantum LDPC의 BP-OSD에서 BP 출력을 확률순 정렬해야 하는데, 입력은 병렬(`n`)·출력은 직렬(OSD)이라 비대칭(PISO) 정렬이 필요.
2. 복잡도 분석: BP·OSD 모두 `O(m)`로 동작 가능하나 사이의 `n≫m` 정렬이 병목. 목표는 하위 `m`개를 `O(m)`에 얻어 전체 복잡도를 맞추는 것.
3. 기존 한계: 직렬 `O(n log n)`은 느리고, 병렬 정렬망은 `O(log n)` 시간이지만 `O(n log n)` 자원으로 실용 불가.
4. 핵심 아이디어: 입력을 트리형 비교기(comparator tree)로 점진 축소해 최소값을 루트로 흘려보내는 구조(merge sort의 병렬 레벨 구성).
5. naive 등록 트리: 각 노드에 레지스터 1개 → critical path는 `n`에 무관해지나 read/write 배타로 "bubbling" 발생, 출력이 유효/공백 교대(`O(2n)`).
6. hourglass 셀: 노드당 출력 레지스터 2개(ping-pong/double buffering)로 같은 사이클에 입력·출력 동시 수행 → bubble 제거.
7. 동기화: valid(`V`)/ready(`R`) 핸드셰이크, `R = ¬V1`, `V1 ⇒ V0`, D0 우선 채움·D1은 예비.
8. 안정성 증명: 루트에 bubble이 나오려면 상위 트리 전체가 비어야 하므로 첫 값 수신(`log n`) 후엔 bubble 불가 → 나머지 `n` 사이클 연속 출력, stable 정렬 보장(좌측 우선).
9. 결과(FPGA, xcvu9p): LUT·REG가 `n·w`에 선형, 클록은 `n` 무관(w=8시 705MHz, w=32시 613MHz), latency `log(n)+n`. index 레지스터 추가 시 오버헤드 `n·log(n)`.
10. 한계: quantum LDPC BP-OSD 전용 정렬 단계 가속이며 LDPC 복호 알고리즘·부호설계 자체는 다루지 않음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| PISO 병렬 정렬기(hourglass) | 대응 없음 | Prime ECC는 min-sum 기반이라 OSD·대량 정렬 단계가 없음 |
| BP-OSD 확률 정렬 | 대응 없음 | 고전 binary min-sum 복호에 OSD 미사용 |
| FPGA HW 정렬 셀 | 대응 없음 | 정렬 HW는 decoder.cpp 파이프라인과 무관 |

적용 가치: **낮음** — quantum LDPC BP-OSD 전용 정렬 가속기로, min-sum 기반 NAND binary LDPC(Prime ECC 3.1)에는 정렬 단계 자체가 없어 이식 대상이 존재하지 않는다.

### D. JSON 블록

```json
{
  "id": "arxiv:2507.16326v1",
  "title": "Hourglass Sorting: A novel parallel sorting algorithm and its implementation",
  "year": 2025,
  "venue": "arXiv cs.AR",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "미상",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "PISO 스킴 병렬 정렬기(hourglass): 첫 출력 log(n), 전체 n+log(n), HW O(n), 클록이 n에 무관",
  "hw_designed": "O",
  "verification": "FPGA",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "정렬 가속기일 뿐이며 quantum LDPC BP-OSD 전용, binary LDPC 복호 알고리즘/부호설계와 무관",
  "todo_check": "Prime ECC는 min-sum 기반이라 OSD용 대량 정렬 단계 자체가 없음 - 적용처 부재"
}
```
