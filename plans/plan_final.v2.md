# BriefApp MVP - Plan Implementacji (POPRAWIONY)

## Context

Tworzymy aplikację GUI (Gradio) do tworzenia briefów projektowych krok po kroku. Problem: przeskakiwanie między oknami, kopiowanie promptów. Rozwiązanie: jeden wizard z 8 krokami i gotowymi szablonami.

---

## Struktura plików

```
C:\Users\ajek1\Desktop\BriefApp\
├── app.py              # główna aplikacja
├── templates.py        # szablony promptów
├── project.json        # stan projektu (runtime)
└── output/
    └── brief_final.md  # eksport (runtime)
```

---

## Struktura State

```python
STATE = {
    "brief": "",           # wygenerowany brief MD z kroku 1
    "model1": "",          # odpowiedź modelu 1
    "model2": "",          # odpowiedź modelu 2
    "model3": "",          # odpowiedź modelu 3
    "improved_brief": "",  # odpowiedź z kroku 3
    "technology": "",      # odpowiedź z kroku 4
    "stages": "",          # odpowiedź z kroku 5
    "work_plan": "",       # odpowiedź z kroku 6
    "control": "",         # odpowiedź z kroku 7
}
```

---

## Etap: Szablony promptów

**Cel:** Plik templates.py z 5 szablonami

**Kroki:**
- Stwórz `templates.py`
- Dodaj dict TEMPLATES z 5 szablonami (treść z wiadomości użytkownika):
  - `improve_brief` - ulepszanie briefu na podstawie ocen modeli
  - `technology` - wybór technologii
  - `stages` - podział na etapy
  - `work_plan` - plan prac
  - `control` - kontrola zgodności
- Dodaj funkcję `get_prompt(name, **kwargs)` - str.format() z placeholderami

**Test:** `python -c "from templates import get_prompt; print(len(get_prompt('improve_brief', brief='x', model_responses='y')))"`

---

## Etap: Persystencja

**Cel:** Zapis/odczyt stanu do JSON

**Kroki:**
- W `app.py` dodaj `get_empty_state()` - zwraca pusty dict ze wszystkimi kluczami
- Dodaj `load_project()` - wczytuje project.json lub zwraca pusty stan
- Dodaj `save_project(data)` - zapisuje do project.json

**Edge cases:** brak pliku → pusty stan, błąd zapisu → return False

**Test:** `python -c "from app import save_project, load_project; save_project({'brief':'test'}); print(load_project())"`

---

## Etap: GUI - Zakładka 1 (Brief)

**Cel:** Formularz briefu z generowaniem MD

**Kroki:**
- Stwórz `app.py` z `gr.Blocks()` + `gr.Tabs()`
- Zakładka 1: 4 pola Textbox (Co boli? Dla kogo? Główne potrzeby? Co może pójść nie tak?)
- Przycisk "Generuj brief" → łączy odpowiedzi w format MD
- Pole readonly z wygenerowanym briefem (`show_copy_button=True`)
- Przycisk "Dalej" → zapisuje stan

**Test:** Wypełnij pola → Generuj → sprawdź czy brief MD się pojawił

---

## Etap: GUI - Zakładka 2 (Oceny modeli)

**Cel:** Miejsce na wklejenie odpowiedzi od 3 modeli

**Kroki:**
- Pole readonly wyświetlające brief z kroku 1 (`show_copy_button=True`)
- 3 pola Textbox na odpowiedzi (Model 1, Model 2, Model 3)
- Przycisk "Dalej" → zapisuje stan

**Uwaga:** Ta zakładka ma INNY układ niż 3-7 (brak promptu, 3 pola zamiast 1)

**Test:** Wklej 3 odpowiedzi → Dalej → sprawdź czy zapisane w state

---

## Etap: GUI - Zakładki 3-7 (Prompty)

**Cel:** 5 zakładek z tym samym wzorem

**Kroki dla każdej zakładki (3-7):**
- Pole readonly z promptem z templates.py (`show_copy_button=True`)
- Pole Textbox na wklejenie odpowiedzi
- Przycisk "Dalej" → zapisuje stan

Zakładki:
- 3: Ulepszony brief (prompt: improve_brief)
- 4: Technologia (prompt: technology)
- 5: Etapy (prompt: stages)
- 6: Plan prac (prompt: work_plan)
- 7: Kontrola (prompt: control)

**Test:** Skopiuj prompt → wklej odpowiedź → Dalej → F5 → dane zachowane

---

## Etap: GUI - Zakładka 8 (Export)

**Cel:** Zapis finalnego briefu do pliku

**Kroki:**
- Pole readonly z finalnym MD (wszystkie sekcje połączone)
- Przycisk "Zapisz do pliku" → tworzy `output/brief_final.md`
- Przycisk "Nowy projekt" → czyści stan, wraca do zakładki 1

**Edge case:** Błąd zapisu → komunikat błędu

**Test:** Kliknij "Zapisz" → sprawdź czy plik istnieje

---

## Etap: Integracja persystencji

**Cel:** F5 nie traci danych

**Kroki:**
- Przy starcie aplikacji: `load_project()` → wypełnij wszystkie pola
- Przy każdym "Dalej": `save_project(state)`
- Przy "Nowy projekt": usuń project.json

**Test:** Wypełnij 3 kroki → F5 → dane są

---

## Weryfikacja końcowa

**Test end-to-end:**
```
python app.py
→ Zakładka 1: wypełnij brief → Generuj → Dalej
→ Zakładka 2: wklej 3 odpowiedzi → Dalej
→ Zakładki 3-7: kopiuj prompt → wklej odpowiedź → Dalej
→ Zakładka 8: Zapisz do pliku
→ Sprawdź output/brief_final.md
→ Nowy projekt → sprawdź czy puste
```

**Scenariusz sukcesu:** Plik MD z wszystkimi sekcjami

**Scenariusz błędu:** Puste pole + Dalej → komunikat "Wypełnij pole"
