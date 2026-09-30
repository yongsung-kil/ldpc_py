### arxiv:2604.07365v1 - Tunneling-Augmented Simulated Annealing for Short-Block LDPC Code Construction (2026, arXiv cs.IT)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 낮음 |
| 대상 | code-design |
| 부호종류 | irregular |
| 부호rate | 0.5 |
| 부호length | 64~128 |
| 연판정 | 무관 |
| 핵심기여 | 터널링 항을 더한 시뮬레이티드 어닐링(TASA)으로 짧은 블록 LDPC의 PCM을 사이클/트래핑셋 페널티 하에 전역 최적화 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | N/A |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | 순수 오프라인 부호구성법(PEG 대비 3만~12만배 느림), 구조개선이 복호이득으로 이어지지 않는 음성결과 다수 |
| 추가확인 | error-floor(BLER<1e-4) 영역 미평가 - 트래핑셋 제거 효과가 그곳에서 나타날지 확인 필요 |

> 총평: 짧은 블록 LDPC를 위한 물리기반 전역 부호구성 연구이나 waterfall에서 PEG를 못 넘고 NAND 고rate QC-LDPC와 거리가 멀어 이식성 하.

### B. 알고리즘 요약

1. 대상: 길이 `n∈{64,96,128}`, rate `R=0.5`, 목표 열가중치 `wc=3`의 짧은 이진 선형/LDPC 부호를 AWGN+BPSK에서 설계.
2. 문제: 짧은 블록에서는 점근특성이 아닌 Tanner 그래프의 유한길이 구조(단주기, stopping/trapping set)가 성능을 지배 → 다목적 구조를 동시에 조절할 전역 최적화 필요.
3. 정식화: `min E(H)`로 PCM을 직접 최적화. `E(H)=α4·C4+α6·C6+αw·W+αd·D+αv·V` (4/6-사이클, 열가중치 편차, 저차수, 유효성 페널티).
4. 핵심식 `C4(H)=Σ_{i<j} cij(cij-1)/2` (행쌍 공유열 `cij`로 4-사이클 수 계산), 가중치 순서 `αv≫α4≫α6>αw>αd`.
5. 기법1: TASA - 고전 SA의 수용확률에 감쇠 터널링 항을 추가 `Paccept=min(1,exp(-ΔE/T(t)))+ptunnel(t)`.
6. 터널링 항 `ptunnel(t)=p0·exp(-t/tmax)`, `p0=0.1`; 온도 `T(t)=Tinit(Tfinal/Tinit)^(t/tmax)`, `Tinit=10, Tfinal=0.01`.
7. 제약처리: all-zero 행/열 발생 시 repair, 열가중치 보존형 이동(열 내 1↔0 교환), 수렴 후 GF(2) rank repair.
8. 이동/정제: 무제약은 단일 비트 토글, 제약은 열가중치 보존 스왑; TASA 후 first-improvement 힐클라이밍 국소정제, `r=8` 병렬 재시작.
9. 결과: 4-사이클 완전 제거, 랜덤 대비 0.1~1.3dB(평균 0.45dB) 이득, PEG 대비 -0.6~+0.09dB(평균 -0.23dB). (4,2) 트래핑셋 1906개 제거해도 +0.08dB뿐.
10. 한계: HW 미설계, waterfall만 평가(error-floor 미평가), 복호기 피드백 없이 대리 그래프지표만 최적화, PEG 대비 4~5자릿수 느림.

### C. Prime ECC 관련 모듈 핀포인트

```
| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| PCM(H) 직접 최적화(부호구성) | ecc_top.cpp Load_PCM() | H-matrix 로드 지점이나 우리 부호는 고정 QC-LDPC라 재구성 부담 큼 |
| block-structured(QC 근사) 제약 | ecc_top.cpp Load_PCM() | QC 구조를 근사만 할 뿐 실제 base+circulant 생성기 아님 |
| BP(sum-product) 복호 평가 | decoder.cpp LDPC_Decoder() | 우리는 min-sum, 논문은 평가용 SP - 알고리즘 기여 없음 |
| 트래핑셋/사이클 페널티 | 대응 없음 | 부호구성 지표일 뿐 디코더 모듈에 직접 대응 없음 |
```

적용 가치: **낮음** - rate 0.5·length 64~128의 짧은 블록 전역 부호구성법이라 NAND 고rate QC-LDPC(z=32, base+circulant)와 스펙이 맞지 않고, 자체 결론상 구조개선이 waterfall 복호이득으로 이어지지 않으며 HW·검증도 없다.

### D. JSON 블록

```json
{
  "id": "arxiv:2604.07365v1",
  "title": "Tunneling-Augmented Simulated Annealing for Short-Block LDPC Code Construction",
  "year": 2026,
  "venue": "arXiv cs.IT",
  "portability": "하",
  "nand_relevance": "낮음",
  "target": "code-design",
  "code_type": "irregular",
  "code_rate": 0.5,
  "code_length": "64~128",
  "soft_quant": "무관",
  "key_contribution": "터널링 항을 더한 시뮬레이티드 어닐링(TASA)으로 짧은 블록 LDPC의 PCM을 사이클/트래핑셋 페널티 하에 전역 최적화",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "N/A",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "순수 오프라인 부호구성법(PEG 대비 3만~12만배 느림), 구조개선이 복호이득으로 이어지지 않는 음성결과 다수",
  "todo_check": "error-floor(BLER<1e-4) 영역 미평가 - 트래핑셋 제거 효과가 그곳에서 나타날지 확인 필요"
}
```
