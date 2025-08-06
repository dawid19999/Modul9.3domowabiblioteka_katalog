 Domowa Biblioteka – API

Aplikacja Flask do zarządzania książkami w domowej bibliotece. Umożliwia dodawanie, edytowanie, usuwanie i przeglądanie książek.

##  Funkcje

- Dodawanie nowej książki – `POST /books`
- Edycja książki – `PUT /books/<id>`
- Usuwanie książki – `DELETE /books/<id>`
- Lista książek – `GET /books`

 Jak uruchomić aplikację



### 1. Utwórz i aktywuj środowisko wirtualne

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 3. Uruchom aplikację

```bash
python app.py
```

Aplikacja działa pod adresem: [http://localhost:5000](http://localhost:5000)




