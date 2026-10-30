# 허구의 재고 점검 연습

이 파일과 items.csv는 공개 가능한 연습 자료다. 실제 시험 문제나 업무 데이터가 아니다.

`items.csv`를 읽어 `result.csv`와 `REPORT.md`를 만든다. 제품별 수량 부족을 확인하는 작은 CLI를 작성하며 UI나 외부 패키지는 필요 없다.

- 입력 열: `sku,on_hand,min_required`.
- 수량은 0 이상의 정수다. 비어 있거나 음수이면 그 행은 invalid이며 결과 CSV에서 제외한다. 실수 형태도 허용하지 않는다.
- 유효한 행은 입력 순서를 보존해 `sku,status,shortage` 열로 출력한다.
- `status`는 `on_hand < min_required`이면 `shortage`, 그 외에는 `ok`다. `shortage`는 부족한 수량이며 부족하지 않으면 0이다.
- REPORT.md에 입력 행 수, 유효 행 수, invalid 행 수, 부족한 제품 수와 실제 실행한 검증을 적는다. 새 CLI의 입력·출력 경로를 명시적으로 받는다.
- 원본 입력을 변경하거나 외부로 전송하지 않는다. 실제 실행하지 않은 검증·사용자 확인을 기록하지 않는다.
