### arxiv:2002.02696v1 - Protograph-Based Decoding of LDPC Codes with Hamming Weight Amplifiers (2020, arXiv preprint)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | protograph |
| 부호rate | 미상 |
| 부호length | 9602~82311 |
| 연판정 | 무관 |
| 핵심기여 | HWA(Hamming weight amplifier)로 얽힌 LDPC-암호 부호를 protograph 확장(state VN 추가)해 turbo-like BP/TMP 메시지 교환으로 디코딩하는 프레임워크 제안 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | waterfall |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | McEliece/LEDAcrypt 암호시스템(post-quantum crypto)용 LDPC-HWA/QC-MDPC 부호가 대상이며, 일반 NAND 채널이 아닌 암호학적 에러패턴(uniform weight error injection)을 가정 |
| 추가확인 | protograph 확장 기법(state VN을 이용한 outer/inner turbo-like 메시지 교환)이 순수 통신용 QC-LDPC의 error-floor 개선에도 적용 가능한지 확인 필요 |

> 총평: 암호시스템(LEDAcrypt) 특화 LDPC-HWA 디코딩 논문이나, protograph 기반 state-VN 확장과 TMP(ternary message passing) 저복잡도 디코딩 기법 자체는 NAND LDPC의 error-floor/복잡도 개선에 간접적으로 참고 가치가 있음.

### B. 알고리즘 요약 (10줄 내외)

1. 시스템: McEliece류 code-based 암호시스템에서 QC-LDPC 부호의 파리티체크행렬 `H`에 column scrambling(HWA) 행렬 `Q`를 곱해 공개키 `H' = HQ`를 만드는 LEDAcrypt 구조(부호길이 `n=N0·p`, 코드 앙상블 예: 9602~82311).
2. 문제: HWA로 인해 암호문의 에러 가중치가 `wht(e') ≈ e·d_Q`로 증폭되어, 단순히 `H'` 기반 LDPC 디코더로 복호하면 정정성능이 저하됨. 반대로 `H`를 QC-MDPC로 보고 복호하면 정정성능은 좋지만 밀도가 높아 계산복잡도가 큼.
3. 핵심 가정: 에러 `e`는 균일 가중치(uniform Hamming weight)로 무작위 주입되는 암호학적 채널 모델(통신 채널의 AWGN/BSC와 다름).
4. 핵심 기법: `H`, `Q`를 각각 inner LDPC 부호와 outer rate-1 HWA 부호로 보고, punctured(state) VN을 도입해 확장 파리티체크행렬 `H_ext = [[Q, I],[0, H]]`(식 (8))로 하나의 protograph를 구성, turbo-like하게 두 디코더 간 메시지를 교환.
5. 핵심 식: `H_ext`의 base matrix `B_ext = [[B_Q, I],[0, B_H]]`(식 (9))가 protograph 그래프 구조를 정의하며, 이를 통해 outer(HWA)-inner(LDPC) 정보 교환이 가능해짐 (기존엔 `H'=HQ`로 합쳐 단일 디코더만 사용).
6. 확장: 두 종류 MP 디코더 적용 - Scaled Sum-Product Algorithm(SPA, CN 감쇠 적용 BP)과 Ternary Message Passing(TMP, 메시지 알파벳 `{-1,0,1}`, VN에서 채널/CN 메시지 가중합 후 양자화).
7. 부수 트릭: TMP의 CN/VN 가중치는 density evolution(DE)으로 사전 최적화, quantized DE로 protograph 앙상블의 점근적 복호 임계값(`δ_SPA`, `δ_TMP`) 계산.
8. 최적화 절차: quantized DE(BP)와 protograph DE(TMP, [19] 방법)로 코드 앙상블 설계 및 임계값 도출, base matrix `B_H·B_Q = B_MDPC`가 되도록 파라미터 설정해 기존 QC-MDPC와 공정 비교.
9. 결과: LEDAcrypt NIST 파라미터(128/192/256-bit)에서 protograph 방식이 basic LDPC 디코딩 대비 정정능력 향상, MDPC 디코딩과 유사한 성능을 훨씬 낮은 복잡도로 달성 (예: TMP 12분 vs MDPC 5시간50분, 2·10^4회 반복 시뮬레이션 기준).
10. 한계: HW 미설계(순수 시뮬레이션/DE 이론), 암호시스템(McEliece/LEDAcrypt) 특화 에러모델이라 NAND 채널 특성과 다름, iteration 수는 100으로 고정(감소 효과 언급 없음).

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 디코딩 알고리즘 전체 (protograph turbo-like MP) | `decoder.cpp` `LDPC_Decoder()`, `C2V_Cal()` | outer/inner 두 디코더 간 메시지 교환 구조는 Prime ECC의 단일 QC-LDPC 이터레이션 루프와 다른 그래프 구조라 직접 이식은 어려움, 개념적 참고만 가능 |
| Scaled Sum-Product (CN 감쇠) | `decoder.cpp` `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | Min-Sum 대신 감쇠형 SPA를 사용해 직접 대응 낮음 |
| Ternary Message Passing (TMP, 3-level 양자화) | `decoder.cpp` `VN_Cal_HD()` 등 (HD/2SD/3SD) | 메시지를 3-level({-1,0,1})로 제한하는 저복잡도 디코딩 아이디어는 hard-1bit/soft-2~3bit 양자화 설계와 개념적으로 유사 |
| H-matrix/protograph 구조 (state VN 확장) | `ecc_top.cpp` `Load_PCM()` | LEDAcrypt 전용 HWA 확장 구조로 Prime ECC의 고정 QC-LDPC H-matrix와 직접 대응 없음 |
| 채널/에러 모델 (암호학적 uniform weight error) | `channel.cpp` `Set_R_Offset()`, `Set_LLR_Th()` | AWGN/RBER 기반 NAND 채널과 다른 모델이라 대응 없음 |

> 적용 가치: 중간 - protograph 기반 state-VN turbo-like 디코딩과 TMP 저복잡도 양자화 아이디어는 개념적으로 참고 가능하나, 암호시스템 특화 구조(HWA)와 에러모델이라 Prime ECC 코드베이스에 직접 이식하기엔 부호설계 레이어부터 재작업이 필요.

### D. JSON 블록

```json
{
  "id": "arxiv:2002.02696v1",
  "title": "Protograph-Based Decoding of LDPC Codes with Hamming Weight Amplifiers",
  "year": 2020,
  "venue": "arXiv preprint",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "protograph",
  "code_rate": null,
  "code_length": "9602~82311",
  "soft_quant": "무관",
  "key_contribution": "HWA로 얽힌 LDPC-암호 부호를 protograph 확장(state VN 추가)해 turbo-like BP/TMP 메시지 교환으로 디코딩하는 프레임워크 제안",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "waterfall",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "McEliece/LEDAcrypt 암호시스템(post-quantum crypto)용 LDPC-HWA/QC-MDPC 부호가 대상이며, 일반 NAND 채널이 아닌 암호학적 에러패턴(uniform weight error injection)을 가정",
  "todo_check": "protograph 확장 기법(state VN을 이용한 outer/inner turbo-like 메시지 교환)이 순수 통신용 QC-LDPC의 error-floor 개선에도 적용 가능한지 확인 필요"
}
```
