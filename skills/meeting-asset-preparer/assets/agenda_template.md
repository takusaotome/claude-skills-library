# Meeting Agenda / 会議アジェンダ

**Title / タイトル**: {{title}}
**Date / 日時**: {{date}} {{time}} {{timezone}}
**Duration / 所要時間**: {{duration_minutes}} minutes / 分

---

## Objectives / 目的

{{#objectives}}
- {{.}}
{{/objectives}}

---

## Attendees / 参加者

| Name / 名前 | Role / 役割 |
|-------------|-------------|
{{#attendees}}
| {{name}} | {{role}} |
{{/attendees}}

---

## Agenda Items / 議題

| # | Topic / 議題 | Duration / 時間 | Presenter / 担当 | Notes / 備考 |
|---|--------------|-----------------|------------------|--------------|
{{#agenda_items}}
| {{index}} | {{topic}} | {{duration}} min | {{presenter}} | {{notes}} |
{{/agenda_items}}

---

## Pre-Reading Materials / 事前資料

{{#references}}
- [{{title}}]({{path}})
{{/references}}

---

## Notes / 備考

_Space for additional notes and context / 追加メモ用スペース_

---

**Next Meeting / 次回会議**: {{next_meeting_date}}
