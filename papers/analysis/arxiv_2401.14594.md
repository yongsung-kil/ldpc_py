### arxiv:2401.14594v1 - Shift-Interleave Coding for DNA-Based Storage: Correction of IDS Errors and Sequence Losses (2024, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | other |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 100000 |
| 연판정 | 무관 |
| 핵심기여 | shift-map-interleave 인코딩+비반복 FB검출/협조 SP복호로 DNA IDS오류·시퀀스손실 동시정정 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 부분 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | DNA 저장 IDS(삽입/삭제/치환)·dropout 채널 전용 상위 코딩구조라 NAND AWGN/RBER 채널과 무관 |
| 추가확인 | 두 LDPC 협조 SP복호가 상위구조 의존적이며 core min-sum 디코더 개선과 무관함을 확인 |

> 총평: DNA 저장의 IDS+시퀀스손실 정정을 위한 shift-interleave 상위 코딩·동기화 마커 스킴으로, 내부는 표준 log-domain SP LDPC일 뿐이라 NAND binary QC-LDPC min-sum 디코더에 이식할 요소가 없다.

### B. 알고리즘 요약

1. 시스템: DNA 저장의 cascaded 채널(IDS 채널 + block erasure), 입력 `X∈Σ4^{n×r}`, 각 열=하나의 DNA 시퀀스(길이 수백 base), 부호는 AWGN용 rate `Ru=0.5` LDPC 2개, `N=100000`.
2. 문제: DNA 시퀀스 길이 제한으로 BLE용 짧은 부호만 쓸 수 있고, SLE(시퀀스손실)와 BLE(IDS)를 따로 다뤄 비효율 -> 하나의 enc/dec로 둘 다, 긴 부호 활용.
3. 모델: 각 base가 확률 `pi`(중복)/`pd`(삭제)/`ps`(치환) 겪는 IDS 채널 + 확률 `pe` erasure. 드리프트는 `[-Dmax:+Dmax]` reflecting random walk HMM.
4. 핵심 기법1(인코딩): 두 부호행렬 `C1,C2`를 3단계 처리 - shift vector `Tu`로 열 이동(식3), 2비트->base quaternion 매핑 `ψ`(식4), 행치환 `X=PX̄`(식5). 각 codeword가 여러 DNA 시퀀스에 분산.
5. 의미: 분산으로 시퀀스손실 영향을 codeword 일부로 국한하고, padding/기결정 심볼이 동기화 마커 역할.
6. 핵심 기법2(검출): `yj`를 HMM으로 보고 forward-backward(FB) 알고리즘으로 ID오류 검출, LH `γj` 산출. 비반복(non-iterative) 순차 추정.
7. 복호: 각 LDPC가 표준 log-domain SP(flooding schedule), mapping node를 통해 두 디코더가 협조 동작, 기결정 CBN이 LLR 신뢰도 강화(식6~10).
8. 최적화: shift vector `(T1,T2)` 선택으로 성능 조절, `Tmax` 클수록 성능↑(검출비용↑), 전송률 `Rtx=L/(L+Tmax)(R1+R2)`(식11).
9. 결과: `n=100, d=1000`에서 SI가 naive 분리·concatenation(marker) 대비 pe∈{0,0.1,0.2} 전 구간 BER waterfall 우수; 검출 복잡도 `O((Tmax+1)ND)`, FB는 병렬 가능.
10. 한계: HW 미설계·시뮬만, DNA IDS/dropout 채널 특화, gatecount/throughput 미제시, achievable rate 분석은 future work.

### C. Prime ECC 관련 모듈 핀포인트

대상이 other(DNA 저장용 상위 코딩구조)이므로 core 디코더 성능 항목은 N/A. 내부 LDPC 복호는 표준 SP로 Prime의 min-sum 개선과 무관.

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| shift-map-interleave 인코딩 | 대응 없음 | DNA base 매핑·마커 구조로 NAND 인코더와 무관 |
| FB(HMM) IDS 검출 | 대응 없음 | Prime은 AWGN/RBER, IDS 동기화 채널 미지원 |
| 표준 log-domain SP 복호 | decoder.cpp `LDPC_Decoder()` | 낮음: 표준 SP일 뿐 Prime의 min-sum HW 개선과 중복/무관 |

적용 가치: **낮음** — DNA 저장의 IDS·시퀀스손실을 겨냥한 상위 shift-interleave 코딩과 HMM 동기화 검출이 본질이고, 내부 LDPC는 표준 SP라 NAND binary QC-LDPC min-sum 디코더/인코더에 떼어 쓸 요소가 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2401.14594v1",
  "title": "Shift-Interleave Coding for DNA-Based Storage: Correction of IDS Errors and Sequence Losses",
  "year": 2024,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "other",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": "100000",
  "soft_quant": "무관",
  "key_contribution": "shift-map-interleave 인코딩+비반복 FB검출/협조 SP복호로 DNA IDS오류·시퀀스손실 동시정정",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "부분",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "DNA 저장 IDS(삽입/삭제/치환)·dropout 채널 전용 상위 코딩구조라 NAND AWGN/RBER 채널과 무관",
  "todo_check": "두 LDPC 협조 SP복호가 상위구조 의존적이며 core min-sum 디코더 개선과 무관함을 확인"
}
```
