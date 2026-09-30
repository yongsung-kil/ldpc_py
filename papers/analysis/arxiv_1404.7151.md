### arxiv:1404.7151v1 - Simplified Variable-Scaled Min Sum LDPC decoder for irregular LDPC Codes (2014, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | decoder |
| 부호종류 | irregular |
| 부호rate | 0.25~0.75 |
| 부호length | 16200~64800 |
| 연판정 | soft-4bit+ |
| 핵심기여 | 반복 인덱스 기반 계단형(stair-step) 스케일링 팩터 `α(i)=1-2^(-⌈i/S⌉)`로 Min-Sum 성능을 SPA에 근접시키되 저장/연산은 shift-subtract만 요구 |
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
| 한계,주의 | DVB-T2 AWGN/256-QAM 채널·MATLAB 시뮬만 존재, HW 구현·NAND 채널 검증 없음 |
| 추가확인 | NAND 채널(비대칭 에러, RBER 특성)에서도 동일 계단형 스케줄이 유효한지 재검증 필요 |

> 총평: Scaled Min-Sum의 반복별 스케일링을 shift-subtract만으로 근사하는 저비용 기법으로, 기존 Prime ECC의 iteration별 LLR 테이블 구조에 대체/보완 아이디어로 참고 가치는 있으나 새로운 부호설계나 HW 이득은 없음.

### B. 알고리즘 요약

1. 대상 코드: DVB-T2 표준의 irregular eIRA LDPC 코드, 길이 N=16200(short)/64800(normal), rate R={0.25,0.5,0.75}(short), {0.5,0.75}(normal).
2. 문제: irregular LDPC에서 고정 스케일링 팩터(Scaled Min-Sum)는 variable node degree마다 message density가 달라 성능이 최적이 아니고, 기존 반복별 가변 스케일링([15])은 비선형 근사 계산과 반복마다 다른 스케일값 저장이 필요해 구현 복잡도가 큼.
3. 채널 모델: AWGN, 256-QAM 변조, 최대 반복 50회.
4. 핵심 기법: 체크노드 업데이트(horizontal step) `r_mn = sign(∏sign(q_nm))·α(i)·min|q_nm|`에서 스케일 `α(i) = 1 - 2^(-⌈i/S⌉)`를 반복 인덱스 i, 계단폭 S로 정의 (SVS Min-Sum).
5. 의미: [15]에서 관찰된 "스케일 팩터가 반복에 따라 지수적으로 증가해 최종 1에 수렴"하는 경향을 계단형(stair) 근사로 단순화 — 반복별 개별 값 저장 대신 파라미터 S 하나만 저장.
6. 확장 없음 (단일 기법, 2-D scaling[16]과 달리 CN/VN 이중 스케일 단계 불필요).
7. 구현 디테일: 스케일 곱셈을 우측 shift(`>>⌈i/S⌉`) 후 뺄셈으로 대체 — 곱셈기 없이 구현 가능. S와 shift 횟수만 레지스터에 저장.
8. 최적화 절차: rate/length별 최적 α(고정 Scaled MS용)와 최적 S(SVS용)를 전수 시뮬레이션으로 탐색(BER<1e-6 기준), Table I에 rate별 결과 제시(S=7~13).
9. 결과: SVS Min-Sum이 Min-Sum 대비 Eb/N0에서 0.41~0.85 dB 개선, Scaled Min-Sum(최적 α) 대비 0~0.43 dB 개선, SPA 대비 0.08~0.24 dB 열위(BER<1e-5 기준).
10. 한계: HW 설계·게이트카운트·throughput 언급 전혀 없음, MATLAB 시뮬로만 검증, DVB-T2/AWGN 채널 한정이며 NAND 채널 특성 미검증. 코드는 짧은 논문(4p)으로 다른 irregular 코드로의 확장은 future work로만 언급.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 반복별 계단형 스케일링 factor α(i) | `decoder.cpp` `CNU_Update_New_Mag()`, `ecc_data.h` `PARAM_LLR` | Min-Sum CN magnitude 계산에 곱하는 scaling을 iteration-index 기반 shift로 대체하는 아이디어, 기존 LLR 테이블(PARAM_LLR) 구조와 유사한 위치 |
| iteration별 LLR threshold 테이블 재사용/대체 가능성 | `decoder.cpp` `Get_VNU_Table_Idx()` | 이미 iteration 구간별 LLR 테이블을 두고 있어 개념적으로 중복 |
| shift-subtract 기반 저비용 곱셈 근사 | `decoder.cpp` `CNU_Update_New_Mag()` | HW 면적 절감 아이디어로 참고 가능하나 논문에 HW 검증 없음 |
```

적용 가치: 낮음 — Prime ECC는 이미 iteration별 LLR 테이블(적응형 LLR)을 보유하고 있어 본 논문의 계단형 스케일링은 개념적으로 중복되며, DVB-T2/AWGN 채널 시뮬만 존재해 NAND 채널 이식 시 추가 검증 부담이 큼.

### D. JSON 블록

```json
{
  "id": "arxiv:1404.7151v1",
  "title": "Simplified Variable-Scaled Min Sum LDPC decoder for irregular LDPC Codes",
  "year": 2014,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "decoder",
  "code_type": "irregular",
  "code_rate": "0.25~0.75",
  "code_length": "16200~64800",
  "soft_quant": "soft-4bit+",
  "key_contribution": "반복 인덱스 기반 계단형 스케일링 팩터 α(i)=1-2^(-ceil(i/S))로 Min-Sum을 SPA에 근접시키되 shift-subtract만 요구",
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
  "caveat": "DVB-T2 AWGN/256-QAM 채널·MATLAB 시뮬만 존재, HW 구현·NAND 채널 검증 없음",
  "todo_check": "NAND 채널(비대칭 에러, RBER 특성)에서도 동일 계단형 스케줄이 유효한지 재검증 필요"
}
```
