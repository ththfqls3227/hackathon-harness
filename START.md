# 제공된 Codex에서 시작·재개

이 문서와 하네스 내부 링크의 상대경로는 각 문서 위치를 기준으로 읽는다. 하네스를 과제 작업 루트로 오인하지 않는다.

1. 실제 과제 README·기존 AGENTS.md를 읽고, 하네스 [작업 계약](AGENTS.md)과 [현재 규정](docs/exam-contract.md)을 적용한다. 현재 단계가 제출물 확정·후속 서술형이면 AI 작업을 중단한다. 재시험의 날짜·시간은 과거 일정에서 가져오지 않는다.
2. 현재 위치와 제한된 파일 목록으로 과제 루트·필수 산출물·기존 구현을 확인한다. 코드 외의 필수 작성 항목과 플랫폼 입력 항목도 출처·작성 단계·AI 허용 범위별로 확인하며 개수를 고정하지 않는다. 사용 가능한 실행 명령, 테스트, 제공 Codex의 스킬·하위 에이전트 지원을 필요한 만큼 확인한다. 인증 파일·전체 환경변수를 읽거나 버전·전역 설정을 바꾸지 않는다.
3. 첫 응답은 **작업 루트 / 현재 단계·남은 시간 / 필수 결과물 / 선택한 흐름 / 다음 행동**을 짧게 정리한다. 파일에서 알 수 있는 사실을 사용자에게 다시 묻지 않는다. 시간이 전달되지 않았다면 미확인으로 남기고 독립적인 읽기부터 진행한다.
4. 새 과제는 [task-flow](.agents/skills/task-flow/SKILL.md)로 진행한다. 기존 작업은 과제 안의 기록·변경 파일·마지막 실행 결과를 대조한 뒤 이어간다. 필요한 스킬만 아래에서 읽으며, 스킬 이름이나 역할 카드만으로 도구가 설치·지원된다고 가정하지 않는다.

| 지금 필요한 일 | 읽을 스킬 |
|---|---|
| 업무 문제·핵심 질문·대안·최소 범위 | [task-scope](.agents/skills/task-scope/SKILL.md) |
| 구현·검토·시간 배분·장애 후 재개 | [task-flow](.agents/skills/task-flow/SKILL.md) |
| 작업 중 필수 문서 작성·기록에 근거한 이해 점검 | [task-understanding](.agents/skills/task-understanding/SKILL.md) |
| 공개 원본 스킬·키트를 고정 버전으로 받아 사용 | [upstream-skills](.agents/skills/upstream-skills/SKILL.md) |
| 요구사항·동작·제출 파일 검증 | [task-verify](.agents/skills/task-verify/SKILL.md) |
| 현재 과제에서 허용된 자체 웹 Playwright 검증 | [web-verify](.agents/skills/web-verify/SKILL.md) |
| 로컬 CSV 구조·결측 확인 | [data-check](.agents/skills/data-check/SKILL.md) |
| 핵심 화면·접근성·실패 상태 | [ui-review](.agents/skills/ui-review/SKILL.md) |
| 근거 있는 SVG·HTML 도해 | [system-diagram](.agents/skills/system-diagram/SKILL.md) |

문제 정의 → 대안과 선택 이유 → 작은 구현 → 실제 검증을 연결한다. 작은 수정에는 전체 기획을 반복하지 않는다. 업무 결정 질문과 참가자의 이해 점검 질문을 구분하며, 답과 독립적인 되돌릴 수 있는 작업은 계속한다. 검증 후에는 바뀐 점·실행 결과·남은 문제·다음 행동을 간결하게 전달한다.

프로젝트 진입 스킬이 보이지 않아도 이 파일을 명시적으로 읽으면 같은 흐름을 사용할 수 있다. 자동 등록 실패를 Codex 업데이트나 개인 설정 반입으로 해결하지 않는다. 이 문서는 모델 능력이나 허용 권한을 바꾸는 실행기가 아니다.
