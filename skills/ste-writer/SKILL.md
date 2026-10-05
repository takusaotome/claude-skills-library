---
name: "ste-writer"
description: "Write new English text, or rewrite existing text, in ASD-STE100 Simplified Technical English. Use for STE, simple technical English, ASD-STE100, or 80% STE, for writing or rewriting procedures, manuals, SOPs, runbooks, and release notes."
---

# ste-writer

Write English that follows the main writing rules of ASD-STE100 (Simplified Technical English). This works in two situations:

- **Rewrite:** the user gives existing text and wants it converted.
- **Write new:** the user gives facts, notes, bullet points, a topic, or code and wants a new document written in STE from the start.

## Why this works

STE exists so that a reader who knows only a little English can follow instructions with no risk of misreading them. The method is simple: one meaning per word, one idea per sentence, and no clever phrasing. The result reads a little plain, but every sentence has one clear meaning. It also machine-translates well.

## Be honest about what this is

This skill applies the core rules from memory. It does not include the official ASD-STE100 specification or its approved-word Dictionary. Do not claim the output is "STE-compliant" or "certified". Say it is "written to the main ASD-STE100 rules". If the user needs formal compliance, tell them to check the result with the official Dictionary or a checker tool. If they provide the spec or a word list, follow it over these notes.

## Choose the strictness

Default to **full** (apply every rule below). If the user asks for a softer result ("80%", "lightly", "keep my tone"), use **soft** mode: apply rules 1 to 6, keep the author's technical terms and natural rhythm, and allow some longer sentences up to about 25 words. State which mode you used.

## Core rules

1. **One instruction per sentence.** In a procedure, write each action as its own numbered step. Keep procedure sentences to 20 words or fewer. Keep descriptive sentences to 25 words or fewer.
2. **Use the imperative for actions.** "Remove the cover." Not "The cover should be removed." Put the command first, then the reason or condition after it.
3. **Use the active voice.** Name who or what does the action. Use the passive only when the actor is unknown or unimportant, and keep it rare in procedures.
4. **Use simple verb tenses only.** Use the simple present, simple past, and future ("will"). Avoid the perfect ("has been done"), the progressive ("is running"), conditional ("would", "could"), and subjunctive forms.
5. **Keep one word for one meaning.** Pick one term for each thing and use it every time, even if it sounds repetitive. Do not swap in synonyms for variety. Use each word only as the part of speech it is mostly used as ("test" as a noun or a verb, but do not turn a noun into a verb on your own).
6. **Choose the simple, common word.** "Use", not "utilize". "Start", not "commence". "Show", not "demonstrate". Keep real technical names as they are, such as part names, product names, and standard terms of the field. See the word swaps below.
7. **Keep articles and short helper words.** Write "the", "a", and "an". Do not drop them to save space, and do not write telegraphic text.
8. **Break up noun clusters.** Use at most three nouns in a row. Rewrite "hydraulic pump pressure relief valve adjustment screw" as "the screw that adjusts the relief valve of the hydraulic pump".
9. **Avoid ambiguous phrasal verbs and idioms.** Replace "set up", "carry out", "figure out", "back off" with a single clear verb such as "install", "do", "find", "loosen". Cut idioms and metaphors entirely.
10. **Avoid contractions and unclear pronouns.** Write "do not", not "don't". Repeat the noun if "it" or "this" could point to more than one thing.
11. **Group related sentences into short paragraphs.** One topic per paragraph, at most six sentences. Put the main point in the first sentence.
12. **Give warnings and cautions first.** Put them before the step they apply to. Write them as a clear command and give the reason. Use "WARNING" for danger to people and "CAUTION" for danger to equipment or data.
13. **Use "must" for requirements, "can" for ability, and "may" for permission.** Avoid "should", "might", "would", and "ought to", which blur whether a step is required.
14. **Write numbers as digits** and keep the unit with the number ("5 mm", "30 seconds"). Use words only for "one" when it is not a measurement.

## Word swaps

These are typical simplifications. Keep a word if it is an approved technical name in the user's field, and keep the same replacement every time in one document.

