# AtmoDrop
<b>kropla w morzu potrzeb współczesnego rolnictwa </b>

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

# Raport PIE
Według raportu Polskiego Instytutu Ekonomicznego „Gospodarcze koszty suszy dla polskiego rolnictwa” (2022), roczne straty w plonach spowodowane suszami w Polsce mogą sięgać nawet 6,5 miliarda złotych. Problem dotyczy całego sektora, ale szczególnie odczuwalny jest dla gospodarstw uprawiających rośliny wrażliwe na niedobory wody. <br>
Przy około 1,3 miliona gospodarstw rolnych w kraju, przeciętny rolnik może tracić ponad 4 600 zł rocznie z powodu nieefektywnego zarządzania wodą i braku dostępu do dokładnych, lokalnych danych opadowych. <br>
AtmoDrop ma na celu ograniczenie tych strat poprzez dostarczanie precyzyjnych prognoz opadów opartych na danych z UAV i pionowych profilach atmosferycznych. Lepsze dane to lepsze decyzje – szczególnie w kontekście rosnącej zmienności klimatycznej i ryzyka susz.
<a href= https://pie.net.pl/wp-content/uploads/2022/11/2022_11_02_65-mld-zl-rocznie-moga-byc-warte-plony-ktore-tracimy-w-Polsce-w-wyniku-susz.pdf>Raport PIE</a>
