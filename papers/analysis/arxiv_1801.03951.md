### arxiv:1801.03951v2 - LDPC Codes with Local and Global Decoding (2019, arXiv cs.IT / ISIT 2018)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 간접 |
| 대상 | code-design |
| 부호종류 | 기타 |
| 부호rate | 0.5~0.8 |
| 부호length | 213~360 |
| 연판정 | 무관 |
| 핵심기여 | local/joint 두 degree-distribution으로 sub-block 지역복호+full-block 전역복호 겸용 LDPCL 부호를 정의하고 BEC 용량달성 구성·2D-DE 분석 제시 |
| HW설계 | X |
| 검증수준 | 이론 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 언급 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | BEC 전용·이론뿐(HW/디코더 미구현), sub-blocked bi-layer 구조라 우리 고정 QC-LDPC 단일 H와 정합 안 됨 |
| 추가확인 | BSC/AWGN·binary QC-LDPC로의 확장 여부, NAND read를 sub-block 지역복호로 매핑 시 rate 손실·전역복호 트리거 조건 |

> 총평: 저지연 read(sub-block 지역복호)+안전망(full-block 전역복호)을 겸하는 새 부호 계열의 이론적 토대. 스토리지 지향 아이디어는 좋으나 BEC 이론·비표준 구조라 우리 고정 QC-LDPC 파이프라인엔 그대로 이식 불가.

### B. 알고리즘 요약

1. 시스템: 길이 `N=Mn` 부호를 `M`개 sub-block(각 `n`)으로 분할, sub-block 자체가 지역부호 codeword이자 전체가 더 강한 전역부호 codeword (multi sub-block coding). 채널은 BEC.
2. 문제: 스토리지는 재전송 불가라 강한(대형) 부호가 필요하나 그러면 read latency·복잡도↑. 저지연 소블록 read와 실패 시 대형 안전망을 동시에 원함.
3. 구조: sub-blocked Tanner graph — variable node를 M개 sub-block으로, check를 local(같은 sub-block만 연결)/joint(제약 없음)로 분리. `local`·`joint` 두 degree distribution으로 정의.
4. 핵심 변수: `P0 = ΛJ,0`(joint degree 0인 변수노드 비율)을 도입 — rate를 올리면서 성능 손실 없음, 구성의 핵심.
5. 복호: 2모드 — local mode(sub-block 그래프에서 BP), 실패 시 global mode(전체 그래프 BP). 지역/전역이 비대칭(`P0>0`, `λJ(0)>0` 허용)이라 2D-DE 필요(식 5a·5b).
6. 임계값: 전역 임계 `ǫ*G`를 (f,g)-고정점 존재 조건으로 특성화(Thm 5·7), 수치계산법 제공.
7. 구성(Construction 1): 목표 `ǫL,ǫG` 입력→ local DD·joint DD·`P0=ǫL/ǫG`로 `ǫ*L=ǫL`, `ǫ*G=ǫG` 보장(Thm 8), BEC 용량달성 수열 존재 증명(Lemma 9, δ≤δL+δJ(1−P0)).
8. 스케줄링: joint iteration 수 `NJI`(대형 데이터 접근 비용)를 최소화하는 최적 스케줄 제시 — local이 "stuck"일 때만 joint 갱신(식 35), 최적성 증명(Lemma 11). rate↔NJI 트레이드오프 존재.
9. 결과: 예제서 M=4·n=211·rate 0.53 LDPCL이 동rate 단일 LDPC(n=211/213)를 BEC global 성능서 상회, local edge 6130 vs 8365/33235로 지역복호 복잡도 대폭↓(식18로 |EL|/|E|≈15%). 유한길이 ML union bound(Thm 13)로 locality↔전역성능 트레이드오프 정량화.
10. 한계: BEC 전용·순수 이론(HW/실디코더 없음), sub-blocked bi-layer 구조는 표준 단일 QC-LDPC와 이질적, BSC/AWGN 확장은 미수행.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| local/joint 이중 degree distribution 부호구조 | ecc_top.cpp `Load_PCM()` + H-matrix | 우리는 단일 고정 QC-LDPC H, sub-blocked bi-layer 구조 미지원이라 이식 난이도 높음 |
| 2모드(local→global) 복호 전략 | decoder.cpp `LDPC_Decoder()` | 조기종료/부분복호 개념은 있으나 sub-block 단위 지역복호+전역 fallback 구조는 대응 없음 |
| joint iteration 최소화 스케줄링 | decoder.cpp 이터레이션 루프 (간접) | 우리 Dual-Update(even/odd 교대) 스케줄과 성격 다름(대형블록 접근비용 최소화 목적) |
| sub-block=read / full-block=write 매핑 | 대응 없음 | NAND read/write 단위 매핑은 컨트롤러 정책 영역, 코드 모듈 대응 없음 |

적용 가치: **낮음** — 스토리지 read latency를 겨냥한 지역/전역 복호 아이디어는 흥미로우나, BEC 이론·비표준 sub-blocked bi-layer 부호구조라 우리 고정 binary QC-LDPC 파이프라인에 그대로 붙일 수 없음. 향후 SC-LDPC 확장([20],[21]) 추적 정도의 참고 가치.

### D. JSON 블록

```json
{
  "id": "arxiv:1801.03951v2",
  "title": "LDPC Codes with Local and Global Decoding",
  "year": 2019,
  "venue": "arXiv cs.IT / ISIT 2018",
  "portability": "하",
  "nand_relevance": "간접",
  "target": "code-design",
  "code_type": "기타",
  "code_rate": null,
  "code_length": "213~360",
  "soft_quant": "무관",
  "key_contribution": "local/joint 이중 degree distribution으로 sub-block 지역복호+full-block 전역복호 겸용 LDPCL 부호를 정의하고 BEC 용량달성 구성·2D-DE 분석 제시",
  "hw_designed": "X",
  "verification": "이론",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "언급",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "BEC 전용·이론뿐(HW/디코더 미구현), sub-blocked bi-layer 구조라 우리 고정 QC-LDPC 단일 H와 정합 안 됨",
  "todo_check": "BSC/AWGN·binary QC-LDPC 확장 여부, NAND read를 sub-block 지역복호로 매핑 시 rate 손실·전역복호 트리거 조건"
}
```
