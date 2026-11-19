INSERT INTO innlegg (id, tittel, dato, tekst) VALUES
(1, 'Topp 10 hundevennlige restauranter i Oslo', '2026-11-12',
'Etter et halvt år med testing har jeg endelig samlet favorittene mine. Her er ti steder i Oslo der både du og hunden er like velkomne.

Felles for alle stedene er at hunden får vannskål uten at du må spørre. Kafe Pote på Løkka topper lista, tett fulgt av Bistro Bjeffen i Gamlebyen.'),

(2, 'Åpningsfest på Pizza Labben', '2026-11-08',
'Pizza Labben i Storgata åpner dørene neste lørdag, og hunder er spesielt invitert til festen.

Det blir smakebiter for tobeinte og hjemmelagde hundekjeks for firbeinte. Surdeigspizzaen med trøffel er verdt turen alene.'),

(3, 'Hundekafe på Løkka', '2026-11-02',
'Kafe Pote har blitt mitt faste stamsted. Her er hundene ikke bare tolerert, de er hele poenget.

Det står en kurv med leker i hjørnet, og baristaen kjenner navnet på de fleste hundene i nabolaget.'),

(4, 'Slik forbereder du hunden på restaurantbesøk', '2026-10-27',
'Ikke alle hunder er født til å ligge rolig under et bord i to timer. Med litt trening går det likevel overraskende bra.

Start med korte besøk når det er lite folk. Ta med et teppe hunden kjenner lukten av, og belønn rolig oppførsel.'),

(5, 'Søndagsbrunsj med vannskål på bordet', '2026-10-20',
'Søndagsbrunsj er det beste jeg vet, og enda bedre når hunden kan bli med.

Bistro Bjeffen serverer eggerøre, nystekt brød og en egen hundetallerken med kokt kylling.'),

(6, 'Uteservering i oktober', '2026-10-13',
'Mange tror at sesongen for uteservering er over når høsten kommer. Det stemmer ikke.

Flere steder i sentrum har varmelamper og pledd, og noen har til og med egne dekken til hunden.'),

(7, 'Fem spørsmål før du tar med hunden inn', '2026-10-05',
'Selv om et sted sier at hunder er velkomne, betyr det ikke alltid det samme overalt.

Spør om hunden kan være inne, om det finnes vannskål, og om det er travlest på bestemte tider.'),

(8, 'Hjemmelaget hundekjeks til kafebesøket', '2026-09-28',
'En liten pose med godbiter i lomma gjør kafebesøket enklere for både deg og hunden.

Du trenger bare havregryn, en moset banan og en skje peanøttsmør uten sukker. Stek i 20 minutter på 180 grader.'),

(9, 'Tur langs Akerselva med pause på kafe', '2026-09-20',
'Akerselva er en av de fineste turene i Oslo, og den passer perfekt for en lang søndagstur med hunden.

Start ved Grünerløkka og gå oppover mot Nydalen. Halvveis ligger det flere kafeer der hunder er velkomne.'),

(10, 'Hvorfor jeg startet denne bloggen', '2026-09-14',
'Da jeg fikk hund, oppdaget jeg fort hvor vanskelig det var å finne steder der vi begge var velkomne.

Denne bloggen er min samling av tips og erfaringer, slik at flere hundeeiere tør å ta med seg hunden ut.');
INSERT INTO tagger (id, navn) VALUES
(1, 'hund'),
(2, 'mat'),
(3, 'oslo'),
(4, 'tips'),
(5, 'pizza'),
(6, 'arrangement'),
(7, 'kafe'),
(8, 'oppskrift'),
(9, 'tur');

INSERT INTO innlegg_tagger (innlegg_id, tag_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4),
(2, 2), (2, 5), (2, 6),
(3, 1), (3, 3), (3, 7),
(4, 1), (4, 4),
(5, 1), (5, 2), (5, 7),
(6, 1), (6, 2), (6, 3),
(7, 1), (7, 4),
(8, 1), (8, 8),
(9, 1), (9, 3), (9, 7), (9, 9),
(10, 1), (10, 3);

INSERT INTO kommentarer (innlegg_id, tittel, dato, tekst) VALUES
(1, 'Hundecafe på Løkka', '2026-11-13', 'Takk for lista! Vi testet Kafe Pote i går, og hunden fikk både vannskål og kos.'),
(1, 'Mat?', '2026-11-13', 'Har noen av disse stedene egen mat eller snacks til hund?'),
(2, 'Gleder meg!', '2026-11-09', 'Vi kommer på åpningen. Er det greit å ta med to hunder?'),
(3, 'Enig', '2026-11-03', 'Kafe Pote er helt fantastisk. Hunden min drar meg dit hver gang vi går forbi.'),
(4, 'Gode tips', '2026-10-28', 'Teppet var et godt tips. Hunden min slappet mye bedre av med noe kjent å ligge på.'),
(8, 'Testet oppskriften', '2026-09-30', 'Laget kjeksene i helgen, og de forsvant på en dag. Takk!');