# AtmoDrop
kropla w morzu potrzeb współczesnego rolnictwa

Witamy w AtmoDrop – systemie prognozowania opadów opartym na pionowych profilach atmosferycznych.
Projekt ma na celu porównanie dokładności lokalnych prognoz opadowych, generowanych na podstawie danych ze stacji pomiarowej, z wynikami ogólnych modeli numerycznych.
Znajdziesz tutaj wszystkie pliki wypracowane przez zespół projektu AtmoDrop podczas SpaceSheld.

Repozytorium zawiera: <br>
🔵 Podstawowe pliki: schematy ideowe, prezentacja, kosztorys. (folder basic)<br>
🔵 Program generujący model uczenia maszynowego. (folder generatorml)<br>
🔵 Dane na podstawie których tworzyliśmy modele uczenia maszynowego (folder generatorml)<br>
🔵 Nasze ML potrzebne do programu analizujące wyniki z przewidywań stacji oraz ogólnych modeli numerycznych (folder MUM)<br>
🔵 Program służący przewidywania opadów na podstawie stacji i UAV (folder PPOSD)<br>
🔵 Program z wstepnym inteferjsem panelu sterowania. (folder control panel)<br>
🔵 Profesjonalnie zaprojektowany przez nas hardware dla pojemnika pomiarowego UAV (folder electronics schematic)<br>

Przetestowaliśmy cały proces cyfrowy – od wykonania pomiarów, poprzez przesyłanie danych za pomocą API na serwer z systemem Ubuntu, aż po ich automatyczne odbieranie i przetwarzanie przez uruchomione na serwerze programy, działające bez udziału operatora.