| Avoid | Use |
|---|---|
| utilize | use |
| commence, initiate | start |
| terminate | stop, end |
| demonstrate, indicate | show |
| ensure | make sure |
| verify | check |
| prior to | before |
| subsequent to, following | after |
| in order to | to |
| in the event that | if |
| approximately | about |
| sufficient | enough |
| require (verb) | need |
| obtain | get |
| attempt (verb) | try |
| assist | help |
| purchase | buy |
| set up, carry out, figure out | install or prepare, do, find |
| back off (a screw) | loosen |
| a number of | some, several (or give the number) |
| it is recommended that | use a command: "Do this." |
| should | must (if required), or rewrite as a command |
| could, would, might | can, will, or remove the doubt |
| don't, can't, won't | do not, cannot, will not |
| ASAP | as soon as possible, or give the time |

Common patterns:

- Passive to command: "The filter shall be replaced every 100 hours." becomes "Replace the filter every 100 hours."
- Two actions to two steps: "Disconnect the cable and remove the cover." becomes "1. Disconnect the cable. 2. Remove the cover."
- Long noun cluster to a phrase: "engine oil pressure sensor connector" becomes "the connector of the engine oil pressure sensor".
- Hidden condition to "If": "In case of leakage, stop." becomes "If there is a leak, stop."

## Workflow

### When rewriting existing text

1. Read the whole text first. Note the technical terms that must not change, and the one term chosen for each concept.
2. Rewrite section by section. Keep the facts, order, and structure (headings, lists, tables, code, links, version numbers) exactly as they are. Never add facts that the source does not give.
3. If a sentence is too vague to rewrite without guessing (a missing actor, an unclear "it", a missing value), do not invent an answer. Rewrite it as clearly as possible, mark the spot with `[CHECK: ...]`, and list it in the notes.
4. Reread the output once against rules 1 to 6 and 9. Split any sentence that still holds two actions.

### When writing new text

1. Find out the reader and the job of the document: who reads it, what they must be able to do, and which kind of document it is (procedure, description, warning, release note). If the user gave only a topic and the facts are missing, ask for them in one short message. If the user is not available to answer, write what the given facts support and mark every gap with `[CHECK: ...]`.
2. Decide the key terms first. Choose one name for each part, tool, screen, and action, and use it every time.
3. Pick the structure that fits the job. Procedures: a one-line purpose, then numbered steps in time order, with warnings before the step they apply to. Descriptions: the main point first, then short paragraphs with one topic each. Release notes: one change per line, starting with a verb.
4. Write from the facts the user gave. Do not invent values, names, limits, or steps. A missing value, such as a torque, a time, or a command, gets a `[CHECK: ...]` marker, not a guess.
5. Reread the draft once against rules 1 to 6 and 9.

## Output format

Reply in the language the user wrote their request in, but keep the document itself in English.

Give, in this order:

1. The document, in a format that suits where it will be used (Markdown stays Markdown; plain text stays plain text). When rewriting a file, write the result to a new file next to it and do not overwrite the original.
2. For a rewrite, a short **Changes** list of the 3 to 6 most important kinds of change, each with one before/after example from the text. For new text, a short list of the key terms that were chosen, so the user can keep them the same in later documents.
3. A **Questions for the author** list for every `[CHECK: ...]` spot. Skip this if there are none.
4. One line giving the mode (full or soft) and the reminder that this is not official certification.

Keep the notes short. The user wants the document first, not an essay about the rules.

## Examples

Rewrite. Input:
"Before the unit is powered on, it should be ensured that all of the connectors have been properly seated, otherwise damage could occur."

Output:
"CAUTION: Make sure that all connectors are fully connected before you start the unit. If a connector is loose, the unit can be damaged."

Notes: the passive was changed to a command, the perfect tense was removed, "should be ensured" became "Make sure", and the caution was moved to the front with its reason.

Write new. Input facts: "Reset procedure for the badge printer. Hold the button, wait for the light. Takes about a minute. Unplug first."

Output:
"# Reset the badge printer\n\nUse this procedure to reset the badge printer to its factory settings.\n\nCAUTION: Disconnect the power cable before you start. [CHECK: Is the reason for this step known? Add it if it is.]\n\n1. Disconnect the power cable.\n2. Connect the power cable.\n3. Push and hold the button. [CHECK: How long must the user hold the button?]\n4. Wait until the light comes on. [CHECK: Which color is the light?]\n5. Wait 1 minute for the reset to end.\"

Notes: the facts did not give the hold time or the light color, so those spots are marked and not guessed. The order of the first steps follows the facts the user gave.
