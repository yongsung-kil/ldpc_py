### arxiv:0801.1208v4 - Hybrid Decoding of Finite Geometry LDPC Codes (2008, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.70~0.76 |
| 부호length | 273~1023 |
| 연판정 | 미상 |
| 핵심기여 | 병렬 bit-flipping(LF-WBF) 변형과 Min-Sum 변형을 직렬 결합한 하이브리드 복호로 MS 성능 유지하며 평균 연산 복잡도 대폭 절감 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 미상 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | X |
| latency | 동등 |
| 추천도 | 중 |
| 한계,주의 | FG-LDPC(heavy row/col weight=32) 특화 복잡도 절감이라 저weight QC-LDPC(NAND)에선 이득 불확실, 성능은 MS 대비 개선 없이 동등 유지 |
| 추가확인 | 우리 z=32 QC-LDPC min-sum에 BF 전단 결합 시 실제 평균복잡도/전력 절감폭 및 오정정 리스크 검증 필요 |

> 총평: 저복잡도 BF 전단 + MS 후단의 2단 하이브리드 복호로 평균 연산량을 절감하는 decoder 기법, FG-LDPC 특화라 NAND QC-LDPC 이득은 재검증 필요.

### B. 알고리즘 요약

1. AWGN/BPSK에서 finite geometry(FG) LDPC 부호((273,191), (1023,781), `dv=dc=32`)의 복호를 다룬다.
2. FG-LDPC는 행·열 weight가 무거워 Min-Sum(MS) 변형으로도 복호 연산량이 크고, 순수 bit-flipping(BF)은 값싸지만 성능 손실이 문제다.
3. 해결책: 값싼 병렬 BF 변형(전단) + MS 변형(후단)을 직렬 결합 — 전단 BF가 대부분의 복호부하를 처리하고 실패 시에만 MS 호출(Fig.1).
4. 신규 BF 변형 `LF-WBF` 제안: SZ-WBF의 BF 함수 `f_i=Σ w_{i,k} f_{i,k}`에 IPWBF식 delay-handling(신뢰비트 지연 flip)을 결합, 매 iteration 다중비트 flip.
5. 조기종료는 syndrome `s=Hĉ=0` 확인으로 처리하고, flipping counter `b_i`/delay counter `a_i` 임계(`α2,α3`)로 flip 대상 결정.
6. 후단 MS는 NMS/OMS(식 8/9, scaling `β5`/offset `β6`)와 VN단 근사 NAB(식 11)를 사용해 standard BP 대비 복잡도 절감하며 near-BP 성능.
7. LF-WBF 파라미터 `(α1,α2,α3,β1,β4)`는 이론적 최적화가 어려워 differential evolution(DE)으로 BER 최소화하도록 튜닝(Table-I).
8. 조건: 두 복호기 성능격차가 작아 waterfall 영역이 겹쳐야 MS 재호출이 줄어 복잡도 절감 극대화.
9. 결과: (1023,781) `dv=dc=32`에서 LF-WBF+NMS가 NMS 단독 대비 real additions 4.93e5→3.10e5로 절감(평균 NMS iter 3.77→0.88), 성능은 MS 동등 유지, high-SNR일수록 절감폭↑.
10. 한계: HW 미설계(복잡도 정성분석만), FG-LDPC 특화, 성능이득 없음(복잡도만 절감), 양자화 미명시.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 하이브리드 복호 프레임워크(BF 전단→MS 후단) | decoder.cpp `LDPC_Decoder()` | 복호 이터레이션 루프에 BF 전단 추가·제어, 평균복잡도 절감용 |
| Min-Sum 변형(NMS/OMS) CN 연산 | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | 이미 보유 min-sum, 논문은 normalized/offset factor 사용 |
| 병렬 bit-flipping(LF-WBF) BF함수/flip counter | 대응 없음 | BF 복호 미보유(신규 전단) |
| syndrome=0 조기종료 | partial_CRC.cpp / full_CRC.cpp | 우리는 CRC 기반 조기종료로 역할 유사 |
| DE 기반 파라미터 자동 최적화 | local_opt.cpp | LLR 자동최적화와 유사한 offline 튜닝 |

적용 가치: **중간** — 값싼 BF 전단으로 평균 복잡도/전력을 줄이는 2단 복호 아이디어는 참고 가치가 있으나, FG-LDPC(heavy weight) 특화라 저weight QC-LDPC에서 이득·오정정 리스크를 재검증해야 한다.

### D. JSON 블록

```json
{
  "id": "arxiv:0801.1208v4",
  "title": "Hybrid Decoding of Finite Geometry LDPC Codes",
  "year": 2008,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "273~1023",
  "soft_quant": "미상",
  "key_contribution": "병렬 bit-flipping(LF-WBF) 변형과 Min-Sum 변형을 직렬 결합한 하이브리드 복호로 MS 성능 유지하며 평균 연산 복잡도 대폭 절감",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "미상",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "X",
  "latency": "동등",
  "recommend": "중",
  "caveat": "FG-LDPC(heavy row/col weight=32) 특화 복잡도 절감이라 저weight QC-LDPC(NAND)에선 이득 불확실, 성능은 MS 대비 개선 없이 동등 유지",
  "todo_check": "우리 z=32 QC-LDPC min-sum에 BF 전단 결합 시 실제 평균복잡도/전력 절감폭 및 오정정 리스크 검증 필요"
}
```
