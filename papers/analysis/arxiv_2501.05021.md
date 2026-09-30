### arxiv:2501.05021v1 - Enhanced Min-Sum Decoding of Quantum Codes Using Previous Iteration Dynamics (2025, arXiv/quant-ph)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | 기타 |
| 부호rate | 미상 |
| 부호length | 72~288 |
| 연판정 | hard-1bit |
| 핵심기여 | 두 블록 CSS QLDPC의 대칭 stabilizer 진동을 이전 iteration 메시지 합산으로 감쇠시키는 비대칭 min-sum(MS-PI) 규칙 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 완전병렬 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | 개선 |
| 추천도 | 하 |
| 한계,주의 | 양자 degeneracy·(w,0) 대칭 stabilizer·두 블록 CSS 구조 전제, 고전 NAND binary LDPC엔 해당 병목 부재 |
| 추가확인 | self-corrected MS(부호변화 시 이전 메시지 합산) 아이디어가 고전 trapping-set에도 유효한지 별도 검증 |

> 총평: 양자 CSS 부호의 degeneracy로 인한 min-sum 메시지 진동을 이전 iteration 부호변화 감지로 감쇠하는 디코더. syndrome-based·양자 특화 구조라 NAND binary LDPC 직접 이식은 하, 다만 sign-flip 시 과거 메시지 합산 아이디어는 참고 가치.

### B. 알고리즘 요약

1. 시스템: 두 블록 CSS QLDPC(bivariate bicycle, BB codes) `[[72,12,6]]`/`[[144,12,12]]`/`[[288,12,18]]`, 두 순환행렬 A·B로 `HX=[A,B], HZ=[Bᵀ,Aᵀ]`, X/Z 오류를 독립 BSC로 분리 복호.
2. 문제: 양자 degeneracy - 최소거리≫stabilizer 무게일 때 대칭 stabilizer의 `(w,0)` trapping set에 `w/2` 오류가 걸리면 표준 min-sum이 수렴 실패.
3. 모델: syndrome-based 복호, 사전 LLR `λ=log((1-α)/α)`, isolation assumption(외부 노드 수렴 가정)으로 check를 사실상 degree-2로 단순화.
4. 핵심 규명(Thm1): computation tree 분석으로 대칭 stabilizer 내 V2C 메시지가 매 iteration 진동함을 증명 - 고유값 `δ=±i√(w/2-1)`이 진동, `δ4=1-w/2`가 발산 유발(식10).
5. 핵심 기법 MS-PI: 두 블록에 서로 다른 VN 업데이트 규칙 적용 - 한 블록은 표준 min-sum(식2), 다른 블록은 부호 변화 감지 시 현재+이전 메시지 합산.
6. 규칙(식12): `sgn(ν)=sgn(ν^(ℓ-1))`이면 `ν`, 아니면 `ν+ν^(ℓ-1)`. 진동 메시지의 진폭을 줄여 비대칭 유발 → tie 파괴로 수렴.
7. 구현: 부수 damping 지시함수 `χ`(식14)로 진동 감쇠, 4개 규칙 조합 diversity decoding으로 추가 이득 가능.
8. 복잡도: 블록길이 n에 선형(post-processing/serial scheduling 불필요), 완전 병렬 스케줄로 동작.
9. 결과: nMS-PI가 nMS 크게 상회, BP-OSD-0을 50 iteration만에 소폭 상회. α=0.02에서 `[[288,12,18]]` logical error rate 3자릿수 감소, BB code family threshold 7.8%(L=100→8%, L=200→8.1%).
10. 한계: HW 미설계, 시뮬만. 양자 CSS·degeneracy·대칭 stabilizer 전제로 고전 부호엔 해당 병목 없음, circuit-level noise 미검증.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| min-sum CN 업데이트(식3, min+sign) | decoder.cpp `CNU_Update_New_Mag()`, `C2V_Cal_New_Sgn()` | 동일 min-sum 연산, 신규성 없음 |
| VN 업데이트 + 이전 메시지 합산 규칙(식12) | decoder.cpp `VN_Cal_HD()`, `Get_VNU_*` | VN 규칙 수정 지점 대응, 다만 이전 iteration 메시지 저장 버퍼 신설 필요 |
| 두 블록 비대칭 규칙(A/B 구분) | 대응 없음 | 두 블록 CSS 전용, Prime ECC의 QC base matrix엔 A/B 블록 개념 부재 |
| syndrome-based 복호(양자 QLDPC) | 대응 없음 | Prime ECC는 codeword 기반 복호(NAND read LLR), syndrome 입력 아님 |
| degeneracy/(w,0) trapping set 진동 | 대응 없음 | 양자 degeneracy 고유 병목, 고전 binary LDPC에 미대응 |

적용 가치: 낮음 - 핵심 기여가 양자 degeneracy·두 블록 CSS·syndrome 복호에 특화되어 NAND binary QC-LDPC엔 해당 병목 자체가 없음. 다만 "sign-flip 시 이전 iteration 메시지 합산"(self-corrected MS 계열)이라는 진동 감쇠 아이디어는 고전 trapping-set/error-floor 대책으로 재검토할 참고 가치는 있음.

### D. JSON 블록

```json
{
  "id": "arxiv:2501.05021v1",
  "title": "Enhanced Min-Sum Decoding of Quantum Codes Using Previous Iteration Dynamics",
  "year": 2025,
  "venue": "arXiv/quant-ph",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "72~288",
  "soft_quant": "hard-1bit",
  "key_contribution": "두 블록 CSS QLDPC의 대칭 stabilizer 진동을 이전 iteration 메시지 합산으로 감쇠시키는 비대칭 min-sum(MS-PI) 규칙",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "완전병렬",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "개선",
  "recommend": "하",
  "caveat": "양자 degeneracy·(w,0) 대칭 stabilizer·두 블록 CSS 구조 전제, 고전 NAND binary LDPC엔 해당 병목 부재",
  "todo_check": "self-corrected MS(부호변화 시 이전 메시지 합산) 아이디어가 고전 trapping-set에도 유효한지 별도 검증"
}
```
