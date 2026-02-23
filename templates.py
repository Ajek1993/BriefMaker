"""Szablony promptów dla BriefApp."""

TEMPLATES = {
    "improve_brief": """Na podstawie poniższego briefu projektowego oraz ocen od modeli AI, przygotuj ulepszony brief - wersja MVP.

## Oryginalny brief:
{brief}

## Oceny i sugestie od modeli:
{model_responses}

## Twoje zadanie:
- Dodaj TYLKO te uwagi z odpowiedzi modeli, które są krytyczne dla działania
- Wyrzuć wszystko, co jest "nice to have" lub "na przyszłość"
- Uprość gdzie się da - jeśli coś można zrobić prościej, zrób prościej
- Bez cache, bez logów, bez config file - to na później
- Bez bibliotek zewnętrznych, jeśli stdlib wystarczy, no chyba że trzeba
- Max 3-4 edge cases, nie 10

Format ulepszonego briefu:
- Co boli (1-2 zdania)
- Dla kogo (1 zdanie)
- Core funkcja MVP (co DOKŁADNIE ma robić, krok po kroku)
- Technologia (język + tylko niezbędne biblioteki)
- Edge cases (max 4 najważniejsze)
- Czego NIE robimy w MVP (lista rzeczy do pominięcia)

Bądź bezwzględny w upraszczaniu. Lepsze działające 20% niż zaplanowane 100%.

Jeśli czegoś nie wiesz, nie masz pewności, coś jest niejasne albo wzajemnie wykluczające się - ZAPYTAJ MNIE, CO MASZ Z TYM ZROBIĆ. NIE podejmuj takich decyzji samodzielnie.

Zwróć ulepszony brief w formacie markdown zachowując formatowanie markdown.""",

    "technology": """Na podstawie poniższego briefu projektowego, rozszerz go o wybór technologii.

## Brief projektu:
{brief}

## Twoje zadanie:
- Zachowaj cały oryginalny brief
- Dlaczego Python pasuje (lub nie) do tego projektu (1-2 zdania)

Biblioteki - podziel na:

**STDLIB (wbudowane, preferowane):**
- nazwa: do czego użyję

**ZEWNĘTRZNE (tylko jeśli stdlib nie wystarczy):**
- nazwa: do czego, dlaczego stdlib nie wystarczy

**Struktura plików (minimalna, dla MVP):**
- jakie pliki/moduły będą potrzebne

**Jak uruchomić (komenda):**
- przykład wywołania z argumentami

Zasady:
- Stdlib > zewnętrzne biblioteki (zawsze preferuj wbudowane)
- Jeśli zewnętrzna biblioteka oszczędza 50+ linii kodu - warto
- Jeśli oszczędza 10 linii - nie warto, użyj stdlib
- Max 2-3 zewnętrzne biblioteki dla MVP
- Żadnych frameworków, jeśli prosty skrypt wystarczy
- Zwróć KOMPLETNY dokument (brief + technologia)

Odpowiedź w formacie markdown zachowując formatowanie markdown.""",

    "stages": """Na podstawie poniższego briefu z technologią, podziel realizację na etapy.

## Brief projektu z technologią:
{brief}

## Twoje zadanie:
- Każdy etap = jedna działająca część (można przetestować osobno)
- Max 4-5 etapów dla MVP
- Etapy idą od fundamentów do funkcji końcowej
- Żaden etap nie zależy od nieukończonego poprzedniego

Format każdego etapu:
- Nazwa etapu (2-3 słowa)
- Co robi (1 zdanie)
- Input: co przyjmuje
- Output: co zwraca
- Test: jak sprawdzić, że działa (konkretny przykład)

Na końcu dodaj:
- Kolejność realizacji (który etap pierwszy, który ostatni)
- Który etap jest KRYTYCZNY (bez niego nic nie działa)
- Który etap można POMINĄĆ w pierwszej wersji

Pamiętaj: prostota > kompletność. Lepiej 3 działające etapy niż 7 zaplanowanych.

Dla każdego etapu określ: cel, zakres, definicję "done".

Odpowiedź w formacie markdown zachowując formatowanie markdown.""",

    "work_plan": """Na podstawie briefu i etapów, stwórz szczegółowy plan prac.

## Brief projektu:
{brief}

## Etapy realizacji:
{stages}

## Twoje zadanie:

Plan musi:
- Przejść przez wszystkie etapy w logicznej kolejności
- Uwzględnić edge cases z briefu
- Kończyć się działającym MVP

Format planu:

**DLA KAŻDEGO ETAPU:**
- Etap X: [nazwa]
- Cel: co ma działać po tym etapie
- Kroki:
  - [konkretna akcja]
  - [konkretna akcja] ...
- Edge cases do obsłużenia: [które z briefu dotyczą tego etapu]
- Definicja "done": jak poznam, że etap skończony
- Test: konkretna komenda/akcja do sprawdzenia

**NA KOŃCU:**
- Test integracyjny: jak przetestować całe MVP end-to-end
- Scenariusz sukcesu: użytkownik robi X, dostaje Y
- Scenariusz błędu: użytkownik robi X źle, dostaje komunikat Z

Zasady:
- Każdy krok to JEDNA akcja (nie "zrób A, B i C")
- Kroki są na tyle szczegółowe, że AI może je wykonać jeden po drugim
- Żadnych kroków "opcjonalnych" - albo robimy, albo nie
- Max 3-5 kroków na etap (jeśli więcej - podziel etap)

Odpowiedź w formacie markdown  zachowując formatowanie markdown.""",

    "control": """Zweryfikuj spójność planu projektu i wygeneruj finalną, poprawioną wersję.

## Brief projektu:
{brief}

## Etapy realizacji:
{stages}

## Plan prac:
{work_plan}

## Twoje zadanie:
- Sprawdź, czy plan realizuje wszystkie wymagania z briefu
- Zidentyfikuj luki lub pominięcia
- Wskaż potencjalne ryzyka i edge case'y
- Oceń, czy kolejność etapów jest optymalna

Checklist:

**ZGODNOŚĆ Z BRIEFEM:**
- [ ] Czy plan realizuje KAŻDĄ funkcję z briefu?
- [ ] Czy WSZYSTKIE edge cases z briefu są obsłużone?
- [ ] Czy technologia w planie zgadza się z briefem?

**KOMPLETNOŚĆ ETAPÓW:**
- [ ] Czy każdy etap ma jasny cel?
- [ ] Czy każdy etap ma definicję "done"?
- [ ] Czy każdy etap ma test sprawdzający?
- [ ] Czy etapy idą w logicznej kolejności?

**WYKONALNOŚĆ:**
- [ ] Czy każdy krok to JEDNA akcja?
- [ ] Czy są jakieś luki między krokami?
- [ ] Czy AI może wykonać te kroki bez zgadywania?

**BRAKI:**
- [ ] Czego brakuje w planie?
- [ ] Co jest w briefie, ale nie ma w planie?
- [ ] Jakie pytania trzeba zadać przed rozpoczęciem?

Odpowiedz:
- PASS/FAIL dla każdego punktu
- Lista BRAKÓW (jeśli są)
- Lista PYTAŃ do wyjaśnienia (jeśli są)
- Ocena gotowości: GOTOWY / WYMAGA POPRAWEK / DO PRZEROBIENIA

Na podstawie analizy, po zatwierdzeniu przez usera, NANIEŚ POPRAWKI I WYGENERUJ FINALNY, POPRAWIONY PLAN.

Odpowiedź w formacie markdown zachowując formatowanie markdown:
- Wygeneruj PEŁNY, POPRAWIONY PLAN PRAC uwzględniający wszystkie korekty

To będzie finalny dokument używany do implementacji projektu."""
}


def get_prompt(name: str, **kwargs) -> str:
    """Zwraca sformatowany prompt z podstawionymi wartościami.

    Args:
        name: Nazwa szablonu (improve_brief, technology, stages, work_plan, control)
        **kwargs: Wartości do podstawienia w placeholdery

    Returns:
        Sformatowany string promptu

    Raises:
        KeyError: Gdy szablon o podanej nazwie nie istnieje
    """
    if name not in TEMPLATES:
        raise KeyError(f"Szablon '{name}' nie istnieje. Dostępne: {list(TEMPLATES.keys())}")

    return TEMPLATES[name].format(**kwargs)
