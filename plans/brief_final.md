# BriefApp MVP - Brief z Technologią

## Co boli
Tworzenie briefu i planu projektu wymaga przeskakiwania między wieloma oknami, kopiowania promptów, wklejania wyników. Chcę mieć jedno GUI, które prowadzi krok po kroku z gotowymi szablonami.

## Dla kogo
Tylko dla mnie - do tworzenia briefów i planów pod Claude Code.

## Core funkcja MVP

Aplikacja webowa (Gradio) z krokami:

**Krok: Brief początkowy**
- Formularz z pytaniami (Co boli? Dla kogo? Główne potrzeby? Co może pójść nie tak?)
- Przycisk "Generuj brief" -> tworzy MD
- Przycisk "Kopiuj do schowka"
- Przycisk "Dalej"

**Krok: Oceny modeli**
- Wyświetla gotowy brief (read-only)
- 3 pola tekstowe na wklejenie odpowiedzi od modeli (Model 1, Model 2, Model 3)
- Przycisk "Dalej"

**Krok: Ulepszony brief**
- Wyświetla szablon promptu z automatycznie wstawionym briefem i odpowiedziami modeli
- Przycisk "Kopiuj prompt"
- Pole na wklejenie odpowiedzi od modelu
- Przycisk "Dalej"

**Krok: Wybór technologii**
- Wyświetla szablon promptu z wstawionym ulepszonym briefem
- Przycisk "Kopiuj prompt"
- Pole na wklejenie odpowiedzi
- Przycisk "Dalej"

**Krok: Podział na etapy**
- Wyświetla szablon promptu z wstawionym briefem
- Przycisk "Kopiuj prompt"
- Pole na wklejenie odpowiedzi
- Przycisk "Dalej"

**Krok: Plan prac**
- Wyświetla szablon promptu z wstawionym briefem i etapami
- Przycisk "Kopiuj prompt"
- Pole na wklejenie odpowiedzi
- Przycisk "Dalej"

**Krok: Kontrola**
- Wyświetla szablon promptu z briefem, etapami i planem
- Przycisk "Kopiuj prompt"
- Pole na wklejenie odpowiedzi
- Przycisk "Dalej"

**Krok: Export**
- Wyświetla finalny brief MD (połączenie wszystkiego)
- Przycisk "Zapisz do pliku" -> zapisuje do `output/brief_final.md`
- Przycisk "Nowy projekt" -> czyści wszystko, wraca do kroku 1

**Persystencja:**
- Przy każdym "Dalej" zapisz stan do `project.json`
- Przy starcie aplikacji wczytaj `project.json` jeśli istnieje
- Jeden aktywny projekt (nowy = nadpisanie)

---

## Technologia

### Dlaczego Python
Python pasuje idealnie - Gradio to biblioteka Pythonowa do szybkiego tworzenia GUI webowych (oszczędza setki linii HTML/JS/CSS). Stdlib ma wszystko do obsługi plików JSON i MD.

### Biblioteki

**STDLIB (wbudowane):**
- `json` - zapis/odczyt `project.json`
- `pathlib` - operacje na ścieżkach, tworzenie folderów, zapis plików MD

**ZEWNĘTRZNE (tylko 1):**
- `gradio` - GUI webowe z formularzami, przyciskami, zakładkami. Stdlib nie ma nic do GUI webowego. Gradio ma wbudowany `show_copy_button=True` w Textbox, więc nie potrzebujemy pyperclip.

### Struktura plików (minimalna)

```
briefapp/
├── app.py              # główna aplikacja (UI + logika)
├── templates.py        # szablony promptów jako stringi
├── project.json        # stan projektu (tworzony runtime)
└── output/             # folder na eksport MD (tworzony runtime)
    └── brief_final.md
```

Alternatywnie dla ultra-MVP: wszystko w jednym `app.py` (szablony jako stringi na górze pliku).

### Jak uruchomić

```bash
pip install gradio
python app.py
```

Otworzy przeglądarkę na `http://localhost:7860`

---

## Edge cases (4 najważniejsze)

- **F5 odświeżenie strony** - dane wczytywane z `project.json` przy starcie
- **Puste wymagane pole** - przycisk "Dalej" zablokowany, komunikat "Wypełnij pole"
- **Brak project.json** - startuj od kroku 1 z pustymi polami
- **Błąd zapisu pliku** - wyświetl komunikat błędu, nie crashuj

## Czego NIE robimy w MVP

- API do modeli (wszystko ręcznie kopiuj/wklej)
- Historia projektów (jeden aktywny projekt)
- Cofanie między krokami (tylko do przodu)
- Wersjonowanie projektów
- gr.BrowserState / localStorage
- Export ZIP
- Template management
- Dark mode
- Docker
- Progress bar
- Retry mechanism
- Token limits
- Logging
- Config file
- Checkboxy "ukończono"
- pyperclip (Gradio ma wbudowane kopiowanie)
