

var plugin = new OverwolfPlugin("process-manager-plugin", true);

/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./node_modules/@overwolf/overwolf-api-ts/dist/index.js":
/*!**************************************************************!*\
  !*** ./node_modules/@overwolf/overwolf-api-ts/dist/index.js ***!
  \**************************************************************/
/***/ (function (__unused_webpack_module, exports, __webpack_require__) {




                var __createBinding = (this && this.__createBinding) || (Object.create ? (function (o, m, k, k2) {
                    if (k2 === undefined) k2 = k;
                    Object.defineProperty(o, k2, { enumerable: true, get: function () { return m[k]; } });
                }) : (function (o, m, k, k2) {
                    if (k2 === undefined) k2 = k;
                    o[k2] = m[k];
                }));
                var __exportStar = (this && this.__exportStar) || function (m, exports) {
                    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
                };
                Object.defineProperty(exports, "__esModule", ({ value: true }));
                __exportStar(__webpack_require__(/*! ./ow-game-listener */ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-game-listener.js"), exports);
                __exportStar(__webpack_require__(/*! ./ow-games-events */ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-games-events.js"), exports);
                __exportStar(__webpack_require__(/*! ./ow-games */ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-games.js"), exports);
                __exportStar(__webpack_require__(/*! ./ow-hotkeys */ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-hotkeys.js"), exports);
                __exportStar(__webpack_require__(/*! ./ow-listener */ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-listener.js"), exports);
                __exportStar(__webpack_require__(/*! ./ow-window */ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-window.js"), exports);


                /***/
            }),

/***/ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-game-listener.js":
/*!*************************************************************************!*\
  !*** ./node_modules/@overwolf/overwolf-api-ts/dist/ow-game-listener.js ***!
  \*************************************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


                Object.defineProperty(exports, "__esModule", ({ value: true }));
                exports.OWGameListener = void 0;
                const ow_listener_1 = __webpack_require__(/*! ./ow-listener */ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-listener.js");
                class OWGameListener extends ow_listener_1.OWListener {
                    constructor(delegate) {
                        super(delegate);
                        this.onGameInfoUpdated = (update) => {
                            if (!update || !update.gameInfo) {
                                return;
                            }
                            if (!update.runningChanged && !update.gameChanged) {
                                return;
                            }
                            if (update.gameInfo.isRunning) {
                                if (this._delegate.onGameStarted) {
                                    this._delegate.onGameStarted(update.gameInfo);
                                }
                            }
                            else {
                                if (this._delegate.onGameEnded) {
                                    this._delegate.onGameEnded(update.gameInfo);
                                }
                            }
                        };
                        this.onRunningGameInfo = (info) => {
                            if (!info) {
                                return;
                            }
                            if (info.isRunning) {
                                if (this._delegate.onGameStarted) {
                                    this._delegate.onGameStarted(info);
                                }
                            }
                        };
                    }
                    start() {
                        super.start();
                        overwolf.games.onGameInfoUpdated.addListener(this.onGameInfoUpdated);
                        overwolf.games.getRunningGameInfo(this.onRunningGameInfo);
                    }
                    stop() {
                        overwolf.games.onGameInfoUpdated.removeListener(this.onGameInfoUpdated);
                    }
                }
                exports.OWGameListener = OWGameListener;


                /***/
            }),

/***/ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-games-events.js":
/*!************************************************************************!*\
  !*** ./node_modules/@overwolf/overwolf-api-ts/dist/ow-games-events.js ***!
  \************************************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


                Object.defineProperty(exports, "__esModule", ({ value: true }));
                exports.OWGamesEvents = void 0;
                const timer_1 = __webpack_require__(/*! ./timer */ "./node_modules/@overwolf/overwolf-api-ts/dist/timer.js");
                class OWGamesEvents {
                    constructor(delegate, requiredFeatures, featureRetries = 10) {
                        this.onInfoUpdates = (info) => {
                            this._delegate.onInfoUpdates(info.info);
                        };
                        this.onNewEvents = (e) => {
                            this._delegate.onNewEvents(e);
                        };
                        this._delegate = delegate;
                        this._requiredFeatures = requiredFeatures;
                        this._featureRetries = featureRetries;
                    }
                    async getInfo() {
                        return new Promise((resolve) => {
                            overwolf.games.events.getInfo(resolve);
                        });
                    }
                    async setRequiredFeatures() {
                        let tries = 1, result;
                        while (tries <= this._featureRetries) {
                            result = await new Promise(resolve => {
                                overwolf.games.events.setRequiredFeatures(this._requiredFeatures, resolve);
                            });
                            if (result.status === 'success') {
                                console.log('setRequiredFeatures(): success: ' + JSON.stringify(result, null, 2));
                                return (result.supportedFeatures.length > 0);
                            }
                            await timer_1.Timer.wait(3000);
                            tries++;
                        }
                        console.warn('setRequiredFeatures(): failure after ' + tries + ' tries' + JSON.stringify(result, null, 2));
                        return false;
                    }
                    registerEvents() {
                        this.unRegisterEvents();
                        overwolf.games.events.onInfoUpdates2.addListener(this.onInfoUpdates);
                        overwolf.games.events.onNewEvents.addListener(this.onNewEvents);
                    }
                    unRegisterEvents() {
                        overwolf.games.events.onInfoUpdates2.removeListener(this.onInfoUpdates);
                        overwolf.games.events.onNewEvents.removeListener(this.onNewEvents);
                    }
                    async start() {
                        console.log(`[ow-game-events] START`);
                        this.registerEvents();
                        await this.setRequiredFeatures();
                        const { res, status } = await this.getInfo();
                        if (res && status === 'success') {
                            this.onInfoUpdates({ info: res });
                        }
                    }
                    stop() {
                        console.log(`[ow-game-events] STOP`);
                        this.unRegisterEvents();
                    }
                }
                exports.OWGamesEvents = OWGamesEvents;


                /***/
            }),

/***/ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-games.js":
/*!*****************************************************************!*\
  !*** ./node_modules/@overwolf/overwolf-api-ts/dist/ow-games.js ***!
  \*****************************************************************/
/***/ ((__unused_webpack_module, exports) => {


                Object.defineProperty(exports, "__esModule", ({ value: true }));
                exports.OWGames = void 0;
                class OWGames {
                    static getRunningGameInfo() {
                        return new Promise((resolve) => {
                            overwolf.games.getRunningGameInfo(resolve);
                        });
                    }
                    static classIdFromGameId(gameId) {
                        let classId = Math.floor(gameId / 10);
                        return classId;
                    }
                    static async getRecentlyPlayedGames(limit = 3) {
                        return new Promise((resolve) => {
                            if (!overwolf.games.getRecentlyPlayedGames) {
                                return resolve(null);
                            }
                            overwolf.games.getRecentlyPlayedGames(limit, result => {
                                resolve(result.games);
                            });
                        });
                    }
                    static async getGameDBInfo(gameClassId) {
                        return new Promise((resolve) => {
                            overwolf.games.getGameDBInfo(gameClassId, resolve);
                        });
                    }
                }
                exports.OWGames = OWGames;


                /***/
            }),

/***/ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-hotkeys.js":
/*!*******************************************************************!*\
  !*** ./node_modules/@overwolf/overwolf-api-ts/dist/ow-hotkeys.js ***!
  \*******************************************************************/
/***/ ((__unused_webpack_module, exports) => {


                Object.defineProperty(exports, "__esModule", ({ value: true }));
                exports.OWHotkeys = void 0;
                class OWHotkeys {
                    constructor() { }
                    static getHotkeyText(hotkeyId, gameId) {
                        return new Promise(resolve => {
                            overwolf.settings.hotkeys.get(result => {
                                if (result && result.success) {
                                    let hotkey;
                                    if (gameId === undefined)
                                        hotkey = result.globals.find(h => h.name === hotkeyId);
                                    else if (result.games && result.games[gameId])
                                        hotkey = result.games[gameId].find(h => h.name === hotkeyId);
                                    if (hotkey)
                                        return resolve(hotkey.binding);
                                }
                                resolve('UNASSIGNED');
                            });
                        });
                    }
                    static onHotkeyDown(hotkeyId, action) {
                        overwolf.settings.hotkeys.onPressed.addListener((result) => {
                            if (result && result.name === hotkeyId)
                                action(result);
                        });
                    }
                }
                exports.OWHotkeys = OWHotkeys;


                /***/
            }),

/***/ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-listener.js":
/*!********************************************************************!*\
  !*** ./node_modules/@overwolf/overwolf-api-ts/dist/ow-listener.js ***!
  \********************************************************************/
/***/ ((__unused_webpack_module, exports) => {


                Object.defineProperty(exports, "__esModule", ({ value: true }));
                exports.OWListener = void 0;
                class OWListener {
                    constructor(delegate) {
                        this._delegate = delegate;
                    }
                    start() {
                        this.stop();
                    }
                }
                exports.OWListener = OWListener;


                /***/
            }),

/***/ "./node_modules/@overwolf/overwolf-api-ts/dist/ow-window.js":
/*!******************************************************************!*\
  !*** ./node_modules/@overwolf/overwolf-api-ts/dist/ow-window.js ***!
  \******************************************************************/
/***/ ((__unused_webpack_module, exports) => {


                Object.defineProperty(exports, "__esModule", ({ value: true }));
                exports.OWWindow = void 0;
                class OWWindow {
                    constructor(name = null) {
                        this._name = name;
                        this._id = null;
                    }
                    async restore() {
                        let that = this;
                        return new Promise(async (resolve) => {
                            await that.assureObtained();
                            let id = that._id;
                            overwolf.windows.restore(id, result => {
                                if (!result.success)
                                    console.error(`[restore] - an error occurred, windowId=${id}, reason=${result.error}`);
                                resolve();
                            });
                        });
                    }
                    async minimize() {
                        let that = this;
                        return new Promise(async (resolve) => {
                            await that.assureObtained();
                            let id = that._id;
                            overwolf.windows.minimize(id, () => { });
                            return resolve();
                        });
                    }
                    async maximize() {
                        let that = this;
                        return new Promise(async (resolve) => {
                            await that.assureObtained();
                            let id = that._id;
                            overwolf.windows.maximize(id, () => { });
                            return resolve();
                        });
                    }
                    async hide() {
                        let that = this;
                        return new Promise(async (resolve) => {
                            await that.assureObtained();
                            let id = that._id;
                            overwolf.windows.hide(id, () => { });
                            return resolve();
                        });
                    }
                    async close() {
                        let that = this;
                        return new Promise(async (resolve) => {
                            await that.assureObtained();
                            let id = that._id;
                            const result = await this.getWindowState();
                            if (result.success &&
                                (result.window_state !== 'closed')) {
                                await this.internalClose();
                            }
                            return resolve();
                        });
                    }
                    dragMove(elem) {
                        elem.className = elem.className + ' draggable';
                        elem.onmousedown = e => {
                            e.preventDefault();
                            overwolf.windows.dragMove(this._name);
                        };
                    }
                    async getWindowState() {
                        let that = this;
                        return new Promise(async (resolve) => {
                            await that.assureObtained();
                            let id = that._id;
                            overwolf.windows.getWindowState(id, resolve);
                        });
                    }
                    static async getCurrentInfo() {
                        return new Promise(async (resolve) => {
                            overwolf.windows.getCurrentWindow(result => {
                                resolve(result.window);
                            });
                        });
                    }
                    obtain() {
                        return new Promise((resolve, reject) => {
                            const cb = res => {
                                if (res && res.status === "success" && res.window && res.window.id) {
                                    this._id = res.window.id;
                                    if (!this._name) {
                                        this._name = res.window.name;
                                    }
                                    resolve(res.window);
                                }
                                else {
                                    this._id = null;
                                    reject();
                                }
                            };
                            if (!this._name) {
                                overwolf.windows.getCurrentWindow(cb);
                            }
                            else {
                                overwolf.windows.obtainDeclaredWindow(this._name, cb);
                            }
                        });
                    }
                    async assureObtained() {
                        let that = this;
                        return new Promise(async (resolve) => {
                            await that.obtain();
                            return resolve();
                        });
                    }
                    async internalClose() {
                        let that = this;
                        return new Promise(async (resolve, reject) => {
                            await that.assureObtained();
                            let id = that._id;
                            overwolf.windows.close(id, res => {
                                if (res && res.success)
                                    resolve();
                                else
                                    reject(res);
                            });
                        });
                    }
                }
                exports.OWWindow = OWWindow;


                /***/
            }),

/***/ "./node_modules/@overwolf/overwolf-api-ts/dist/timer.js":
/*!**************************************************************!*\
  !*** ./node_modules/@overwolf/overwolf-api-ts/dist/timer.js ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, exports) => {


                Object.defineProperty(exports, "__esModule", ({ value: true }));
                exports.Timer = void 0;
                class Timer {
                    constructor(delegate, id) {
                        this._timerId = null;
                        this.handleTimerEvent = () => {
                            this._timerId = null;
                            this._delegate.onTimer(this._id);
                        };
                        this._delegate = delegate;
                        this._id = id;
                    }
                    static async wait(intervalInMS) {
                        return new Promise(resolve => {
                            setTimeout(resolve, intervalInMS);
                        });
                    }
                    start(intervalInMS) {
                        this.stop();
                        this._timerId = setTimeout(this.handleTimerEvent, intervalInMS);
                    }
                    stop() {
                        if (this._timerId == null) {
                            return;
                        }
                        clearTimeout(this._timerId);
                        this._timerId = null;
                    }
                }
                exports.Timer = Timer;


                /***/
            }),

/***/ "./src/AppWindow.ts":
/*!**************************!*\
  !*** ./src/AppWindow.ts ***!
  \**************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


                Object.defineProperty(exports, "__esModule", ({ value: true }));
                exports.AppWindow = void 0;
                const overwolf_api_ts_1 = __webpack_require__(/*! @overwolf/overwolf-api-ts */ "./node_modules/@overwolf/overwolf-api-ts/dist/index.js");
                class AppWindow {
                    constructor(windowName) {
                        this.maximized = false;
                        this.mainWindow = new overwolf_api_ts_1.OWWindow('background');
                        this.currWindow = new overwolf_api_ts_1.OWWindow(windowName);
                        const closeButton = document.getElementById('closeButton');
                        const maximizeButton = document.getElementById('maximizeButton');
                        const minimizeButton = document.getElementById('minimizeButton');
                        const header = document.getElementById('header');
                        this.setDrag(header);
                        const yo_btn = document.getElementById('meboss');
                        /*connect_button.addEventListener('click',() => {
                            let IP_addr = document.getElementById('ip_input').value;
                            let port_addr = document.getElementById('port_input').value;
                            this.create_phone_socket(IP_addr,port_addr);
                        });*/
                        closeButton.addEventListener('click', () => {
                            this.mainWindow.close();
                        });
                        minimizeButton.addEventListener('click', () => {
                            this.currWindow.minimize();
                        });
                        maximizeButton.addEventListener('click', () => {
                            if (!this.maximized) {
                                this.currWindow.maximize();
                            }
                            else {
                                this.currWindow.restore();
                            }
                            this.maximized = !this.maximized;
                        });
                    }
                    async getWindowState() {
                        return await this.currWindow.getWindowState();
                    }
                    async setDrag(elem) {
                        this.currWindow.dragMove(elem);
                    }
                }
                exports.AppWindow = AppWindow;


                /***/
            }),


/***/ "./src/consts.ts":
/*!***********************!*\
  !*** ./src/consts.ts ***!
  \***********************/
/***/ ((__unused_webpack_module, exports) => {


                Object.defineProperty(exports, "__esModule", ({ value: true }));
                exports.kHotkeys = exports.kWindowNames = exports.kGameClassIds = exports.kGamesFeatures = void 0;
                exports.kGamesFeatures = new Map([
                    [
                        21640,
                        [
                            'me',
                            'game_info',
                            'match_info',
                            'kill',
                            'death'
                        ]
                    ],
                ]);
                exports.kGameClassIds = Array.from(exports.kGamesFeatures.keys());
                exports.kWindowNames = {
                    inGame: 'in_game',
                    desktop: 'desktop'
                };
                exports.kHotkeys = {
                    toggle: 'sample_app_ts_showhide'
                };


                /***/
            })

        /******/
    });
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		if (__webpack_module_cache__[moduleId]) {
/******/ 			return __webpack_module_cache__[moduleId].exports;
            /******/
        }
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
            /******/
        };
