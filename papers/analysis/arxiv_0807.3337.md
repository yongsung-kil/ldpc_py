### arxiv:0807.3337v1 - Algebraic constructions of LDPC codes with no short cycles (2008, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 중 |
| NAND관련성 | 간접 |
| 대상 | code-design |
| 부호종류 | QC-LDPC |
| 부호rate | 0.5~0.75 |
| 부호length | 96~1296 |
| 연판정 | 무관 |
| 핵심기여 | 군환(group ring) unit-derived 대수 구성으로 4-cycle 없는(girth>=6) 이진 circulant-by-circulant LDPC 생성, 차분집합 무중복 조건(Thm 2.2) |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 중 |
| 한계,주의 | girth>=6(4-cycle 제거)만 보장하고 error-floor/trapping set 미보증, 코드 전면 재설계·재검증 필요, 고rate(~0.9) NAND ECC 사례 없음(최대 3/4) |
| 추가확인 | circulant-by-circulant를 z=32 lifting QC 구조로 매핑 가능한지, 고rate(0.9)에서도 girth·성능 유지되는지 |

> 총평: 이진 QC(circulant-by-circulant) LDPC 대수 구성법으로 도메인 정합성은 있으나 girth-6는 표준 수준이고 이미 최적화된 고정 고rate 코드에는 재설계 부담이 커 이식성 중.

### B. 알고리즘 요약

1. 시스템: 이진(`Z2=F2`) LDPC, AWGN/BPSK 및 QAM64(802.11n/802.16e) 채널로 BER/BLER 비교.
2. 문제: Tanner 그래프의 short cycle(길이 4)이 복호 성능을 저하 → 4-cycle 없는 코드를 대수적으로 구성.
3. 모델: 군환 `RG`의 unit-derived 코드 — `u,v in RG`, `uv=1`, `v`가 small support면 대응 행렬 `V`가 저밀도(LDPC).
4. 핵심기법: unit `u`의 행렬 `U`에서 `r`개 행으로 생성행렬, `V`에서 대응 열 삭제로 검사행렬 구성.
5. 핵심정리(Thm 2.2): `U`가 4-cycle 없음 <=> 군차분 집합 `DS(u)`에 중복 원소 없음(순수 행렬 성질로 환원, 그래프 이론 불필요).
6. 확장: `DS(u)`에 중복이 있어도 특정 행/열(`g_m^{-1}g_p` 등)을 배제하면 4-cycle 회피 가능.
7. 구현: `G=Cn x C4`이면 행렬이 circulant-by-circulant(=QC 구조), 소수 파라미터(15~17개)로 H를 line-by-line 재생성 → 저장·전력 절감.
8. 특수군: 순환군->circulant, 이면군 `D2n`->[[A,B],[B,A]] reverse-circulant(비가환 코드).
9. 결과: TFI-96/504/816 코드가 MacKay·PEGReg252x504와 대등하거나 우수, 802.11n(648, r=2/3)·802.16e(1152, r=2/3) IEEE 코드와 BER/iteration 유사(staircase 부분은 IEEE 구조 재사용).
10. 한계: HW 미설계, 시뮬만, 4-cycle 제거만 보장(고girth/trapping set 미보증), 최대 rate 3/4까지만 예시.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| 대수적 QC(circulant-by-circulant) H 구성 | ecc_top.cpp Load_PCM() | 4-cycle 없는 새 QC H-matrix 설계·로드 경로이나 우리 부호는 고정 |
| staircase(인코딩) 구조 재사용 | encoder.cpp LDPC_encoder_4KB() | 논문 staircase는 dual-diagonal류이나 우리 인코더는 고정 |
| 소수 파라미터 line-by-line H 재생성 | 대응 없음 | Prime ECC는 H-matrix 로드 방식(저장 최소화 생성기는 별도) |
```

적용 가치: 낮음 — binary QC-LDPC 구성법으로 원리적 관련성은 있으나 girth-6는 표준 수준이고 고정 고rate 코드 재설계·재검증 부담이 큼.

### D. JSON 블록

```json
{
  "id": "arxiv:0807.3337v1",
  "title": "Algebraic constructions of LDPC codes with no short cycles",
  "year": 2008,
  "venue": "arXiv",
  "portability": "중",
  "nand_relevance": "간접",
  "target": "code-design",
  "code_type": "QC-LDPC",
  "code_rate": null,
  "code_length": "96~1296",
  "soft_quant": "무관",
  "key_contribution": "군환 unit-derived 대수 구성으로 4-cycle 없는(girth>=6) 이진 circulant-by-circulant LDPC 생성, 차분집합 무중복 조건(Thm 2.2)",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "중",
  "caveat": "girth>=6(4-cycle 제거)만 보장하고 error-floor/trapping set 미보증, 코드 전면 재설계·재검증 필요, 고rate(~0.9) NAND ECC 사례 없음(최대 3/4)",
  "todo_check": "circulant-by-circulant를 z=32 lifting QC 구조로 매핑 가능한지, 고rate(0.9)에서도 girth·성능 유지되는지"
}
```
