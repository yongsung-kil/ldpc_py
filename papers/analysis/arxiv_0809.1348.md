### arxiv:0809.1348v1 - MBBP for improved iterative channel decoding in 802.16e WiMAX systems (2008, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5 |
| 부호length | 576~960 |
| 연판정 | 무관 |
| 핵심기여 | 여러 중복 PCM으로 BP 디코더를 완전 병렬 실행 후 Euclidean 최근접 코드워드 선택(decoder diversity) |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | X |
| latency | 동등 |
| 추천도 | 하 |
| 한계,주의 | l=7~30 병렬 BP 디코더가 필요해 NAND ECC 면적 예산에 비현실적, 이득은 waterfall ~0.15dB로 소폭 |
| 추가확인 | 우리 고rate QC-LDPC에서 저중량 중복 체크 생성이 가능한지, l-병렬 면적 대비 이득 타당성 |

> 총평: WiMAX QC-LDPC용 다중기저 BP(MBBP) 디코더 다양성 기법. 개념은 binary LDPC에 이식 가능하나 l개 병렬 디코더 복제 비용이 NAND ECC에 비현실적이고 이득이 작아 실효성 낮음.

### B. 알고리즘 요약

1. 시스템: AWGN 채널, systematic `[n,k,d]` block code, IEEE 802.16e WiMAX rate-1/2 LDPC (`576 ≤ n ≤ 960`), 비교군 PEG 최적화 부호(`500 ≤ n ≤ 1000`).
2. 문제: 표준 BP는 suboptimal이라 특정 error pattern을 못 잡음 - 중복 parity-check 표현으로 디코더 다양성을 얻어 성능 개선 목표.
3. 핵심기법(MBBP): 동일 부호의 서로 다른 PCM `H_1..H_l`을 각기 다른 BP 디코더에 병렬 투입, 각 추정 `x̂_1..x̂_l` 생성.
4. 후처리: post-processing이 Euclidean 거리로 수신 `y`에 가장 가까운 코드워드 하나를 선택(MBBP-NX-S), 통신 없는 비협력 병렬 디코더 구성.
5. 완전 병렬이라 디코딩 지연이 단일 BP와 동일 - 이것이 RRD(직렬)/adaptive-BP(비병렬) 대비 강점.
6. Leaking(L-MBBP): 채널 정보를 첫 iteration엔 확률 `pL`로만 반영하고 iteration이 오를수록 점진 leak(`I'_max=300`) - 짧은 cycle 문제 완화.
7. 중복 PCM 생성(핵심 트릭): binary `H` 대신 base matrix `Hb`에서 양의 원소가 겹치지 않는 두 행을 선형결합해 저중량 중복 체크 생성 후 lifting - WiMAX 구조 활용.
8. 예) `Hb`의 11,12행 결합 → weight-10 중복 체크 `z`개. 길이별 10~16개 parity check 교체, full-rank 보장.
9. 결과: `l=7`에서 이득 대부분 확보, `l=15/30`은 소폭 추가. 모든 길이서 ~0.15dB 이득, Gallager bound 대비 gap을 ~20%(0.14dB) 축소.
10. 한계: HW 미설계, 시뮬만, AWGN/WiMAX 특화, gate count/throughput 없음, 최대 30 병렬 디코더 전제.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| MBBP 병렬 BP 디코더 인스턴스 | decoder.cpp `LDPC_Decoder()` | 디코더 루프 자체는 재사용 가능하나 서로 다른 PCM로 `l`개 인스턴스를 동시 구동해야 해 면적이 `l`배 |
| 중복 PCM 생성/로드 | `ecc_top.cpp` `Load_PCM()` | base matrix에서 파생한 중복 체크 세트를 로드하는 지점에 대응 |
| Leaking(iteration별 채널정보 점진 반영) | `ecc_data.h` `PARAM_LLR`, `decoder.cpp` `Get_VNU_Table_Idx()` | iteration 구간별 LLR 스케줄과 유사하나 목적(중복체크 short-cycle 완화)이 달라 관련성 낮음 |
| Post-processing Euclidean 최근접 선택 | 대응 없음 | 다중 디코더 출력 중 최적 선택 로직은 현 코드에 부재 |

적용 가치: **낮음** - binary QC-LDPC 디코더 계층 기법이라 개념 이식은 가능하나, `l`개 병렬 BP 디코더 복제와 중복 PCM 유지 비용이 고rate NAND ECC에 비현실적이고 이득(waterfall ~0.15dB)이 작다.

### D. JSON 블록

```json
{
  "id": "arxiv:0809.1348v1",
  "title": "MBBP for improved iterative channel decoding in 802.16e WiMAX systems",
  "year": 2008,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": 0.5,
  "code_length": "576~960",
  "soft_quant": "무관",
  "key_contribution": "여러 중복 PCM으로 BP 디코더를 완전 병렬 실행 후 Euclidean 최근접 코드워드 선택(decoder diversity)",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "X",
  "latency": "동등",
  "recommend": "하",
  "caveat": "l=7~30 병렬 BP 디코더가 필요해 NAND ECC 면적 예산에 비현실적, 이득은 waterfall ~0.15dB로 소폭",
  "todo_check": "우리 고rate QC-LDPC에서 저중량 중복 체크 생성이 가능한지, l-병렬 면적 대비 이득 타당성"
}
```
