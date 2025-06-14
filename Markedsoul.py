<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Idle Lands - Aura Farming Update</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #111827; /* bg-gray-900 */
            color: #f3f4f6; /* text-gray-200 */
        }
        .progress-bar-container { background-color: #374151; border-radius: 0.5rem; overflow: hidden; height: 1.5rem; }
        .progress-bar { background-color: #10b981; height: 100%; transition: width 0.3s ease-in-out; text-align: center; color: white; font-weight: 500; font-size: 0.875rem; line-height: 1.5rem; }
        .hp-bar { background-color: #ef4444; } /* red-500 */
        .attack-bar { background-color: #f97316; } /* orange-500 */
        .strength-bar { background-color: #eab308; } /* yellow-500 */
        .defense-bar { background-color: #22c55e; } /* green-500 */
        canvas { background-color: #1a202c; border-radius: 0.5rem; cursor: pointer; }
        
        .section-header { cursor: pointer; user-select: none; }
        .section-content { transition: max-height 0.3s ease-out, opacity 0.2s ease-out; overflow: hidden; }
        .section-content.collapsed { max-height: 0 !important; opacity: 0; }

        #context-menu {
            position: absolute;
            display: none;
            background-color: #1f2937;
            border: 1px solid #4b5563;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            padding: 0.5rem;
            z-index: 1000;
        }
        #context-menu button {
            display: block;
            width: 100%;
            padding: 0.5rem 1rem;
            text-align: left;
            background: none;
            border: none;
            color: #d1d5db;
            border-radius: 0.25rem;
            cursor: pointer;
        }
        #context-menu button:hover {
            background-color: #374151;
        }

        .item-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(56px, 1fr));
            gap: 8px;
        }
        .item-slot {
            position: relative;
            width: 56px;
            height: 56px;
            background-color: #374151;
            border: 2px solid #4b5563;
            border-radius: 0.375rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        .item-count {
            position: absolute;
            bottom: 2px;
            right: 4px;
            font-size: 0.75rem;
            font-weight: bold;
            color: white;
            text-shadow: 1px 1px 2px black;
        }
    </style>
</head>
<body class="antialiased flex items-center justify-center min-h-screen">

    <main id="game-container" class="w-full max-w-7xl mx-auto p-4">
        <div class="grid lg:grid-cols-3 gap-6">
            <div class="lg:col-span-2 relative">
                 <canvas id="game-canvas"></canvas>
                 <div id="context-menu"></div>
            </div>
            <div id="ui-panel" class="bg-gray-800 p-6 rounded-lg shadow-lg flex flex-col space-y-4 overflow-y-auto max-h-[90vh]">
                <header class="text-center">
                    <h1 class="text-3xl font-bold text-white tracking-wider">Idle Lands</h1>
                     <p class="text-xs text-gray-500 mt-1">(Progress saved locally)</p>
                </header>
                <section>
                     <h2 class="text-xl font-semibold text-white border-b border-gray-700 pb-2 mb-3">Actions</h2>
                     <div id="action-status" class="text-center text-gray-400 h-10 p-2 bg-gray-900 rounded-md flex items-center justify-center text-sm">
                        Right-click to interact.
                     </div>
                </section>
                <section id="inventory-section">
                    <div class="section-header flex justify-between items-baseline border-b border-gray-700 pb-2 mb-3">
                        <h2 class="text-xl font-semibold text-white">Inventory</h2>
                        <span id="inventory-capacity" class="text-sm text-gray-400">0 / 2</span>
                    </div>
                    <div class="section-content">
                        <div id="inventory-grid" class="item-grid"></div>
                    </div>
                </section>
                <section id="bank-section" class="hidden">
                    <div class="section-header flex justify-between items-baseline border-b border-gray-700 pb-2 mb-3">
                        <h2 class="text-xl font-semibold text-white">Storage Box</h2>
                    </div>
                     <div class="section-content">
                        <div id="bank-grid" class="item-grid"></div>
                    </div>
                </section>
                <section id="skills-section">
                    <div class="section-header flex justify-between items-baseline border-b border-gray-700 pb-2 mb-3">
                        <h2 class="text-xl font-semibold text-white">Skills</h2>
                    </div>
                     <div id="skills-list" class="section-content space-y-4">
                        <div><div class="flex justify-between items-center mb-1"><span class="font-medium">Hitpoints</span><span id="hp-level" class="font-bold text-red-400">Lv 1</span></div><div class="progress-bar-container"><div id="hp-progress" class="progress-bar hp-bar" style="width: 0%;"></div></div><div class="text-right text-xs text-gray-400 mt-1"><span id="hp-xp">0</span> / <span id="hp-xp-needed">100</span> XP</div></div>
                        <div><div class="flex justify-between items-center mb-1"><span class="font-medium">Attack</span><span id="attack-level" class="font-bold text-orange-400">Lv 1</span></div><div class="progress-bar-container"><div id="attack-progress" class="progress-bar attack-bar" style="width: 0%;"></div></div><div class="text-right text-xs text-gray-400 mt-1"><span id="attack-xp">0</span> / <span id="attack-xp-needed">100</span> XP</div></div>
                        <div><div class="flex justify-between items-center mb-1"><span class="font-medium">Strength</span><span id="strength-level" class="font-bold text-yellow-400">Lv 1</span></div><div class="progress-bar-container"><div id="strength-progress" class="progress-bar strength-bar" style="width: 0%;"></div></div><div class="text-right text-xs text-gray-400 mt-1"><span id="strength-xp">0</span> / <span id="strength-xp-needed">100</span> XP</div></div>
                        <div><div class="flex justify-between items-center mb-1"><span class="font-medium">Defense</span><span id="defense-level" class="font-bold text-green-400">Lv 1</span></div><div class="progress-bar-container"><div id="defense-progress" class="progress-bar defense-bar" style="width: 0%;"></div></div><div class="text-right text-xs text-gray-400 mt-1"><span id="defense-xp">0</span> / <span id="defense-xp-needed">100</span> XP</div></div>
                        <div><div class="flex justify-between items-center mb-1"><span class="font-medium">Woodcutting</span><span id="woodcutting-level" class="font-bold text-emerald-400">Lv 1</span></div><div class="progress-bar-container"><div id="woodcutting-progress" class="progress-bar" style="width: 0%;"></div></div><div class="text-right text-xs text-gray-400 mt-1"><span id="woodcutting-xp">0</span> / <span id="woodcutting-xp-needed">100</span> XP</div></div>
                        <div><div class="flex justify-between items-center mb-1"><span class="font-medium">Mining</span><span id="mining-level" class="font-bold text-sky-400">Lv 1</span></div><div class="progress-bar-container"><div id="mining-progress" class="progress-bar bg-sky-500" style="width: 0%;"></div></div><div class="text-right text-xs text-gray-400 mt-1"><span id="mining-xp">0</span> / <span id="mining-xp-needed">100</span> XP</div></div>
                     </div>
                </section>
            </div>
        </div>
    </main>
    
    <script type="module">
        const SAVE_KEY = 'rpgmo-idle-savegame';
        const TILE_WIDTH_ISO = 64;
        const TILE_HEIGHT_ISO = 32;
        const MAP_WIDTH_TILES = 25;
        const MAP_HEIGHT_TILES = 25;
        const RESPAWN_TIME = 15000;

        const TILES = { GRASS: 0, TREE: 1, ROCK: 2, STORAGE_BOX: 4, SLIME_SPAWN: 5, WATER: 6 };
        const ITEM_SPRITES = { wood: '🪵', ore: '🪨', slimeGoo: '💧' };
        const MONSTERS_DATA = { SLIME: { hp: 10, attack: 1, strength: 1, defense: 1, xp: 10, loot: { slimeGoo: 1 } } };

        const mapData = [
            [2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2],[2,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,2],[1,0,0,0,5,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],[1,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],[2,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,2],[2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2],
        ];
        
        let monsters = {};
        let deadMonsters = [];
        let gameState = {};
        let isPerformingAction = false;
        
        const ui = {
            canvas: document.getElementById('game-canvas'),
            ctx: document.getElementById('game-canvas').getContext('2d'),
            inventoryGrid: document.getElementById('inventory-grid'),
            bankGrid: document.getElementById('bank-grid'),
            inventoryCapacity: document.getElementById('inventory-capacity'),
            actionStatus: document.getElementById('action-status'),
            bankSection: document.getElementById('bank-section'),
            contextMenu: document.getElementById('context-menu'),
        };

        function getDefaultGameState() {
            return {
                player: { x: 12, y: 12 },
                hp: { level: 10, xp: 0, current: 55, max: 55 },
                attack: { level: 10, xp: 0 },
                strength: { level: 10, xp: 0 },
                defense: { level: 10, xp: 0 },
                woodcutting: { level: 1, xp: 0 },
                mining: { level: 1, xp: 0 },
                inventory: { wood: 0, ore: 0, slimeGoo: 0, maxSize: 2 },
                bank: { wood: 0, ore: 0, slimeGoo: 0 },
                automation: { active: false, task: null, state: 'IDLE', path: [], targetId: null, destination: null, markedTargets: [] },
                ui: { inventoryCollapsed: false, bankCollapsed: false, skillsCollapsed: false },
                combat: { active: false, targetId: null }
            };
        }

        function saveGameState() { try { localStorage.setItem(SAVE_KEY, JSON.stringify(gameState)); } catch (e) { console.error("Could not save game state:", e); } }
        function loadGameState() { try { const s = localStorage.getItem(SAVE_KEY); gameState = s ? JSON.parse(s) : getDefaultGameState(); if(!gameState.ui || !gameState.combat || !gameState.automation.markedTargets) gameState = {...getDefaultGameState(), ...gameState}; } catch (e) { console.error("Could not load game state:", e); gameState = getDefaultGameState(); } }

        function initGame() {
            const canvasContainer = ui.canvas.parentElement;
            ui.canvas.width = canvasContainer.offsetWidth;
            ui.canvas.height = Math.min(window.innerHeight * 0.85, TILE_HEIGHT_ISO * MAP_HEIGHT_TILES * 1.5);
            
            ui.canvas.addEventListener('contextmenu', handleRightClick);
            ui.canvas.addEventListener('click', handleLeftClick);
            window.addEventListener('keydown', handleInput);
            document.addEventListener('click', (event) => { if(!event.target.closest('#context-menu')) ui.contextMenu.style.display = 'none'; });

            document.querySelectorAll('.section-header').forEach(header => {
                header.addEventListener('click', () => {
                    const sectionContent = header.nextElementSibling;
                    const sectionId = header.parentElement.id;
                    const isCollapsed = sectionContent.classList.toggle('collapsed');
                    if (sectionId === 'inventory-section') gameState.ui.inventoryCollapsed = isCollapsed;
                    else if (sectionId === 'bank-section') gameState.ui.bankCollapsed = isCollapsed;
                    else if (sectionId === 'skills-section') gameState.ui.skillsCollapsed = isCollapsed;
                    saveGameState();
                });
            });
            loadGameState();
            spawnMonsters();
            updateAllUI();
            gameLoop();
        }

        function spawnMonsters() {
            monsters = {};
            let idCounter = 0;
            for (let y = 0; y < MAP_HEIGHT_TILES; y++) {
                for (let x = 0; x < MAP_WIDTH_TILES; x++) {
                    if (mapData[y][x] === TILES.SLIME_SPAWN) {
                        const id = `slime_${idCounter++}`;
                        monsters[id] = { id, type: 'SLIME', x, y, spawnX: x, spawnY: y, ...JSON.parse(JSON.stringify(MONSTERS_DATA.SLIME)), currentHp: MONSTERS_DATA.SLIME.hp };
                    }
                }
            }
        }
        
        function cartToIso(x, y) { return { x: (x - y) * (TILE_WIDTH_ISO / 2), y: (x + y) * (TILE_HEIGHT_ISO / 2) }; }
        function isoToCart(isoX, isoY, camera) {
            const worldX = isoX + camera.x;
            const worldY = isoY + camera.y;
            const cartX = Math.round((worldX / (TILE_WIDTH_ISO / 2) + worldY / (TILE_HEIGHT_ISO / 2)) / 2);
            const cartY = Math.round((worldY / (TILE_HEIGHT_ISO / 2) - worldX / (TILE_WIDTH_ISO / 2)) / 2);
            return {x: cartX, y: cartY};
        }

        let lastUpdateTime = 0;
        function gameLoop(timestamp) { 
            const now = timestamp || 0;
            const deltaTime = now - lastUpdateTime;

            if (gameState.combat.active && deltaTime > 1000) { 
                updateCombat();
                lastUpdateTime = now;
            }
            if(deltaTime > 1000) { 
                checkRespawns();
                updateAutomation(); 
                lastUpdateTime = now;
            }
            draw(); 
            requestAnimationFrame(gameLoop); 
        }

        function checkRespawns() {
            const now = Date.now();
            for(let i = deadMonsters.length - 1; i >= 0; i--) {
                const dead = deadMonsters[i];
                if(now >= dead.respawnTime) {
                    monsters[dead.id] = dead.data;
                    deadMonsters.splice(i, 1);
                }
            }
        }

        function draw() {
            const ctx = ui.ctx;
            ctx.clearRect(0, 0, ui.canvas.width, ui.canvas.height);
            const playerScreenPos = cartToIso(gameState.player.x, gameState.player.y);
            const cameraX = playerScreenPos.x - (ui.canvas.width / 2);
            const cameraY = playerScreenPos.y - (ui.canvas.height / 2);
            ctx.save();
            ctx.translate(-cameraX, -cameraY);
            for (let y = 0; y < MAP_HEIGHT_TILES; y++) { for (let x = 0; x < MAP_WIDTH_TILES; x++) { drawTile(x, y); } }
            drawMonsters();
            drawPlayer();
            ctx.restore();
        }

        function drawTile(x, y) {
            const tileType = mapData[y][x];
            const isoPos = cartToIso(x, y);
            const ctx = ui.ctx;
            ctx.save();
            ctx.translate(isoPos.x, isoPos.y);
            
            ctx.beginPath();
            ctx.moveTo(0, 0); ctx.lineTo(TILE_WIDTH_ISO / 2, TILE_HEIGHT_ISO / 2); ctx.lineTo(0, TILE_HEIGHT_ISO); ctx.lineTo(-TILE_WIDTH_ISO / 2, TILE_HEIGHT_ISO / 2); ctx.closePath();
            
            ctx.fillStyle = (tileType === TILES.WATER) ? '#3b82f6' : '#228B22';
            ctx.fill();
            ctx.strokeStyle = (tileType === TILES.WATER) ? '#2563eb' : '#1e771e';
            ctx.stroke();
            
            ctx.translate(0, TILE_HEIGHT_ISO / 2); 
            
            switch(tileType) {
                case TILES.TREE:
                    ctx.fillStyle = '#8B4513';
                    ctx.fillRect(-4, -32, 8, 16);
                    ctx.fillStyle = '#006400';
                    ctx.beginPath();
                    ctx.arc(0, -34, 15, 0, Math.PI * 2);
                    ctx.fill();
                    break;
                case TILES.ROCK:
                    const rockYOffset = -32;
                    ctx.fillStyle = '#808080';
                    ctx.beginPath();
                    ctx.moveTo(-15, 0 + rockYOffset); ctx.lineTo(-10, -15 + rockYOffset); ctx.lineTo(10, -12 + rockYOffset); ctx.lineTo(15, -5 + rockYOffset); ctx.lineTo(5, 5 + rockYOffset);
                    ctx.closePath();
                    ctx.fill();
                    break;
                case TILES.STORAGE_BOX:
                    const boxYOffset = -36;
                    ctx.fillStyle = '#8B4513'; ctx.fillRect(-15, boxYOffset, 30, 20);
                    ctx.fillStyle = '#a0522d'; ctx.fillRect(-18, boxYOffset - 2, 36, 5);
                    break;
                case TILES.MAGIC_FLOWER:
                    ctx.fillStyle = '#006400';
                    ctx.fillRect(-2, -16, 4, 16);
                    ctx.fillStyle = '#f472b6';
                    ctx.beginPath();
                    ctx.arc(0, -16, 8, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = '#fef08a';
                    ctx.beginPath();
                    ctx.arc(0, -16, 3, 0, Math.PI * 2);
                    ctx.fill();
                    break;
            }
            ctx.restore();
        }

        function drawMonsters() {
            for(const id in monsters) {
                const monster = monsters[id];
                const isoPos = cartToIso(monster.x, monster.y);
                const ctx = ui.ctx;
                
                const spriteYOffset = TILE_HEIGHT_ISO / 2;
                
                if (gameState.automation.markedTargets.includes(id)) {
                    ctx.beginPath();
                    ctx.ellipse(isoPos.x, isoPos.y + spriteYOffset, TILE_WIDTH_ISO/2.5, TILE_HEIGHT_ISO/2.5, 0, 0, Math.PI * 2);
                    ctx.strokeStyle = 'yellow';
                    ctx.lineWidth = 2;
                    ctx.stroke();
                }

                ctx.fillStyle = 'rgba(0, 255, 0, 0.7)';
                ctx.beginPath();
                ctx.arc(isoPos.x, isoPos.y, 15, Math.PI, 0);
                ctx.closePath();
                ctx.fill();
            }
        }
        
        function drawPlayer() {
            const isoPos = cartToIso(gameState.player.x, gameState.player.y);
            const ctx = ui.ctx;
            const x = isoPos.x;
            const y = isoPos.y + TILE_HEIGHT_ISO / 2;
            const playerYOffset = -32;
            
            ctx.fillStyle = '#fef08a'; // Yellow
            ctx.fillRect(x - 10, y - 20 + playerYOffset, 20, 15);
            ctx.beginPath();
            ctx.moveTo(x - 10, y - 5 + playerYOffset);
            ctx.lineTo(x - 14, y + 2 + playerYOffset);
            ctx.lineTo(x + 14, y + 2 + playerYOffset);
            ctx.lineTo(x + 10, y - 5 + playerYOffset);
            ctx.closePath();
            ctx.fill();

            ctx.fillStyle = '#ffc0cb';
            ctx.beginPath();
            ctx.arc(x, y - 25 + playerYOffset, 10, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.fillStyle = '#f472b6';
            ctx.beginPath();
            ctx.arc(x, y - 28 + playerYOffset, 12, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillRect(x - 12, y - 28 + playerYOffset, 24, 10);
        }

        const xpForLevel = (level) => Math.floor(100 * Math.pow(1.2, level - 1));
        
        function getInventorySize() {
            return Object.keys(gameState.inventory).reduce((acc, key) => key !== 'maxSize' ? acc + gameState.inventory[key] : acc, 0);
        }

        function updateDynamicGrid(gridElement, source) {
            gridElement.innerHTML = '';
            for (const item in source) {
                if (item !== 'maxSize' && source[item] > 0) {
                    const slot = document.createElement('div');
                    slot.className = 'item-slot';
                    slot.innerHTML = `
                        ${ITEM_SPRITES[item] || '?'}
                        <span class="item-count">${source[item]}</span>
                    `;
                    gridElement.appendChild(slot);
                }
            }
         }

        function handleLeftClick(e) {
            if (e.shiftKey) {
                e.preventDefault();
                const rect = ui.canvas.getBoundingClientRect();
                const playerScreenPos = cartToIso(gameState.player.x, gameState.player.y);
                const cameraX = playerScreenPos.x - (ui.canvas.width / 2);
                const cameraY = playerScreenPos.y - (ui.canvas.height / 2);
                const clickedCart = isoToCart(e.clientX - rect.left, e.clientY - rect.top, {x: cameraX, y: cameraY});
                
                for (const id in monsters) {
                    const monster = monsters[id];
                    if (monster.x === clickedCart.x && monster.y === clickedCart.y) {
                        const index = gameState.automation.markedTargets.indexOf(id);
                        if (index > -1) {
                            gameState.automation.markedTargets.splice(index, 1);
                        } else {
                            gameState.automation.markedTargets.push(id);
                        }
                        saveGameState();
                        break;
                    }
                }
            }
        }

        function handleRightClick(e) {
            e.preventDefault();
            const rect = ui.canvas.getBoundingClientRect();
            const playerScreenPos = cartToIso(gameState.player.x, gameState.player.y);
            const cameraX = playerScreenPos.x - (ui.canvas.width / 2);
            const cameraY = playerScreenPos.y - (ui.canvas.height / 2);
            const clickedCart = isoToCart(e.clientX - rect.left, e.clientY - rect.top, {x: cameraX, y: cameraY});
            
            ui.contextMenu.innerHTML = '';
            
            const tileType = (clickedCart.x >= 0 && clickedCart.x < MAP_WIDTH_TILES && clickedCart.y >= 0 && clickedCart.y < MAP_HEIGHT_TILES) ? mapData[clickedCart.y][clickedCart.x] : null;

            let clickedMonsterId = null;
            for(const id in monsters) {
                if(monsters[id].x === clickedCart.x && monsters[id].y === clickedCart.y) {
                    clickedMonsterId = id;
                    break;
                }
            }

            if(clickedMonsterId) {
                const btn = document.createElement('button');
                btn.textContent = `Attack Slime`;
                btn.onclick = () => startCombat(clickedMonsterId);
                ui.contextMenu.appendChild(btn);
            } else if (tileType === TILES.TREE) {
                 const btn = document.createElement('button');
                 btn.textContent = `Automate Woodcutting`;
                 btn.onclick = () => { startAutomation('woodcutting'); };
                 ui.contextMenu.appendChild(btn);
            } else if (tileType === TILES.ROCK) {
                 const btn = document.createElement('button');
                 btn.textContent = `Automate Mining`;
                 btn.onclick = () => { startAutomation('mining'); };
                 ui.contextMenu.appendChild(btn);
            } else {
                 if (gameState.automation.markedTargets.length > 0) {
                    const startBtn = document.createElement('button');
                    startBtn.textContent = `Start Marked Route`;
                    startBtn.onclick = () => { startAutomation('hunting'); };
                    ui.contextMenu.appendChild(startBtn);
                }
                if (gameState.automation.markedTargets.length > 0) {
                    const clearBtn = document.createElement('button');
                    clearBtn.textContent = `Clear All Marks`;
                    clearBtn.onclick = () => { gameState.automation.markedTargets = []; };
                    ui.contextMenu.appendChild(clearBtn);
                }
            }
            
            if (gameState.automation.active) {
                const stopBtn = document.createElement('button');
                stopBtn.textContent = 'Stop Automation';
                stopBtn.onclick = stopAutomation;
                ui.contextMenu.appendChild(stopBtn);
            }
            
            if (ui.contextMenu.children.length > 0) {
                ui.contextMenu.style.left = `${e.clientX - rect.left}px`;
                ui.contextMenu.style.top = `${e.clientY - rect.top}px`;
                ui.contextMenu.style.display = 'block';
            }
        }
        
        function startAutomation(task) {
            stopAutomation();
            gameState.automation.task = task;
            gameState.automation.active = true;
            gameState.automation.state = 'IDLE';
        }

        function stopAutomation() {
            gameState.automation.active = false;
            gameState.automation.state = 'IDLE';
            gameState.automation.task = null;
            gameState.automation.targetId = null;
            ui.actionStatus.textContent = 'Automation stopped.';
        }
        
        async function startCombat(monsterId, isAutomated = false) {
            if (gameState.combat.active || isPerformingAction) return;
            if (!isAutomated) {
                stopAutomation();
            }

            const monster = monsters[monsterId];
            if (!monster) return;

            const destination = findWalkableNeighbor(monster, gameState.player);
            if (!destination) { ui.actionStatus.textContent = "Can't reach that monster!"; return; }

            if (!isAdjacent(gameState.player, monster)) {
                ui.actionStatus.textContent = "Walking to monster...";
                const path = findPath(gameState.player, destination);
                if (path) {
                   await moveAlongPath(path);
                }
            }
            
            gameState.combat.active = true;
            gameState.combat.targetId = monsterId;
        }
        
        async function moveAlongPath(path) {
            isPerformingAction = true;
            for(const step of path) {
                gameState.player.x = step.x;
                gameState.player.y = step.y;
                updateAllUI();
                await new Promise(r => setTimeout(r, 200));
            }
            isPerformingAction = false;
        }

        let playerTurn = true;
        function updateCombat() {
            const combat = gameState.combat;
            if (!combat.active) return;
            const monster = monsters[combat.targetId];
            if(!monster) {
                endCombat(true); // Player won
                return;
            }
            
            ui.actionStatus.textContent = `Fighting Slime...`;

            if(playerTurn) {
                let damage = calculateDamage(gameState.attack.level, gameState.strength.level, monster.defense);
                monster.currentHp -= damage;
                gainCombatXp('attack', 5);
                gainCombatXp('strength', 5);
            } else {
                let damage = calculateDamage(monster.attack, monster.strength, gameState.defense.level);
                gameState.hp.current -= damage;
                gainCombatXp('defense', 5);
                gainCombatXp('hp', 2);
            }
            playerTurn = !playerTurn;

            if (monster.currentHp <= 0) {
                endCombat(true);
            } else if (gameState.hp.current <= 0) {
                endCombat(false);
            }
        }

        function calculateDamage(attackLevel, strengthLevel, defenseLevel) {
            const hitChance = 0.5 + (attackLevel - defenseLevel) * 0.05;
            if (Math.random() > hitChance) return 0;
            return Math.max(1, Math.floor(strengthLevel * (1 + Math.random() * 0.2)));
        }

        function gainCombatXp(skill, amount) {
            gameState[skill].xp += amount;
            let needed = xpForLevel(gameState[skill].level);
            if (gameState[skill].xp >= needed) {
                gameState[skill].xp -= needed;
                gameState[skill].level++;
                if(skill === 'hp') {
                    gameState.hp.max += 5;
                    gameState.hp.current = gameState.hp.max;
                }
            }
            updateAllUI();
        }

        function endCombat(playerWon) {
            const combat = gameState.combat;
            if (!combat.targetId) return;
            const deadMonster = monsters[combat.targetId];

            if(playerWon && deadMonster) {
                ui.actionStatus.textContent = 'You defeated the Slime!';
                const loot = deadMonster.loot;
                for(const item in loot) {
                    if(Math.random() <= (loot[item] || 1)) { 
                        gameState.inventory[item] = (gameState.inventory[item] || 0) + 1;
                    }
                }
            } else if (!playerWon) {
                 ui.actionStatus.textContent = "You have been defeated!";
            }

            if(deadMonster) {
                deadMonsters.push({
                    id: deadMonster.id,
                    respawnTime: Date.now() + RESPAWN_TIME,
                    data: { ...deadMonster, currentHp: deadMonster.hp } 
                });
                delete monsters[combat.targetId];
            }

            if(!playerWon) {
                isPerformingAction = true;
                setTimeout(() => {
                    gameState.player.x = 12;
                    gameState.player.y = 12;
                    gameState.hp.current = gameState.hp.max;
                    isPerformingAction = false;
                    ui.actionStatus.textContent = "You have respawned.";
                }, 5000);
            }

            combat.active = false;
            combat.targetId = null;
            if (gameState.automation.active) {
                gameState.automation.state = 'IDLE';
            }
        }

        function handleInput(e) {
            if (isPerformingAction || gameState.automation.active || gameState.combat.active) return;
            let { x, y } = gameState.player;
            let moved = false;
            switch(e.key) {
                case 'ArrowUp': y--; moved = true; break;
                case 'ArrowDown': y++; moved = true; break;
                case 'ArrowLeft': x--; moved = true; break;
                case 'ArrowRight': x++; moved = true; break;
                case ' ': e.preventDefault(); break; 
            }
            if (moved && isWalkable(x, y)) { gameState.player.x = x; gameState.player.y = y; updateAllUI(); saveGameState(); }
        }
        function isWalkable(x, y) {
            if (x < 0 || x >= MAP_WIDTH_TILES || y < 0 || y >= MAP_HEIGHT_TILES) return false;
             if (mapData[y][x] !== TILES.GRASS) return false;
             for (const id in monsters) {
                if(monsters[id].x === x && monsters[id].y === y) return false;
             }
            return true;
        }
        function updateSkillUI(skill) {
            const levelEl = document.getElementById(`${skill}-level`);
            const xpEl = document.getElementById(`${skill}-xp`);
            const xpNeededEl = document.getElementById(`${skill}-xp-needed`);
            const progressEl = document.getElementById(`${skill}-progress`);
            if(!levelEl) return;
            const level = gameState[skill]?.level || 1;
            const xp = gameState[skill]?.xp || 0;
            const xpNeeded = xpForLevel(level);
            const progressPercent = xpNeeded > 0 ? (xp / xpNeeded) * 100 : 100;
            levelEl.textContent = `Lv ${level}`;
            xpEl.textContent = xp;
            xpNeededEl.textContent = xpNeeded;
            progressEl.style.width = `${progressPercent}%`;
        }
        function updateAllUI() {
            if (!gameState) return;
            updateDynamicGrid(ui.inventoryGrid, gameState.inventory);
            updateDynamicGrid(ui.bankGrid, gameState.bank);
            ['hp', 'attack', 'strength', 'defense', 'woodcutting', 'mining'].forEach(skill => updateSkillUI(skill));
            
            const invSize = getInventorySize();
            ui.inventoryCapacity.textContent = `${invSize} / ${gameState.inventory.maxSize}`;
            const isNearBank = !!findWalkableNeighbor(findNearest(TILES.STORAGE_BOX, gameState.player.x, gameState.player.y), gameState.player);
            ui.bankSection.classList.toggle('hidden', !isNearBank);

            document.querySelector('#inventory-section .section-content').classList.toggle('collapsed', gameState.ui.inventoryCollapsed);
            document.querySelector('#bank-section .section-content').classList.toggle('collapsed', gameState.ui.bankCollapsed);
            document.querySelector('#skills-section .section-content').classList.toggle('collapsed', gameState.ui.skillsCollapsed);
        }
        
        async function performGatheringAction(skill, duration, xpGain, resource) {
            if (isPerformingAction) return;
            isPerformingAction = true;
            ui.actionStatus.textContent = `Gathering ${resource}...`;
            await new Promise(resolve => {
                setTimeout(() => {
                    gameState[skill].xp = (gameState[skill].xp || 0) + xpGain;
                    gameState.inventory[resource.toLowerCase()] = (gameState.inventory[resource.toLowerCase()] || 0) + 1;
                    let needed = xpForLevel(gameState[skill].level);
                    if (gameState[skill].xp >= needed) {
                        gameState[skill].xp -= needed;
                        gameState[skill].level++;
                    }
                    updateAllUI();
                    saveGameState();
                    isPerformingAction = false;
                    resolve();
                }, duration);
            });
        }
        
        function updateAutomation() {
            if (isPerformingAction || gameState.combat.active || !gameState.automation.active) {
                return;
            }

            const { automation, player } = gameState;
            const setStatus = (msg) => ui.actionStatus.textContent = msg;
            
            if (getInventorySize() >= gameState.inventory.maxSize && !['FINDING_BANK', 'WALKING_TO_BANK', 'BANKING'].includes(automation.state)) {
                automation.state = 'FINDING_BANK';
            }

            switch(automation.state) {
                case 'IDLE':
                    if (automation.task === 'hunting') {
                        automation.state = 'FINDING_TARGET';
                    } else if (automation.task === 'woodcutting' || automation.task === 'mining') {
                        automation.state = 'FINDING_RESOURCE';
                    }
                    break;
                case 'FINDING_TARGET':
                    setStatus("Finding next marked target...");
                    const target = findNearestMarked(player.x, player.y);
                    if(target) {
                        automation.targetId = target.id;
                        automation.state = 'WALKING_TO_TARGET';
                    } else {
                        setStatus("Waiting for respawns...");
                        automation.state = 'WAITING_FOR_RESPAWN';
                    }
                    break;
                case 'WAITING_FOR_RESPAWN':
                    if(gameState.automation.markedTargets.some(id => !!monsters[id])) {
                        automation.state = 'FINDING_TARGET';
                    }
                    break;
                case 'WALKING_TO_TARGET':
                    setStatus("Walking to target...");
                    const currentTarget = monsters[automation.targetId];
                    if (!currentTarget) { automation.state = 'FINDING_TARGET'; break; }
                    
                    const destination = findWalkableNeighbor(currentTarget, player);
                    if(!destination) { setStatus("Can't reach target."); stopAutomation(); break; }
                    
                    if(isAdjacent(player, currentTarget)){
                        automation.state = 'FIGHTING';
                        break;
                    }

                    const path = findPath(player, destination);
                    automation.state = 'AWAITING_ARRIVAL';
                    moveAlongPath(path || []).then(() => {
                        if (monsters[automation.targetId] && isAdjacent(gameState.player, monsters[automation.targetId])) {
                            automation.state = 'FIGHTING';
                        } else {
                            automation.state = 'FINDING_TARGET';
                        }
                    });
                    break;
                 case 'FINDING_RESOURCE':
                    const resourceType = gameState.automation.task === 'woodcutting' ? TILES.TREE : TILES.ROCK;
                    const resourceName = gameState.automation.task === 'woodcutting' ? 'Tree' : 'Rock';
                    setStatus(`Finding nearest ${resourceName.toLowerCase()}...`);
                    const resourceTarget = findNearest(resourceType, player.x, player.y);
                    if(resourceTarget) {
                        automation.target = resourceTarget;
                        automation.state = 'WALKING_TO_RESOURCE';
                    } else {
                        setStatus(`No ${resourceName.toLowerCase()}s found!`);
                        stopAutomation();
                    }
                    break;
                case 'WALKING_TO_RESOURCE':
                    setStatus(`Walking to ${gameState.automation.task === 'woodcutting' ? 'tree' : 'rock'}...`);
                    const resourceDest = findWalkableNeighbor(automation.target, player);
                    if(!resourceDest) { setStatus("Can't reach resource!"); stopAutomation(); break; }
                    if(isAdjacent(player, automation.target)){ automation.state = 'GATHERING'; break; }
                    const resourcePath = findPath(player, resourceDest);
                    automation.state = 'AWAITING_ARRIVAL';
                    moveAlongPath(resourcePath || []).then(() => {
                        if (isAdjacent(gameState.player, automation.target)) {
                            automation.state = 'GATHERING';
                        } else {
                            automation.state = 'FINDING_RESOURCE';
                        }
                    });
                    break;
                case 'GATHERING':
                    const taskName = gameState.automation.task;
                    const itemName = taskName === 'woodcutting' ? 'Wood' : 'Ore';
                    setStatus(`Gathering ${itemName}...`);
                    automation.state = 'AWAITING_GATHER';
                    performGatheringAction(taskName, 1000, 10, itemName).then(() => {
                         automation.state = 'IDLE';
                    });
                    break;
                case 'FIGHTING':
                    setStatus("Starting combat...");
                    startCombat(automation.targetId, true); 
                    automation.state = 'IN_COMBAT';
                    break;
                case 'IN_COMBAT':
                    if (!gameState.combat.active) {
                        automation.state = 'IDLE'; 
                    }
                    break;
                case 'FINDING_BANK':
                    setStatus("Inventory full! Finding storage...");
                    const bankTarget = findNearest(TILES.STORAGE_BOX, player.x, player.y);
                    if (bankTarget) {
                        const bankDest = findWalkableNeighbor(bankTarget, player);
                         if(bankDest) {
                            automation.state = 'WALKING_TO_BANK';
                         } else { setStatus("Cannot reach storage!"); stopAutomation(); }
                    } else { setStatus("No storage found!"); stopAutomation(); }
                    break;
                case 'WALKING_TO_BANK':
                    setStatus("Walking to storage...");
                    const bank = findNearest(TILES.STORAGE_BOX, player.x, player.y);
                    const bankDest = findWalkableNeighbor(bank, player);
                    const bankPath = findPath(player, bankDest);
                    automation.state = 'AWAITING_ARRIVAL';
                    moveAlongPath(bankPath || []).then(() => { automation.state = 'BANKING'; });
                    break;
                case 'BANKING':
                    setStatus("Depositing items...");
                    for(const item in gameState.inventory){
                        if(item !== 'maxSize'){
                            gameState.bank[item] = (gameState.bank[item] || 0) + gameState.inventory[item];
                            gameState.inventory[item] = 0;
                        }
                    }
                    updateAllUI();
                    saveGameState();
                    automation.state = 'AWAITING_DEPOSIT_TIMER';
                    setTimeout(() => {
                        if(gameState.automation.state === 'AWAITING_DEPOSIT_TIMER') automation.state = 'IDLE';
                    }, 1000);
                    break;
                case 'AWAITING_ARRIVAL':
                case 'AWAITING_DEPOSIT_TIMER':
                case 'AWAITING_GATHER':
                    break;
            }
        }
        
        function findPath(start, end) { if (!start || !end) return null; const queue = [[start]]; const visited = new Set([`${start.x},${start.y}`]); while (queue.length > 0) { const path = queue.shift(); const { x, y } = path[path.length - 1]; if (x === end.x && y === end.y) return path.slice(1); const neighbors = [{x: x, y: y-1}, {x: x, y: y+1}, {x: x-1, y: y}, {x: x+1, y: y}]; for (const n of neighbors) { if (isWalkable(n.x, n.y) && !visited.has(`${n.x},${n.y}`)) { visited.add(`${n.x},${n.y}`); const newPath = [...path, n]; queue.push(newPath); } } } return null; }
        function isAdjacent(posA, posB) { if (!posA || !posB) return false; const dx = Math.abs(posA.x - posB.x); const dy = Math.abs(posA.y - posB.y); return dx + dy === 1; }
        function findNearest(tileType, startX, startY) { let nearest = null; let minDistance = Infinity; for (let y = 0; y < MAP_HEIGHT_TILES; y++) { for (let x = 0; x < MAP_WIDTH_TILES; x++) { if (mapData[y][x] === tileType) { const distance = Math.abs(x - startX) + Math.abs(y - startY); if (distance < minDistance) { minDistance = distance; nearest = {x, y}; } } } } return nearest; }
        function findNearestMarked(startX, startY) { let nearest = null; let minDistance = Infinity; for (const id of gameState.automation.markedTargets) { const monster = monsters[id]; if (monster) { const distance = Math.abs(monster.x - startX) + Math.abs(monster.y - startY); if (distance < minDistance) { minDistance = distance; nearest = monster; } } } return nearest; }
        function findWalkableNeighbor(target, fromPos) { if (!target || !fromPos) return null; const neighbors = [{x: target.x, y: target.y - 1}, {x: target.x, y: target.y + 1}, {x: target.x - 1, y: target.y}, {x: target.x + 1, y: target.y}]; if (isAdjacent(fromPos, target)) return fromPos; neighbors.sort((a,b) => (Math.abs(a.x - fromPos.x) + Math.abs(a.y - fromPos.y)) - (Math.abs(b.x - fromPos.x) + Math.abs(b.y - fromPos.y))); for (const n of neighbors) { if(isWalkable(n.x, n.y)) return n; } return null; }

        initGame();
    </script>
</body>
</html>
