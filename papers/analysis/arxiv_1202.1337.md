### arxiv:1202.1337v2 - Enhancing the Error Correction of Finite Alphabet Iterative Decoders via Adaptive Decimation (2012, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 0.753~0.87 |
| 부호length | 155~732 |
| 연판정 | soft-2~3bit |
| 핵심기여 | 7-level(3-bit) FAID에 적응형 decimation(보수적→공격적 규칙 순차 적용)을 결합해 stopping set 기반 오류패턴에 대한 보증 정정능력과 error-floor slope를 개선 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | 악화 |
| 추천도 | 중 |
| 한계,주의 | BSC(hard 채널) 가정이며 column-weight 3(dv=3) 코드에 한정, decimation 라운드마다 메시지 리셋+재반복이라 반복수/지연 오히려 증가 |
| 추가확인 | Φdv/decimation rule β 설계가 코드별 stopping set 구조 분석에 의존(예제 코드 전용 표 II/III)이라 Prime ECC 고정 H-matrix에서 별도 설계 필요 |

> 총평: BSC 환경에서 min-sum 유사 유한 알파벳(3-bit) 디코더에 stopping-set 분석 기반 적응형 decimation을 추가해 error-floor slope를 크게 개선하지만, 코드별 맞춤 설계와 반복 재시작 구조로 인해 latency 증가와 이식 난이도가 있음.

### B. 알고리즘 요약

1. 대상 코드는 column-weight `dv=3`, BSC(binary symmetric channel) 상의 (155,64) Tanner code와 rate-0.753 (732,551) structured code(`dmin=12`)이며 3-bit(7-level) 메시지를 전달하는 FAID(Finite Alphabet Iterative Decoder).
2. 문제는 기존 FAID/decimation-enhanced FAID(DFAID)가 error-floor에서 BP를 능가하지만 stopping set에 의한 실패로 보증 정정능력이 제한된다는 점.
3. 채널 모델은 BSC(cross-over probability `α`)이며 메시지는 `M={0,±L1,±L2,±L3}` 유한 알파벳(식 없음, 표 I 형태 LUT)으로 제한.
4. 핵심 기법은 두 개의 decimation 규칙 집합 `B={β(1),β(2)}`를 이용한 adaptive decimation: `β(1)`은 3회 반복 후 1회만 적용, `β(2)[j]`는 보수적(`j=1`)에서 공격적(`j=Nβ`) 순서로 점점 완화하며 2회 반복마다 적용, 매 라운드 메시지를 0으로 리셋 후 재시작.
5. 핵심 관찰(Theorem 1/Corollary 1)은 `β(2)j=1`이고 오류노드가 decimate 안 되면, 잔여 그래프가 stopping set이 됨 - 즉 실패 원인이 stopping set과 직결됨을 규명.
6. 확장 기법은 서로 다른 두 갱신함수 `Φ_v^d`(decimation 진행 중), `Φ_v^r`(decimation 후 잔여 노드 복호, 기존 7-level FAID의 Φv 재사용)를 분리 운용.
7. 구현 디테일은 decimation된 노드가 항상 최댓값(±L3)을 이웃에 전송하도록 고정, Alg.1의 8단계 절차(3회 반복→β(1)→2회 반복→β(2)[j]→수렴 확인→β 강도 증가 반복)로 명시.
8. 규칙 설계는 학습이 아닌 코드별 stopping set 분석(오류패턴을 stopping set 내부로 한정)으로 `Ξ(1)`, `Ξ(2)=Λ∪Γ`(Γ는 코드 종속, 표 II/III)를 수작업 구성.
9. 결과: (155,64) Tanner code에서 7-level ADFAID는 모든 6-error 패턴을 정정(7-level FAID는 5-error까지, BP는 5-error 실패), (732,551) 고rate 코드에서도 error-floor slope 대폭 개선.
10. 한계: BSC(hard-1bit 등가) 전용 분석·시뮬뿐이며 HW 설계·정량적 gate/throughput 없음, decimation 라운드마다 전체 재반복이라 실제 latency는 증가 방향.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 유한 알파벳(3-bit) VN 갱신 함수 Φv (LUT 기반) | `decoder.cpp` `VN_Cal_HD()` 등 (HD/2SD/3SD), `decoder.h` `Get_VNU_*` | 3-bit 메시지 전달은 Prime ECC의 soft-2~3bit LLR 양자화 레이어와 형태적으로 유사하나 min-sum이 아닌 LUT 기반이라 전면 재설계 필요 |
| Adaptive decimation (반복 중 노드 고정 + 메시지 리셋 재시작) | `decoder.cpp` `LDPC_Decoder()` 이터레이션 루프 | 이터레이션 루프에 decimation 상태·리셋 로직 추가 가능하나 기존 조기종료(Partial/Full CRC)와는 다른 메커니즘 |
| CN 갱신 (min 기반 Φc) | `decoder.cpp` `CNU_Update_New_Mag()` | Φc가 min-sum과 유사한 형태(`sgn·min`)라 개념적으로 대응되나 FAID 고유 LUT 규칙 자체는 미보유 |
| stopping-set 기반 오류 분석/규칙 설계 | 대응 없음 | Prime ECC는 코드별 stopping-set 분석 도구 없음, H-matrix 종속 수작업 설계 요구 |

> 적용 가치: 낮음. FAID 자체는 min-sum과 유사한 저복잡도 CN 연산을 쓰지만, adaptive decimation은 코드별 stopping-set 분석에 기반한 수작업 규칙 설계와 반복 재시작 구조가 필요해 Prime ECC 고정 QC-LDPC 구조에 이식하려면 높은 재설계 비용이 든다. 다만 error-floor 개선이라는 목표와 3-bit 저정밀 메시지라는 점은 NAND ECC 관심사와 방향은 일치.

### D. JSON 블록

```json
{
  "id": "arxiv:1202.1337v2",
  "title": "Enhancing the Error Correction of Finite Alphabet Iterative Decoders via Adaptive Decimation",
  "year": 2012,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "155~732",
  "soft_quant": "soft-2~3bit",
  "key_contribution": "7-level(3-bit) FAID에 적응형 decimation(보수적→공격적 규칙 순차 적용)을 결합해 stopping set 기반 오류패턴에 대한 보증 정정능력과 error-floor slope를 개선",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "악화",
  "recommend": "중",
  "caveat": "BSC(hard 채널) 가정이며 column-weight 3(dv=3) 코드에 한정, decimation 라운드마다 메시지 리셋+재반복이라 반복수/지연 오히려 증가",
  "todo_check": "Φdv/decimation rule β 설계가 코드별 stopping set 구조 분석에 의존(예제 코드 전용 표 II/III)이라 Prime ECC 고정 H-matrix에서 별도 설계 필요"
}
```
