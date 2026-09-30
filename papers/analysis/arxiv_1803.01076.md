### arxiv:1803.01076v2 - Low-Complexity Concatenated LDPC-Staircase Codes (2018, J. Lightwave Technology / arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 0.8~0.85 |
| 부호length | 6000~30000 |
| 연판정 | soft-4bit+ |
| 핵심기여 | inner LDPC degree분포를 data-flow 최소화로 최적화(일부 bit는 uncoded로 방치)해 복잡도 최대 71% 절감 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | OTN(광통신) 타깃·outer staircase 연접 전제, AWGN+float SPA 시뮬만, HW 미합성, inner code가 BER를 outer threshold까지만 낮추는 구조 |
| 추가확인 | staircase outer code 없이 NAND 단독 사용 시 error-floor·정정능력, uncoded bit 방치 전략의 NAND RBER 적합성 |

> 총평: 광통신용 inner LDPC+outer staircase 연접 FEC의 복잡도 최적 설계로, QC/layered decoding은 일반 binary LDPC에 참고되나 outer staircase 연접·soft-4bit+·OTN 전제라 Prime ECC 단독 NAND ECC 이식성은 하.

### B. 알고리즘 요약

1. 구조: inner soft-decision LDPC + outer hard-decision staircase code 연접 FEC(OTN용), QPSK/AWGN 채널, 목표 BER `<10⁻¹⁵`.
2. 문제: soft-decision 디코더는 hard-decision 대비 전력·복잡도가 한 자릿수 크므로, 성능 유지하며 inner 디코더 data-flow를 줄여야 함.
3. 핵심 아이디어: inner LDPC 앙상블에 degree-0(uncoded) 및 degree-1 variable node를 허용 - degree-0은 outer code만으로 보호돼 inner 복잡도 0.
4. 복잡도 척도 `ηi = (1-Rin)(dc-ν)I / Rin` (data-flow 기반, `ν=dcλ1`은 CN당 평균 degree-1 VN 수)를 최소화 목표로 설정.
5. EXIT chart 분석: 오류확률 EXIT 함수 `pout=fΛ(pin)`을 elementary EXIT `fi(pin)`의 λ 가중합으로 구성, ν 고려해 Monte-Carlo로 사전계산.
6. 요구 iteration `I ≈ ∫ dp/(p·log(p/fΛ(p)))` 근사식으로, 목적함수를 `(L0, Λ)`에 대한 볼록 최적화로 정식화.
7. 최적화: `dc, ν, L0` 3중 루프 + 각 고정 시 SQP(sequential quadratic programming)로 inner 앙상블 결정, staircase code 표를 순회해 최소 복잡도 쌍 선택.
8. inner/outer 사이 diagonal interleaver로 상관 오류 완화(packing ratio m≥4에서 손실 무시 가능).
9. 결과: [6] 대비 15%OH에서 복잡도 71% 절감·Shannon limit 0.23dB 근접; QC(길이 6000~30000)+layered schedule로 flooding 대비 복잡도 추가 50% 절감.
10. 한계: OTN 광통신 타깃, AWGN+float SPA(및 offset-MS) 시뮬만, HW 미합성, inner code는 BER를 outer threshold까지만 낮추는 연접 전제.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| inner LDPC degree분포 최적화(EXIT/data-flow) | ecc_top.cpp Load_PCM() (부호구조) | inner LDPC 부호설계이나 QC-LDPC H-matrix 고정된 Prime ECC와 재검증 부담, staircase 연접 전제 |
| layered message-passing 스케줄 | decoder.cpp LDPC_Decoder() 이터레이션 루프 | Prime ECC는 flooding+Dual-Update 계열, layered 도입 시 복잡도 절감 참고 가능 |
| offset-MS / SPA inner 복호 | decoder.cpp CNU_Update_New_Mag(), C2V_Cal() | Prime ECC는 min-sum 보유, SPA/offset-MS는 중복 또는 float |
| uncoded(degree-0) bit 전략 | 대응 없음 | outer staircase 연접이 있어야 성립, Prime ECC 단독 구조에 대응 없음 |
```

적용 가치: **낮음** — inner LDPC 복잡도 최적화·QC·layered decoding은 개념적으로 참고되나, 전체가 outer staircase 연접과 OTN soft-4bit+ 전제 위에 성립해 Prime ECC 단독 NAND binary QC-LDPC에 떼어 쓸 층이 좁다.

### D. JSON 블록

```json
{
  "id": "arxiv:1803.01076v2",
  "title": "Low-Complexity Concatenated LDPC-Staircase Codes",
  "year": 2018,
  "venue": "J. Lightwave Technology / arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "6000~30000",
  "soft_quant": "soft-4bit+",
  "key_contribution": "inner LDPC degree분포를 data-flow 최소화로 최적화(일부 bit는 uncoded로 방치)해 복잡도 최대 71% 절감",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "하",
  "caveat": "OTN(광통신) 타깃·outer staircase 연접 전제, AWGN+float SPA 시뮬만, HW 미합성, inner code가 BER를 outer threshold까지만 낮추는 구조",
  "todo_check": "staircase outer code 없이 NAND 단독 사용 시 error-floor·정정능력, uncoded bit 방치 전략의 NAND RBER 적합성"
}
```
