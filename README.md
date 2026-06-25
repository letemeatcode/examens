# examens
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exàmens Oficials i Solucions - Proves d'Accés</title>
    <!-- Tailwind CSS per a un disseny professional i responsive -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- FontAwesome per a les icones del portal -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
    </style>
</head>
<body class="bg-gray-50 text-gray-800 min-h-screen flex flex-col">

    <!-- Capçalera Global -->
    <header class="bg-gradient-to-r from-blue-700 to-indigo-800 text-white shadow-md">
        <div class="max-w-7xl mx-auto px-4 py-8 sm:py-10 sm:px-6 lg:px-8">
            <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
                <div class="text-center sm:text-left cursor-pointer" onclick="navegarAHome()">
                    <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight text-white m-0">
                        Portal d'Exàmens Oficials
                    </h1>
                    <p class="mt-1 text-blue-100 max-w-2xl text-sm sm:text-base m-0">
                        Recull dels últims 10 anys de proves d'accés per a totes les matèries i vies.
                    </p>
                </div>
                <div class="flex flex-wrap gap-2 justify-center">
                    <span class="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-semibold bg-blue-600 text-white border border-blue-400">
                        PAU / Selectivitat
                    </span>
                    <span class="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-semibold bg-indigo-600 text-white border border-indigo-400">
                        Majors de 25
                    </span>
                    <span class="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-semibold bg-emerald-600 text-white border border-emerald-400">
                        Grau Superior
                    </span>
                </div>
            </div>
        </div>
    </header>

    <!-- Contingut Principal -->
    <main class="flex-grow max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8 w-full">
        
        <!-- VISTA 1: CATÀLEG DE MATÈRIES (HOME) -->
        <div id="vista-cataleg" class="transition-all duration-300">
            <!-- Cercador i Filtres -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
                <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center m-0">
                    <i class="fa-solid fa-graduation-cap text-blue-600 mr-2"></i> Selecciona una assignatura per estudiar:
                </h3>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <!-- Camp de cerca -->
                    <div class="md:col-span-2 relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <i class="fa-solid fa-magnifying-glass text-gray-400"></i>
                        </div>
                        <input type="text" id="search" placeholder="Cerca assignatura (ex: Anglès, Matemàtiques, Història...)" 
                               class="block w-full pl-10 pr-3 py-2.5 border border-gray-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                               onkeyup="filtrarMateries()">
                    </div>
                    <!-- Filtre per branca -->
                    <div>
                        <select id="filtre-branca" onchange="filtrarMateries()"
                                class="block w-full px-3 py-2.5 border border-gray-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all">
                            <option value="">Totes les Branques / Fases</option>
                            <option value="Fase Comuna">Fase Comuna (Obligatòria)</option>
                            <option value="Científica-Tecnològica">Científica-Tecnològica</option>
                            <option value="Ciències de la Salut">Ciències de la Salut</option>
                            <option value="Socials i Jurídiques">Socials i Jurídiques</option>
                            <option value="Arts i Humanitats">Arts i Humanitats</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Llistat de Matèries en format Graella -->
            <div id="graella-materies" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Es carrega amb JS -->
            </div>

            <!-- Avís sense resultats -->
            <div id="sense-resultats" class="hidden text-center py-12 bg-white rounded-xl border border-dashed border-gray-300">
                <i class="fa-regular fa-folder-open text-gray-300 text-5xl mb-4"></i>
                <h4 class="text-md font-medium text-gray-900 m-0">No s'ha trobat cap matèria</h4>
                <p class="text-sm text-gray-500 mt-1">Neteja els filtres per tornar a començar.</p>
                <button onclick="netejarFiltres()" class="mt-4 px-4 py-2 text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 cursor-pointer border-0 transition-colors">
                    Netejar Filtres
                </button>
            </div>
        </div>

        <!-- VISTA 2: DETALL DE LA MATÈRIA (PÀGINA INDIVIDUAL) -->
        <div id="vista-materia" class="hidden transition-all duration-300">
            <!-- Botó de retorn -->
            <button onclick="navegarAHome()" class="mb-6 inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-800 bg-transparent border-0 cursor-pointer p-0 transition-colors">
                <i class="fa-solid fa-arrow-left mr-2"></i> Tornar al llistat de matèries
            </button>

            <!-- Capçalera de l'assignatura -->
            <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div class="text-left">
                    <span id="detall-branca" class="inline-block px-2.5 py-0.5 rounded text-xs font-semibold mb-2 bg-blue-100 text-blue-800">
                        -
                    </span>
                    <h2 id="detall-titol" class="text-2xl sm:text-3xl font-extrabold text-gray-900 m-0">-</h2>
                    <p id="detall-descripcio" class="text-sm sm:text-base text-gray-600 mt-2 mb-0 max-w-3xl">-</p>
                </div>
                <div class="flex items-center gap-2 bg-gray-50 p-3 rounded-lg border border-gray-200">
                    <i class="fa-solid fa-circle-info text-blue-600 text-lg"></i>
                    <span class="text-xs text-gray-600 leading-tight">Trobaràs els exàmens i les solucions separades per vies de dret d'accés.</span>
                </div>
            </div>

            <!-- Taula / Graella de 3 columnes (PAU, M25, GS) dels darrers 10 anys -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                
                <!-- Columna 1: PAU / Selectivitat -->
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
                    <div class="flex items-center gap-2 pb-4 mb-4 border-b border-gray-100 text-left">
                        <div class="p-2 rounded bg-blue-100 text-blue-700">
                            <i class="fa-solid fa-graduation-cap"></i>
                        </div>
                        <div>
                            <h3 class="text-base font-bold text-gray-900 m-0">PAU / Selectivitat</h3>
                            <p class="text-[11px] text-gray-500 m-0">Proves d'accés general batxillerat</p>
                        </div>
                    </div>
                    <div id="llista-pau" class="space-y-3">
                        <!-- Es genera per JS -->
                    </div>
                </div>

                <!-- Columna 2: Proves Majors de 25 anys -->
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
                    <div class="flex items-center gap-2 pb-4 mb-4 border-b border-gray-100 text-left">
                        <div class="p-2 rounded bg-indigo-100 text-indigo-700">
                            <i class="fa-solid fa-user-graduate"></i>
                        </div>
                        <div>
                            <h3 class="text-base font-bold text-gray-900 m-0">Majors de 25 anys</h3>
                            <p class="text-[11px] text-gray-500 m-0">Prova d'accés per a majors de 25</p>
                        </div>
                    </div>
                    <div id="llista-m25" class="space-y-3">
                        <!-- Es genera per JS -->
                    </div>
                </div>

                <!-- Columna 3: Prova d'Accés a Grau Superior -->
                <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
                    <div class="flex items-center gap-2 pb-4 mb-4 border-b border-gray-100 text-left">
                        <div class="p-2 rounded bg-emerald-100 text-emerald-700">
                            <i class="fa-solid fa-briefcase"></i>
                        </div>
                        <div>
                            <h3 class="text-base font-bold text-gray-900 m-0">Grau Superior</h3>
                            <p class="text-[11px] text-gray-500 m-0">Proves per a Cicles Formatius GS</p>
                        </div>
                    </div>
                    <div id="llista-gs" class="space-y-3">
                        <!-- Es genera per JS -->
                    </div>
                </div>

            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-gray-950 text-gray-400 mt-12 py-8 border-t border-gray-800">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm">
            <p>&copy; Portal de Preparació de Proves d'Accés. Publicat íntegrament a GitHub Pages.</p>
        </div>
    </footer>

    <!-- SCRIPT DE DADES I DIRECCIONAMENT -->
    <script>
        // BASE DE DADES D'EXÀMENS (Últims 10 anys: 2017 a 2026)
        // Les rutes apunten a carpetes ordenades: pdf/{materia}/{via}/{any}-{examen/solucio}.pdf
        const dadesMateries = [
            {
                id: "angles",
                assignaturaNom: "Anglès",
                branca: "Fase Comuna",
                descripcio: "Preparació de l'examen d'idioma estranger obligatori per a la fase comuna de PAU, Majors de 25 i Grau Superior.",
                // 10 Anys de dades (2017-2026)
                anys: [
                    {
                        any: 2026,
                        pau: { examen: "pdf/angles/pau/2026-examen.pdf", solucio: "pdf/angles/pau/2026-solucio.pdf" },
                        m25: { examen: "pdf/angles/m25/2026-examen.pdf", solucio: "pdf/angles/m25/2026-solucio.pdf" },
                        gs: { examen: "pdf/angles/gs/2026-examen.pdf", solucio: null } // null vol dir no disponible / pendent
                    },
                    {
                        any: 2025,
                        pau: { examen: "pdf/angles/pau/2025-examen.pdf", solucio: "pdf/angles/pau/2025-solucio.pdf" },
                        m25: { examen: "pdf/angles/m25/2025-examen.pdf", solucio: "pdf/angles/m25/2025-solucio.pdf" },
                        gs: { examen: "pdf/angles/gs/2025-examen.pdf", solucio: "pdf/angles/gs/2025-solucio.pdf" }
                    },
                    {
                        any: 2024,
                        pau: { examen: "pdf/angles/pau/2024-examen.pdf", solucio: "pdf/angles/pau/2024-solucio.pdf" },
                        m25: { examen: "pdf/angles/m25/2024-examen.pdf", solucio: "pdf/angles/m25/2024-solucio.pdf" },
                        gs: { examen: "pdf/angles/gs/2024-examen.pdf", solucio: "pdf/angles/gs/2024-solucio.pdf" }
                    },
                    {
                        any: 2023,
                        pau: { examen: "pdf/angles/pau/2023-examen.pdf", solucio: "pdf/angles/pau/2023-solucio.pdf" },
                        m25: { examen: "pdf/angles/m25/2023-examen.pdf", solucio: "pdf/angles/m25/2023-solucio.pdf" },
                        gs: { examen: "pdf/angles/gs/2023-examen.pdf", solucio: "pdf/angles/gs/2023-solucio.pdf" }
                    },
                    {
                        any: 2022,
                        pau: { examen: "pdf/angles/pau/2022-examen.pdf", solucio: "pdf/angles/pau/2022-solucio.pdf" },
                        m25: { examen: "pdf/angles/m25/2022-examen.pdf", solucio: "pdf/angles/m25/2022-solucio.pdf" },
                        gs: { examen: "pdf/angles/gs/2022-examen.pdf", solucio: "pdf/angles/gs/2022-solucio.pdf" }
                    },
                    {
                        any: 2021,
                        pau: { examen: "pdf/angles/pau/2021-examen.pdf", solucio: "pdf/angles/pau/2021-solucio.pdf" },
                        m25: { examen: "pdf/angles/m25/2021-examen.pdf", solucio: "pdf/angles/m25/2021-solucio.pdf" },
                        gs: { examen: "pdf/angles/gs/2021-examen.pdf", solucio: "pdf/angles/gs/2021-solucio.pdf" }
                    },
                    {
                        any: 2020,
                        pau: { examen: "pdf/angles/pau/2020-examen.pdf", solucio: "pdf/angles/pau/2020-solucio.pdf" },
                        m25: { examen: "pdf/angles/m25/2020-examen.pdf", solucio: "pdf/angles/m25/2020-solucio.pdf" },
                        gs: { examen: "pdf/angles/gs/2020-examen.pdf", solucio: "pdf/angles/gs/2020-solucio.pdf" }
                    },
                    {
                        any: 2019,
                        pau: { examen: "pdf/angles/pau/2019-examen.pdf", solucio: "pdf/angles/pau/2019-solucio.pdf" },
                        m25: { examen: "pdf/angles/m25/2019-examen.pdf", solucio: "pdf/angles/m25/2019-solucio.pdf" },
                        gs: { examen: "pdf/angles/gs/2019-examen.pdf", solucio: "pdf/angles/gs/2019-solucio.pdf" }
                    },
                    {
                        any: 2018,
                        pau: { examen: "pdf/angles/pau/2018-examen.pdf", solucio: "pdf/angles/pau/2018-solucio.pdf" },
                        m25: { examen: "pdf/angles/m25/2018-examen.pdf", solucio: "pdf/angles/m25/2018-solucio.pdf" },
                        gs: { examen: "pdf/angles/gs/2018-examen.pdf", solucio: "pdf/angles/gs/2018-solucio.pdf" }
                    },
                    {
                        any: 2017,
                        pau: { examen: "pdf/angles/pau/2017-examen.pdf", solucio: "pdf/angles/pau/2017-solucio.pdf" },
                        m25: { examen: "pdf/angles/m25/2017-examen.pdf", solucio: "pdf/angles/m25/2017-solucio.pdf" },
                        gs: { examen: "pdf/angles/gs/2017-examen.pdf", solucio: "pdf/angles/gs/2017-solucio.pdf" }
                    }
                ]
            },
            {
                id: "matematiques",
                assignaturaNom: "Matemàtiques",
                branca: "Científica-Tecnològica",
                descripcio: "Matemàtiques per a enginyeries i ciències. Àlgebra elemental, càlcul integral i diferencial, geometria plana i estadística.",
                anys: [
                    {
                        any: 2026,
                        pau: { examen: "pdf/matematiques/pau/2026-examen.pdf", solucio: "pdf/matematiques/pau/2026-solucio.pdf" },
                        m25: { examen: "pdf/matematiques/m25/2026-examen.pdf", solucio: "pdf/matematiques/m25/2026-solucio.pdf" },
                        gs: { examen: "pdf/matematiques/gs/2026-examen.pdf", solucio: "pdf/matematiques/gs/2026-solucio.pdf" }
                    },
                    {
                        any: 2025,
                        pau: { examen: "pdf/matematiques/pau/2025-examen.pdf", solucio: "pdf/matematiques/pau/2025-solucio.pdf" },
                        m25: { examen: "pdf/matematiques/m25/2025-examen.pdf", solucio: "pdf/matematiques/m25/2025-solucio.pdf" },
                        gs: { examen: "pdf/matematiques/gs/2025-examen.pdf", solucio: null }
                    },
                    {
                        any: 2024,
                        pau: { examen: "pdf/matematiques/pau/2024-examen.pdf", solucio: "pdf/matematiques/pau/2024-solucio.pdf" },
                        m25: { examen: "pdf/matematiques/m25/2024-examen.pdf", solucio: null },
                        gs: { examen: "pdf/matematiques/gs/2024-examen.pdf", solucio: "pdf/matematiques/gs/2024-solucio.pdf" }
                    }
                    // S'afegirien la resta d'anys històrics en aquest format...
                ]
            },
            {
                id: "comentari-text",
                assignaturaNom: "Comentari de Text",
                branca: "Fase Comuna",
                descripcio: "Exercicis d'anàlisi de textos, estructuració d'idees, expressió escrita, redacció d'articles i comentari crític.",
                anys: [
                    {
                        any: 2026,
                        pau: { examen: "pdf/comentari/pau/2026-examen.pdf", solucio: "pdf/comentari/pau/2026-solucio.pdf" },
                        m25: { examen: "pdf/comentari/m25/2026-examen.pdf", solucio: "pdf/comentari/m25/2026-solucio.pdf" },
                        gs: { examen: "pdf/comentari/gs/2026-examen.pdf", solucio: "pdf/comentari/gs/2026-solucio.pdf" }
                    }
                ]
            }
        ];

        // INICIALITZACIÓ I SISTEMA D'ENLLAÇOS HASH (Rutes dinàmiques)
        document.addEventListener('DOMContentLoaded', () => {
            interpretarRuta();
            window.addEventListener('hashchange', interpretarRuta);
        });

        // Llegeix la URL per saber quina vista mostrar (Home o la matèria específica)
        function interpretarRuta() {
            const ruta = window.location.hash;
            if (ruta.startsWith('#/materia/')) {
                const idMateria = ruta.replace('#/materia/', '');
                mostrarDetallMateria(idMateria);
            } else {
                mostrarCatalegHome();
            }
        }

        // --- FUNCIONS DE NAVEGACIÓ ---
        function navegarAMateria(id) {
            window.location.hash = `#/materia/${id}`;
        }

        function navegarAHome() {
            window.location.hash = '';
        }

        // --- VISTA 1: CATÀLEG PRINCIPAL ---
        function mostrarCatalegHome() {
            document.getElementById('vista-materia').classList.add('hidden');
            document.getElementById('vista-cataleg').classList.remove('hidden');
            document.title = "Exàmens Oficials i Solucions - Proves d'Accés";
            filtrarMateries(); // Carrega la graella amb els filtres actius
        }

        function renderitzarCataleg(llistat) {
            const graella = document.getElementById('graella-materies');
            const senseResultats = document.getElementById('sense-resultats');
            const comptador = document.getElementById('comptador-resultats');
            
            graella.innerHTML = '';

            if (llistat.length === 0) {
                graella.classList.add('hidden');
                senseResultats.classList.remove('hidden');
                comptador.innerHTML = "S'han trobat <strong>0</strong> matèries";
                return;
            }

            graella.classList.remove('hidden');
            senseResultats.classList.add('hidden');
            comptador.innerHTML = `Mostrant <strong>${llistat.length}</strong> matèries`;

            llistat.forEach(materia => {
                let colorBadge = "bg-gray-100 text-gray-800";
                if (materia.branca === "Fase Comuna") colorBadge = "bg-purple-100 text-purple-800";
                else if (materia.branca === "Científica-Tecnològica") colorBadge = "bg-blue-100 text-blue-800";
                else if (materia.branca === "Ciències de la Salut") colorBadge = "bg-emerald-100 text-emerald-800";
                else if (materia.branca === "Socials i Jurídiques") colorBadge = "bg-orange-100 text-orange-800";

                const targeta = document.createElement('div');
                targeta.className = "bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden flex flex-col justify-between hover:shadow-md cursor-pointer transition-all duration-200 hover:-translate-y-0.5";
                targeta.onclick = () => navegarAMateria(materia.id);

                targeta.innerHTML = `
                    <div class="p-5 text-left flex-grow">
                        <span class="inline-block px-2.5 py-0.5 rounded text-[10px] font-semibold mb-2.5 ${colorBadge}">
                            ${materia.branca}
                        </span>
                        <h4 class="text-xl font-bold text-gray-950 m-0">${materia.assignaturaNom}</h4>
                        <p class="text-xs text-gray-500 mt-2 mb-0 leading-relaxed">${materia.descripcio}</p>
                    </div>
                    <div class="px-5 py-3.5 bg-gray-50 border-t border-gray-100 flex items-center justify-between text-xs font-semibold text-blue-600">
                        <span>Veure els 10 anys de proves</span>
                        <i class="fa-solid fa-chevron-right text-[10px] transform group-hover:translate-x-1 transition-transform"></i>
                    </div>
                `;
                graella.appendChild(targeta);
            });
        }

        function filtrarMateries() {
            const cerca = document.getElementById('search').value.toLowerCase();
            const filtreBranca = document.getElementById('filtre-branca').value;

            const resultatsFiltrats = dadesMateries.filter(materia => {
                const coincideixCerca = 
                    materia.assignaturaNom.toLowerCase().includes(cerca) || 
                    materia.descripcio.toLowerCase().includes(cerca);

                const coincideixBranca = filtreBranca === "" || materia.branca === filtreBranca;

                return coincideixCerca && coincideixBranca;
            });

            renderitzarCataleg(resultatsFiltrats);
        }

        function netejarFiltres() {
            document.getElementById('search').value = '';
            document.getElementById('filtre-branca').value = '';
            filtrarMateries();
        }


        // --- VISTA 2: DISSENY DE PÀGINA DE MATÈRIA INDIVIDUAL ---
        function mostrarDetallMateria(id) {
            const materia = dadesMateries.find(m => m.id === id);
            if (!materia) {
                // Si no existeix la matèria, tornem a la home de seguretat
                navegarAHome();
                return;
            }

            document.getElementById('vista-cataleg').classList.add('hidden');
            document.getElementById('vista-materia').classList.remove('hidden');

            // Actualitzem capçalera de matèria
            document.getElementById('detall-titol').textContent = materia.assignaturaNom;
            document.getElementById('detall-branca').textContent = materia.branca;
            document.getElementById('detall-descripcio').textContent = materia.descripcio;
            document.title = `${materia.assignaturaNom} - Recursos i Exàmens de Proves d'Accés`;

            // Construïm els llistats dels 10 anys per a les 3 rutes
            construirColumnaRuta('llista-pau', materia.anys, 'pau');
            construirColumnaRuta('llista-m25', materia.anys, 'm25');
            construirColumnaRuta('llista-gs', materia.anys, 'gs');

            // Pugem dalt de tot de la pantalla
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Dibuixa el llistat de fitxers de cada any per una ruta concreta
        function construirColumnaRuta(elementId, anysArray, clauRuta) {
            const llista = document.getElementById(elementId);
            llista.innerHTML = '';

            // Generem els blocs de descàrrega ordenats per any
            anysArray.forEach(anyDada => {
                const dadesRuta = anyDada[clauRuta];
                const fila = document.createElement('div');
                fila.className = "flex items-center justify-between p-2.5 rounded-lg border border-gray-100 hover:bg-gray-50 transition-colors";

                let accionsHTML = '';

                if (dadesRuta) {
                    // Botó examen (sempre hauria d'existir)
                    const botoExamen = dadesRuta.examen 
                        ? `<a href="${dadesRuta.examen}" class="inline-flex items-center px-2.5 py-1 border border-blue-600 text-[11px] font-semibold rounded text-white bg-blue-600 hover:bg-blue-700 no-underline transition-colors" target="_blank">
                               <i class="fa-solid fa-file-pdf mr-1"></i> Examen
                           </a>`
                        : `<span class="text-xs text-gray-400">Pendent</span>`;

                    // Botó solució
                    const botoSolucio = dadesRuta.solucio
                        ? `<a href="${dadesRuta.solucio}" class="inline-flex items-center px-2.5 py-1 border border-emerald-500 text-[11px] font-semibold rounded text-emerald-700 bg-emerald-50 hover:bg-emerald-100 no-underline transition-colors" target="_blank">
                               <i class="fa-solid fa-check mr-1 text-emerald-500"></i> Solució
                           </a>`
                        : `<span class="inline-flex items-center px-2 py-1 border border-gray-200 text-[11px] font-medium rounded text-gray-400 bg-gray-50 cursor-not-allowed">
                               Pendent
                           </span>`;

                    accionsHTML = `
                        <div class="flex items-center space-x-2">
                            ${botoExamen}
                            ${botoSolucio}
                        </div>
                    `;
                } else {
                    accionsHTML = `<span class="text-xs text-gray-400 italic">No convocat/Sense dades</span>`;
                }

                fila.innerHTML = `
                    <span class="font-bold text-gray-800 text-sm bg-gray-100 px-2 py-0.5 rounded">
                        ${anyDada.any}
                    </span>
                    ${accionsHTML}
                `;
                llista.appendChild(fila);
            });
        }
    </script>
</body>
</html>
