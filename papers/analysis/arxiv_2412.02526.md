### arxiv:2412.02526v1 - On the lifting degree of girth-8 QC-LDPC codes (2024, IEEE (arXiv preprint, cs.IT))

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | both |
| 부호종류 | QC-LDPC |
| 부호rate | 미상 |
| 부호length | 85~162 |
| 연판정 | 무관 |
| 핵심기여 | (3,L) fully-connected QC-LDPC의 girth-8 lifting degree 하한을 고전 `p>=2L-1`에서 `p>=(5L^2-11L+13)/2 +1/2`로 개선하고 하한 근접 결정적 구성법 제시 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | error-floor |
| iteration감소 | X |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | J=3(dv=3) 저열가중치·소형(L<=12) 부호 전용 이론, error-floor는 girth 확보에 따른 정성적 개선일 뿐 정량 BER/floor 수치 없음 |
| 추가확인 | Prime ECC의 고정 H-matrix(dv=17, high-rate)와 부호 파라미터가 전혀 달라 실제 이식·재검증 부담 여부 |

> 총평: girth-8 보장 QC-LDPC 결정적 구성 이론으로 부호설계 관점 참고는 되나 dv=3 소형 부호 전용이라 Prime ECC(고rate·고degree 고정 H)로의 직접 이식성은 낮음.

### B. 알고리즘 요약 (10줄 내외)

1. 대상은 `(3,L)` fully-connected QC-LDPC 부호로 3xL exponent matrix `E`와 lifting degree `p`(CPM 크기)로 결정, 예제 부호길이 85, 162.
2. 문제: girth 8(6-cycle 제거) 보장에 필요한 최소 lifting degree `p`를 줄여 짧은 부호를 얻는 것 - 작은 `p`가 곧 짧은 부호.
3. 핵심 모델: cycle 존재 필요충분조건 `sum(e_mi,ni - e_mi,ni+1)=0 mod p`, 이를 girth-8 matrix `M8`(대각/행/열 원소 distinct)로 재정식화(Lemma 1).
4. 핵심기법1: `M8`의 distinct 원소 수가 `p`의 하한 - arithmetic 부분수열 길이 `m`이 있으면 `p>=m^2/2 -3m/2 +2L`(Lemma 2).
5. 의미: distinct 원소 개수 count가 곧 필요 lifting degree이므로 원소 중복을 최대화하면 `p`를 최소화.
6. 핵심기법2: pigeonhole + Corollary 1로 일반 (3,L) 부호의 새 하한 `p>=(5L^2-11L+13)/2 +1/2` 유도(고전 `2L-1` 대비 첫 개선, Theorem 1).
7. 구현 디테일: d=1이면 `a_i=i`, `-b_i`를 (L+1)i / (L+2)(L-1-i)+1로 배치해 비대각 원소가 정확히 2번씩 나오게 구성(Theorem 2), d>=2는 complete residue system 활용.
8. 학습/최적화: 없음(순수 조합론·정수론 구성).
9. 결과: 구성 lifting degree가 하한 `L^2/2+L/2`와 `floor((L-1)/2)`만 차이, [14]의 `3L^2/4` 대비 작음(표 I); L=5,p=17 및 L=6,p=27 min-sum(20 iter) AWGN 시뮬에서 [14]·random lifting보다 FER 우수.
10. 한계: HW 미설계, dv=3 소형 부호(L<=12) 전용, error-floor 개선은 girth 확보 근거의 정성적 주장이며 실제 floor 곡선/정량치 없음.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| exponent matrix / CPM lifting 구성 | ecc_top.cpp `Load_PCM()` | H-matrix 로드 위치는 대응하나 우리는 dv=17 고rate 고정 base+shift라 (3,L) 구성 직접 대입 불가 |
| girth-8 부호구조(H-matrix 설계) | ecc_data.h `PCM_b`(base+shift) | 우리 부호도 QC-LDPC이나 파라미터(dv, rate, z)가 전혀 달라 재설계·재검증 부담 큼 |
| min-sum 복호(성능 검증용) | decoder.cpp `LDPC_Decoder()`, `CNU_Update_New_Mag()` | 논문은 min-sum으로 결과 검증만, 복호 알고리즘 기여는 없음 |
| lifting/CPM 세부 shift 규칙 | 대응 없음 | Prime ECC의 shift 테이블은 이미 고정, 논문의 결정적 구성 규칙과 무관 |
| error-floor/trapping-set 보장 | 대응 없음 | girth 기반 정성적 근거뿐, 우리 코드의 error-floor 대책 모듈 없음 |

적용 가치: **낮음** - 순수 QC-LDPC 부호설계(girth-8 lifting degree) 이론으로 Prime ECC의 고정 고rate·dv=17 H-matrix와 파라미터가 크게 달라 직접 이식·재검증 비용이 크고, 얻는 기여는 부호설계 레이어(가장 이식 난이도 높음)에 국한된다.

### D. JSON 블록

```json
{
  "id": "arxiv:2412.02526v1",
  "title": "On the lifting degree of girth-8 QC-LDPC codes",
  "year": 2024,
  "venue": "IEEE (arXiv preprint, cs.IT)",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "both",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "85~162",
  "soft_quant": "무관",
  "key_contribution": "(3,L) fully-connected QC-LDPC의 girth-8 lifting degree 하한을 고전 p>=2L-1에서 p>=(5L^2-11L+13)/2 +1/2로 개선하고 하한 근접 결정적 구성법 제시",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "error-floor",
  "iter_reduction": "X",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "J=3(dv=3) 저열가중치·소형(L<=12) 부호 전용 이론, error-floor는 girth 확보에 따른 정성적 개선일 뿐 정량 BER/floor 수치 없음",
  "todo_check": "Prime ECC의 고정 H-matrix(dv=17, high-rate)와 부호 파라미터가 전혀 달라 실제 이식·재검증 부담 여부"
}
```
