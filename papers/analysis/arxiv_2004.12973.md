### arxiv:2004.12973v1 - Comparison of Windowed-Decoder Configurations for Spatially Coupled LDPC Codes Under Equal-Complexity Constraints (2020, arXiv/Elsevier preprint)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | SC-LDPC |
| 부호rate | 0.48 |
| 부호length | 51200 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 동일 최대복잡도 제약 하에서 SC-LDPC windowed decoder의 창(window) 크기·업데이트 전략(VN-centered vs CN-centered)·parity-check 기반 조기종료 조합을 비교해 FBD 대비 평균 복호 복잡도를 절반으로 줄이는 저오버헤드 구성을 도출 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | O |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | SC-LDPC(convolutional) 코드 전용 windowed decoding 기법으로 Prime ECC의 block QC-LDPC 구조에는 그대로 이식 불가하며, HW 미설계·순수 알고리즘/시뮬 비교 수준 |
| 추가확인 | 조기종료(ET)에 사용하는 target-CN 부분집합(Ct) 선택 아이디어가 Prime ECC의 partial CRC termination point 설계와 유사한지 추가 비교 필요 |

> 총평: SC-LDPC(convolutional) 코드 전용 windowed decoder의 window 크기·업데이트 전략·조기종료 조합 최적화 연구로, block QC-LDPC인 Prime ECC에 구조 자체는 이식 불가하나 조기종료·메모리 절감 설계 아이디어는 참고 가치가 있음.

### B. 알고리즘 요약

1. 대상 부호는 (dv,dc)=(5,10) 규칙적 QC-SC-LDPC 앙상블, lifting factor `Q=256`, coupling length `L=100`, 코드길이 `n=51200`, 실효 rate `R=0.48`(점근 rate `R∞=1/2`).
2. 풀려는 문제: Full Block Decoder(FBD) 대비 Windowed Decoder(WD)는 메모리·지연을 줄이지만, window 크기·업데이트 전략·조기종료(ET) 설계가 성능/복잡도에 미치는 영향에 대한 종합 비교가 부재.
3. 채널 모델은 4-path Rayleigh fading + AWGN(MRC 결합), 16-QAM, 5G NR 유사 설정이며, 디코더는 fixed-point 10bit LLR-magnitude 해상도의 min-sum 근사(SPA/MSA 혼합, [32] 방식) 사용.
4. 핵심 기법 1: window 정의를 VN 집합으로 하는 `U_VN`(일부 메시지 read-only, 갱신 생략)과 CN 집합으로 하는 `U_CN`(창 내 모든 관련 edge 갱신) 두 전략을 비교. 동일 window 크기에서 `U_VN`이 메시지 갱신 수가 적어 더 큰 window를 쓸 수 있음.
5. 핵심 기법 2: parity-check 기반 조기종료(ET)에서 창의 top-most CN 부분집합 `C_t`(target CNs, `|C_t|=(ms+1)*Ms*Q`)만 검사하는 것이 전체 CN `C_a`나 완전 CN `C_c`보다 계산량을 최대 60% 절감.
6. 복잡도는 메시지 갱신 횟수(`I_1`, exponent-matrix 기준)로 정규화하여 모든 구성(FBD/WD)이 동일 최대 `I_max`를 갖도록 최대 iteration 수 `Λ_max`를 역산(식 26).
7. 부수 트릭: 4-cycle이 있는 Tanner graph 실현은 시뮬레이션에서 배제, row-wise serial layered scheduling([12] 방식)으로 layer 단위 순차 갱신.
8. 최적화 절차 없음(GA/DE/NN 미사용) — 파라미터 스윕(W∈{12,16,20} 등)에 의한 실험적 비교.
9. 결과: `W=16`, `U_VN`, ET=`C_t` 조합에서 FBD 대비 평균 복호 복잡도(ANMU) 절반 수준, BLER `Pc=10^-2`에서 SNR gap 약 0.25dB.
10. 한계: HW 구현 미설계(저복잡도 지향 서술만), error floor가 FBD조차 상대적으로 높음(4-cycle 배제에도 불구), AWGN/Rayleigh 무선 채널 특화이며 NAND read-noise 채널 검증 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| Min-Sum 근사 CN 갱신 (SPA/MSA 혼합) | `decoder.cpp` `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | Prime ECC도 min-sum 기반이나 SC-LDPC의 window 슬라이딩 구조 자체는 대응 없음 (Prime ECC는 block QC-LDPC, 단일 고정 그래프) |
| Parity-check 기반 조기종료 (target-CN 부분집합 Ct) | `partial_CRC.cpp` `partial_crc_HW_T4()`, `full_CRC.cpp` | 개념적으로 유사(부분 검사로 조기종료·계산량 절감)하나 구현 방식은 SC-LDPC 창 이동과 무관, 직접 이식보다 아이디어 참고 수준 |
| Windowed decoder 메모리 절감(창 크기 제한) | 대응 없음 | Prime ECC는 block 코드로 전체 PCM 동시 처리, SC-LDPC의 sliding-window 메모리 구조와 대응 모듈 없음 |
| row-wise serial layered scheduling | `decoder.cpp` `LDPC_Decoder()` 이터레이션 루프 | Prime ECC의 iteration 루프도 layered/scheduled 갱신을 사용하나 SC-LDPC 특유의 창 이동 로직은 미대응 |

> 적용 가치: **중간** — SC-LDPC 자체 구조(창 슬라이딩)는 block QC-LDPC인 Prime ECC에 그대로 이식 불가하지만, "target CN 부분집합만으로 조기종료"라는 계산량 절감 아이디어는 partial CRC 설계와 비교 검토할 가치가 있음.

### D. JSON 블록

```json
{
  "id": "arxiv:2004.12973v1",
  "title": "Comparison of Windowed-Decoder Configurations for Spatially Coupled LDPC Codes Under Equal-Complexity Constraints",
  "year": 2020,
  "venue": "arXiv/Elsevier preprint",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "SC-LDPC",
  "code_rate": 0.48,
  "code_length": 51200,
  "soft_quant": "soft-4bit+",
  "key_contribution": "동일 최대복잡도 제약 하에서 SC-LDPC windowed decoder의 창(window) 크기·업데이트 전략(VN-centered vs CN-centered)·parity-check 기반 조기종료 조합을 비교해 FBD 대비 평균 복호 복잡도를 절반으로 줄이는 저오버헤드 구성을 도출",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "O",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "SC-LDPC(convolutional) 코드 전용 windowed decoding 기법으로 Prime ECC의 block QC-LDPC 구조에는 그대로 이식 불가하며, HW 미설계·순수 알고리즘/시뮬 비교 수준",
  "todo_check": "조기종료(ET)에 사용하는 target-CN 부분집합(Ct) 선택 아이디어가 Prime ECC의 partial CRC termination point 설계와 유사한지 추가 비교 필요"
}
```
