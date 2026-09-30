### arxiv:1607.05647v2 - Design of LDPC Codes using Multipath EMD Strategies and Progressive Edge Growth (2016, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | irregular |
| 부호rate | 0.2468~0.5 |
| 부호length | 230~282 |
| 연판정 | 무관 |
| 핵심기여 | PEG 후보 check node 선택 시 최단경로 개수+평균 path EMD 진행형 메트릭으로 stopping set 생성을 억제해 error-floor 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | 부분 |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | 부호구성(offline) 기법이라 Prime ECC 고정 QC-LDPC(z=32) 재설계 부담, 예제는 저rate·짧은 길이·block fading 중심 |
| 추가확인 | 고rate QC-LDPC(대형 circulant)에서의 error-floor 이득과 경로탐색 복잡도 확장성 |

> 총평: 짧은 부호의 error-floor를 stopping set 회피로 낮추는 PEG 계열 구성법. 디코더 알고리즘이 아닌 offline 부호설계라 Prime ECC 이식은 H-matrix 재설계를 요해 이식성은 중간.

### B. 알고리즘 요약

1. 시스템: 일반 LDPC (Encoder-Channel-Decoder), 채널은 BEC/AWGN 및 block fading (`F`개 독립 fade). 짧은~중간 블록 길이(N=230~282, rate 1/4~1/2)를 표적.
2. 문제: 짧은 블록에서 그래프의 닫힌 경로(cycle)로 메시지 독립성이 깨져 error-floor 발생. 기존 PEG/ACE-EMD는 stopping set을 근사적으로만 회피.
3. 핵심 가정: error 이벤트는 stopping set/trapping set에서 기인. BEC에서는 stopping set이 성능을 완전히 규정 → stopping set 최소화가 목표.
4. 핵심 기법: PEG tree 확장으로 최대거리·최소weight check node 후보군 축소 후, 각 후보에 대해 root VN→candidate CN 사이 distinct path 개수 `Pci`를 계산.
5. 핵심 식: `C = {ci : Pci = min Pcy}` (식11) — 최소 경로수 후보 선택. 최단 cycle 개수를 줄여 stopping set 생성 확률을 낮춤.
6. 2단 tie-break: 동수일 때 각 path의 EMD `Ep,ci`(식12, PCM 열 합의 1 개수)의 평균 `γci`(식13)를 최대화하는 후보 선택 (식14).
7. 구현 디테일: EMD는 path 내 VN들의 PCM 열을 합산해 1의 개수를 세는 단순 연산. weight-2 VN 제약으로 zero-EMD cycle을 사전 배제.
8. 확장: block fading full-diversity 부호 클래스 제안 — systematic 노드가 systematic stopping set에 들지 않도록 서브행렬(`Hβ`)을 조합, `R<=1/F` 제약과 rate-compatible puncturing 지원.
9. 결과: QC-LDPC(N=256, Q=8)에서 PEG 대비 0.4dB, IPEG 대비 0.3dB(BER<1e-7) 이득. IRA는 약 0.25dB. cycle-6 개수 최소(Table I). block fading에서 수렴속도 개선.
10. 한계: HW 미설계, 시뮬만. 경로탐색 복잡도 큼(Fig.18). 예제가 저rate·짧은 길이·block fading 중심이라 NAND 고rate QC-LDPC와 거리.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Multipath EMD PEG 부호구성 (H-matrix 생성) | ecc_top.cpp `Load_PCM()` | offline 구성 결과를 PCM으로 로드해야 하나 구성 자체는 코드 밖 |
| error-floor 개선(stopping set 회피) 부호 | decoder.cpp `LDPC_Decoder()` | 개선된 H-matrix가 디코더 error-floor에 간접 영향 |
| block fading full-diversity 부호/puncturing | 대응 없음 | Prime ECC는 NAND(AWGN/RBER)용, block fading 무관 |

마지막에 한 문장으로 **적용 가치**: 낮음 — error-floor 억제 원리는 유효하나 Prime ECC의 고정 QC-LDPC(z=32, 고rate)를 재설계·재검증해야 하고, 논문 예제(저rate·짧은 길이·block fading)가 NAND ECC와 정합성이 낮다.

### D. JSON 블록

```json
{
  "id": "arxiv:1607.05647v2",
  "title": "Design of LDPC Codes using Multipath EMD Strategies and Progressive Edge Growth",
  "year": 2016,
  "venue": "arXiv cs.IT",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "irregular",
  "code_rate": "0.2468~0.5",
  "code_length": "230~282",
  "soft_quant": "무관",
  "key_contribution": "PEG 후보선택에 최단경로 개수+평균 path EMD 진행형 메트릭을 적용해 stopping set 생성을 억제하고 error-floor 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "부분",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "offline 부호구성 기법이라 Prime ECC 고정 QC-LDPC 재설계 부담, 예제는 저rate·짧은 길이·block fading 중심",
  "todo_check": "고rate 대형 circulant QC-LDPC에서 error-floor 이득과 경로탐색 복잡도 확장성 확인"
}
```
