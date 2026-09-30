### arxiv:1302.4516v1 - Bilayer Protograph Codes for Half-Duplex Relay Channels (2013, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | protograph |
| 부호rate | 0.33~0.9 |
| 부호length | 16000~23660 |
| 연판정 | 무관 |
| 핵심기여 | Half-duplex relay channel(source-relay-destination)용 bilayer(lengthened/expurgated) protograph LDPC 코드 구조로, rate-compatible 임베디드 코드 패밀리를 낮은 인코딩 복잡도로 설계 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | relay 채널(3-노드 협력통신) 특화 코드 구조로 NAND 저장장치의 point-to-point 채널과 무관, 표준 message-passing 디코더(max iter 200) 사용해 디코더 자체 기여 없음 |
| 추가확인 | bilayer lengthened/expurgated 구조의 rate-compatible 설계 아이디어가 NAND의 가변 rate ECC(예: 수명에 따른 rate 적응)에 참고될 여지가 있는지 |

> 총평: 협력통신(relay channel) 특화 protograph LDPC 코드 설계 논문으로, NAND 저장 채널과 무관하고 표준 BP 디코더만 사용해 Prime ECC 이식 가치가 낮음.

### B. 알고리즘 요약

1. 시스템은 half-duplex relay channel(소스 S, 릴레이 R, 목적지 D 3-노드), 두 타임슬롯(broadcast/multiple-access)으로 나뉘며 각 링크(SR/SD/RD)가 서로 다른 SNR을 가짐; 코드 rate는 예시로 1/2~9/10(lengthened), 1/3~3/4(expurgated) 등 다양.
2. 풀려는 문제: 기존 relay용 LDPC 코드는 특정 채널 조건에 맞춰 무겁게 최적화되어 재최적화 없이 다양한 채널에 적응하기 어렵고, 인코딩 복잡도가 높거나 capacity에 접근하려면 긴 블록길이가 필요했음.
3. 핵심 가정/모델: BI-AWGN 채널, decode-forward(DF) 프로토콜, source-relay/source-destination/relay-destination 3개 링크의 서로 다른 SNR을 가정.
4. 핵심 기법: protograph(작은 bipartite proto-matrix)를 확장하는 bilayer 구조 2종 — `lengthened`(저rate 코드에 변수노드 추가로 고rate 코드 구성, `H_SR1=[H_SD1 H_e]`)와 `expurgated`(고rate 코드에 체크노드 추가로 저rate 코드 구성, `H_SD1=[H_SR1; H_e]`).
5. 핵심 식: proto-matrix 확장 시 열합(column sum)이 3 이상이어야 최소거리의 선형 증가(error floor 회피) 보장; PEXIT(Protograph EXIT) 기법으로 iterative decoding threshold를 dB 단위로 계산해 비용함수로 사용.
6. 확장: 단일 릴레이 구조를 2-relay 채널로 확장, 3-layer bilayer expurgated 구조(Layer 1/2/3 순차 릴레이 디코딩)로 다중 협력 노드 지원.
7. 부수 트릭: PEG(progressive edge growth) 알고리즘으로 2단계 lifting(우선 4배로 parallel edge 제거, 이후 목표 블록길이까지 circulant permutation 결정), 고rate 코드 하나만 디코더 설계하면 나머지 저rate 코드는 erasure 처리로 재사용 가능.
8. 최적화 절차: proto-matrix의 parallel edge 수(x_i, y_i ∈ {0,1,2})를 제한한 뒤 PEXIT threshold를 비용함수로 하는 탐색(GA/DE 아님, 제한된 파라미터 그리드 탐색).
9. 결과: 대부분 코드가 capacity 대비 0.1~0.33dB 이내 threshold, 시뮬레이션(16k 정보블록)에서 WER 10^-6까지 error floor 관찰 안 됨; end-to-end 성능은 capacity 대비 0.7~1.2dB.
10. 한계: relay 채널(3-노드 협력) 특화 구조로 NAND의 point-to-point 채널과 무관, 디코더는 표준 message-passing(max iteration 200)으로 디코더 알고리즘 자체의 기여는 없음, HW 미설계.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| bilayer protograph 부호 구조 설계 | `ecc_top.cpp` `Load_PCM()` | relay 채널 특화 구조(SR/SD/RD 링크별 서브코드)로 NAND 단일채널 구조와 이질적, 재설계 필요 |
| rate-compatible 임베디드 코드 패밀리 | 대응 없음 | Prime ECC는 고정 rate QC-LDPC 구조이며 이런 형태의 nested rate-compatible 설계는 없음 |
| 표준 message-passing 디코더 | `decoder.cpp` `LDPC_Decoder()` | 디코더 알고리즘 자체는 표준(개선 없음), Prime ECC 대비 추가 기여 없음 |

적용 가치: **낮음** — relay channel 협력통신 특화 부호 구조로 NAND 저장 채널과 무관하며, 디코더 알고리즘 개선이 없어 Prime ECC에 이식할 실질적 요소가 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1302.4516v1",
  "title": "Bilayer Protograph Codes for Half-Duplex Relay Channels",
  "year": 2013,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "protograph",
  "code_rate": "0.33~0.9",
  "code_length": "16000~23660",
  "soft_quant": "무관",
  "key_contribution": "Half-duplex relay channel용 bilayer(lengthened/expurgated) protograph LDPC 코드 구조로 rate-compatible 임베디드 코드 패밀리를 낮은 인코딩 복잡도로 설계",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "relay 채널(3-노드 협력통신) 특화 코드 구조로 NAND 저장장치의 point-to-point 채널과 무관, 표준 message-passing 디코더(max iter 200) 사용해 디코더 자체 기여 없음",
  "todo_check": "bilayer lengthened/expurgated 구조의 rate-compatible 설계 아이디어가 NAND의 가변 rate ECC(예: 수명에 따른 rate 적응)에 참고될 여지가 있는지"
}
```
