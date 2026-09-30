### arxiv:1704.04618v1 - Advances in Detection and Error Correction for Coherent Optical Communications: Regular, Irregular, and Spatially Coupled LDPC Code Designs (2017, arXiv/Wiley book chapter)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | irregular |
| 부호rate | 0.8 |
| 부호length | 32000 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 위상슬립 채널의 반복적 차동복조에 맞춘 EXIT/PEXIT 기반 (irregular·SC) LDPC 차수분포 설계법 |
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
| 한계,주의 | 광통신 위상슬립·차동변조(QPSK/16-QAM)에 결합된 soft-decision 코드설계로 NAND binary QC-LDPC와 채널·구조 상이 |
| 추가확인 | SC-LDPC windowed decoder의 wave-like 수렴이 NAND 고rate 부호에 독립적으로 쓸 만한지 |

> 총평: 광 coherent 채널 전용 LDPC/SC-LDPC 코드설계 튜토리얼로 이론·시뮬만이며 NAND 이식성 낮음.

### B. 알고리즘 요약

1. 시스템: coherent 광통신 100/400 Gbit/s FEC, QPSK/16-QAM, code rate `r=0.8`(25% OH), 대표 부호길이 `n=32000`, soft-decision.
2. 문제: feed-forward 위상추정에서 발생하는 phase slip이 차동복호 시 error floor를 유발하여 기존 차동+LDPC 방식이 부족.
3. 채널모델: AWGN + 확률 `Pslip`의 phase slip. slip 확률 `ξ`를 slip 모델식 (1)~(3)로 pre-FEC BER(`γ`)에 연동해 모델링.
4. 핵심기법1: slip을 트렐리스에 흡수한 model-matched BCJR 차동복호(`V`=4, 16→4 상태 축소)로 monotonic EXIT 특성 확보.
5. 핵심식: `IE[V,D]` 결합 EXIT 특성 (식15)으로 차동복호+VND를 하나로 묶어 수렴조건 `fV,D(I) > fC^-1(I)` 판정.
6. 핵심기법2: full/partial interleaving 두 방식 비교, partial은 `λ`에 선형→선형계획 최적화 가능. 차수 {2,3,vmax}로 제약해 1차원 탐색(Algorithm 1).
7. 구현 디테일: `L2 ≤ 1-r` 제약으로 degree-2 노드 사이클을 없애 error floor 억제; check-regular로 CN 하드웨어 단순화.
8. 확장: protograph 기반 SC-LDPC(`ms=2`, `B0/B1/B2`)를 P=40 lifting 후 50×50 circulant QC 부호로 생성, windowed decoder(`w`,`Iw`).
9. 결과: `γ=0`에서 partial-interleave Gray가 이론한계 1dB 이내; `γ=0.2`에서 SC-LDPC가 error floor 없이 universal하게 우수.
10. 한계: HW 미설계, 시뮬만. 광 위상슬립·차동변조에 강결합된 코드설계라 일반 채널로 그대로 이식 어려움.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| irregular LDPC 차수분포 설계 (EXIT) | ecc_top.cpp `Load_PCM()` | H-matrix 설계층이나 우리는 특정 고rate QC-LDPC 고정이라 재검증 부담 큼 |
| protograph SC-LDPC → QC circulant | `ecc_top.cpp` `Load_PCM()` | 부호구조 로드층 접점뿐, SC/windowed 구조는 우리 blockwise 구조와 상이 |
| min-sum / sum-product 복호(Appendix) | `decoder.cpp` `LDPC_Decoder()` | 교과서 min-sum이라 이미 보유, 신규성 없음 |
| BCJR 차동복호 (위상슬립 트렐리스) | 대응 없음 | NAND에는 차동변조·위상슬립 개념 자체가 없음 |
| soft LLR (BPSK/QPSK) | `channel.cpp` `Set_LLR_Th()` | 광 채널 LLR로 NAND read 비용모델과 무관 |

적용 가치: **낮음** — 광 coherent 위상슬립 채널·차동변조에 강결합된 soft-decision LDPC/SC-LDPC 코드설계 튜토리얼이라 NAND binary QC-LDPC ECC로의 직접 이식 요소가 거의 없음.

### D. JSON 블록

```json
{
  "id": "arxiv:1704.04618v1",
  "title": "Advances in Detection and Error Correction for Coherent Optical Communications: Regular, Irregular, and Spatially Coupled LDPC Code Designs",
  "year": 2017,
  "venue": "arXiv/Wiley book chapter",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "irregular",
  "code_rate": 0.8,
  "code_length": "32000",
  "soft_quant": "soft-4bit+",
  "key_contribution": "위상슬립 채널의 반복적 차동복조에 맞춘 EXIT/PEXIT 기반 (irregular·SC) LDPC 차수분포 설계법",
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
  "caveat": "광통신 위상슬립·차동변조(QPSK/16-QAM)에 결합된 soft-decision 코드설계로 NAND binary QC-LDPC와 채널·구조 상이",
  "todo_check": "SC-LDPC windowed decoder의 wave-like 수렴이 NAND 고rate 부호에 독립적으로 쓸 만한지"
}
```
