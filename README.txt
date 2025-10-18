MyCryptoFI — staattinen sivu (GitHub Pages)
===============================================

Mitä tämä on?
-------------
Valmis, builditon Render-tyylinen etusivu suomalaisille — näyttää uutiset `news.json`ista ja listaa pörssit/lompakot affi-linkeillä.

Tiedostot
---------
- index.html  — varsinainen sivu
- style.css   — minimalistinen mustavalko-tyyli (Inter-fontti)
- app.js      — hakee ./news.json ja piirtää listan
- CNAME       — sisältää domainin: mycryptofi.com

Vaatimukset
-----------
- Repossa (juuressa) on `news.json`. Sen tuottaa GitHub Actions -workflow (fetch_news.yml) joka sinulla on jo valmiina.
- Lataa myös `mycryptofi_logo_key.png` ja `mycryptofi_favicon.png` repojuureen.

Asennus GitHub Pagesiin
-----------------------
1) Avaa GitHub-reposi (sama jossa news.json päivittyy)
2) Paina **Add file → Upload files** ja lataa nämä neljä tiedostoa repojuureen
3) Varmista Settings → Pages → Source: `Deploy from a branch` → `main` / `/ (root)`
4) Odota hetki ja avaa https://mycryptofi.com

Vinkit
-----
- Tarkista selaimen dev-konsoli: ei punaisia virheilmoituksia.
- news.json pitää olla juurihakemistossa (samalla tasolla kuin index.html).
- Polut ovat suhteellisia (`./news.json`, `./style.css`, `./app.js`).
