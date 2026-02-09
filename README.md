# BriefApp - Kreator briefów projektowych

Aplikacja webowa do tworzenia briefów projektowych w sposób iteracyjny z wykorzystaniem modeli AI.

## Opis

BriefApp prowadzi użytkownika przez proces tworzenia briefu projektowego w 8 krokach:

- **Brief** - odpowiedzi na podstawowe pytania o projekt
- **Oceny modeli** - zbieranie feedbacku od różnych modeli AI (GPT, Gemini, Claude)
- **Ulepszony brief** - synteza uwag i stworzenie wersji MVP
- **Technologia** - wybór stosu technologicznego
- **Etapy** - podział na etapy realizacji
- **Plan prac** - szczegółowy plan implementacji
- **Kontrola** - weryfikacja spójności planu
- **Export** - eksport plików do dalszej pracy

## Funkcje

- Pisanie głosem (Speech-to-Text) - ikona mikrofonu przy każdym polu tekstowym (Chrome/Edge)
- Automatyczny zapis stanu projektu do pliku JSON
- Generowanie promptów do kopiowania dla modeli AI
- Eksport wyników do plików Markdown

## Wymagania

- Python 3.8+
- Przeglądarka Chrome/Edge (dla funkcji Speech-to-Text)

## Instalacja

```bash
git clone https://github.com/Ajek1993/BriefMaker.git
cd BriefMaker
pip install -r requirements.txt
```

## Uruchomienie

```bash
python app.py
```

Aplikacja uruchomi się pod adresem `http://localhost:7860`

## Użycie

- Wypełniaj pola tekstowe ręcznie lub kliknij ikonę mikrofonu, aby dyktować
- Po każdym kroku kliknij "Dalej", aby przejść do następnej zakładki
- Kopiuj wygenerowane prompty i wysyłaj do modeli AI
- Wklej odpowiedzi od modeli w odpowiednie pola
- Na końcu eksportuj pliki do katalogu `output/`

## Struktura projektu

```
BriefApp/
├── app.py           # Główna aplikacja Gradio
├── templates.py     # Szablony promptów
├── project.json     # Zapisany stan projektu
├── requirements.txt # Zależności
├── output/          # Eksportowane pliki
└── plans/           # Przykładowe plany
```

## Eksportowane pliki

- `brief_technology.md` - brief z wyborem technologii
- `etaps.md` - podział na etapy
- `plan_final.md` - szczegółowy plan prac
- `plan_final_v2.md` - finalny plan po kontroli

## Licencja

MIT
