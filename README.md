# TicketHub – FastAPI servis za korisničke tickete

TicketHub je middleware REST servis razvijen u sklopu AI Academy 2025. Cilj mu je dohvaćanje i izlaganje "support ticketa" iz vanjskog izvora (DummyJSON), uz napredne funkcionalnosti poput filtriranja, pretrage, paginacije, keširanja i autentifikacije.

---

## Tehnologije

- **Python 3.11**
- **FastAPI 0.111**
- **httpx 0.27** – asinkroni HTTP klijent
- **Pydantic 2.7** – validacija i serializacija
- **Redis** – keširanje podataka
- **SlowAPI** – rate limiting
- **Docker / Docker Compose** – razvoj i pokretanje
- **Pytest** – testiranje

---

## Funkcionalnosti

| Endpoint            | Opis                                            |
| ------------------- | ----------------------------------------------- |
| `GET /tickets`      | Lista ticketa + filtriranje, paginacija, search |
| `GET /tickets/{id}` | Detalji pojedinačnog ticketa                    |
| `POST /auth/login`  | Login putem DummyJSON korisnika                 |
| `GET /stats`        | Agregirane statistike ticketa                   |
| `GET /health`       | Health check za Docker/Kubernetes               |

---

## Keširanje i Redis

- Podaci o korisnicima i ticketima se keširaju pomoću Redis-a
- TTL je postavljen na npr. 60 sekundi da bi se smanjio broj vanjskih poziva
- Redis se koristi kroz aioredis

## Rate limiting

- Implementirano pomoću SlowAPI
- Default: 10 zahtjeva/min po IP adresi
- 429 greška ako se prekorači

## Autentifikacija

- POST /auth/login koristi DummyJSON login
- username/password kombinacija: emilys/emilyspass

## Korišteni alati (AI)

- Pomoć u pisanju koda i dokumentacije korištenjem ChatGPT i Perplexity

## Postavljanje lokalno

### 1. Kloniraj repozitorij

```bash
git clone https://github.com/ime/tickethub.git
cd tickethub
```

### 2. Kreiraj i aktiviraj virtualno okruženje

```bash
python -m venv venv
source venv/bin/activate #ili .\venv\Scripts\activate na Windowsu
```

### 3. Instaliraj ovisnosti

```bash
make install
```

### 4. Pokreni servis

```bash
make run
#Aplikacija je dostupna na http://localhost:8000
#Swagger dokumentacija je dostupna na http://localhost:8000/docs
```

## Pokretanje s Docker Compose

```bash
make docker
#Servis: http://localhost:8000
#Redis: http://localhost:6739
```

## Testiranje

```bash
make test
```

## Struktura projekta
