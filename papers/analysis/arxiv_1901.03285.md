### arxiv:1901.03285v1 - Protograph-Based LDPC Code Design for Probabilistic Shaping with On-Off Keying (2019, arXiv/cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | both |
| 부호종류 | protograph |
| 부호rate | 0.5~0.75 |
| 부호length | 64800 |
| 연판정 | soft-4bit+ |
| 핵심기여 | OOK 확률적 성형(time-sharing)에 맞춘 protograph LDPC 부호를 P-EXIT+DE로 설계, 균일신호 대비 1.1dB 이득 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | OOK 확률적성형(FSO/심우주 광통신) 특화 부호설계로 NAND read/RBER와 무관, 성형 채널에 부호가 결합되어 이식 어려움 |
| 추가확인 | 없음 (성형 결합 protograph 설계는 Prime ECC 고정 QC-LDPC와 정합 불가) |

> 총평: OOK 확률적 성형 광통신 채널에 결합된 protograph 부호설계로 NAND binary QC-LDPC ECC와 도메인이 달라 이식 가치 낮음.

### B. 알고리즘 요약

1. 시스템: 평균전력 제약 AWGN + OOK 변조, FSO/심우주 광통신 대상. protograph LDPC, block length `n=64800`, 부호율 `RC ∈ {0.5, 0.67, 0.75}`.
2. 문제: OOK는 균일분포 신호가 저SNR에서 용량 대비 큰 손실. PPM+BMD도 1.7dB 손실. 성형(shaping)과 FEC 결합이 어려움(PAS는 비대칭 OOK에 부적용).
3. 채널/모델: `Y = X + N`, `X ∈ {0, A}`, SNR `Es/N0 = 1/(2σ²)`. 정보비트만 비균일(성형), parity는 근사 균일.
4. 핵심 기법: Time-Sharing(TS) 성형 — 체계적 부호의 정보 OOK 심볼 `RC·n`개는 비균일 분포(CCDM으로 성형), parity `(1-RC)·n`개는 균일 전송.
5. 핵심 식: 전송률 `RTX = H(XS)·RC` (식4), soft-demap LLR = 채널LLR + prior `log(PX(A)/PX(0))` (식6). prior가 consistency 조건 깨뜨림.
6. 확장(케이스2): 정보/parity 심볼 진폭 `AS≠AU` 허용해 추가 자유도로 성형 이득 증대.
7. 구현 디테일: prior가 P-EXIT consistency 위반 → surrogate AWGN 채널(균일입력, `H(X̃|Ỹ)=H(XS|YS)`)로 등가 변환해 임계값 분석.
8. 최적화: Differential Evolution(DE) 유전 알고리즘으로 protograph base matrix 탐색(최대 degree-2 VN 제한, 최대 엔트리 4).
9. 결과: `RTX=0.25 bpcu`에서 균일 OOK+DVB-S2 대비 케이스2가 1.1dB 이득. DVB-S2는 error floor 보임, 설계 부호는 waterfall 개선+floor 제거. 임계값 케이스1 -3.82dB / 케이스2 -4.49dB.
10. 한계: 시뮬(finite-length + asymptotic threshold)만, HW 미설계, OOK 성형 광통신 채널 특화, 부호가 성형 신호분포에 결합됨.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| protograph 부호설계 / DE 탐색 | `ecc_top.cpp` `Load_PCM()` (H-matrix 로드만) | Prime ECC는 고정 QC-LDPC(base+shift), protograph copy-permute·DE 설계 없음 → 이식 어려움 |
| OOK 성형 채널 / prior LLR | `channel.cpp` `Set_LLR_Th()` (LLR만) | Prime ECC 채널은 AWGN/RBER/fixed-error, OOK 확률적 성형 아님 |
| P-EXIT / surrogate 임계값 분석 | 대응 없음 | Prime ECC에 EXIT/threshold 설계 도구 없음 |
| BP 복호 | `decoder.cpp` `LDPC_Decoder()` | 일반 BP는 대응되나 부호가 성형 채널 특화라 그대로는 무의미 |

적용 가치: **낮음** — OOK 확률적 성형(FSO/심우주 광통신)에 결합된 protograph 부호설계로, NAND read/RBER 기반 고정 binary QC-LDPC ECC와 채널·부호구조가 달라 떼어 쓸 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1901.03285v1",
  "title": "Protograph-Based LDPC Code Design for Probabilistic Shaping with On-Off Keying",
  "year": 2019,
  "venue": "arXiv/cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "both",
  "code_type": "protograph",
  "code_rate": "0.5~0.75",
  "code_length": "64800",
  "soft_quant": "soft-4bit+",
  "key_contribution": "OOK 확률적 성형(time-sharing)에 맞춘 protograph LDPC 부호를 P-EXIT+DE로 설계, 균일신호 대비 1.1dB 이득",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "OOK 확률적성형(FSO/심우주 광통신) 특화 부호설계로 NAND read/RBER와 무관, 성형 채널에 부호가 결합되어 이식 어려움",
  "todo_check": "없음 (성형 결합 protograph 설계는 Prime ECC 고정 QC-LDPC와 정합 불가)"
}
```
