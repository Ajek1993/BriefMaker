"""BriefApp - aplikacja do tworzenia briefów projektowych."""

import json
from pathlib import Path

import gradio as gr

from templates import get_prompt

PROJECT_FILE = Path(__file__).parent / "project.json"


def get_empty_state() -> dict:
    """Zwraca pusty stan projektu ze wszystkimi kluczami."""
    return {
        "brief": "",
        "extra_questions": [],  # Lista dodatkowych pytań [{"q": "pytanie", "a": "odpowiedź"}, ...]
        "model_responses": ["", ""],  # Lista odpowiedzi modeli (min 2)
        "improved_brief": "",
        "technology": "",
        "stages": "",
        "work_plan": "",
        "control": "",  # plan_final_v2 - finalny plan po kontroli
    }


def load_project() -> dict:
    """Wczytuje stan projektu z pliku JSON.

    Returns:
        Dict ze stanem projektu lub pusty stan jeśli plik nie istnieje.
    """
    if not PROJECT_FILE.exists():
        return get_empty_state()

    try:
        with open(PROJECT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Uzupełnij brakujące klucze
        empty = get_empty_state()
        for key in empty:
            if key not in data:
                data[key] = empty[key]
        return data
    except (json.JSONDecodeError, IOError):
        return get_empty_state()


def save_project(data: dict) -> bool:
    """Zapisuje stan projektu do pliku JSON.

    Args:
        data: Dict ze stanem projektu do zapisania.

    Returns:
        True jeśli zapis się powiódł, False w przypadku błędu.
    """
    try:
        with open(PROJECT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False


def generate_brief_md(co_boli: str, dla_kogo: str, potrzeby: str, ryzyka: str, extra_questions: list = None) -> str:
    """Generuje brief w formacie Markdown z odpowiedzi na pytania."""
    brief = f"""# Brief projektu

## Co boli?
{co_boli}

## Dla kogo to rozwiązanie?
{dla_kogo}

## Jakie są główne potrzeby?
{potrzeby}

## Co może pójść nie tak?
{ryzyka}
"""
    # Dodaj dodatkowe pytania jeśli istnieją
    if extra_questions:
        for eq in extra_questions:
            if eq.get("q") and eq.get("a"):
                brief += f"\n## {eq['q']}\n{eq['a']}\n"

    return brief


def format_model_responses(responses: list) -> str:
    """Formatuje odpowiedzi modeli do wstawienia w prompt."""
    formatted = []
    for i, resp in enumerate(responses, 1):
        if resp.strip():
            formatted.append(f"### Model {i}:\n{resp}")
    return "\n\n".join(formatted)


# --- GUI ---

def create_app():
    """Tworzy i zwraca aplikację Gradio."""

    with gr.Blocks(title="BriefApp") as app:
        gr.Markdown("# BriefApp - Kreator briefów projektowych")

        # Wczytaj zapisany stan
        saved_state = load_project()

        with gr.Tabs() as tabs:
            # === Zakładka 1: Brief ===
            with gr.Tab("1. Brief", id=0):
                gr.Markdown("### Odpowiedz na pytania, aby stworzyć brief projektu")

                # Podstawowe pytania
                co_boli = gr.Textbox(
                    label="Co boli? (jaki problem rozwiązujesz)",
                    lines=3,
                    placeholder="Opisz problem, który chcesz rozwiązać..."
                )
                dla_kogo = gr.Textbox(
                    label="Dla kogo to rozwiązanie?",
                    lines=2,
                    placeholder="Kto będzie użytkownikiem..."
                )
                potrzeby = gr.Textbox(
                    label="Jakie są główne potrzeby?",
                    lines=3,
                    placeholder="Wymień kluczowe funkcje i wymagania..."
                )
                ryzyka = gr.Textbox(
                    label="Co może pójść nie tak?",
                    lines=3,
                    placeholder="Potencjalne problemy, edge cases..."
                )

                # Dodatkowe pytania (max 5, początkowo ukryte)
                gr.Markdown("#### Dodatkowe pytania (opcjonalne)")

                # Wczytaj zapisane dodatkowe pytania
                saved_extra = saved_state.get("extra_questions", [])

                extra_q1 = gr.Textbox(label="Dodatkowe pytanie 1", lines=1, visible=len(saved_extra) > 0,
                                       value=saved_extra[0]["q"] if len(saved_extra) > 0 else "")
                extra_a1 = gr.Textbox(label="Odpowiedź 1", lines=2, visible=len(saved_extra) > 0,
                                       value=saved_extra[0]["a"] if len(saved_extra) > 0 else "")

                extra_q2 = gr.Textbox(label="Dodatkowe pytanie 2", lines=1, visible=len(saved_extra) > 1,
                                       value=saved_extra[1]["q"] if len(saved_extra) > 1 else "")
                extra_a2 = gr.Textbox(label="Odpowiedź 2", lines=2, visible=len(saved_extra) > 1,
                                       value=saved_extra[1]["a"] if len(saved_extra) > 1 else "")

                extra_q3 = gr.Textbox(label="Dodatkowe pytanie 3", lines=1, visible=len(saved_extra) > 2,
                                       value=saved_extra[2]["q"] if len(saved_extra) > 2 else "")
                extra_a3 = gr.Textbox(label="Odpowiedź 3", lines=2, visible=len(saved_extra) > 2,
                                       value=saved_extra[2]["a"] if len(saved_extra) > 2 else "")

                # Stan licznika dodatkowych pytań
                extra_count = gr.State(value=len(saved_extra))

                btn_add_question = gr.Button("+ Dodaj pytanie", variant="secondary", size="sm")

                def add_extra_question(count):
                    count = min(count + 1, 3)
                    return (
                        count,
                        gr.update(visible=count >= 1), gr.update(visible=count >= 1),
                        gr.update(visible=count >= 2), gr.update(visible=count >= 2),
                        gr.update(visible=count >= 3), gr.update(visible=count >= 3),
                    )

                btn_add_question.click(
                    fn=add_extra_question,
                    inputs=[extra_count],
                    outputs=[extra_count, extra_q1, extra_a1, extra_q2, extra_a2, extra_q3, extra_a3]
                )

                gr.Markdown("---")
                btn_generuj = gr.Button("Generuj brief", variant="primary")

                brief_output = gr.Textbox(
                    label="Wygenerowany brief (skopiuj do modeli AI)",
                    lines=15,
                    interactive=False,
                    value=saved_state.get("brief", "")
                )

                btn_dalej_1 = gr.Button("Dalej →", variant="secondary")
                status_1 = gr.Markdown("")

                # Funkcja generowania briefu
                def on_generuj(co_boli, dla_kogo, potrzeby, ryzyka, eq1, ea1, eq2, ea2, eq3, ea3):
                    if not all([co_boli.strip(), dla_kogo.strip(), potrzeby.strip(), ryzyka.strip()]):
                        return gr.update(), "**Wypełnij wszystkie podstawowe pola!**"

                    # Zbierz dodatkowe pytania
                    extra = []
                    if eq1.strip() and ea1.strip():
                        extra.append({"q": eq1, "a": ea1})
                    if eq2.strip() and ea2.strip():
                        extra.append({"q": eq2, "a": ea2})
                    if eq3.strip() and ea3.strip():
                        extra.append({"q": eq3, "a": ea3})

                    brief = generate_brief_md(co_boli, dla_kogo, potrzeby, ryzyka, extra)

                    # Zapisz dodatkowe pytania w state
                    state = load_project()
                    state["extra_questions"] = extra
                    save_project(state)

                    return brief, ""

                btn_generuj.click(
                    fn=on_generuj,
                    inputs=[co_boli, dla_kogo, potrzeby, ryzyka, extra_q1, extra_a1, extra_q2, extra_a2, extra_q3, extra_a3],
                    outputs=[brief_output, status_1]
                )

                # Funkcja "Dalej" - zapisuje stan
                def on_dalej_1(brief):
                    if not brief.strip():
                        return gr.update(selected=0), "**Najpierw wygeneruj brief!**"
                    state = load_project()
                    state["brief"] = brief
                    save_project(state)
                    return gr.update(selected=1), ""

                btn_dalej_1.click(
                    fn=on_dalej_1,
                    inputs=[brief_output],
                    outputs=[tabs, status_1]
                )

            # === Zakładka 2: Oceny modeli ===
            with gr.Tab("2. Oceny modeli", id=1):
                gr.Markdown("### Wklej odpowiedzi od modeli AI (minimum 2)")
                gr.Markdown("Skopiuj brief i wyślij do różnych modeli (np. GPT, Gemini, Claude). Wklej ich oceny poniżej.")

                brief_readonly_2 = gr.Textbox(
                    label="Twój brief (skopiuj i wyślij do modeli)",
                    lines=10,
                    interactive=False,
                    value=saved_state.get("brief", "")
                )

                # Wczytaj zapisane odpowiedzi modeli
                saved_models = saved_state.get("model_responses", ["", ""])
                # Upewnij się, że mamy min 2 elementy
                while len(saved_models) < 2:
                    saved_models.append("")

                # Modele 1-2 (wymagane, zawsze widoczne)
                model1_input = gr.Textbox(
                    label="Odpowiedź Model 1 (wymagane)",
                    lines=6,
                    placeholder="Wklej odpowiedź od pierwszego modelu...",
                    value=saved_models[0] if len(saved_models) > 0 else ""
                )
                model2_input = gr.Textbox(
                    label="Odpowiedź Model 2 (wymagane)",
                    lines=6,
                    placeholder="Wklej odpowiedź od drugiego modelu...",
                    value=saved_models[1] if len(saved_models) > 1 else ""
                )

                # Modele 3-5 (opcjonalne, początkowo ukryte)
                model3_input = gr.Textbox(
                    label="Odpowiedź Model 3 (opcjonalne)",
                    lines=6,
                    placeholder="Wklej odpowiedź od trzeciego modelu...",
                    visible=len(saved_models) > 2 and saved_models[2],
                    value=saved_models[2] if len(saved_models) > 2 else ""
                )
                model4_input = gr.Textbox(
                    label="Odpowiedź Model 4 (opcjonalne)",
                    lines=6,
                    placeholder="Wklej odpowiedź od czwartego modelu...",
                    visible=len(saved_models) > 3 and saved_models[3],
                    value=saved_models[3] if len(saved_models) > 3 else ""
                )
                model5_input = gr.Textbox(
                    label="Odpowiedź Model 5 (opcjonalne)",
                    lines=6,
                    placeholder="Wklej odpowiedź od piątego modelu...",
                    visible=len(saved_models) > 4 and saved_models[4],
                    value=saved_models[4] if len(saved_models) > 4 else ""
                )

                # Licznik widocznych modeli
                visible_models = gr.State(value=max(2, sum(1 for m in saved_models if m.strip())))

                btn_add_model = gr.Button("+ Dodaj model", variant="secondary", size="sm")

                def add_model(count):
                    count = min(count + 1, 5)
                    return (
                        count,
                        gr.update(visible=count >= 3),
                        gr.update(visible=count >= 4),
                        gr.update(visible=count >= 5),
                    )

                btn_add_model.click(
                    fn=add_model,
                    inputs=[visible_models],
                    outputs=[visible_models, model3_input, model4_input, model5_input]
                )

                btn_dalej_2 = gr.Button("Dalej →", variant="secondary")
                status_2 = gr.Markdown("")

                # Aktualizuj brief gdy zmieni się w zakładce 1
                btn_dalej_1.click(
                    fn=lambda b: b,
                    inputs=[brief_output],
                    outputs=[brief_readonly_2]
                )

                # Funkcja "Dalej" - zapisuje odpowiedzi modeli
                def on_dalej_2(m1, m2, m3, m4, m5):
                    if not all([m1.strip(), m2.strip()]):
                        return gr.update(selected=1), "**Wypełnij odpowiedzi od minimum 2 modeli!**"

                    # Zbierz wszystkie niepuste odpowiedzi
                    responses = [m for m in [m1, m2, m3, m4, m5] if m.strip()]

                    state = load_project()
                    state["model_responses"] = responses
                    save_project(state)
                    return gr.update(selected=2), ""

                btn_dalej_2.click(
                    fn=on_dalej_2,
                    inputs=[model1_input, model2_input, model3_input, model4_input, model5_input],
                    outputs=[tabs, status_2]
                )

            # === Zakładka 3: Ulepszony brief ===
            with gr.Tab("3. Ulepszony brief", id=2):
                gr.Markdown("### Ulepszony brief na podstawie ocen modeli")
                gr.Markdown("Skopiuj prompt poniżej, wyślij do modelu AI i wklej odpowiedź.")

                # Generuj prompt z zapisanych danych
                prompt_3_initial = ""
                saved_responses = saved_state.get("model_responses", [])
                if saved_state.get("brief") and saved_responses:
                    prompt_3_initial = get_prompt(
                        "improve_brief",
                        brief=saved_state.get("brief", ""),
                        model_responses=format_model_responses(saved_responses)
                    )

                prompt_3 = gr.Textbox(
                    label="Prompt do skopiowania",
                    lines=12,
                    interactive=False,
                    value=prompt_3_initial
                )

                response_3 = gr.Textbox(
                    label="Wklej odpowiedź od modelu",
                    lines=10,
                    placeholder="Wklej tutaj ulepszony brief...",
                    value=saved_state.get("improved_brief", "")
                )

                btn_dalej_3 = gr.Button("Dalej →", variant="secondary")
                status_3 = gr.Markdown("")

                # Aktualizuj prompt gdy przejdziemy z zakładki 2
                def update_prompt_3():
                    state = load_project()
                    responses = state.get("model_responses", [])
                    if state.get("brief") and responses:
                        return get_prompt(
                            "improve_brief",
                            brief=state.get("brief", ""),
                            model_responses=format_model_responses(responses)
                        )
                    return "Brak danych - wróć do poprzednich kroków"

                btn_dalej_2.click(fn=update_prompt_3, outputs=[prompt_3])

                def on_dalej_3(response):
                    if not response.strip():
                        return gr.update(selected=2), "**Wklej odpowiedź od modelu!**"
                    state = load_project()
                    state["improved_brief"] = response
                    save_project(state)
                    return gr.update(selected=3), ""

                btn_dalej_3.click(
                    fn=on_dalej_3,
                    inputs=[response_3],
                    outputs=[tabs, status_3]
                )

            # === Zakładka 4: Technologia ===
            with gr.Tab("4. Technologia", id=3):
                gr.Markdown("### Wybór technologii")
                gr.Markdown("Skopiuj prompt, wyślij do modelu AI i wklej propozycję stosu technologicznego.")

                prompt_4_initial = ""
                if saved_state.get("improved_brief"):
                    prompt_4_initial = get_prompt("technology", brief=saved_state.get("improved_brief", ""))

                prompt_4 = gr.Textbox(
                    label="Prompt do skopiowania",
                    lines=12,
                    interactive=False,
                    value=prompt_4_initial
                )

                response_4 = gr.Textbox(
                    label="Wklej odpowiedź od modelu",
                    lines=10,
                    placeholder="Wklej tutaj propozycję technologii...",
                    value=saved_state.get("technology", "")
                )

                btn_dalej_4 = gr.Button("Dalej →", variant="secondary")
                status_4 = gr.Markdown("")

                def update_prompt_4():
                    state = load_project()
                    if state.get("improved_brief"):
                        return get_prompt("technology", brief=state.get("improved_brief", ""))
                    return "Brak danych - wróć do poprzednich kroków"

                btn_dalej_3.click(fn=update_prompt_4, outputs=[prompt_4])

                def on_dalej_4(response):
                    if not response.strip():
                        return gr.update(selected=3), "**Wklej odpowiedź od modelu!**"
                    state = load_project()
                    state["technology"] = response
                    save_project(state)
                    return gr.update(selected=4), ""

                btn_dalej_4.click(
                    fn=on_dalej_4,
                    inputs=[response_4],
                    outputs=[tabs, status_4]
                )

            # === Zakładka 5: Etapy ===
            with gr.Tab("5. Etapy", id=4):
                gr.Markdown("### Podział na etapy realizacji")
                gr.Markdown("Skopiuj prompt, wyślij do modelu AI i wklej podział projektu na etapy.")

                prompt_5_initial = ""
                if saved_state.get("technology"):
                    prompt_5_initial = get_prompt("stages", brief=saved_state.get("technology", ""))

                prompt_5 = gr.Textbox(
                    label="Prompt do skopiowania",
                    lines=12,
                    interactive=False,
                    value=prompt_5_initial
                )

                response_5 = gr.Textbox(
                    label="Wklej odpowiedź od modelu",
                    lines=10,
                    placeholder="Wklej tutaj etapy realizacji...",
                    value=saved_state.get("stages", "")
                )

                btn_dalej_5 = gr.Button("Dalej →", variant="secondary")
                status_5 = gr.Markdown("")

                def update_prompt_5():
                    state = load_project()
                    if state.get("technology"):
                        return get_prompt("stages", brief=state.get("technology", ""))
                    return "Brak danych - wróć do poprzednich kroków"

                btn_dalej_4.click(fn=update_prompt_5, outputs=[prompt_5])

                def on_dalej_5(response):
                    if not response.strip():
                        return gr.update(selected=4), "**Wklej odpowiedź od modelu!**"
                    state = load_project()
                    state["stages"] = response
                    save_project(state)
                    return gr.update(selected=5), ""

                btn_dalej_5.click(
                    fn=on_dalej_5,
                    inputs=[response_5],
                    outputs=[tabs, status_5]
                )

            # === Zakładka 6: Plan prac ===
            with gr.Tab("6. Plan prac", id=5):
                gr.Markdown("### Szczegółowy plan prac")
                gr.Markdown("Skopiuj prompt, wyślij do modelu AI i wklej szczegółowy plan implementacji.")

                prompt_6_initial = ""
                if saved_state.get("technology") and saved_state.get("stages"):
                    prompt_6_initial = get_prompt(
                        "work_plan",
                        brief=saved_state.get("technology", ""),
                        stages=saved_state.get("stages", "")
                    )

                prompt_6 = gr.Textbox(
                    label="Prompt do skopiowania",
                    lines=12,
                    interactive=False,
                    value=prompt_6_initial
                )

                response_6 = gr.Textbox(
                    label="Wklej odpowiedź od modelu",
                    lines=10,
                    placeholder="Wklej tutaj plan prac...",
                    value=saved_state.get("work_plan", "")
                )

                btn_dalej_6 = gr.Button("Dalej →", variant="secondary")
                status_6 = gr.Markdown("")

                def update_prompt_6():
                    state = load_project()
                    if state.get("technology") and state.get("stages"):
                        return get_prompt(
                            "work_plan",
                            brief=state.get("technology", ""),
                            stages=state.get("stages", "")
                        )
                    return "Brak danych - wróć do poprzednich kroków"

                btn_dalej_5.click(fn=update_prompt_6, outputs=[prompt_6])

                def on_dalej_6(response):
                    if not response.strip():
                        return gr.update(selected=5), "**Wklej odpowiedź od modelu!**"
                    state = load_project()
                    state["work_plan"] = response
                    save_project(state)
                    return gr.update(selected=6), ""

                btn_dalej_6.click(
                    fn=on_dalej_6,
                    inputs=[response_6],
                    outputs=[tabs, status_6]
                )

            # === Zakładka 7: Kontrola ===
            with gr.Tab("7. Kontrola", id=6):
                gr.Markdown("### Kontrola zgodności")
                gr.Markdown("Skopiuj prompt, wyślij do modelu AI i wklej weryfikację spójności planu.")

                prompt_7_initial = ""
                if saved_state.get("technology") and saved_state.get("stages") and saved_state.get("work_plan"):
                    prompt_7_initial = get_prompt(
                        "control",
                        brief=saved_state.get("technology", ""),
                        stages=saved_state.get("stages", ""),
                        work_plan=saved_state.get("work_plan", "")
                    )

                prompt_7 = gr.Textbox(
                    label="Prompt do skopiowania",
                    lines=12,
                    interactive=False,
                    value=prompt_7_initial
                )

                response_7 = gr.Textbox(
                    label="Wklej odpowiedź od modelu",
                    lines=10,
                    placeholder="Wklej tutaj wyniki kontroli...",
                    value=saved_state.get("control", "")
                )

                btn_dalej_7 = gr.Button("Dalej →", variant="secondary")
                status_7 = gr.Markdown("")

                def update_prompt_7():
                    state = load_project()
                    if state.get("technology") and state.get("stages") and state.get("work_plan"):
                        return get_prompt(
                            "control",
                            brief=state.get("technology", ""),
                            stages=state.get("stages", ""),
                            work_plan=state.get("work_plan", "")
                        )
                    return "Brak danych - wróć do poprzednich kroków"

                btn_dalej_6.click(fn=update_prompt_7, outputs=[prompt_7])

                def on_dalej_7(response):
                    if not response.strip():
                        return gr.update(selected=6), "**Wklej odpowiedź od modelu!**"
                    state = load_project()
                    state["control"] = response
                    save_project(state)
                    return gr.update(selected=7), ""

                btn_dalej_7.click(
                    fn=on_dalej_7,
                    inputs=[response_7],
                    outputs=[tabs, status_7]
                )

            # === Zakładka 8: Export ===
            with gr.Tab("8. Export", id=7):
                gr.Markdown("### Export plików projektu")
                gr.Markdown("Pobierz 4 pliki z wynikami pracy:")

                # Podgląd finalnego planu (plan_final_v2)
                def get_final_plan():
                    state = load_project()
                    return state.get("control", "Brak danych - przejdź przez wszystkie kroki")

                final_md = gr.Textbox(
                    label="Podgląd: plan_final_v2.md (finalny plan po kontroli)",
                    lines=15,
                    interactive=False,
                    value=get_final_plan()
                )

                # Aktualizuj podgląd gdy przejdziemy z zakładki 7
                btn_dalej_7.click(fn=get_final_plan, outputs=[final_md])

                gr.Markdown("---")
                gr.Markdown("#### Pobierz pliki:")

                with gr.Row():
                    btn_save_tech = gr.Button("brief_technology.md", variant="secondary")
                    btn_save_etaps = gr.Button("etaps.md", variant="secondary")

                with gr.Row():
                    btn_save_plan = gr.Button("plan_final.md", variant="secondary")
                    btn_save_plan_v2 = gr.Button("plan_final_v2.md", variant="primary")

                gr.Markdown("---")

                with gr.Row():
                    btn_save_all = gr.Button("Zapisz wszystkie 4 pliki", variant="primary")
                    btn_new = gr.Button("Nowy projekt", variant="secondary")

                status_8 = gr.Markdown("")

                output_dir = Path(__file__).parent / "output"

                def save_file(filename, content_key):
                    """Zapisuje pojedynczy plik."""
                    state = load_project()
                    content = state.get(content_key, "")
                    if not content:
                        return f"**Brak danych dla {filename}**"
                    try:
                        output_dir.mkdir(exist_ok=True)
                        filepath = output_dir / filename
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(content)
                        return f"**Zapisano:** `{filepath}`"
                    except IOError as e:
                        return f"**Błąd:** {e}"

                btn_save_tech.click(
                    fn=lambda: save_file("brief_technology.md", "technology"),
                    outputs=[status_8]
                )
                btn_save_etaps.click(
                    fn=lambda: save_file("etaps.md", "stages"),
                    outputs=[status_8]
                )
                btn_save_plan.click(
                    fn=lambda: save_file("plan_final.md", "work_plan"),
                    outputs=[status_8]
                )
                btn_save_plan_v2.click(
                    fn=lambda: save_file("plan_final_v2.md", "control"),
                    outputs=[status_8]
                )

                def save_all_files():
                    """Zapisuje wszystkie 4 pliki."""
                    state = load_project()
                    files = [
                        ("brief_technology.md", "technology"),
                        ("etaps.md", "stages"),
                        ("plan_final.md", "work_plan"),
                        ("plan_final_v2.md", "control"),
                    ]
                    try:
                        output_dir.mkdir(exist_ok=True)
                        saved = []
                        for filename, key in files:
                            content = state.get(key, "")
                            if content:
                                filepath = output_dir / filename
                                with open(filepath, "w", encoding="utf-8") as f:
                                    f.write(content)
                                saved.append(filename)
                        if saved:
                            return f"**Zapisano {len(saved)} plików do:** `{output_dir}`\n\n" + ", ".join(saved)
                        return "**Brak danych do zapisania**"
                    except IOError as e:
                        return f"**Błąd:** {e}"

                btn_save_all.click(fn=save_all_files, outputs=[status_8])

                def on_new_project():
                    """Czyści stan i wraca do zakładki 1."""
                    if PROJECT_FILE.exists():
                        PROJECT_FILE.unlink()
                    return (
                        gr.update(selected=0),  # tabs
                        # Zakładka 1 - podstawowe
                        "", "", "", "",  # co_boli, dla_kogo, potrzeby, ryzyka
                        "",  # brief_output
                        # Zakładka 1 - dodatkowe pytania
                        gr.update(visible=False), gr.update(visible=False),  # eq1, ea1
                        gr.update(visible=False), gr.update(visible=False),  # eq2, ea2
                        gr.update(visible=False), gr.update(visible=False),  # eq3, ea3
                        # Zakładka 2
                        "",  # brief_readonly_2
                        "", "",  # model1, model2 (wymagane)
                        gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),  # model3-5
                        # Zakładka 3
                        "", "",  # prompt_3, response_3
                        # Zakładka 4
                        "", "",  # prompt_4, response_4
                        # Zakładka 5
                        "", "",  # prompt_5, response_5
                        # Zakładka 6
                        "", "",  # prompt_6, response_6
                        # Zakładka 7
                        "", "",  # prompt_7, response_7
                        # Zakładka 8
                        "",  # final_md
                        "**Utworzono nowy projekt**",  # status
                    )

                btn_new.click(
                    fn=on_new_project,
                    outputs=[
                        tabs,
                        # Zakładka 1 - podstawowe
                        co_boli, dla_kogo, potrzeby, ryzyka, brief_output,
                        # Zakładka 1 - dodatkowe pytania
                        extra_q1, extra_a1, extra_q2, extra_a2, extra_q3, extra_a3,
                        # Zakładka 2
                        brief_readonly_2, model1_input, model2_input,
                        model3_input, model4_input, model5_input,
                        # Zakładka 3
                        prompt_3, response_3,
                        # Zakładka 4
                        prompt_4, response_4,
                        # Zakładka 5
                        prompt_5, response_5,
                        # Zakładka 6
                        prompt_6, response_6,
                        # Zakładka 7
                        prompt_7, response_7,
                        # Zakładka 8
                        final_md, status_8
                    ]
                )

    return app


if __name__ == "__main__":
    app = create_app()
    app.launch()
