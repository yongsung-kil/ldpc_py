### arxiv:1209.0744v1 - Balanced Modulation for Nonvolatile Memories (2012, arXiv)

| 카테고리 | 값 |
|---|---|
| 이식성 | 하 |
| NAND관련성 | 직접 |
| 대상 | code-design |
| 부호종류 | irregular |
| 부호rate | 미상 |
| 부호length | 120~1200 |
| 연판정 | hard-1bit |
| 핵심기여 | balanced LDPC code(첫 i비트 반전으로 balanced word 생성) + 동적 balancing threshold로 비대칭 에러를 대칭화 |
| HW설계 | X |
| 검증수준 | 시뮬 |
| 복잡도 | 미상 |
| 병렬화 | 미상 |
| Throughput | 미상 |
| 메모리라우팅 | 없음 |
| 정정능력향상 | X |
| 개선영역 | N/A |
| iteration감소 | N/A |
| latency | N/A |
| 추천도 | 하 |
| 한계,주의 | balanced code는 선형이 아니고 반전 인덱스 i를 저장하지 않는 대신 복호 시 탐색해야 해 Prime ECC의 선형 QC-LDPC 구조·인코더/디코더 파이프라인과 근본적으로 다름 |
| 추가확인 | 반전 인덱스 탐색(半-interval search, 벨리프전파 기반 i 추정)의 HW 비용이 실제 NAND 컨트롤러 read latency에 미치는 영향 |

> 총평: dynamic threshold + balanced LDPC 구성법으로 비대칭 노이즈를 완화하는 이론/시뮬 논문이며, 정정능력 자체는 원본(unbalanced) LDPC와 거의 동일함을 보인 수준이라 Prime ECC 3.1의 고정 QC-LDPC/디코더에 이식할 요소가 적음.

### B. 알고리즘 요약

1. NAND/PCM 등 비휘발성 메모리의 셀 레벨 드리프트로 인한 비대칭 에러(1→0 ≫ 0→1)를 완화하기 위해 balanced modulation을 제안한다.
2. 기존 고정 threshold 읽기는 시간 경과에 따른 셀 레벨 드리프트로 비대칭 에러가 누적되는 문제가 있다.
3. 저장 코드워드는 balanced(1과 0 개수 동일)로 인코딩되고, 읽기 시 결과 워드가 balanced가 되도록 threshold `v`를 동적으로 조정(balancing threshold `vb`)한다.
4. `Ne(vb) ≤ 2Ne(vo)` (Theorem 1) - balancing threshold의 총 에러수는 최적 threshold 대비 최대 2배로 suboptimal이 보장된다.
5. balanced LDPC code는 일반 (n,k) LDPC 코드워드 `z=Gu`의 첫 `i`비트를 반전(`x = z + 1^i 0^{n-i}`)해 balanced word `x`를 만들며, 인덱스 `i`는 별도 저장하지 않고 복호 시 추정한다.
6. BEC 복호는 message-passing에 "inversion node"를 추가해 가능한 `i` 후보 집합(inversion set `I`)을 파싱-체크 노드 갱신으로 축소한다.
7. BSC/AWGN 복호는 belief propagation을 각 `i` 후보에 대해 `ℓ`(작은 상수, 예 2) 라운드만 돌려 parity check 만족도 지표 `λ(y,ℓ)=Σtanh(m_vc/2)`로 가장 유력한 `i`를 O(n) 시간에 추정(Theorem 3)한다.
8. 별도 학습/최적화 절차는 없음(구성적 증명 + 시뮬레이션).
9. (280,4,7) balanced LDPC와 원본 unbalanced LDPC의 word error rate가 ℓ=2, c=4 조건에서 거의 동일함을 시뮬로 확인; 인덱스 `i` 보정 비용이 무시할 수준.
10. 인코더/디코더 HW 설계 없음, 시뮬레이션 수준 검증뿐이며 부호는 소규모(n=120~1200) 예제에 한정.

### C. Prime ECC 관련 모듈 핀포인트

| 논문 요소 | Prime ECC 모듈 | 관련성 |
|---|---|---|
| balanced LDPC 구성(첫 i비트 반전) | `ecc_top.cpp` `Load_PCM()` | 선형 코드가 아니어서 고정 QC-LDPC PCM 구조와 직접 대응 안 됨, 참고용 |
| BSC/AWGN용 belief propagation 기반 i 추정 | `decoder.cpp` `LDPC_Decoder()` | Prime ECC는 min-sum이고 논문은 sum-product(tanh) belief propagation이라 알고리즘 자체는 대응 없음 |
| 동적 balancing threshold (읽기 시 적응형 threshold) | `channel.cpp` `Set_R_Offset()`, `Set_LLR_Th()` | 개념적으로 soft-read threshold 조정과 유사하나 목적(balanced 강제)이 달라 간접 관련 |
| 비대칭 채널→대칭 채널 변환 | 대응 없음 | NAND read-retry/threshold 최적화와는 다른 접근 |

> 적용 가치: 낮음. balanced code 구성법은 비선형이라 Prime ECC의 QC-LDPC 부호 구조와 근본적으로 다르고, 정정능력 자체 개선도 없어(원본 LDPC와 동등) 이식 실익이 적음.

### D. JSON 블록

```json
{
  "id": "arxiv:1209.0744v1",
  "title": "Balanced Modulation for Nonvolatile Memories",
  "year": 2012,
  "venue": "arXiv",
  "portability": "하",
  "nand_relevance": "직접",
  "target": "code-design",
  "code_type": "irregular",
  "code_rate": null,
  "code_length": "120~1200",
  "soft_quant": "hard-1bit",
  "key_contribution": "balanced LDPC code(첫 i비트 반전으로 balanced word 생성) + 동적 balancing threshold로 비대칭 에러를 대칭화",
  "hw_designed": "X",
  "verification": "시뮬",
  "complexity": "미상",
  "parallelism": "미상",
  "throughput_gbps": null,
  "mem_routing": "없음",
  "correction_gain": "X",
  "improve_region": "N/A",
  "iter_reduction": "N/A",
  "latency": "N/A",
  "recommend": "하",
  "caveat": "balanced code는 선형이 아니고 반전 인덱스 i를 저장하지 않는 대신 복호 시 탐색해야 해 Prime ECC의 선형 QC-LDPC 구조·인코더/디코더 파이프라인과 근본적으로 다름",
  "todo_check": "반전 인덱스 탐색(半-interval search, 벨리프전파 기반 i 추정)의 HW 비용이 실제 NAND 컨트롤러 read latency에 미치는 영향"
}
```
