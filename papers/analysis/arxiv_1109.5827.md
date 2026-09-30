### arxiv:1109.5827v6 - Security and complexity of the McEliece cryptosystem based on QC-LDPC codes (2013, IET Information Security)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.67~0.75 |
| 부호length | 12288~65536 |
| 연판정 | hard-1bit |
| 핵심기여 | McEliece 암호계용 QC-LDPC에 bit-flipping 복호 도입 + BF 임계치(t_th)를 시뮬 없이 예측하는 해석식으로 보안·복잡도 트레이드오프 설계 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | waterfall |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 채널코딩이 아닌 post-quantum 공개키 암호(McEliece) 맥락; hard-decision BF 전용이라 Prime ECC의 soft min-sum과 무관 |
| 추가확인 | BF 임계치 해석식(cycle-free 가정)이 유한장 QC-LDPC waterfall 예측에 재사용 가능한지 (NAND용은 min-sum이라 실효성 낮음) |

> 총평: NAND ECC가 아닌 QC-LDPC 기반 McEliece 암호계 논문으로, hard-decision bit-flipping 복호와 보안 work-factor 분석이 핵심이라 Prime ECC(soft min-sum) 이식가치가 없다.

### B. 알고리즘 요약

1. 시스템: post-quantum 공개키 암호 McEliece를 Goppa 대신 QC-LDPC로 대체. 코드 `n=n0·p`, `k=(n0-1)p`, rate `(n0-1)/n0` (`n0=3,4` → 2/3, 3/4), `p`는 수천 단위.
2. 문제: Goppa 기반 McEliece는 키가 크고 rate 낮음; QC-LDPC로 키축소·고rate를 얻되 sparse 노출로 인한 구조공격을 막아야 함.
3. 모델: 공개키 `G' = S^-1·G·Q^-1` (S 밀집, Q sparse weight m). 암호문 `x=u·G'+e`, 오류 `t'` 개; 복호측은 `e·Q` (weight ≤ `t=t'm`)를 정정.
4. 핵심기법1(복호): sum-product 대신 hard-decision bit-flipping(BF) 복호 도입 — 채널 soft 정보가 없는 암호 맥락에 적합, 복잡도 대폭 절감.
5. BF 규칙: 각 VN이 불만족 parity-check 수를 세어 임계값 `b` 이상이면 비트 반전(Gallager A: `b=dv-1` 고정, B: `b` 가변).
6. 핵심기법2(설계도구): cycle-free 가정하에 잔여오류 재귀식 `q_l = t - [t·f_b(q_{l-1}) - (n-t)·g_b(q_{l-1})]`로 waterfall 임계치 `t_th = max{t : lim q_l = 0}`를 시뮬 없이 산출, `b` 최적화.
7. 트릭: circulant×vector 곱을 Winograd(Karatsuba-Ofman 일반화) convolution으로 가속, 암/복호 비트당 이진연산 수 추정.
8. 보안: 구조공격(dual code, density-reduction)과 복호공격(Stern/ball-collision ISD)의 work-factor를 해석적으로 산정; QC 성질 때문에 shifted ciphertext로 공격 가속 고려.
9. 결과: 80-bit 보안에서 `n0=4,p=6144,dv=13`이 Goppa 대비 공개키 25배 축소(2304 B), rate 0.75, 복호 비트당 ~1790 이진연산으로 SPA(~9260) 대비 대폭 절감.
10. 한계: 순수 이론(binary op count·work-factor); HW 없음, cycle-free 무한장 가정이라 유한장 waterfall은 낙관적, hard-decision 전용.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| bit-flipping(BF) 복호 알고리즘 | decoder.cpp `LDPC_Decoder()` | 반복복호 루프 위치는 대응되나 Prime ECC는 min-sum(soft), BF(hard)는 알고리즘 자체가 다름 |
| BF waterfall 임계치 해석식 (`q_l` 재귀) | 대응 없음 | Prime ECC에 DE형 임계치 예측 모듈 없음, 오프라인 설계도구 |
| QC-LDPC circulant PCM 구조 | `ecc_top.cpp` `Load_PCM()` | 둘 다 QC-LDPC이나 논문의 코드는 암호용 랜덤 difference family, NAND 고rate 부호와 무관 |
| Winograd circulant 곱 | 대응 없음 | 인코딩 가속 기법이나 Prime ECC는 dual-diagonal 고정, 대응 모듈 없음 |

적용 가치: 낮음 — QC-LDPC라는 부호계열만 공유할 뿐, 대상이 암호계·hard BF 복호·보안 work-factor라 NAND용 soft min-sum QC-LDPC ECC에 떼어 이식할 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1109.5827v6",
  "title": "Security and complexity of the McEliece cryptosystem based on QC-LDPC codes",
  "year": 2013,
  "venue": "IET Information Security",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": "0.67~0.75",
  "code_length": "12288~65536",
  "soft_quant": "hard-1bit",
  "key_contribution": "McEliece 암호계용 QC-LDPC에 bit-flipping 복호 도입 + BF 임계치를 시뮬 없이 예측하는 해석식으로 보안·복잡도 트레이드오프 설계",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "waterfall",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "채널코딩이 아닌 post-quantum 공개키 암호 맥락; hard-decision BF 전용이라 Prime ECC의 soft min-sum과 무관",
  "todo_check": "BF 임계치 해석식(cycle-free 가정)이 유한장 QC-LDPC waterfall 예측에 재사용 가능한지"
}
```
