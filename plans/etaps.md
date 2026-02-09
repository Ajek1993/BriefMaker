# BriefApp MVP - Etapy Realizacji

---

## Etap: Szablony promptów

**Co robi:** Definiuje wszystkie prompty jako stringi z placeholderami i funkcję do ich formatowania.

**Input:** nazwa szablonu + wartości do podstawienia (brief, odpowiedzi modeli, etapy, plan)

**Output:** sformatowany string gotowy do skopiowania

**Test:**
```python
from templates import get_prompt
result = get_prompt("improve_brief", brief="mój brief", model_responses=["odp1", "odp2"])
print(result)  # sprawdź czy podstawiło wartości w odpowiednie miejsca
```

---

## Etap: Persystencja

**Co robi:** Funkcje do zapisu i odczytu stanu projektu z pliku JSON.

**Input:** dict z danymi projektu (current_step, brief, model_responses, improved_brief, ...)

**Output:** plik `project.json` / dict z wczytanymi danymi

**Test:**
```python
from app import save_project, load_project

save_project({"step": 2, "brief": "test brief"})
# sprawdź czy plik project.json istnieje

data = load_project()
print(data)  # {"step": 2, "brief": "test brief"}
```

---

## Etap: GUI Wizard

**Co robi:** Gradio z 8 zakładkami - formularze, pola tekstowe, przyciski kopiuj/dalej, przepływ danych między krokami.

**Input:** kliknięcia użytkownika, wklejony tekst

**Output:** wypełnione formularze, skopiowane prompty do schowka, zapisany stan

**Test:**
```
1. Uruchom: python app.py
2. Wypełnij brief -> kliknij "Dalej"
3. Wklej odpowiedzi modeli -> kliknij "Dalej"
4. Naciśnij F5
5. Sprawdź czy dane są zachowane (wczytane z project.json)
```

---

## Etap: Export MD

**Co robi:** Ostatni krok generuje finalny dokument MD ze wszystkich danych i zapisuje do pliku.

**Input:** wszystkie dane z poprzednich kroków (brief, odpowiedzi, plan, kontrola)

**Output:** plik `output/brief_final.md`

**Test:**
```
1. Przejdź cały flow do końca
2. Kliknij "Zapisz do pliku"
3. Otwórz output/brief_final.md
4. Sprawdź czy zawiera wszystkie sekcje
```

---

## Podsumowanie

**Kolejność realizacji:**
- Szablony promptów (pierwszy - to tylko stringi, można zrobić od razu)
- Persystencja (drugi - proste funkcje JSON)
- GUI Wizard (trzeci - główna praca)
- Export MD (ostatni - finalizacja)

**Etap KRYTYCZNY:** GUI Wizard - bez niego nie ma aplikacji

**Etap można POMINĄĆ w pierwszej wersji:** Export MD - użytkownik może ręcznie skopiować finalny brief z ostatniej zakładki
