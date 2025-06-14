<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gridfall: Marked Souls</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto Mono', monospace;
            background-color: #0a0a0a;
            color: #e5e5e5;
            overflow: hidden;
        }
        .ui-panel {
            background-color: #1c1c1c;
            border: 1px solid #2a2a2a;
        }
        .progress-bar-container { background-color: #333; border-radius: 0.25rem; overflow: hidden; height: 1.25rem; }
        .progress-bar { 
            height: 100%; 
            transition: width 0.3s ease-in-out; 
            text-align: center; 
            color: white; 
            font-weight: 500; 
            font-size: 0.75rem; 
            line-height: 1.25rem; 
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        .hp-bar { background-color: #c026d3; } /* fuchsia-600 */
        
        #context-menu {
            position: absolute; display: none; background-color: #222; border: 1px solid #444;
            border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.4); padding: 0.5rem; z-index: 1000;
        }
        #context-menu button {
            display: block; width: 100%; padding: 0.5rem 1rem; text-align: left;
            background: none; border: none; color: #ccc; border-radius: 0.25rem; cursor: pointer;
        }
        #context-menu button:hover { background-color: #333; }
        
        .damage-popup {
            position: absolute;
            color: white;
            font-weight: bold;
            font-size: 1.1rem;
            text-shadow: 2px 2px 2px black;
            pointer-events: none;
            transition: transform 1s ease-out, opacity 1s ease-out;
            transform: translateY(0);
            opacity: 1;
        }
        .damage-popup.player { color: #f87171; } /* red-400 */
        .damage-popup.enemy { color: #fef08a; } /* yellow-200 */

        .altar-item {
            display: flex; justify-content: space-between; align-items: center; width: 100%;
            cursor: pointer; padding: 0.5rem 1rem; transition: background-color 0.2s;
            border-radius: 4px; user-select: none; font-size: 1rem; border: 1px solid #3f3f46;
        }
        .altar-item:hover { background-color: #3f3f46; }
        .altar-item.disabled {
            color: #6b7280; cursor: default; pointer-events: none;
        }
        .altar-item.disabled:hover { background-color: transparent; }
        .altar-item .cost { color: #fef08a; font-weight: bold; } /* yellow-200 */
        .altar-item.disabled .cost { color: #6b7280; }
        .altar-item.cannot-afford .cost { color: #f87171; } /* red-400 */
    </style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">

    <main id="game-container" class="w-full max-w-7xl mx-auto grid lg:grid-cols-3 gap-6">
        
        <div class="lg:col-span-2 relative">
            <canvas id="game-canvas" class="bg-black rounded-lg"></canvas>
            <div id="context-menu"></div>
        </div>
        
        <div id="ui-panel" class="p-4 rounded-lg flex flex-col space-y-4 max-h-[90vh] overflow-y-auto">
            <header class="text-center pb-2 border-b border-gray-700">
                <h1 class="text-2xl font-bold text-fuchsia-400 tracking-wider">Gridfall</h1>
                <p class="text-xs text-gray-500 mt-1">Marked Souls</p>
            </header>

            <section id="combat-info-section" class="space-y-2">
                 <div>
                    <div class="flex justify-between items-baseline">
                        <span class="text-sm font-bold text-fuchsia-300">Player</span>
                        <span id="player-souls" class="text-xs text-yellow-200">0 ✧</span>
                    </div>
                    <div class="progress-bar-container"><div id="player-hp-bar" class="progress-bar hp-bar">5/5</div></div>
                 </div>
                 <div id="enemy-combat-info" class="hidden">
                    <div id="enemy-name" class="text-sm font-bold text-green-400">Slime</div>
                    <div class="progress-bar-container"><div id="enemy-hp-bar" class="progress-bar bg-green-500">10/10</div></div>
                 </div>
            </section>

            <section>
                <h2 class="text-lg font-semibold text-white mb-2">Status</h2>
                <div id="action-status" class="text-center text-gray-400 h-10 p-2 bg-black bg-opacity-25 rounded-md flex items-center justify-center text-sm">
                    Connecting...
                </div>
            </section>
            
            <section id="stats-section">
                <h2 class="text-lg font-semibold text-white mb-2">Player Stats</h2>
                 <div id="stats-list" class="space-y-3">
                    <div>
                        <div class="flex justify-between items-center mb-1 text-sm">
                            <span class="font-medium text-fuchsia-300">Level</span>
                            <span id="player-level">Lv 1</span>
                        </div>
                        <div class="progress-bar-container">
                            <div id="xp-progress" class="progress-bar bg-fuchsia-500" style="width: 0%;"></div>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-4 text-center text-sm pt-2">
                        <div>
                            <div class="font-bold text-pink-400">Damage</div>
                            <div id="player-damage-stat">2</div>
                        </div>
                        <div>
                            <div class="font-bold text-orange-400">Dmg. Reduction</div>
                            <div id="player-defense-stat">0</div>
                        </div>
                    </div>
                 </div>
            </section>
        </div>
    </main>
    
    <!-- Soul Altar Modal -->
    <div id="soulAltarModal" class="hidden fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
        <div id="soulAltarContainer" class="bg-zinc-900 border border-zinc-700 text-white p-6 rounded-lg shadow-xl w-full max-w-sm">
            <div class="flex justify-between items-center mb-6">
                 <h2 class="text-2xl font-bold text-fuchsia-400">Soul Altar</h2>
                 <span id="altar-souls-display" class="text-lg text-yellow-200 font-bold">0 ✧</span>
            </div>
            <div id="altarListContainer" class="flex flex-col items-center space-y-3">
                <!-- List items will be generated by JS -->
            </div>
            <button id="closeAltarButton" class="mt-8 w-full bg-zinc-600 hover:bg-zinc-700 p-2 rounded transition-colors">Close</button>
        </div>
    </div>

    <script type="module">
        // --- Firebase Integration ---
        import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
        import { getFirestore, doc, getDoc, setDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

        // Firebase variables
        let app, db, auth, userId;
        const appId = typeof __app_id !== 'undefined' ? __app_id : 'gridfall-dev';
        
        async function initFirebase() {
            try {
                const firebaseConfig = JSON.parse(__firebase_config);
                app = initializeApp(firebaseConfig);
                db = getFirestore(app);
                auth = getAuth(app);
        
                if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
                    await signInWithCustomToken(auth, __initial_auth_token);
                } else {
                    await signInAnonymously(auth);
                }
                userId = auth.currentUser.uid;
                
                // Once authenticated, start the game
                await initGame();

            } catch (error) {
                console.error("Firebase Initialization Error:", error);
                document.getElementById('action-status').textContent = "Connection failed!";
            }
        }

        // --- Game Constants ---
        const TILE_SIZE = 24;
        const MAP_WIDTH_TILES = 30;
        const MAP_HEIGHT_TILES = 30;
        const RESPAWN_TIME = 10000;

        const TILES = { GRASS: 0, WALL: 1, STORAGE_BOX: 2 };
        const ITEM_SPRITES = { soulFragment: '✧' };

        const MONSTERS_DATA = { 
            GREEN_SLIME: { name: 'Green Slime', color: '#4ade80', hp: 10, attack: 1, defense: 1, loot: { soulFragment: 1 } },
            YELLOW_SLIME: { name: 'Yellow Slime', color: '#facc15', hp: 25, attack: 3, defense: 2, loot: { soulFragment: 5 } }
        };

        const SPAWN_POINTS = [
            { x: 7, y: 7, type: 'GREEN_SLIME' }, { x: 8, y: 9, type: 'GREEN_SLIME' },
            { x: 6, y: 11, type: 'GREEN_SLIME' }, { x: 22, y: 22, type: 'GREEN_SLIME' },
            { x: 24, y: 24, type: 'GREEN_SLIME' }, { x: 26, y: 22, type: 'GREEN_SLIME' },
            { x: 25, y: 5, type: 'YELLOW_SLIME' }, { x: 26, y: 7, type: 'YELLOW_SLIME' }
        ];

        const ALTAR_UPGRADES = {
            plusOneDamage: {
                name: "+1 Damage",
                maxLevel: 10,
                cost: (level) => 5 * Math.pow(2, level),
                stat: 'damage'
            },
            plusOneDefense: {
                name: "+1 Defense",
                maxLevel: 10,
                cost: (level) => 8 * Math.pow(2, level),
                stat: 'defense'
            }
        };
        
        // --- Game State ---
        let gameState = {};
        let monsters = {};
        let deadMonsters = [];
        let isPerformingAction = false;
        let lastCombatUpdateTime = 0;
        let lastLogicUpdateTime = 0;
        let playerTurn = true;

        // --- UI Elements ---
        const ui = {
            canvas: document.getElementById('game-canvas'),
            ctx: document.getElementById('game-canvas').getContext('2d'),
            actionStatus: document.getElementById('action-status'),
            contextMenu: document.getElementById('context-menu'),
            playerHpBar: document.getElementById('player-hp-bar'),
            playerSouls: document.getElementById('player-souls'),
            enemyCombatInfo: document.getElementById('enemy-combat-info'),
            enemyName: document.getElementById('enemy-name'),
            enemyHpBar: document.getElementById('enemy-hp-bar'),
            playerLevel: document.getElementById('player-level'),
            xpProgress: document.getElementById('xp-progress'),
            playerDamageStat: document.getElementById('player-damage-stat'),
            playerDefenseStat: document.getElementById('player-defense-stat'),
            soulAltarModal: document.getElementById('soulAltarModal'),
            altarListContainer: document.getElementById('altarListContainer'),
            closeAltarButton: document.getElementById('closeAltarButton'),
            altarSoulsDisplay: document.getElementById('altar-souls-display'),
        };

        // --- Map Data ---
        const mapData = Array.from({ length: MAP_HEIGHT_TILES }, (_, y) =>
            Array.from({ length: MAP_WIDTH_TILES }, (_, x) => {
                if (y === 0 || y === MAP_HEIGHT_TILES - 1 || x === 0 || x === MAP_WIDTH_TILES - 1) return TILES.WALL;
                if (x === 15 && y === 2) return TILES.STORAGE_BOX;
                return TILES.GRASS;
            })
        );
        
        // --- Initialization ---
        function getDefaultGameState() {
            return {
                player: { x: 15, y: 15 },
                level: { current: 1, xp: 0 },
                hp: { current: 5, max: 5 },
                souls: 10000000,
                upgrades: {
                    plusOneDamage: 0,
                    plusOneDefense: 0
                },
                automation: { active: false, task: null, state: 'IDLE', path: [], targetId: null, markedTargets: [] },
                combat: { active: false, targetId: null }
            };
        }

        async function initGame() {
            ui.canvas.width = TILE_SIZE * MAP_WIDTH_TILES;
            ui.canvas.height = TILE_SIZE * MAP_HEIGHT_TILES;
            ui.canvas.addEventListener('contextmenu', handleRightClick);
            ui.canvas.addEventListener('click', handleLeftClick);
            document.addEventListener('click', (e) => {
                if (ui.contextMenu.style.display === 'block' && !ui.contextMenu.contains(e.target)) {
                    ui.contextMenu.style.display = 'none';
                }
            });
            ui.closeAltarButton.addEventListener('click', closeSoulAltar);
            
            await loadGameState(); // Now async
            spawnMonsters();
            updateAllUI();
            ui.actionStatus.textContent = "Right-click to interact";
            requestAnimationFrame(gameLoop);
        }
        
        // --- Game Loop ---
        function gameLoop(timestamp) {
            const now = timestamp || 0;
            const combatDelta = now - lastCombatUpdateTime;
            const logicDelta = now - lastLogicUpdateTime;
            if (gameState.combat.active && combatDelta > 1500) {
                updateCombat();
                lastCombatUpdateTime = now;
            }
            if (logicDelta > 150) {
                checkRespawns();
                updateAutomation();
                lastLogicUpdateTime = now;
            }
            draw();
            requestAnimationFrame(gameLoop);
        }

        // --- Drawing Functions ---
        function draw() {
            const ctx = ui.ctx;
            ctx.clearRect(0, 0, ui.canvas.width, ui.canvas.height);
            const cameraOffsetX = 0, cameraOffsetY = 0;
            ctx.save();
            ctx.translate(cameraOffsetX, cameraOffsetY);
            for (let y = 0; y < MAP_HEIGHT_TILES; y++) {
                for (let x = 0; x < MAP_WIDTH_TILES; x++) {
                    drawTile(x, y);
                    const monsterId = Object.keys(monsters).find(id => monsters[id].x === x && monsters[id].y === y);
                    if (monsterId) drawMonster(monsters[monsterId]);
                    if (gameState.player.x === x && gameState.player.y === y) drawPlayer();
                }
            }
            ctx.restore();
        }

        function drawTile(x, y) {
            const tileType = mapData[y][x];
            ui.ctx.fillStyle = tileType === TILES.WALL ? '#52525b' : (tileType === TILES.STORAGE_BOX ? '#a16207' : '#27272a');
            ui.ctx.fillRect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE);
            if(tileType !== TILES.WALL) {
                ui.ctx.strokeStyle = '#3a3a3a';
                ui.ctx.strokeRect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE);
            }
        }
        
        function drawMonster(monster) {
            const monsterData = MONSTERS_DATA[monster.type];
            if (!monsterData) return;
            ui.ctx.fillStyle = monsterData.color;
            ui.ctx.fillRect(monster.x * TILE_SIZE + 4, monster.y * TILE_SIZE + 4, TILE_SIZE - 8, TILE_SIZE - 8);
            if (gameState.automation.markedTargets.includes(monster.id)) {
                ui.ctx.strokeStyle = 'white';
                ui.ctx.lineWidth = 2;
                ui.ctx.strokeRect(monster.x * TILE_SIZE + 1, monster.y * TILE_SIZE + 1, TILE_SIZE - 2, TILE_SIZE - 2);
            }
        }

        function drawPlayer() {
            ui.ctx.fillStyle = '#f472b6';
            ui.ctx.fillRect(gameState.player.x * TILE_SIZE + 6, gameState.player.y * TILE_SIZE + 6, TILE_SIZE - 12, TILE_SIZE - 12);
        }
        
        function showDamagePopup(x, y, amount, isPlayerDamage) {
            if (amount <= 0) return;
            const popup = document.createElement('div');
            popup.textContent = amount;
            popup.className = `damage-popup ${isPlayerDamage ? 'player' : 'enemy'}`;
            ui.canvas.parentElement.appendChild(popup);
            popup.style.left = `${(x * TILE_SIZE) + (TILE_SIZE / 2) - popup.offsetWidth / 2}px`;
            popup.style.top = `${(y * TILE_SIZE) - popup.offsetHeight}px`;
            setTimeout(() => {
                popup.style.transform = 'translateY(-30px)';
                popup.style.opacity = '0';
                setTimeout(() => popup.remove(), 1000);
            }, 10);
        }

        // --- Soul Altar Functions ---
        function renderAltarList() {
            const listContainer = ui.altarListContainer;
            listContainer.innerHTML = '';
            ui.altarSoulsDisplay.textContent = `${gameState.souls} ${ITEM_SPRITES.soulFragment}`;

            for (const id in ALTAR_UPGRADES) {
                const upgrade = ALTAR_UPGRADES[id];
                const currentLevel = gameState.upgrades[id] || 0;
                
                const itemEl = document.createElement('div');
                itemEl.className = 'altar-item';
                
                const nameEl = document.createElement('span');
                nameEl.textContent = `${upgrade.name} (${currentLevel}/${upgrade.maxLevel})`;
                
                const costEl = document.createElement('span');
                costEl.className = 'cost';

                if (currentLevel >= upgrade.maxLevel) {
                    itemEl.classList.add('disabled');
                    costEl.textContent = "MAX";
                } else {
                    const cost = upgrade.cost(currentLevel);
                    costEl.textContent = `${cost} ${ITEM_SPRITES.soulFragment}`;
                    if (gameState.souls < cost) {
                        itemEl.classList.add('cannot-afford');
                    }
                    itemEl.addEventListener('click', () => purchaseUpgrade(id));
                }
                
                itemEl.appendChild(nameEl);
                itemEl.appendChild(costEl);
                listContainer.appendChild(itemEl);
            }
        }

        function purchaseUpgrade(id) {
            const upgrade = ALTAR_UPGRADES[id];
            const currentLevel = gameState.upgrades[id] || 0;
            if (currentLevel >= upgrade.maxLevel) return;

            const cost = upgrade.cost(currentLevel);
            if (gameState.souls >= cost) {
                gameState.souls -= cost;
                gameState.upgrades[id]++;
                saveGameState();
                updateAllUI();
                renderAltarList();
            }
        }

        function openSoulAltar() {
            renderAltarList();
            ui.soulAltarModal.classList.remove('hidden');
        }

        function closeSoulAltar() {
            ui.soulAltarModal.classList.add('hidden');
        }

        // --- Input Handling ---
        function getTileFromClick(e) {
            const rect = ui.canvas.getBoundingClientRect();
            const x = Math.floor((e.clientX - rect.left) / TILE_SIZE);
            const y = Math.floor((e.clientY - rect.top) / TILE_SIZE);
            return {x, y};
        }

        function handleLeftClick(e) {
            if (e.shiftKey) {
                e.preventDefault();
                const { x, y } = getTileFromClick(e);
                const monsterId = Object.keys(monsters).find(id => monsters[id].x === x && monsters[id].y === y);
                if (monsterId) {
                    const index = gameState.automation.markedTargets.indexOf(monsterId);
                    if (index > -1) gameState.automation.markedTargets.splice(index, 1);
                    else gameState.automation.markedTargets.push(monsterId);
                    saveGameState();
                }
                return;
            }
            const { x, y } = getTileFromClick(e);
            if (mapData[y][x] === TILES.STORAGE_BOX) {
                openSoulAltar();
            }
        }

        function handleRightClick(e) {
            e.preventDefault();
            ui.contextMenu.innerHTML = '';
            const { x, y } = getTileFromClick(e);
            const monsterId = Object.keys(monsters).find(id => monsters[id].x === x && monsters[id].y === y);
            if (monsterId) {
                const monsterType = monsters[monsterId].type;
                const monsterName = MONSTERS_DATA[monsterType].name;
                addContextMenuButton(`Attack ${monsterName}`, () => startCombat(monsterId));
            } else {
                if (gameState.automation.markedTargets.length > 0) {
                    addContextMenuButton(`Start Marked Route`, () => startAutomation('hunting'));
                    addContextMenuButton(`Clear All Marks`, () => { gameState.automation.markedTargets = []; saveGameState(); });
                }
            }
            if (gameState.automation.active) {
                addContextMenuButton('Stop Automation', stopAutomation);
            }
            if (ui.contextMenu.children.length > 0) {
                const rect = ui.canvas.getBoundingClientRect();
                ui.contextMenu.style.left = `${e.clientX - rect.left}px`;
                ui.contextMenu.style.top = `${e.clientY - rect.top}px`;
                ui.contextMenu.style.display = 'block';
            }
        }

        function addContextMenuButton(text, onClick) {
            const btn = document.createElement('button');
            btn.textContent = text;
            btn.onclick = () => { onClick(); ui.contextMenu.style.display = 'none'; };
            ui.contextMenu.appendChild(btn);
        }

        // --- Combat & Player State ---
        function calculatePlayerStats() {
            const baseDamage = 2 + Math.floor(gameState.level.current);
            const baseDefense = Math.floor(gameState.level.current / 4);
            const damageBonus = gameState.upgrades.plusOneDamage || 0;
            const defenseBonus = gameState.upgrades.plusOneDefense || 0;
            return {
                damage: baseDamage + damageBonus,
                defense: baseDefense + defenseBonus,
            };
        }

        function updateCombat() {
            const { combat } = gameState;
            const monster = monsters[combat.targetId];
            if (!combat.active || !monster) {
                endCombat(true);
                return;
            }
            const monsterData = MONSTERS_DATA[monster.type];
            ui.actionStatus.textContent = `Fighting ${monsterData.name}...`;
            const playerStats = calculatePlayerStats();
            let damage;
            if (playerTurn) {
                damage = Math.max(playerStats.damage);
                monster.currentHp -= damage;
                showDamagePopup(monster.x, monster.y, damage, false);
                gainXp(damage);
            } else {
                damage = Math.max(1, monsterData.attack - playerStats.defense);
                gameState.hp.current -= damage;
                showDamagePopup(gameState.player.x, gameState.player.y, damage, true);
            }
            playerTurn = !playerTurn;
            updateCombatUI();
            if (monster.currentHp <= 0) endCombat(true);
            else if (gameState.hp.current <= 0) endCombat(false);
        }
        
        async function startCombat(monsterId, isAutomated = false) {
            if (gameState.combat.active || isPerformingAction) return;
            if (!isAutomated) stopAutomation();
            const monster = monsters[monsterId];
            if (!monster) return;
            if (!isAdjacent(gameState.player, monster)) {
                ui.actionStatus.textContent = "Walking to monster...";
                const path = findPath(gameState.player, monster);
                if (path) await moveAlongPath(path);
                else { ui.actionStatus.textContent = "Can't reach target."; if(isAutomated) stopAutomation(); return; }
            }
            if (isAdjacent(gameState.player, monster)) {
                gameState.combat.active = true;
                gameState.combat.targetId = monsterId;
                playerTurn = true;
                updateCombatUI();
            }
        }

        function endCombat(playerWon) {
            const { combat } = gameState;
            if (!combat.targetId) return;
            const deadMonster = monsters[combat.targetId];
            if (playerWon && deadMonster) {
                const monsterData = MONSTERS_DATA[deadMonster.type];
                ui.actionStatus.textContent = 'Target neutralized.';
                gameState.souls += monsterData.loot.soulFragment;
            } else if (!playerWon) {
                ui.actionStatus.textContent = "You have been defeated!";
            }
            if (deadMonster) {
                deadMonsters.push({
                    id: deadMonster.id,
                    respawnTime: Date.now() + RESPAWN_TIME,
                    data: { ...deadMonster, currentHp: MONSTERS_DATA[deadMonster.type].hp }
                });
                delete monsters[combat.targetId];
            }
            if (!playerWon) {
                isPerformingAction = true;
                setTimeout(() => {
                    gameState.player = getDefaultGameState().player;
                    gameState.hp.current = gameState.hp.max;
                    isPerformingAction = false;
                    ui.actionStatus.textContent = "Respawned.";
                    updateAllUI();
                }, 3000);
            }
            combat.active = false;
            combat.targetId = null;
            if (gameState.automation.active && playerWon) gameState.automation.state = 'IDLE';
            updateAllUI();
            saveGameState(); // Save after combat ends
        }

        function xpForLevel(level) {
            return Math.floor(50 * Math.pow(1.23, level - 1));
        }

        function gainXp(amount) {
            const { level } = gameState;
            level.xp += amount;
            let needed = xpForLevel(level.current);
            while (level.xp >= needed) {
                level.xp -= needed;
                level.current++;
                gameState.hp.max = level.current * 5;
                gameState.hp.current = gameState.hp.max;
                needed = xpForLevel(level.current);
            }
            updateAllUI();
        }

        // --- Automation & Movement ---
        function updateAutomation() {
            if (isPerformingAction || gameState.combat.active || !gameState.automation.active) return;
            const { automation, player } = gameState;
            const setStatus = (msg) => { ui.actionStatus.textContent = msg; };
            switch(automation.state) {
                case 'IDLE':
                    if (automation.task === 'hunting') automation.state = 'FINDING_TARGET';
                    break;
                case 'FINDING_TARGET':
                    setStatus("Finding marked soul...");
                    const target = findNearestMarked(player.x, player.y);
                    if (target) {
                        automation.targetId = target.id;
                        automation.state = 'WALKING_TO_TARGET';
                    } else {
                        setStatus("Awaiting respawns...");
                        automation.state = 'WAITING_FOR_RESPAWN';
                    }
                    break;
                case 'WALKING_TO_TARGET':
                    const currentTarget = monsters[automation.targetId];
                    if (!currentTarget) { automation.state = 'FINDING_TARGET'; break; }
                    if (isAdjacent(player, currentTarget)) { automation.state = 'FIGHTING'; }
                    else {
                        setStatus("Walking to target...");
                        const path = findPath(player, currentTarget);
                        if (path && path.length > 0) moveAlongPath(path);
                        else {
                            setStatus("Can't reach target!"); 
                            automation.markedTargets = automation.markedTargets.filter(id => id !== automation.targetId);
                            automation.state = 'FINDING_TARGET';
                        }
                    }
                    break;
                case 'FIGHTING':
                    setStatus("Initiating combat...");
                    startCombat(automation.targetId, true);
                    break;
                case 'WAITING_FOR_RESPAWN':
                    if (gameState.automation.markedTargets.some(id => !!monsters[id])) {
                        automation.state = 'FINDING_TARGET';
                    }
                    break;
            }
        }
        
        async function moveAlongPath(path) {
            if (!path || path.length === 0) return;
            isPerformingAction = true;
            for (const step of path) {
                gameState.player.x = step.x;
                gameState.player.y = step.y;
                await new Promise(r => setTimeout(r, 150));
            }
            isPerformingAction = false;
        }

        function findPath(start, end) {
            const endNode = findWalkableNeighbor(end);
            if (!endNode) return null;
            const queue = [[start]];
            const visited = new Set([`${start.x},${start.y}`]);
            while (queue.length > 0) {
                const path = queue.shift();
                const { x, y } = path[path.length - 1];
                if (x === endNode.x && y === endNode.y) return path.slice(1);
                const neighbors = [{x:x,y:y-1},{x:x,y:y+1},{x:x-1,y:y},{x:x+1,y:y}];
                for (const n of neighbors) {
                    if (isWalkable(n.x, n.y) && !visited.has(`${n.x},${n.y}`)) {
                        visited.add(`${n.x},${n.y}`);
                        const newPath = [...path, n];
                        queue.push(newPath);
                    }
                }
            }
            return null;
        }

        function isWalkable(x, y) {
            if (x < 0 || x >= MAP_WIDTH_TILES || y < 0 || y >= MAP_HEIGHT_TILES) return false;
            const tile = mapData[y][x];
            if (Object.values(monsters).some(m => m.x === x && m.y === y)) return false;
            return tile === TILES.GRASS;
        }

        function findWalkableNeighbor(target) {
            if (!target) return null;
            if (isWalkable(target.x, target.y)) return target;
            const neighbors = [{x: target.x, y: target.y - 1}, {x: target.x, y: target.y + 1}, {x: target.x - 1, y: target.y}, {x: target.x + 1, y: target.y}];
            return neighbors.find(n => isWalkable(n.x, n.y)) || null;
        }
        
        function startAutomation(task) { stopAutomation(); gameState.automation.task = task; gameState.automation.active = true; gameState.automation.state = 'IDLE'; }
        function stopAutomation() { gameState.automation.active = false; gameState.automation.state = 'IDLE'; gameState.automation.task = null; gameState.automation.targetId = null; ui.actionStatus.textContent = 'Automation stopped.'; }
        
        // --- Spawning ---
        function spawnMonsters() {
            monsters = {};
            let idCounter = 0;
            SPAWN_POINTS.forEach(point => {
                const id = `${point.type}_${idCounter++}`;
                const monsterData = MONSTERS_DATA[point.type];
                monsters[id] = { 
                    id, type: point.type, x: point.x, y: point.y, spawnX: point.x, spawnY: point.y, 
                    ...JSON.parse(JSON.stringify(monsterData)), currentHp: monsterData.hp 
                };
            });
        }

        function checkRespawns() {
            const now = Date.now();
            for(let i = deadMonsters.length - 1; i >= 0; i--) {
                const dead = deadMonsters[i];
                if(now >= dead.respawnTime) { monsters[dead.id] = dead.data; deadMonsters.splice(i, 1); }
            }
        }

        function isAdjacent(posA, posB) { return Math.abs(posA.x - posB.x) + Math.abs(posA.y - posB.y) === 1; }

        function findNearestMarked(startX, startY) {
            let nearest = null, minDistance = Infinity;
            for (const id of gameState.automation.markedTargets) {
                const monster = monsters[id];
                if (monster) {
                    const distance = Math.abs(monster.x - startX) + Math.abs(monster.y - startY);
                    if (distance < minDistance) { minDistance = distance; nearest = monster; }
                }
            }
            return nearest;
        }
        
        function updateAllUI() {
            if (!gameState || !gameState.level || !gameState.hp) return;
            const { level } = gameState;
            const neededXp = xpForLevel(level.current);
            const playerStats = calculatePlayerStats();
            
            ui.playerLevel.textContent = `Lv ${level.current}`;
            ui.xpProgress.style.width = `${(level.xp / neededXp) * 100}%`;
            ui.playerDamageStat.textContent = playerStats.damage;
            ui.playerDefenseStat.textContent = playerStats.defense;
            ui.playerSouls.textContent = `${gameState.souls} ${ITEM_SPRITES.soulFragment}`;
            updateCombatUI();
        }
        
        function updateCombatUI() {
            const { hp } = gameState;
            ui.playerHpBar.style.width = `${(hp.current / hp.max) * 100}%`;
            ui.playerHpBar.textContent = `${Math.ceil(hp.current)}/${hp.max}`;
            const monster = monsters[gameState.combat.targetId];
            if (monster) {
                const monsterData = MONSTERS_DATA[monster.type];
                ui.enemyCombatInfo.classList.remove('hidden');
                ui.enemyName.textContent = monsterData.name;
                ui.enemyHpBar.style.width = `${(monster.currentHp / monsterData.hp) * 100}%`;
                ui.enemyHpBar.textContent = `${Math.ceil(monster.currentHp)}/${monsterData.hp}`;
            } else {
                ui.enemyCombatInfo.classList.add('hidden');
            }
        }
        
        // --- Save/Load with Firebase ---
        async function saveGameState() {
            if (!userId) return; // Don't save if not logged in
            try {
                const docRef = doc(db, `artifacts/${appId}/users/${userId}/gamestate/main`);
                await setDoc(docRef, { ...gameState, lastSaved: serverTimestamp() });
            } catch(e) { console.error("Failed to save game state:", e); }
        }
        
        async function loadGameState() {
            if (!userId) { // Should not happen if called after auth
                gameState = getDefaultGameState();
                return;
            }
            const docRef = doc(db, `artifacts/${appId}/users/${userId}/gamestate/main`);
            const docSnap = await getDoc(docRef);

            if (docSnap.exists()) {
                const loadedState = docSnap.data();
                // Basic validation
                if (!loadedState || !loadedState.level || !loadedState.hp || !loadedState.upgrades) {
                    gameState = getDefaultGameState();
                } else {
                    gameState = loadedState;
                    if (!gameState.automation) gameState.automation = getDefaultGameState().automation;
                    if (!gameState.combat) gameState.combat = getDefaultGameState().combat;
                    if (!gameState.upgrades) gameState.upgrades = getDefaultGameState().upgrades;
                }
            } else {
                // No save file exists, create a new one
                gameState = getDefaultGameState();
                await saveGameState(); // Save the new state to create the document
            }
            // Post-load adjustments
            gameState.hp.max = gameState.level.current * 5;
            if (gameState.hp.current === undefined || gameState.hp.current > gameState.hp.max) {
                 gameState.hp.current = gameState.hp.max;
            }
        }
        
        // --- Start Game ---
        initFirebase();

    </script>
</body>
</html>