/******/
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
        /******/
    }
    /******/
    /************************************************************************/
    var __webpack_exports__ = {};

    // This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
    (() => {
        var exports = __webpack_exports__;


        /*!********************************!*\
          !*** ./src/in_game/in_game.ts ***!
          \********************************/

        Object.defineProperty(exports, "__esModule", ({ value: true }));
        const overwolf_api_ts_1 = __webpack_require__(/*! @overwolf/overwolf-api-ts */ "./node_modules/@overwolf/overwolf-api-ts/dist/index.js");
        const AppWindow_1 = __webpack_require__(/*! ../AppWindow */ "./src/AppWindow.ts");
        const consts_1 = __webpack_require__(/*! ../consts */ "./src/consts.ts");
        class InGame extends AppWindow_1.AppWindow {
            constructor() {
                super(consts_1.kWindowNames.inGame);
                this._eventsLog = document.getElementById('eventsLog');
                this._infoLog = document.getElementById('infoLog');
                this.MeLog = document.getElementById('MeLog');
                this.setToggleHotkeyBehavior();
                this.setToggleHotkeyText();
            }
            static instance() {
                if (!this._instance) {
                    this._instance = new InGame();
                }
                return this._instance;
            }
            async run() {
                const gameClassId = await this.getCurrentGameClassId();
                const gameFeatures = consts_1.kGamesFeatures.get(gameClassId);
                if (gameFeatures && gameFeatures.length) {
                    this._gameEventsListener = new overwolf_api_ts_1.OWGamesEvents({
                        onInfoUpdates: this.onInfoUpdates.bind(this),
                        onNewEvents: this.onNewEvents.bind(this),
                        //onNewEvents: this.custom_action_new_event.bind(this)
                    }, gameFeatures);
                    this._gameEventsListener.start();
                }
                //this.create_phone_socket("localhost", "8765");
                this.check_for_backend();
            }

            
            check_for_backend(){
                let curreLoco = window.location.href;
                let uuid = curreLoco.split('://')[1].split('/in_game.html')[0];
                overwolf.io.fileExists(overwolf.io.paths.localAppData + "\\overwolf\\extensions\\" + uuid + "\\1.0\\Local_Api_py\\dist\\main.exe",data =>{
                    if (data.found == false) {
                        console.log(data.found);
                        overwolf.utils.openFilePicker("Pick Main.exe",data =>{
                            this.create_phone_socket("localhost","8765",data.file);
                        })
                    } 
                })
            }

            create_phone_socket(IP, PORT,Exe_path) {
                console.log("attempted http Request");
                console.log("i have been called, socket connection");
                let curreLoco = window.location.href;
                console.log(curreLoco)
                overwolf.io.fileExists(curreLoco,console.log)
                let uuid = curreLoco.split('://')[1].split('/in_game.html')[0];
                console.log(uuid);
                let absolute_path = overwolf.io.paths.localAppData + "\\overwolf\\extensions\\" + uuid + "\\1.0\\Local_Api_py\\dist\\main.exe"
                console.log(overwolf.io.paths.localAppData + "\\overwolf\\extensions\\" + uuid + "\\1.0\\Local_Api_py\\dist\\main.exe")
                //overwolf.io.dir(overwolf.io.paths.localAppData + "\\overwolf\\extensions\\" + extracted + "\\1.0", console.log)
                let IP_REAL = IP;
                let PORT_REAL = PORT;
                plugin.initialize(status => {
                    if (status == false) {
                        this.logLine(this.MeLog, "Doesn't load plugin", true);
                        return;
                    }

                    // fix path when you complie the python file
                    const path = overwolf.io.paths.localAppData + "\\overwolf\\extensions\\" + uuid + "\\1.0\\Local_Api_py\\dist\\main.exe";
                    const args = "";
                    const environmentVariables = {};

                    const hidden = true;


                    
                    plugin.get().onDataReceivedEvent.addListener(({ error, data }) => {
                        if (error) {
                            console.error(error);
                        }

                        if (data) {
                            console.log(data);
                        }
                    });

                    let _processId = -1;
                    plugin.get().onProcessExited.addListener(({ processId, exitCode }) => {
                        console.log(`process exit - pid=${processId} exitCode=${exitCode}`);
                        if (_processId == processId) {
                            processId = -1;
                        }
                    });
                    
                    try {
                        plugin.get().launchProcess(Exe_path,
                            args,
                            JSON.stringify(environmentVariables),
                            hidden,
                            true,
                            ({ error, data }) => {
                                if (error) {
                                    console.log(error);
                                    this.logLine(this.MeLog, error, true);
                                }

                                if (data) {
                                    _processId = data;
                                    console.log(_processId)
                                }
                            });
                    } catch (error) {
                        console.log(error)
                        overwolf.utils.openFilePicker("Pick the main.exe",console.log);

                    }

                    //plugin.get().suspendProcess(processId,console.log)
                    //plugin.get().resumeProcess(processId,console.log)
                    //plugin.get().terminateProcess(processId)
                });

                connection = new WebSocket(`ws://${IP_REAL}:${PORT_REAL}`);;

                console.log("after");
                connection.onopen = function () {
                    console.log("Connected: Local Servers");
                    connection.send("connected?Yes");
                };
                connection.onmessage = function (e) {
                    console.log(e);
                    if (e.data == "from_phone") {
                        document.getElementById("connection_status").className = "overlap-group2";
                        document.getElementById('disconnected').src = "img/Connected.png"
                        document.getElementById('input_container').style.visibility = "invisible";
                    }
                    if (e.data == "phone_left") {
                        document.getElementById("connection_status").className = "overlap-group1";
                        document.getElementById('input_container').style.visibility = "visible";
                        document.getElementById('disconnected').src = "img/disconnected@1x.jpg"
                    }
                };
                connection.onclose = function (event) {
                    if (event.code === 1000) {
                        console.log("The connection was closed unexpectedly. Attempting to reconnect...");
                        ws.reconnect();
                    }
                }
                connection.onerror = function (e) {
                    console.log(e)
                }
            };



            onInfoUpdates(info) {
                //this.logLine(this._infoLog, info, true);
                console.log("info updated");
                //connection.send(info)
                try {
                    // It is sending json Objects, Maybe convert to string 
                    const info_log = JSON.stringify(info)
                    connection.send(info_log)
                    //this.logLine(this.MeLog,"info sent",true)
                } catch (error) {
                    this.logLine(this.MeLog, "Not match info", true)
                    //console.log(error)
                }

                try {
                    // It is sending json Objects, Maybe convert to string 
                    if (info.game_info.scene === "CharacterSelectPersistentLevel") {
                        this.logLine(this.MeLog, "Agent Select", true);
                        connection.send("CharacterSelectPersistentLevel");
                    } else if (info.game_info.scene === "MainMenu") {
                        this.logLine(this.MeLog, "Menu", true);
                        connection.send("MainMenu");
                    } else if (info.game_info.state === "WaitingToStart") {
                        this.logLine(this.MeLog, "Game starting", true);
                        connection.send("Game starting");
                    } else if (info.match_info) {
                        // Fix this, its fucking retarded....find a way to know if it is agent selection Info Event
                        const info_to_string = JSON.stringify(info)
                        connection.send(info_to_string)
                    } else if (info.match_info.round_phase == "game_start") {
                        this.logLine(this.MeLog, "game_start", true)

                    }
                    //this.logLine(this.MeLog,"info sent",true)
                } catch (error) {
                    //console.log(error)
                }

            }

            //test fun



            /* Phone Websocket
            Send_to_client() {
                connection.onopen = function () {
                    InGame._instance.logLine(InGame._instance.MeLog, 'Connected!', true);
                    connection.send("connected");
                    this.test_func();
                    const data = null;
                    const xhr = new XMLHttpRequest();
                    xhr.withCredentials = true;

                    xhr.addEventListener("readystatechange", function () {
                        if (this.readyState === this.DONE) {
                            console.log(this.responseText);
                        }
                    });

                    xhr.open("POST", "https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/c180c414-dad1-4352-80f7-6080f0bd02b6/startcustomgame");
                    xhr.setRequestHeader("X-Riot-Entitlements-JWT", "eyJraWQiOiJrMSIsImFsZyI6IlJTMjU2In0.eyJlbnRpdGxlbWVudHMiOltdLCJhdF9oYXNoIjoiOHZYM1ZjdWxuZGlpWlY3bnViZW9qZyIsInN1YiI6IjI2Y2ZlNTg4LTA2ZmEtNWQwOS05NWU3LTQ3NjFjNjg0Zjc5MCIsImlzcyI6Imh0dHBzOlwvXC9lbnRpdGxlbWVudHMuYXV0aC5yaW90Z2FtZXMuY29tIiwiaWF0IjoxNjU5MzY1MjQ1LCJqdGkiOiJrNTFucEZwNDlmNCJ9.1DYiuVWoBdURV1yj9wSRuEguL9ugpgjMhCNziG49Ik-qH7WV1X17X8ShW-QREdRZLfes6caKkgMp--V9L2GhXwWN49orNC5gWo9ksMoyJdmVPgIRlLNoAj9qv9oeU9njoTQTD-KZLOVRPsUtRrt1AD_2PL8Xo6Jor2yDsJqdyo7tKawhrQi1sC-lCxqwBuAQr7SG4nR4BmKFZcokM3xqCTwGaNnRZ-kKwKRdvHDUl0raUyZpkEaTx1tgSxxYmEeCSsELDdqyHWufEh4CaWlnoX0vevRWadnFpWEqhJZpiAQdVGdoK7ZhnX2OCWZEGecd4wpJiMMunltAe4dX1l37mA");
                    xhr.setRequestHeader("X-Riot-ClientVersion", "release-05.01-12-732296");
                    xhr.setRequestHeader("Authorization", "Bearer eyJraWQiOiJzMSIsImFsZyI6IlJTMjU2In0.eyJwcCI6eyJjIjpudWxsfSwic3ViIjoiMjZjZmU1ODgtMDZmYS01ZDA5LTk1ZTctNDc2MWM2ODRmNzkwIiwic2NwIjpbImFjY291bnQiLCJvcGVuaWQiXSwiY2xtIjpbImVtYWlsX3ZlcmlmaWVkIiwib3BlbmlkIiwicHciLCJyZ25fRVVXMSIsInBob25lX251bWJlcl92ZXJpZmllZCIsImFjY3RfZ250IiwibG9jYWxlIiwiYWNjdCIsImFnZSIsImFjY291bnRfdmVyaWZpZWQiLCJhZmZpbml0eSJdLCJkYXQiOnsicCI6bnVsbCwiciI6IkVVVzEiLCJjIjoiZWMxIiwidSI6MjY3NjYwODM4ODExMzQ3MiwibGlkIjoiRHpwZEwzdGtwOXlNRFVpaFRWZVo0QSJ9LCJpc3MiOiJodHRwczpcL1wvYXV0aC5yaW90Z2FtZXMuY29tIiwiZXhwIjoxNjU5MzY4ODQ0LCJpYXQiOjE2NTkzNjUyNDQsImp0aSI6Ims1MW5wRnA0OWY0IiwiY2lkIjoicGxheS12YWxvcmFudC13ZWItcHJvZCJ9.RhziB-lXxYc40mwepPWFRQfZwYkQPYj9OXmn8WKpX1KfeJAdlqBrfo5mgqXBO6xCC_AnjnsfoSDDIkVU3pF77R5AcaAjJnp_VlYVveSL_AxPX18Nd4xMaz6ohmlfAdR62sdF2AZWGfdeoUxmL-YCMP5kmlHCOICONG_PTOEo6z0");
                    xhr.send(data);
                };
                // Log errors
                connection.onerror = function (error) {
                    console.log('WebSocket Error ' + error);

                };

                // Log messages from the server
                connection.onmessage = function (e) {
                    console.log('Server: ' + e.data);
                    this.logLine(this.MeLog, "message from android", true);
                };

                connection.close = async function () {
                    InGame._instance.logLine(InGame._instance.MeLog, 'Disconnected', true);
                }
            }*/

            /*
            custom_action_new_event(e) {
                switch (e.events[0].name) {
                    case "kill":
                        InGame._instance.logLine(InGame._instance.MeLog, connection.readyState, true);
                        connection.send("kill");
                    case "match_start":
                        this.logLine(this.MeLog,"Should send the command now",true);
                        connection.send("Started");
                    //"Start jiggling here"
                    case "match_end":
                        this.logLine(this.MeLog, "Game Over", true);
                        connection.send("Ended")
                    // Start new match here
                    case "death":
                        this.logLine(this.MeLog,"Dead",true)
                        connection.send("death")
                }
                //this.logLine(this.MeLog,e.events[0].name,true);
                this.logLine(this._eventsLog, e, true);
            }*/

            // Only One event Function can exist at once, the one below doesn't work if the above exists
            onNewEvents(e) {
                const shouldHighlight = e.events.some(event => {
                    /*switch (event.name) {
                        case 'kill':
                            this.logLine(this.MeLog,"You killed a nigger",true)
                        case 'death':
                            this.logLine(this.MeLog,"you died",true)
                        case 'assist':
                        case 'level':
                        case 'matchStart':
                            this.logLine(this.MeLog,"I am the real starter",true)
                        case 'match_start':
                            this.logLine(this.MeLog,"This might be the real one",true)
                        case 'matchEnd':
                        case 'match_end':
                            return true;
                    }
                    return false;
                    */
                    if (event.name == "kill") {
                        this.logLine(this.MeLog, "You killed", true)
                        console.log("Kill");
                        try {
                            connection.send("kill");
                        } catch (error) {

                        }
                    } else if (event.name == "match_start") {
                        this.logLine(this.MeLog, "match started", true)
                        console.log("Match_Start");
                        try {
                            connection.send("Started");
                        } catch (error) {

                        }

                    } else if (event.name == "match_end") {
                        this.logLine(this.MeLog, "Match has ended");
                        console.log("Match Ended");
                        try {
                            connection.send("match end");
                        } catch (error) {

                        }

                    }
                });
                //this.logLine(this._eventsLog, e, shouldHighlight);
            }
            async setToggleHotkeyText() {
                const gameClassId = await this.getCurrentGameClassId();
                const hotkeyText = await overwolf_api_ts_1.OWHotkeys.getHotkeyText(consts_1.kHotkeys.toggle, gameClassId);
                const hotkeyElem = document.getElementById('hotkey');
                hotkeyElem.textContent = hotkeyText;
            }

            // Here is the hotkey toggle behavior
            async setToggleHotkeyBehavior() {
                const toggleInGameWindow = async (hotkeyResult) => {
                    console.log(`pressed hotkey for ${hotkeyResult.name}`);
                    const inGameState = await this.getWindowState();
                    if (inGameState.window_state === "normal" ||
                        inGameState.window_state === "maximized") {
                        this.currWindow.minimize();
                    }
                    else if (inGameState.window_state === "minimized" ||
                        inGameState.window_state === "closed") {
                        this.currWindow.restore();
                        //this.currWindow.maximize();
                    }
                };
                overwolf_api_ts_1.OWHotkeys.onHotkeyDown(consts_1.kHotkeys.toggle, toggleInGameWindow);
            }
            logLine(log, data, highlight) {
                const line = document.createElement('pre');
                line.textContent = JSON.stringify(data);
                if (highlight) {
                    line.className = 'highlight';
                }
                const shouldAutoScroll = log.scrollTop + log.offsetHeight >= log.scrollHeight - 10;
                log.appendChild(line);
                if (shouldAutoScroll) {
                    log.scrollTop = log.scrollHeight;
                }
            }
            async getCurrentGameClassId() {
                const info = await overwolf_api_ts_1.OWGames.getRunningGameInfo();
                return (info && info.isRunning && info.classId) ? info.classId : null;
            }
        }


        //let connection = new WebSocket("ws://192.168.1.13:4444");

        //let connection = new WebSocket("ws://192.168.1.22:4444")
        var connection;


        InGame.instance().run();

    })();


    /******/
})()
    ;
