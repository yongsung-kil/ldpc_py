### arxiv:1510.04589v1 - A Fully-Unrolled LDPC Decoder Based on Quantized Message Passing (2015, arXiv preprint (cs.IT))

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | regular |
| 부호rate | 0.8125 |
| 부호length | 2048 |
| 연판정 | soft-2~3bit |
| 핵심기여 | 표준 min-sum VN 업데이트를 상호정보량 최대화 기반 LUT 트리로 대체해 3비트 메시지로 5비트 min-sum과 동등한 FER 성능 달성 |
| HW설계 | O |
| 검증수준 | ASIC합성 |
| 복잡도 | 33.79mm²@90nm |
| 병렬화 | 완전병렬 |
| Throughput | 1665Gbps |
| 메모리라우팅 | 언급 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | 개선 |
| 추천도 | 중 |
| 한계,주의 | 부호(IEEE 802.3an (6,32)-regular, N=2048)당 iteration별 LUT를 fully-unrolled 구조에 하드코딩해야 하므로 QC-LDPC의 부분/완전병렬 재사용 구조에는 그대로 적용하기 어려움 |
| 추가확인 | Prime ECC의 z_sb=32 QC-LDPC lifting 구조에서 dv=17 VN에 대한 LUT 트리 크기/합성 가능성 재검토 필요 |

> 총평: min-sum 대체용 정보이론 기반 LUT-VN 설계는 이미 min-sum을 보유한 Prime ECC 대비 성능 동등·비트폭 절감 관점에서 참고 가치가 있으나, fully-unrolled 아키텍처 전제와 iteration별 개별 LUT 재설계 필요성 때문에 이식 난이도는 중간 수준.

### B. 알고리즘 요약 (10줄 내외)

1. 대상은 (dv, dc)-regular LDPC 부호이며 실험에서는 IEEE 802.3an 10GbE 표준의 (6,32)-regular, rate `R=13/16`, `N=2048` 부호를 사용, BI-AWGN 채널 가정.
2. 문제의식은 기존 min-sum이 4~7비트 양자화 메시지를 필요로 하는데, 더 낮은 비트폭에서는 error-floor 영역 성능이 크게 저하된다는 점이다.
3. 핵심 기법은 VN 업데이트 규칙 `Φv`만 LUT로 교체하고 CN 업데이트는 표준 min-sum(`Φc(µ)=sign(µ)·min|µ|`)을 그대로 유지하는 하이브리드 방식이다 - 대칭 채널 특성상 CN 출력 부호가 메시지 label에서 직접 추론 가능해 LUT-CN이 불필요.
4. VN LUT는 CN→VN 메시지 분포 `p(m|x)`를 iteration별로 갱신하며 `Φv_MI = argmax_Q I(Q(L,m̄); x)`로 상호정보량을 국소 최대화하는 매핑을 설계(density-evolution 유사 반복 계산, 식 (8)~(13)).
5. `Φv`의 입력 차원이 커 직접 계산이 어려우므로 트리 구조 LUT(부분 매핑 계층)를 구성해 각 스테이지가 입력 일부만 처리하도록 근사한다.
6. HW 구현은 fully-unrolled·fully-parallel 아키텍처(선행 연구[9] 기반)로, CN/VN/DN 3종 스테이지가 iteration마다 별도 인스턴스화된 시스톨릭 파이프라인이며 클록마다 새 코드워드 출력.
7. 양자화 파라미터는 `Qch=4bit`(채널 LLR), `Qmsg=3bit`(내부 메시지)로 LUT 기반 디코더가 5bit/5bit 표준 min-sum과 동등 FER 달성(design SNR 4.5dB, I=5 iteration).
8. 별도 신경망/GA 없이 density-evolution 유사 반복 최적화(SNR별 오프라인 사전설계)로 iteration별 LUT를 생성.
9. 결과: TSMC 90nm 합성에서 LUT 기반 디코더가 adder 기반 min-sum 대비 면적 8% 감소, 동작주파수 64% 향상, throughput 1665Gbps(vs 1014Gbps), area efficiency 73% 향상, 배선 약 40% 감소.
10. 한계: fully-unrolled 구조 전제(면적 매우 큼, N·I개 VN/CN 인스턴스화)이고, LUT는 특정 부호·iteration·design SNR에 종속되어 재설계 필요, placement&routing 이후 실측치는 미제공(합성 결과만).

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| min-sum VN 업데이트를 상호정보량 LUT로 대체 | `decoder.cpp` `VN_Cal_HD()` 등 (HD/2SD/3SD), `decoder.h` `Get_VNU_*` | 현재 magnitude 양자화 테이블 기반 VN 처리를 대체할 수 있는 정보이론적 LUT 설계 아이디어와 직접 연관 |
| iteration별 LLR/메시지 재현 방식 | `ecc_data.h` `PARAM_LLR`, `decoder.cpp` `Get_VNU_Table_Idx()` | 이미 iteration 구간별 threshold 테이블을 두고 있어 유사 구조, LUT 설계 알고리즘 자체를 참고할 수 있음 |
| CN min-sum 유지 (부호 label 기반 sign 추론) | `decoder.cpp` `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | CN은 그대로 min-sum이라 변경 불필요, 논문의 하이브리드 접근과 구조 일치 |
| fully-unrolled 파이프라인 HW 아키텍처 | 대응 없음 | Prime ECC는 z=32 병렬 iterative 구조로 fully-unrolled(iteration별 별도 인스턴스)와는 근본적으로 다른 HW 형태 |
```

> 적용 가치: **중간** - min-sum VN을 정보이론 기반 LUT로 교체해 저비트폭에서 성능 유지하는 아이디어는 Prime ECC의 soft-2~3bit LLR 설계에 직접 참고 가능하나, fully-unrolled HW 전제와 부호별 재설계 필요성이 이식 장벽.

### D. JSON 블록 (DB 적재용)

```json
{
  "id": "arxiv:1510.04589v1",
  "title": "A Fully-Unrolled LDPC Decoder Based on Quantized Message Passing",
  "year": 2015,
  "venue": "arXiv preprint (cs.IT)",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "regular",
  "code_rate": 0.8125,
  "code_length": 2048,
  "soft_quant": "soft-2~3bit",
  "key_contribution": "표준 min-sum VN 업데이트를 상호정보량 최대화 기반 LUT 트리로 대체해 3비트 메시지로 5비트 min-sum과 동등한 FER 성능 달성",
  "hw_designed": "O",
  "verification": "ASIC합성",
  "complexity": "33.79mm²@90nm",
  "parallelism": "완전병렬",
  "throughput_gbps": 1665,
  "mem_routing": "언급",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "개선",
  "recommend": "중",
  "caveat": "부호(IEEE 802.3an (6,32)-regular, N=2048)당 iteration별 LUT를 fully-unrolled 구조에 하드코딩해야 하므로 QC-LDPC의 부분/완전병렬 재사용 구조에는 그대로 적용하기 어려움",
  "todo_check": "Prime ECC의 z_sb=32 QC-LDPC lifting 구조에서 dv=17 VN에 대한 LUT 트리 크기/합성 가능성 재검토 필요"
}
```
