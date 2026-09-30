### arxiv:1912.05182v1 - A Code-specific Conservative Model for the Failure Rate of Bit-flipping Decoding of LDPC Codes with Cryptographic Applications (2019, PQCrypto/CBC workshop)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5 |
| 부호length | 9602 |
| 연판정 | hard-1bit |
| 핵심기여 | 랜덤순서 in-place bit-flipping(RIP-BF) 디코더의 worst-case DFR을 subset-sum 카운팅과 PFSA로 폐형·코드특정 상한으로 모델링 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 없음 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 암호(McEliece/Niederreiter IND-CCA2) 목적의 DFR 상한 분석 - hard-decision bit-flip이라 soft NAND LDPC와 무관, 디코더 성능개선 아님 |
| 추가확인 | 구성 특정 DFR 상한(subset-sum 카운팅) 아이디어가 NAND UBER 보증에 개념 차용 가능한지 |

> 총평: 암호용 QC-LDPC/MDPC의 bit-flipping DFR을 보수적으로 상한하는 분석 도구로, hard-decision·비HW·암호목적이라 NAND soft LDPC 디코더 이식성은 낮음.

### B. 알고리즘 요약

1. 시스템: 암호용 QC-LDPC/QC-MDPC(McEliece/Niederreiter), `n=n0·p`, rate `(n0-1)/n0`, (v,w)-regular H; 사례 `n0=2, p=4801, v=45`(즉 n=9602, rate 1/2), hard-decision.
2. 문제: bit-flipping 디코더는 bounded-distance가 아니라 DFR≠0 - IND-CCA2(δ-correctness)엔 DFR≤2^-128 필요, 시뮬로 검증 불가 → 해석적 상한 필요.
3. 핵심 기법(RIP-BF): 고전 in-place BF에 매 iteration마다 error 위치 처리 순서를 랜덤 순열 `π ←$ Pn`로 섞는 단 하나의 변형 추가(Alg.1) - side-channel 방어 겸 worst-case 해석 가능케 함.
4. 확률 모델: bit 평가가 독립이라 가정(Assump.1), H 각 행을 weight w 균일랜덤으로 이상화(Assump.2)해 flip/유지 확률 `Pf|1`, `Pm|0`를 이항분포 폐형으로 유도(Lemma 1).
5. 핵심 식: 열쌍 교집합 weight 행렬 `Γ`(`γ_{x,y}=wH(h:,x ∧ h:,y)`)로 z-th upc를 표현, DFR 상한을 subset-sum 카운팅 문제로 환원(식1~3).
6. 코드특정 상한: `Γ` 행의 distinct 값 수 `η_z ≪ t`를 이용해 지수복잡도를 `η_z`에 대해서만 지수로 낮춘 카운팅 알고리즘 `N(γz,:, ·, ·)`(Appendix B).
7. worst-case 순열 `π* ∈ Pn*`(불일치 위치를 뒤로 몰기)이 성공확률 최소임을 증명(Lemma 2), 이를 매 iteration 강제 가정.
8. DFR 전개: 잔차오류 `t̂0`, `t̂1` 분포를 확률유한상태자동자(PFSA) 전이행렬 `K0`, `K1`로 iteration마다 갱신, 다중 iteration DFR을 합성(식4~6).
9. 결과: `n0=2, p=4801, v=45, b=25`에서 1-iteration DFR은 시뮬과 완전 일치, 2-iteration은 보수적(상한) 일치; 상한 계산은 1초 미만.
10. 한계: 암호(constant-time·DFR 상한) 목적, HW 미설계, hard-decision bit-flip 전용, 디코더 정정성능 개선이 아니라 실패율 분석 도구.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| in-place bit-flipping 복호 루프 | decoder.cpp `LDPC_Decoder()` | Prime ECC는 min-sum(soft) - bit-flipping(hard) 계열이 달라 대응 약함 |
| syndrome/upc 기반 flip 판정 | 대응 없음 | min-sum message passing과 다른 hard-decision BF 판정 |
| worst-case DFR / subset-sum 상한 모델 | 대응 없음 | Prime ECC에 해석적 DFR 상한 도구 없음(통계는 시뮬 기반) |
| QC-LDPC (v,w)-regular H 구조 | ecc_top.cpp `Load_PCM()` | 둘 다 QC-LDPC이나 암호용 MDPC(고밀도)라 부호 스펙 상이 |

적용 가치: 낮음 - hard-decision bit-flipping·암호(IND-CCA2 DFR 상한) 목적으로 min-sum soft NAND 디코더와 계열이 다르고 HW 설계도 없다. 다만 구성-특정 실패율 상한 아이디어는 NAND UBER 보증 논의에 개념적 참고 여지만 있음.

### D. JSON 블록

```json
{
  "id": "arxiv:1912.05182v1",
  "title": "A Code-specific Conservative Model for the Failure Rate of Bit-flipping Decoding of LDPC Codes with Cryptographic Applications",
  "year": 2019,
  "venue": "PQCrypto/CBC workshop (LNCS)",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": 0.5,
  "code_length": "9602",
  "soft_quant": "hard-1bit",
  "key_contribution": "랜덤순서 in-place bit-flipping(RIP-BF) 디코더의 worst-case DFR을 subset-sum 카운팅과 PFSA로 폐형·코드특정 상한으로 모델링",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "없음",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "암호(McEliece/Niederreiter IND-CCA2) 목적의 DFR 상한 분석 - hard-decision bit-flip이라 soft NAND LDPC와 무관, 디코더 성능개선 아님",
  "todo_check": "구성 특정 DFR 상한(subset-sum 카운팅) 아이디어가 NAND UBER 보증에 개념 차용 가능한지"
}
```
