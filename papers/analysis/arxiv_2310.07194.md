### arxiv:2310.07194v2 - Boosting Learning for LDPC Codes to Improve the Error-Floor Performance (2023, NeurIPS 2023)

| 카테고리 | 값 |
|---|---|
| 이식성 | 상 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5~0.83 |
| 부호length | 552~1248 |
| 연판정 | soft-4bit+ |
| 핵심기여 | uncorrected word 부스팅 학습으로 NMS 디코더 error-floor 제거 (추가 HW 비용 없음) |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | O |
| latency | 개선 |
| 추천도 | 상 |
| 한계,주의 | binary QC-LDPC엔 맞으나 5-bit LLR·off-line 학습 전제, gate/throughput 실측 없음 |
| 추가확인 | 우리 5-bit LLR 양자화·min-sum 스케줄과 UCN/SCN 가중치 정합 여부, 저rate WiMAX급 코드 학습 이식성 |

> 총평: 학습된 UCN/SCN 가중치만 테이블화하면 min-sum 디코더에 무비용 이식 가능한 error-floor 제거 기법으로 우선 검토 가치 높음.

### B. 알고리즘 요약

1. 대상: WiMAX/802.11n/5G 표준 **binary QC-LDPC** (예: WiMAX `n=576, R=3/4, z=24`), AWGN 채널 + 5-bit 균일 양자화(`max 7.5, step 0.5`) NMS 디코더.
2. 문제: 저복잡도 양자화 MS/WMS 디코더는 waterfall 최적화 시 오히려 error-floor가 심해짐 → 초저 FER(ultra-reliable) 달성 곤란.
3. 모델: NMS 메시지 갱신 `m_v→c = w_v·m_ch + Σm_c'→v`, `m_c→v = w_c→v·Πsgn·min|·|`, 마지막 iter에 `m_o = m_ch + Σm_c'→v`.
4. 기법1 (부스팅 학습): 디코더를 base(iter 1~20) + post(21~50)로 분할. base는 waterfall용 수신어로, post는 base가 실패한 **uncorrected words**(주로 trapping/absorbing set 소오류)로만 학습.
5. 왜: error-floor 오류는 소수 오류비트에 집중 → post를 소오류 패턴 교정에 특화시키면 floor가 크게 낮아짐 (test FER 0.315배).
6. 기법2 (block-wise 학습 스케줄): 50 iter 심층망의 vanishing gradient 회피 위해 `Δ1=5`개 iter 블록씩 순차 학습하되 앞선 `Δ2=10` iter를 재학습(retraining)으로 local minimum 탈출.
7. 기법3 (UCN 가중치 공유): iter별 SCN 가중치 `w`와 UCN 가중치 `ŵ`를 분리(`{w(ℓ),w(ℓ),ŵ(ℓ)}`), 전체 가중치를 full-diversity 대비 2.6%(`3ℓ`)로 축소하며 성능 유지.
8. 학습: Adam(lr 0.001), 100 epoch, uncorrected word 50k train / FER loss `½(1−sgn(min m_o))` 사용.
9. 결과: 모든 코드에서 conventional WMS 대비 floor 시작 FER 2자릿수 이상 개선, floor 없이 FER 1e-7 도달, SOTA post-processing[22] 대비 iteration 1/3(50 vs 150).
10. 한계: HW 미설계(gate/throughput 무), AWGN·5-bit 양자화 전제, off-line 학습·uncorrected word 수집 비용(저 FER 영역) 존재.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| NMS CN min-sum 연산 (sgn·min) | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | 우리 min-sum 코어에 CN 가중치 곱만 추가하면 됨 |
| VN 갱신 + iter별 UCN/SCN 가중치 적용 | decoder.cpp `VN_Cal_HD()` 등, `ecc_data.h` `PARAM_LLR` / `Get_VNU_Table_Idx()` | 학습된 3ℓ 가중치를 iter별 테이블로 삽입, 우리 적응형 LLR 테이블 구조와 유사 |
| base/post 이중 스케줄(iter 구간별 가중치) | decoder.cpp `LDPC_Decoder()` 이터레이션 루프 | 루프 구간별로 가중치 세트 전환만 필요 |
| UCN 판별(check 만족 여부) | decoder.cpp `LDPC_Decoder()` (parity check 결과 재사용) | 디코더가 이미 CN 만족 여부를 알므로 무비용 |
| 학습 프레임워크(Adam, FER loss) | 대응 없음 | off-line GPU 학습, 코드베이스 외부 |

적용 가치: **높음** — 우리가 이미 쓰는 min-sum + iter별 LLR/가중치 테이블 구조에 학습된 UCN/SCN 가중치만 얹으면 추가 HW 없이 error-floor를 낮출 수 있어, 학습 파이프라인만 외부에서 확보하면 이식성이 매우 높다.

### D. JSON 블록

```json
{
  "id": "arxiv:2310.07194v2",
  "title": "Boosting Learning for LDPC Codes to Improve the Error-Floor Performance",
  "year": 2023,
  "venue": "NeurIPS 2023",
  "portability": "상",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": "0.5~0.83",
  "code_length": "552~1248",
  "soft_quant": "soft-4bit+",
  "key_contribution": "uncorrected word 부스팅 학습으로 NMS 디코더 error-floor 제거 (추가 HW 비용 없음)",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "O",
  "latency": "개선",
  "recommend": "상",
  "caveat": "binary QC-LDPC엔 맞으나 5-bit LLR·off-line 학습 전제, gate/throughput 실측 없음",
  "todo_check": "우리 5-bit LLR 양자화·min-sum 스케줄과 UCN/SCN 가중치 정합 여부, 저rate WiMAX급 코드 학습 이식성"
}
```
