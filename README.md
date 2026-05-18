# RootlessCTF

> Piattaforma CTF moderna sviluppata con Django e PostgreSQL, pensata per formazione pratica nel campo della cybersecurity tramite challenge interattive, gestione progressi e sistema di ranking utenti.

---

## 📌 Descrizione

**RootlessCTF** è una piattaforma web dedicata all'apprendimento della cybersecurity attraverso sfide in stile **Capture The Flag (CTF)**.  
Il sistema permette agli utenti di registrarsi, completare challenge, inviare flag, ottenere punti esperienza e salire di livello.

L'applicazione implementa:

- autenticazione utenti completa
- gestione profilo
- catalogo challenge filtrabile
- tracking dei progressi
- hint system con penalità
- backend Django con PostgreSQL

---

# 🖼️ Immagini

## Home

<img width="2880" height="1800" alt="Screenshot 2026-05-18 103705" src="https://github.com/user-attachments/assets/48cbb79d-9d8e-408c-b2ec-1a7635c33abe" />

## Dashboard

<img width="2880" height="1620" alt="Screenshot 2026-05-18 104049" src="https://github.com/user-attachments/assets/9201ddfa-a687-494c-9486-46a973a3434a" />

## Catalogo Challenge

<img width="2880" height="1612" alt="Screenshot 2026-05-18 103744" src="https://github.com/user-attachments/assets/1fe7567a-14cf-4054-9a21-c8e0ca2780dd" />


## Pagina Challenge

<img width="2880" height="1656" alt="Screenshot 2026-05-18 103811" src="https://github.com/user-attachments/assets/97c82e36-a7d0-4074-8443-208ae80b43ab" />



---

# 🚀 Features

- Sistema di autenticazione Django
- Password hashate
- Gestione sessioni
- Dashboard utente
- Sistema livelli
- Gestione challenge
- Multi-flag validation
- Hint system con penalità
- Persistenza progresso challenge
- Filtri per categoria/difficoltà/stato
- Ricerca challenge
- ORM Django
- PostgreSQL backend
- Architettura 3-tier

---

# 🏗️ Stack Tecnologico

| Componente | Tecnologia |
|---|---|
| Backend | Python |
| Framework | Django |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Versionamento | Git + GitHub |

---

# 📂 Architettura

L'applicazione segue una classica architettura **3-tier**.

## 1. Presentation Layer

Gestito tramite:

- Django Templates
- HTML/CSS/JS

Responsabile del rendering dinamico delle pagine.

---

## 2. Logic Layer

Gestito da Django:

- routing HTTP
- business logic
- autenticazione
- gestione sessioni
- validazione flag
- ORM

---

## 3. Data Layer

Gestito tramite PostgreSQL:

- utenti
- challenge
- flag
- hint
- progressi
- punteggi

---

# 🔐 Sistema Flag

Le flag:

- sono case sensitive
- seguono il formato:

```txt
KEY{}
```

- vengono validate lato backend
- salvano il progresso parziale
- completano la challenge solo dopo tutte le flag corrette

---

# 💡 Hint System

Ogni hint:

- è associato a una flag specifica
- resta persistente dopo lo sblocco
- applica una penalità di:

```txt
-5 punti
```

sul punteggio massimo ottenibile.

---

# 🗄️ Schema Database

```sql
Utente(id, nome, cognome, username, email, password, f_profilo, punteggio, livello)

Sfida(id, titolo, descrizione, l_difficolta, p_massimo, immagine, id_categoria)

Categoria(id, nome)

Flag(id, chiave, id_sfida)

Indizio(id, testo, id_flag)

Partecipa(id_utente, id_sfida, stato, punteggio_ottenuto)

Consegna(id_utente, id_flag)
```

---

# 📊 Stato Challenge

Ogni challenge può trovarsi in uno dei seguenti stati:

| Stato | Descrizione |
|---|---|
| Non iniziata | Nessuna flag inviata |
| Incompleta | Almeno una flag corretta |
| Completata | Tutte le flag validate |

---

# 👤 Gestione Utente

L'utente può:

- modificare:
  - nome
  - cognome
  - email

- cambiare password
- monitorare:
  - livello
  - punteggio
  - challenge completate
  - challenge in corso

---

# 🔒 Sicurezza

Funzionalità implementate:

- password hashing
- autenticazione Django
- session management
- validazione input
- protezione accesso challenge
- protezione pannello admin

---


# 👨‍💻 Autore

D'Addato Nicolò

---

# 📜 Licenza

Distribuito sotto licenza MIT.
