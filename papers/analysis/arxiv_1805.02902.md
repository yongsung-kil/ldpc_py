### arxiv:1805.02902v2 - Reliability-Based Windowed Decoding for Spatially-Coupled LDPC Codes (2018, arXiv cs.IT / IEEE Comm. Letters)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | SC-LDPC |
| 부호rate | 0.5 |
| 부호length | 38016~38024 |
| 연판정 | hard-1bit |
| 핵심기여 | SC-LDPC 슬라이딩 윈도우 복호에서 complete VN 메시지만 보존하는 PMR + complete VN 대상 PSC 조기종료로 WBF error floor 대폭 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | SC-LDPC(convolutional) + hard-decision WBF 특화라 block QC-LDPC min-sum 구조와 불일치, HW 미설계, 윈도우/incomplete VN 개념은 SC 구조 종속 |
| 추가확인 | complete/incomplete VN 신뢰도 구분 아이디어를 block QC-LDPC의 punctured/저차수 col 신뢰도 가중에 전용 가능한지 |

> 총평: SC-LDPC 윈도우 복호기의 error-floor를 신뢰 메시지 선별(PMR)과 부분 syndrome 조기종료(PSC)로 잡는 저복잡도 기법. block QC-LDPC/min-sum이 아닌 SC-LDPC+WBF 특화라 Prime ECC 직접 이식성은 낮음.

### B. 알고리즘 요약

1. 대상: protograph 기반 SC(spatially-coupled) LDPC, base matrix `B`를 edge spreading해 `BL` 구성 (`ms`=syndrome former memory, `L`=termination length, lifting `M`). 실험 부호 길이 `38024` (7,49)·`38016` (3,6).
2. 복호는 슬라이딩 윈도우(size `W`, `W·Mr` CN·`W·Mc` VN)로 일부만 처리 — FBD 대비 latency·메모리 절감이나 성능 저하(높은 error floor) 발생.
3. 관찰: 윈도우 밖 CN에 연결된 `incomplete VN`은 유효 column weight가 낮아 메시지 신뢰도가 낮고, 이 오염 메시지가 다음 윈도우로 전파되어 error floor 유발.
4. 복호 코어는 conventional WBF(hard-decision bit-flipping): flipping metric `Ei(l)=Σ_{j∈N(i)}(2s_j-1)·w_j`, 가중치 `w_j=min|r_i|`, 최대 metric VN을 flip.
5. 핵심 기법1 PMR(partial message reservation): 다음 윈도우로 넘기는 메시지 `u_k`를 complete VN(`k∈VC`)이면 복호결과 `z_{t,k}`, incomplete VN(`k∈VI`)이면 hard decision `v_k`만 — 신뢰 메시지만 보존.
6. 식 의미: complete VN 수 > incomplete VN이 되도록 `W` 선택해 신뢰 메시지 전파 극대화, 오염 차단.
7. 핵심 기법2 PSC(partial syndrome check) 조기종료: 윈도우 내 complete VN에 연결된 앞쪽 `W'=(W-ms)·Mr` parity-check row만 검사해 종료 — hard-only 환경에 맞춘 정지규칙.
8. 알고리즘1로 PMR+PSC+SBF-WBF를 통합, 최대 iteration 200(FBD 2000).
9. 결과: length-38024 (7,49) SC-LDPC에서 PMR이 error rate를 크게 개선, PSC가 error floor를 추가로 낮춰 FBD 대비 0.1dB 이내; RBWD가 MBF/SBF-PMR 대비 SNR 5.6~6dB에서 평균 업데이트 수 약 절반(Table I).
10. 한계: BPSK/AWGN 시뮬만, HW 미설계, SC-LDPC(convolutional) 및 hard-decision WBF에 특화.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| WBF hard-decision 복호 루프 | decoder.cpp `LDPC_Decoder()` 이터레이션 루프 | Prime은 min-sum message passing이라 WBF 자체는 대응 없음, 신뢰도 가중 아이디어만 참고 |
| PSC 부분 syndrome 조기종료 | partial_CRC.cpp `partial_crc_HW_T4()` | 부분 검사 조기종료라는 개념은 유사하나 Prime은 CRC 기반·이미 보유 |
| complete/incomplete VN 신뢰도 구분 | 대응 없음 (SC 윈도우 구조 종속) | block QC-LDPC엔 윈도우/incomplete VN 개념 부재 |
| SC-LDPC 부호구조 | 대응 없음 (Prime은 block QC-LDPC 고정) | SC/convolutional 구조 미지원 |

적용 가치: **낮음** — SC-LDPC 슬라이딩 윈도우 복호에 특화된 기법으로 block binary QC-LDPC min-sum 기반 Prime ECC와 구조가 근본적으로 다르며, 조기종료는 이미 partial-CRC로 보유. VN 신뢰도 가중 아이디어 정도만 개념 참고.

### D. JSON 블록

```json
{
  "id": "arxiv:1805.02902v2",
  "title": "Reliability-Based Windowed Decoding for Spatially-Coupled LDPC Codes",
  "year": 2018,
  "venue": "arXiv cs.IT (IEEE Communications Letters)",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "SC-LDPC",
  "code_rate": 0.5,
  "code_length": "38016~38024",
  "soft_quant": "hard-1bit",
  "key_contribution": "SC-LDPC 윈도우 복호에서 complete VN 메시지만 보존하는 PMR + complete VN 대상 PSC 조기종료로 WBF error floor 대폭 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "하",
  "caveat": "SC-LDPC(convolutional)+hard-decision WBF 특화라 block QC-LDPC min-sum 구조와 불일치, HW 미설계",
  "todo_check": "complete/incomplete VN 신뢰도 구분을 block QC-LDPC의 punctured/저차수 col 신뢰도 가중에 전용 가능한지"
}
```
