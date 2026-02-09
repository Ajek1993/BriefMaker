# BriefApp MVP - Plan Prac

---

## Etap: Szablony promptów

**Cel:** Wszystkie prompty gotowe do użycia w GUI - jako stringi z placeholderami.

**Kroki:**
- Stwórz plik `templates.py`
- Dodaj dict `TEMPLATES` z 5 szablonami: improve_brief, technology, stages, work_plan, control
- Dodaj funkcję `get_prompt(name, **kwargs)` - podstawia wartości w placeholdery `{brief}`, `{model_responses}`, etc.

**Edge cases do obsłużenia:** brak

**Definicja "done":** `from templates import get_prompt` działa, funkcja zwraca sformatowany string

**Test:**
```bash
python -c "from templates import get_prompt; print(get_prompt('improve_brief', brief='test brief', model_responses='odp1\nodp2')[:100])"
```

---

## Etap: Persystencja

**Cel:** Zapis i odczyt stanu projektu z pliku JSON.

**Kroki:**
- Dodaj funkcję `get_empty_state()` - zwraca dict z pustymi polami dla wszystkich kroków
- Dodaj funkcję `load_project()` - wczytuje `project.json` lub zwraca pusty stan jeśli brak pliku
- Dodaj funkcję `save_project(data)` - zapisuje dict do `project.json`, zwraca True/False

**Edge cases do obsłużenia:**
- Brak project.json → zwróć pusty stan (nie crashuj)
- Błąd zapisu → zwróć False, nie crashuj

**Definicja "done":** save → load zwraca te same dane

**Test:**
```bash
python -c "from app import save_project, load_project; save_project({'step': 1, 'brief': 'test'}); print(load_project())"
```

---

## Etap: GUI Wizard

**Cel:** Działające GUI z 8 zakładkami, przepływem danych i persystencją.

**Kroki:**
- Stwórz `app.py` ze szkieletem: `gr.Blocks` + `gr.Tabs` z 8 zakładkami (puste)
- Zaimplementuj zakładkę "Brief początkowy": 4 pola tekstowe + przycisk "Generuj MD" + pole readonly z wygenerowanym briefem (show_copy_button=True) + przycisk "Dalej"
- Zaimplementuj zakładki 2-7 według wzoru: pole readonly z promptem (show_copy_button=True) + pole na odpowiedź + przycisk "Dalej"
- Dodaj `gr.State` do przechowywania danych między krokami
- Podłącz persystencję: przy starcie `load_project()` wypełnia pola, przy "Dalej" wywołuje `save_project()`

**Edge cases do obsłużenia:**
- F5 odświeżenie → przy starcie wczytaj dane z JSON
- Puste wymagane pole → zablokuj "Dalej" lub pokaż komunikat

**Definicja "done":** można przejść przez wszystkie zakładki, F5 zachowuje dane

**Test:**
```
- python app.py
- Wypełnij brief, kliknij "Dalej"
- Wklej odpowiedzi modeli, kliknij "Dalej"
- Naciśnij F5
- Sprawdź czy pola mają poprzednie wartości
```

---

## Etap: Export MD

**Cel:** Ostatnia zakładka zapisuje kompletny brief do pliku.

**Kroki:**
- Dodaj funkcję `generate_final_md(state)` - łączy wszystkie dane w jeden dokument MD
- Zaimplementuj przycisk "Zapisz do pliku" - tworzy `output/brief_final.md`
- Zaimplementuj przycisk "Nowy projekt" - czyści stan, wraca do kroku 1

**Edge cases do obsłużenia:**
- Błąd zapisu pliku → wyświetl komunikat błędu

**Definicja "done":** kliknięcie tworzy plik z wszystkimi sekcjami

**Test:**
```
- Przejdź cały flow
- Kliknij "Zapisz do pliku"
- Otwórz output/brief_final.md
- Sprawdź czy są wszystkie sekcje (brief, odpowiedzi modeli, technologia, etapy, plan, kontrola)
```

---

## Test integracyjny

**Jak przetestować całe MVP end-to-end:**
```
- Uruchom: python app.py
- Zakładka 1: wypełnij 4 pola briefu → "Generuj" → "Dalej"
- Zakładka 2: wklej 3 odpowiedzi od modeli → "Dalej"
- Zakładki 3-7: skopiuj prompt → wklej do modelu → wklej odpowiedź → "Dalej"
- Zakładka 8: kliknij "Zapisz do pliku"
- Sprawdź plik output/brief_final.md
- Kliknij "Nowy projekt" → sprawdź czy wrócił do pustego stanu
```

**Scenariusz sukcesu:**
Użytkownik przechodzi 8 kroków, na końcu klika "Zapisz" → dostaje plik `output/brief_final.md` z kompletnym briefem zawierającym wszystkie sekcje.

**Scenariusz błędu:**
Użytkownik zostawia puste pole "Co boli?" i klika "Dalej" → widzi komunikat "Wypełnij wszystkie pola" → nie przechodzi dalej.
