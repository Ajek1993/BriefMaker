# Changelog

Wszystkie istotne zmiany w projekcie są dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/pl/1.0.0/).

## [0.2.0] - 2025-02-09

### Dodane
- Pisanie głosem (Speech-to-Text) z Web Speech API
- Ikona mikrofonu przy każdym edytowalnym polu tekstowym
- Obsługa języka polskiego (pl-PL)
- Wizualny feedback podczas nagrywania
- MutationObserver dla dynamicznie dodawanych pól

### Uwagi
- Funkcja działa tylko w przeglądarkach Chrome/Edge (Chromium)
- Wymaga połączenia z internetem (przetwarzanie przez serwery Google)

## [0.1.0] - 2025-02-09

### Dodane
- Inicjalizacja projektu BriefApp
- Interfejs 8-zakładkowy w Gradio
- Formularz briefu z podstawowymi i dodatkowymi pytaniami
- Zbieranie ocen od wielu modeli AI (2-5)
- Generowanie promptów dla kolejnych kroków
- Automatyczny zapis stanu do project.json
- Eksport wyników do plików Markdown
- Szablony promptów dla wszystkich kroków
