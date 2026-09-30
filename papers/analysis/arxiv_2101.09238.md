### arxiv:2101.09238v1 - Unequal Error Protection Achieves Threshold Gains on BEC and BSC via Higher Fidelity Messages (2021, arXiv cs.IT / ISIT-class)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 0.58~0.85 |
| 부호length | 미상 |
| 연판정 | 무관 |
| 핵심기여 | RA-LDPC의 parity bit에 UEP(더 높은 신뢰도) 적용 시 BEC 17%/BSC 28% threshold 이득을 EXIT 차트로 이론 증명 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | BEC/BSC 점근(threshold) 해석뿐 — 유한길이·AWGN·soft-read 없음, HW 미설계, RA 구조에 특화 |
| 추가확인 | UEP를 constrained code 없이 실제 NAND(고rate QC-LDPC, soft-read)에서 유한길이로 재현 가능한지 |

> 총평: parity bit 보호(UEP) 아이디어의 순수 threshold 이론 증명 — RA 코드·BEC/BSC 한정이라 Prime ECC(QC-LDPC, AWGN/RBER) 직접 이식성은 낮음.

### B. 알고리즘 요약

1. 시스템: RA(repeat-accumulate) LDPC, `H=[J P]` 형태(J는 dual-diagonal 형태의 accumulator), rate 대략 `0.58~0.85`, BEC/BSC 두 채널.
2. 풀려는 문제: [8]의 MR 실험에서 constrained(LOCO) 코드로 parity bit만 보호 시 최대 20% density 이득이 관측 — 이 UEP 효과를 이론적으로 규명.
3. 핵심 가정: parity bit는 정보 bit보다 낮은 erasure/crossover 확률(`q1<q2`, `ε1<ε2`)을 갖도록 UEP 모델링. 각 정보 VN이 CN 통해 최소 1개 parity VN과 연결(확산 조건).
4. 핵심 기법: EXIT 차트로 VN/CN의 a-priori(`IA`)↔extrinsic(`IE`) 정보 전달 함수를 유도, VN 곡선이 CN 역곡선 위에 있어야 수렴.
5. 핵심 식: UEP EXIT는 branch 가중합 `IE*,v = a·IE,v(σ1,dv=2) + b·IE,v(σ2,dv=2) + Σλi·IE,v(σ2,i)` — parity(`a`)에만 낮은 오류율 `σ1` 적용.
6. 확장: BSC용 VN/CN EXIT 함수를 Theorem 1·2로 폐형식 유도(`θ1i,θ2i`, `(1-2δ)^{dc-1}`).
7. 최적화 절차: 수렴 제약 하 rate 최대화를 선형계획(LP)으로 풀어 최적 차수분포 `λ` 도출(두 가지 방법: uniform 최적/UEP 최적).
8. 결과: BEC에서 최대 약 17%(method2)/10%(method1), BSC에서 최대 28% threshold 이득.
9. 데이터 저장 함의: 소자 노화 시 rate 손실 없이 lifetime 이득 가능하다고 주장.
10. 한계: 점근 threshold 해석만, 유한길이 시뮬·AWGN·실제 soft-read·HW 전무. AWGN/Flash/MR 확장은 future work.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| UEP(parity bit 신뢰도 차등) 부호/채널 설계 | 대응 없음 | Prime ECC는 균등 보호 QC-LDPC — parity 차등 보호 개념 자체가 없음 |
| RA H=[J P] 구조 (dual-diagonal accumulator) | encoder.cpp Generate_PCM_encoding() | dual-diag 인코딩과 형태 유사하나 UEP·rate 최적화는 무관 |
| EXIT/LP 기반 차수분포 최적화 | ecc_top.cpp Load_PCM() | H-matrix 설계 단계에 대응하나 특정 QC-LDPC 고정 — 재설계 부담 큼 |
| soft-info/LLR 신뢰도 차등 | channel.cpp Set_LLR_Th() | 개념적으로만 관련, BEC/BSC 모델이라 실제 LLR 양자화와 무관 |
```

적용 가치: **낮음** — RA·BEC/BSC 한정의 순수 threshold 이론이며, Prime ECC의 고rate binary QC-LDPC + AWGN/soft-read + 균등보호 구조와 부호종류·채널·검증수준 모두 어긋나 직접 이식 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:2101.09238v1",
  "title": "Unequal Error Protection Achieves Threshold Gains on BEC and BSC via Higher Fidelity Messages",
  "year": 2021,
  "venue": "arXiv cs.IT (ISIT-class)",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "미상",
  "soft_quant": "무관",
  "key_contribution": "RA-LDPC parity bit UEP의 BEC 17%/BSC 28% threshold 이득을 EXIT 차트로 이론 증명",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "BEC/BSC 점근 threshold 해석뿐 — 유한길이·AWGN·soft-read 없음, HW 미설계, RA 구조 특화",
  "todo_check": "UEP를 constrained code 없이 실제 NAND 고rate QC-LDPC soft-read 유한길이에서 재현 가능한지"
}
```
