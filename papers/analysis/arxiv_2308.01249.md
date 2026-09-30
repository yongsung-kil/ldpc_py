### arxiv:2308.01249v2 - A Spatially Coupled LDPC Coding Scheme with Scalable Decoders for Space Division Multiplexing (2023, arXiv cs.IT / ECOC 2023)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | SC-LDPC |
| 부호rate | 0.8 |
| 부호length | 미상 |
| 연판정 | soft-4bit+ |
| 핵심기여 | sub-block locality SC-LDPCL의 분산 수신기용 semi-joint 디코더와 정보교환 절감 2변형(SJVar, SJ-HD) 제안 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | SDM 광통신·AWGN(Eb/N0) 타깃 SC-LDPC로 NAND single-block QC-LDPC와 구조 상이, HW·throughput 없음 |
| 추가확인 | 다중 sub-block 간 정보흐름 절감 아이디어(SJ-HD의 hard 교환)가 NAND 단일 디코더 맥락에 의미 있는지 |

> 총평: 광통신 SDM용 sub-block locality SC-LDPC의 분산 수신기 semi-joint 디코더 논문으로, NAND 단일 binary QC-LDPC 디코더에 이식 가치는 낮음.

### B. 알고리즘 요약

1. 대상은 sub-block locality를 갖는 unit-memory spatially-coupled LDPC(`SC-LDPCL`), 예시 `(dv=4, dc=20, t=1/4)` (rate≈0.8), 각 sub-block을 SDM 공간채널 하나에 할당.
2. 풀려는 문제: SDM 수신기가 통합/분산/반분산 회로일 수 있어, 디코더 간 정보교환량을 줄이면서 성능을 유지하는 확장형 복호가 필요.
3. 부호 구조: parity-check가 sub-block 내부만 잇는 local check(`Hlocal`)와 이웃 sub-block을 잇는 coupled check(`Hleft`/`Hright`)로 구성, 세 모드(separate/joint/semi-joint) 지원.
4. 핵심 기법 1: semi-joint(SJ) 디코더 — 타깃 sub-block `T`를 `d`개 helper와 함께 복호, 가장 먼 helper부터 local BP 후 좌/우로 이웃 정보 `ŷ`를 전파(helper 양측 병렬 가능).
5. 핵심 식: helper의 unfulfilled check 비율 `δc`로 BER `δ̂b = ½(1-(1-2δc)^{1/dc})`를 추정, hard decision `x̂`를 LLR `y=x̂·ln((1-δ̂b)/δ̂b)`로 환산.
6. 핵심 기법 2(SJVar): SDM에서 모든 sub-channel 관측이 동시 가용함을 이용해, 복호 시작 전에만 채널정보를 모아 `(d+1)`-sub-block 확장 PCM `B`로 한 번에 BP → 정보흐름·복잡도 동일하게 유지하며 약 0.2 dB 이득.
7. 부수 트릭(SJ-HD): sub-block 간 soft(q=5~7bit) 대신 hard decision + BER 추정만 교환해 정보흐름을 q배 축소, 성능 손실 약 0.1 dB.
8. 학습/최적화 절차: 없음(구조적 디코딩 스케줄 설계).
9. 결과: helper `d` 증가 시 BER 감소(separate=상한, joint=하한 사이), SJVar 약 0.2 dB 이득, SJ-HD 약 0.1 dB 손실로 정보흐름 q배 절감(BER 곡선, Eb/N0 2.4~4 dB AWGN).
10. 한계: 순수 시뮬(HW·gatecount·throughput 없음), 광통신 SDM·AWGN 타깃, 두 변형은 동시 결합 불가.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SC-LDPCL sub-block/coupled-check 부호구조 | 대응 없음 | Prime ECC는 단일 blocklength QC-LDPC(`ecc_top.cpp` `Load_PCM()`), spatially-coupled sub-block 구조 미지원 |
| BP(sum-product) windowed/semi-joint 복호 | `decoder.cpp` `LDPC_Decoder()` | 우리는 단일 블록 min-sum 이터레이션, 다중 sub-block helper 스케줄과 구조 상이 |
| hard/soft 정보교환·LLR 환산 | `channel.cpp` `Set_LLR_Th()` (참고) | 우리 LLR은 채널 read 기반, sub-block 간 교환 개념 자체가 없음 |
| soft 양자화 q=5~7bit | 대응 없음 | Prime ECC는 hard/2SD/3SD(2~3bit)까지만, 4bit+ 미지원 |

적용 가치: `낮음` - 다중 디코더 회로 간 정보흐름 절감이 핵심인 SC-LDPC(광통신 SDM) 논문으로, NAND 단일 binary QC-LDPC 디코더/HW 구조와 정합되지 않아 떼어 쓸 요소가 거의 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2308.01249v2",
  "title": "A Spatially Coupled LDPC Coding Scheme with Scalable Decoders for Space Division Multiplexing",
  "year": 2023,
  "venue": "arXiv cs.IT (ECOC 2023)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "SC-LDPC",
  "code_rate": 0.8,
  "code_length": null,
  "soft_quant": "soft-4bit+",
  "key_contribution": "sub-block locality SC-LDPCL의 분산 수신기용 semi-joint 디코더와 정보교환 절감 2변형(SJVar, SJ-HD) 제안",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "SDM 광통신·AWGN(Eb/N0) 타깃 SC-LDPC로 NAND single-block QC-LDPC와 구조 상이, HW·throughput 없음",
  "todo_check": "다중 sub-block 간 정보흐름 절감(SJ-HD hard 교환)이 NAND 단일 디코더 맥락에 의미 있는지"
}
```
