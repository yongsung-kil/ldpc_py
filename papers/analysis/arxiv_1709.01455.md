### arxiv:1709.01455v3 - ML and Near-ML Decoding of LDPC Codes Over the BEC: Bounds and Decoding Algorithms (2018, IEEE Trans. Inf. Theory / arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | decoder |
| 부호종류 | QC-LDPC |
| 부호rate | 0.25~0.75 |
| 부호length | 48~96000 |
| 연판정 | 무관 |
| 핵심기여 | BEC ML 복호 오류확률 rank/spectrum 상하한 + QC-LDPC용 wrap-around 슬라이딩윈도우 near-ML 복호 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | O |
| 개선영역 | both |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | BEC(소실채널) 전용 - NAND의 BSC/AWGN 및 min-sum BP와 채널·연산 모델이 다름, HW 미설계 |
| 추가확인 | 소실채널 near-ML(가우스소거/Viterbi 기반)이 NAND soft-read LLR BP 파이프라인에 어떤 형태로든 대응 가능한지 |

> 총평: BEC 유한길이 LDPC의 ML 성능 경계·threshold 이론과 QC-LDPC용 슬라이딩윈도우 near-ML 복호로, NAND용 binary QC-LDPC min-sum BP 엔진에는 채널·복호구조가 근본적으로 달라 이식성 하.

### B. 알고리즘 요약

1. 대상: BEC(소실확률 `ε`)에서 유한길이 (J,K)-정규 및 QC LDPC 부호의 ML/near-ML 복호 성능 분석, 부호 길이 `n=48~96000`, rate `R=1/4~3/4`.
2. 문제: BEC ML 복호는 소실위치 부분행렬 `H_I`의 rank 계산(선형방정식 풀이)이나, 길이가 수만 bit면 계산 불가능 → 실용적 near-ML 필요.
3. 모델: ML 오류확률 `Pe = Pr(rank(H_I) < |I|)`, 소실 개수 `ν`, redundancy `r`.
4. 상한 1(S-bound): 평균 weight spectrum 기반 union-type 상한 `Pe`. Gallager 앙상블 평균 spectrum을 Lemma 1 재귀식으로 정밀 계산(복잡도 길이에 선형).
5. 상한 2(R-bound): `H_I` 부분행렬 rank 추정 기반 상한 (Thm 3 RU 앙상블, Thm 4 Gallager 앙상블), `Pe|ν ≤ 2^{ν-r}(1+...)`.
6. 하한(Thm 2): 최소거리 `d0` 이용한 tightened sphere-packing 하한 - 저 `ε` 영역에서 기존 대비 크게 개선.
7. threshold: R-bound에서 ML 복호 threshold 하한 해석식 `ε = 1 - (J/K)log(1+(1-ε)^K)/log2` 유도(식26).
8. 핵심 복호기법: QC-LDPC를 tail-biting 컨볼루셔널 부호로 보고 wrap-around 슬라이딩윈도우 ML(SWML) 적용 - BP 실패 후 창(window) 단위로 ZT 컨볼루셔널 부호 ML 복호, 창 shift `s=c`.
9. 결과: SWML이 near-capacity 영역에서 BP 대비 FER 크게 개선(예 DH부호 n=4800), 창 크기 키우면 ML 성능 접근, 복잡도는 창 길이에 cubic·부호 길이에 선형.
10. 한계: BEC 전용, HW 미설계, 순수 시뮬/이론, quasi-cyclic 구조 제약으로 앙상블 평균 ML 성능엔 미달.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| SWML/BP 하이브리드 복호 루프 | decoder.cpp LDPC_Decoder() | 대응 개념은 있으나 BEC 가우스소거·Viterbi 기반이라 min-sum BP 루프에 직접 이식 불가 |
| QC-LDPC H-matrix / TB 컨볼루셔널 구조 로드 | ecc_top.cpp Load_PCM() | QC 구조 로드 접점은 있으나 부호구조 특화(고정 QC-LDPC)라 이식 부담 큼 |
| ML 오류확률 rank/spectrum 경계 | 대응 없음 | 설계·검증 단계의 성능 예측 이론 - 런타임 코드 경로 없음 |
| BEC 소실채널 모델 | channel.cpp (AWGN/RBER) | Prime ECC는 소실채널 미지원, 대응 없음에 가까움 |
```

적용 가치: **낮음** - BEC 소실채널 전용 이론·복호로, NAND의 BSC/AWGN soft-read + min-sum BP 엔진과 채널·연산 모델이 근본적으로 달라 떼어 쓸 수 있는 재사용 요소가 사실상 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:1709.01455v3",
  "title": "ML and Near-ML Decoding of LDPC Codes Over the BEC: Bounds and Decoding Algorithms",
  "year": 2018,
  "venue": "IEEE Trans. Inf. Theory / arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "decoder",
  "code_type": "QC-LDPC",
  "code_rate": "0.25~0.75",
  "code_length": "48~96000",
  "soft_quant": "무관",
  "key_contribution": "BEC ML 복호 오류확률 rank/spectrum 상하한 + QC-LDPC용 wrap-around 슬라이딩윈도우 near-ML 복호",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "O",
  "improve_region": "both",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "BEC(소실채널) 전용 - NAND의 BSC/AWGN 및 min-sum BP와 채널·연산 모델이 다름, HW 미설계",
  "todo_check": "소실채널 near-ML(가우스소거/Viterbi 기반)이 NAND soft-read LLR BP 파이프라인에 어떤 형태로든 대응 가능한지"
}
```
