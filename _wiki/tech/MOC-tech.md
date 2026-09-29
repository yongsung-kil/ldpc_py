# 기술 문서 (tech) 목록

코드가 어떻게 도는지를 설명하는 문서. 알고리즘 설명, 모듈 동작, 사용법. 원재료는 `docs/profile/`, `docs/explore/`, 코드 주석이다.

문서 21편. 마지막 갱신 2026-09-30 (wiki 스킬 첫 실행).

| 문서 | 요약 | 근거 파일 |
|---|---|---|
| [20260807_flip-condition-ch-le-7dv](20260807_flip-condition-ch-le-7dv.md) | 반전 불가 조건 `ch > dv*top`의 유도, 클리핑 일반형 `Q + (dv-1)*P`, 레벨 0 시절의 공명 조건, 스케일 인사이트, 알려진 위반 상태, dv별 사망 경계 판단 절차 | src/decoder.py, src/llr_matrix.py, Input/LLR/LLR_MATRIX_HD_0.txt, Input/LLR/LLR_MATRIX_HD_1.txt, docs/profile/constraints.md, _pm/TODO.md, _pm/DONE.md, _pm/tasks/20260808_review/r3_round3_lv2_verification/team_a_verification.md, workspace/_template/config.json |
| [20260930_channel-models](20260930_channel-models.md) | 채널 모델 3종(rber, fixed_error, strong_error)의 산식과 출력 dict, 디코딩 모드 정합 3층 | src/channel.py, src/run.py, src/decoder.py |
| [20260930_channels-section-and-experiment-loop](20260930_channels-section-and-experiment-loop.md) | channels 섹션의 정규화 규칙, 채널 x 포인트 측정 루프, 포인트별 난수 스트림 파생, stop_below_fer 동작 | src/run.py, workspace/_template/config.json |
| [20260930_cnu-min1-min2-update](20260930_cnu-min1-min2-update.md) | CN 상태 (min1, min2, min1_pos, check_sum, edge_sgn)의 remove old, insert new 갱신 규칙과 C2V 메시지 재구성 | src/decoder.py, docs/차이.md |
| [20260930_config-validation-rules](20260930_config-validation-rules.md) | load_config가 config JSON에 거는 검사 3층(키맵, 필수값, 값 제약)의 순서와 헬퍼 4개, 정규화 결과의 꼴 | src/run.py, src/sim.py, workspace/_template/config.json |
| [20260930_decoder-stages-and-state](20260930_decoder-stages-and-state.md) | decoder_main이 부르는 단계 함수 7개의 순서, _DecodeState 배열의 축과 dtype, 반환 dict의 키 | src/decoder.py, src/pcm.py |
| [20260930_diff-from-cpp-original](20260930_diff-from-cpp-original.md) | 원본 C++ 디코더 대비 Python의 차이 10행 (번호 1~9와 6b)과 등가 확인 14행 (정본 번호는 13까지, 10번이 둘) 요지, 리뷰에서 확정한 원본 C++ 구조 사실 7개 | docs/차이.md, src/decoder.py, src/llr_matrix.py, docs/profile/techniques.md, _pm/done/20260730_review/r2_round2_lv1_analysis/report.md, _pm/done/20260806_review/r3_round3_lv2_verification/report.md, _pm/tasks/20260808_review/r3_round3_lv2_verification/team_a_verification.md |
| [20260930_fer-point-loop-and-metrics](20260930_fer-point-loop-and-metrics.md) | run_fer_point의 배치 루프와 종료 조건, FER와 post_fec_ber와 avg_decoding_iteration 산식, 진행 줄, 반환 dict, FER CSV 열 | src/sim.py |
| [20260930_genie-check-and-batch-compress](20260930_genie-check-and-batch-compress.md) | 정보 구간을 정답 all-zero와 비교하는 genie 성공 판정, 성공 프레임을 배치에서 빼는 압축 목록, 결과 버퍼의 의미, 함께 바꿔야 하는 전제 묶음 | src/decoder.py, src/encoder.py, src/pcm.py, docs/차이.md |
| [20260930_llr-matrix-file-format-and-loader](20260930_llr-matrix-file-format-and-loader.md) | DAO LLR_MATRIX 텍스트 형식, 파일명 모드 판별, LLRMatrix.load와 _validate의 검사 항목, 생성자가 만드는 배열 | src/llr_matrix.py, src/run.py, docs/차이.md |
| [20260930_qccode-and-h-file](20260930_qccode-and-h-file.md) | QCCode의 H 파일 형식(Ref-C), edge 배열 구성(column 우선), QC 연결의 roll 규약, syndrome 계산 | src/pcm.py, src/decoder.py |
| [20260930_replacement-points-six](20260930_replacement-points-six.md) | BaseDecoder 자식이 재정의하는 교체 지점 6개의 시그니처, 입력 축, 지킬 경계, 교체 지점에 맞지 않는 변경의 수정 범위 | src/decoder.py, src/run.py, src/sim.py, workspace/_template/run.py, docs/profile/replacement_points.md, docs/profile/techniques.md |
| [20260930_run-dir-and-output-files](20260930_run-dir-and-output-files.md) | 실행 폴더 구조와 거기 남는 파일(summary.txt, CSV 4종, LLR 사본, PNG)의 열 정의, 로그 항목의 C++ 대응과 용도 | src/run.py, src/sim.py |
| [20260930_run-main-flow](20260930_run-main-flow.md) | src/run.py의 main이 부르는 5단계, 직접 실행과 런처 실행 두 경로, 실험 요약 불릿 11개, 공개 API | src/run.py, workspace/_template/run.py, src/__init__.py |
| [20260930_sd-region-and-pre-stage](20260930_sd-region-and-pre-stage.md) | 2SD/3SD에서 채널 플래그를 ch 열 인덱스(region)로 바꾸는 식, 채널 magnitude를 CN에 심는 Pre 단계, SD restart의 동작과 C++ 함수 대응 사슬 | src/decoder.py, src/channel.py, src/llr_matrix.py, docs/차이.md, _pm/done/20260809_2SD3SD구현/cpp_sd_analysis.md |
| [20260930_setup-llr-supply-paths](20260930_setup-llr-supply-paths.md) | setup이 H-matrix를 읽은 뒤 LLR matrix를 파일 로드 또는 균일 합성 후 저장 후 로드로 공급하는 두 경로, 생성 파일명, 단일 로더 | src/run.py, src/llr_matrix.py |
| [20260930_syndrome-aided-column-step](20260930_syndrome-aided-column-step.md) | syndrome-aided flip 도메인 규약과 한 iteration 안에서 column block 하나를 처리하는 순서 (C2V 합산, 판정, VNU 양자화, CNU 갱신) | src/decoder.py, src/pcm.py, docs/차이.md |
| [20260930_table-row-select-and-restart](20260930_table-row-select-and-restart.md) | iteration과 직전 CSW로 LLR 테이블 row를 고르는 규칙 (ITER, CSW 그룹), 그룹 겹침 금지와 정방향 순회가 한 쌍인 이유, restart (Edge Clear)의 CN 클리어와 -1 값 동작 | src/llr_matrix.py, src/decoder.py, docs/차이.md |
| [20260930_testbed-copy-vs-original-layout](20260930_testbed-copy-vs-original-layout.md) | 시험장 사본(ldpc_py)과 원본 배치(2_LDPC_base)의 차이. 런처 탐색과 디코더 주입 사슬, -m 경로의 BaseDecoder 고정, .gitignore와 형제 프로젝트 부재, 온보딩 코드 무수정 | workspace/_template/run.py, workspace/README.md, src/run.py, docs/profile/structure.md, docs/explore/프로젝트전체.md |
| [20260930_uniform-llr-matrix-synthesis](20260930_uniform-llr-matrix-synthesis.md) | 파일 없이 균일 간격 edge 레벨과 전 dv 공통 ch로 그룹 1개 LLR matrix를 합성해 저장하고 같은 로더로 읽으며, th 값 패턴으로 레벨을 되찾는 규칙 | src/llr_matrix.py, src/run.py, src/decoder.py, workspace/_template/config.json |
| [20260930_vnu-quantize-cascade](20260930_vnu-quantize-cascade.md) | VNU 출력 \|raw\|를 th 캐스케이드로 edge_mag 레벨에 양자화하는 규칙, 균일 레벨 등가식이 성립하는 조건 (정수 raw), raw == 0일 때의 부호 규칙 | src/decoder.py, src/llr_matrix.py, docs/차이.md |
