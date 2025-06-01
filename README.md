# Zadanie 2 – CI (Emil Loś)

Repozytorium: https://github.com/Losiak99/weather-app-emil  
Obraz Dockera: https://github.com/users/Losiak99/packages/container/weather-app-emil

---
## Opis działania workflowa `docker-publish.yml`

Workflow uruchamia się:
- automatycznie przy każdym `push` na gałąź `main`
- lub ręcznie przez `workflow_dispatch`

### Etapy:

1. **Checkout kodu**  
   `actions/checkout@v4`

2. **Konfiguracja środowiska Buildx + QEMU**  
   `docker/setup-buildx-action@v3`, `docker/setup-qemu-action@v3`  

3. **Definicja tagów i metadanych**  
   `docker/metadata-action@v5`  
   Generuje tagi takie jak: `latest`, `main`, `sha-commit`

4. **Logowanie do rejestrów**  
   - GitHub Container Registry (`ghcr.io`)
   - DockerHub (dla cache)  
   `docker/login-action@v3`

5. **Budowanie obrazu tymczasowego do skanowania**  
   `docker/build-push-action@v5` (z `load: true`)

6. **Skanowanie Trivy (CVE)**  
   `aquasecurity/trivy-action@master`  
   Publikacja obrazu jest blokowana, jeśli wykryte zostaną luki `CRITICAL` lub `HIGH`.

7. **Finalne budowanie i publikacja multiarch**  
   `docker/build-push-action@v5`  
   Obraz wysyłany do `ghcr.io/losiak99/weather-app-emil`

---
## Tagowanie obrazów

Obrazy są oznaczane automatycznie:
- `latest`
- `main` 
- `sha-xxxxx` 

---

## Cache (DockerHub)

Cache budowania przechowywany jest w publicznym repozytorium cache:
- `docker.io/<DOCKERHUB_USERNAME>/weather-app-cache`
- Użyto trybu: `type=registry, mode=max`

---

## Bezpieczeństwo (CVE)

Użyto Trivy do skanowania obrazów przed publikacją.  
Publikacja jest możliwa tylko, jeśli obraz:
- nie zawiera żadnych luk typu HIGH lub CRITICAL

---

## Sekrety użyte w workflow

| Sekret | Opis |
|--------|------|
| `GHCR_PAT` | Personal Access Token do `ghcr.io` (GitHub Container Registry) |
| `DOCKERHUB_USERNAME` | Login do DockerHub |
| `DOCKERHUB_TOKEN` | Access token z DockerHub |

---

##  Testy i efekt

Workflow uruchomił się poprawnie i zakończył sukcesem.  
Obraz został opublikowany w `ghcr.io/losiak99/weather-app-emil`.
Komenda do uruchomienia:
docker run -p 5020:5000 ghcr.io/losiak99/weather-app-emil:latest


---

##  Autor

Emil Loś  

