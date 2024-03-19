"use strict";(()=>{var Ee=Object.create;var J=Object.defineProperty;var ke=Object.getOwnPropertyDescriptor;var Se=Object.getOwnPropertyNames;var _e=Object.getPrototypeOf,Re=Object.prototype.hasOwnProperty;var X=(e,t)=>()=>(t||e((t={exports:{}}).exports,t),t.exports);var Pe=(e,t,n,r)=>{if(t&&typeof t=="object"||typeof t=="function")for(let o of Se(t))!Re.call(e,o)&&o!==n&&J(e,o,{get:()=>t[o],enumerable:!(r=ke(t,o))||r.enumerable});return e};var Y=(e,t,n)=>(n=e!=null?Ee(_e(e)):{},Pe(t||!e||!e.__esModule?J(n,"default",{value:e,enumerable:!0}):n,e));var ie=X((tt,B)=>{"use strict";var C=typeof Reflect=="object"?Reflect:null,Q=C&&typeof C.apply=="function"?C.apply:function(t,n,r){return Function.prototype.apply.call(t,n,r)},S;C&&typeof C.ownKeys=="function"?S=C.ownKeys:Object.getOwnPropertySymbols?S=function(t){return Object.getOwnPropertyNames(t).concat(Object.getOwnPropertySymbols(t))}:S=function(t){return Object.getOwnPropertyNames(t)};function Ie(e){console&&console.warn&&console.warn(e)}var Z=Number.isNaN||function(t){return t!==t};function i(){i.init.call(this)}B.exports=i;B.exports.once=Be;i.EventEmitter=i;i.prototype._events=void 0;i.prototype._eventsCount=0;i.prototype._maxListeners=void 0;var $=10;function _(e){if(typeof e!="function")throw new TypeError('The "listener" argument must be of type Function. Received type '+typeof e)}Object.defineProperty(i,"defaultMaxListeners",{enumerable:!0,get:function(){return $},set:function(e){if(typeof e!="number"||e<0||Z(e))throw new RangeError('The value of "defaultMaxListeners" is out of range. It must be a non-negative number. Received '+e+".");$=e}});i.init=function(){(this._events===void 0||this._events===Object.getPrototypeOf(this)._events)&&(this._events=Object.create(null),this._eventsCount=0),this._maxListeners=this._maxListeners||void 0};i.prototype.setMaxListeners=function(t){if(typeof t!="number"||t<0||Z(t))throw new RangeError('The value of "n" is out of range. It must be a non-negative number. Received '+t+".");return this._maxListeners=t,this};function ee(e){return e._maxListeners===void 0?i.defaultMaxListeners:e._maxListeners}i.prototype.getMaxListeners=function(){return ee(this)};i.prototype.emit=function(t){for(var n=[],r=1;r<arguments.length;r++)n.push(arguments[r]);var o=t==="error",s=this._events;if(s!==void 0)o=o&&s.error===void 0;else if(!o)return!1;if(o){var a;if(n.length>0&&(a=n[0]),a instanceof Error)throw a;var c=new Error("Unhandled error."+(a?" ("+a.message+")":""));throw c.context=a,c}var l=s[t];if(l===void 0)return!1;if(typeof l=="function")Q(l,this,n);else for(var u=l.length,d=ae(l,u),r=0;r<u;++r)Q(d[r],this,n);return!0};function te(e,t,n,r){var o,s,a;if(_(n),s=e._events,s===void 0?(s=e._events=Object.create(null),e._eventsCount=0):(s.newListener!==void 0&&(e.emit("newListener",t,n.listener?n.listener:n),s=e._events),a=s[t]),a===void 0)a=s[t]=n,++e._eventsCount;else if(typeof a=="function"?a=s[t]=r?[n,a]:[a,n]:r?a.unshift(n):a.push(n),o=ee(e),o>0&&a.length>o&&!a.warned){a.warned=!0;var c=new Error("Possible EventEmitter memory leak detected. "+a.length+" "+String(t)+" listeners added. Use emitter.setMaxListeners() to increase limit");c.name="MaxListenersExceededWarning",c.emitter=e,c.type=t,c.count=a.length,Ie(c)}return e}i.prototype.addListener=function(t,n){return te(this,t,n,!1)};i.prototype.on=i.prototype.addListener;i.prototype.prependListener=function(t,n){return te(this,t,n,!0)};function Oe(){if(!this.fired)return this.target.removeListener(this.type,this.wrapFn),this.fired=!0,arguments.length===0?this.listener.call(this.target):this.listener.apply(this.target,arguments)}function ne(e,t,n){var r={fired:!1,wrapFn:void 0,target:e,type:t,listener:n},o=Oe.bind(r);return o.listener=n,r.wrapFn=o,o}i.prototype.once=function(t,n){return _(n),this.on(t,ne(this,t,n)),this};i.prototype.prependOnceListener=function(t,n){return _(n),this.prependListener(t,ne(this,t,n)),this};i.prototype.removeListener=function(t,n){var r,o,s,a,c;if(_(n),o=this._events,o===void 0)return this;if(r=o[t],r===void 0)return this;if(r===n||r.listener===n)--this._eventsCount===0?this._events=Object.create(null):(delete o[t],o.removeListener&&this.emit("removeListener",t,r.listener||n));else if(typeof r!="function"){for(s=-1,a=r.length-1;a>=0;a--)if(r[a]===n||r[a].listener===n){c=r[a].listener,s=a;break}if(s<0)return this;s===0?r.shift():Fe(r,s),r.length===1&&(o[t]=r[0]),o.removeListener!==void 0&&this.emit("removeListener",t,c||n)}return this};i.prototype.off=i.prototype.removeListener;i.prototype.removeAllListeners=function(t){var n,r,o;if(r=this._events,r===void 0)return this;if(r.removeListener===void 0)return arguments.length===0?(this._events=Object.create(null),this._eventsCount=0):r[t]!==void 0&&(--this._eventsCount===0?this._events=Object.create(null):delete r[t]),this;if(arguments.length===0){var s=Object.keys(r),a;for(o=0;o<s.length;++o)a=s[o],a!=="removeListener"&&this.removeAllListeners(a);return this.removeAllListeners("removeListener"),this._events=Object.create(null),this._eventsCount=0,this}if(n=r[t],typeof n=="function")this.removeListener(t,n);else if(n!==void 0)for(o=n.length-1;o>=0;o--)this.removeListener(t,n[o]);return this};function re(e,t,n){var r=e._events;if(r===void 0)return[];var o=r[t];return o===void 0?[]:typeof o=="function"?n?[o.listener||o]:[o]:n?Ae(o):ae(o,o.length)}i.prototype.listeners=function(t){return re(this,t,!0)};i.prototype.rawListeners=function(t){return re(this,t,!1)};i.listenerCount=function(e,t){return typeof e.listenerCount=="function"?e.listenerCount(t):oe.call(e,t)};i.prototype.listenerCount=oe;function oe(e){var t=this._events;if(t!==void 0){var n=t[e];if(typeof n=="function")return 1;if(n!==void 0)return n.length}return 0}i.prototype.eventNames=function(){return this._eventsCount>0?S(this._events):[]};function ae(e,t){for(var n=new Array(t),r=0;r<t;++r)n[r]=e[r];return n}function Fe(e,t){for(;t+1<e.length;t++)e[t]=e[t+1];e.pop()}function Ae(e){for(var t=new Array(e.length),n=0;n<t.length;++n)t[n]=e[n].listener||e[n];return t}function Be(e,t){return new Promise(function(n,r){function o(a){e.removeListener(t,s),r(a)}function s(){typeof e.removeListener=="function"&&e.removeListener("error",o),n([].slice.call(arguments))}se(e,t,s,{once:!0}),t!=="error"&&De(e,o,{once:!0})})}function De(e,t,n){typeof e.on=="function"&&se(e,"error",t,n)}function se(e,t,n,r){if(typeof e.on=="function")r.once?e.once(t,n):e.on(t,n);else if(typeof e.addEventListener=="function")e.addEventListener(t,function o(s){r.once&&e.removeEventListener(t,o),n(s)});else throw new TypeError('The "emitter" argument must be of type EventEmitter. Received type '+typeof e)}});var pe=X((st,p)=>{p.exports.boot=function(e){return e};p.exports.ssrMiddleware=function(e){return e};p.exports.configure=function(e){return e};p.exports.preFetch=function(e){return e};p.exports.route=function(e){return e};p.exports.store=function(e){return e};p.exports.bexBackground=function(e){return e};p.exports.bexContent=function(e){return e};p.exports.bexDom=function(e){return e};p.exports.ssrProductionExport=function(e){return e};p.exports.ssrCreate=function(e){return e};p.exports.ssrListen=function(e){return e};p.exports.ssrClose=function(e){return e};p.exports.ssrServeStaticContent=function(e){return e};p.exports.ssrRenderPreloadTag=function(e){return e}});var ue=Y(ie());var D,R=0,f=new Array(256);for(let e=0;e<256;e++)f[e]=(e+256).toString(16).substring(1);var je=(()=>{let e=typeof crypto!="undefined"?crypto:typeof window!="undefined"?window.crypto||window.msCrypto:void 0;if(e!==void 0){if(e.randomBytes!==void 0)return e.randomBytes;if(e.getRandomValues!==void 0)return t=>{let n=new Uint8Array(t);return e.getRandomValues(n),n}}return t=>{let n=[];for(let r=t;r>0;r--)n.push(Math.floor(Math.random()*256));return n}})(),ce=4096;function le(){(D===void 0||R+16>ce)&&(R=0,D=je(ce));let e=Array.prototype.slice.call(D,R,R+=16);return e[6]=e[6]&15|64,e[8]=e[8]&63|128,f[e[0]]+f[e[1]]+f[e[2]]+f[e[3]]+"-"+f[e[4]]+f[e[5]]+"-"+f[e[6]]+f[e[7]]+"-"+f[e[8]]+f[e[9]]+"-"+f[e[10]]+f[e[11]]+f[e[12]]+f[e[13]]+f[e[14]]+f[e[15]]}var Ne={undefined:()=>0,boolean:()=>4,number:()=>8,string:e=>2*e.length,object:e=>e?Object.keys(e).reduce((t,n)=>j(n)+j(e[n])+t,0):0},j=e=>Ne[typeof e](e),L=class extends ue.EventEmitter{constructor(t){super(),this.setMaxListeners(1/0),this.wall=t,t.listen(n=>{Array.isArray(n)?n.forEach(r=>this._emit(r)):this._emit(n)}),this._sendingQueue=[],this._sending=!1,this._maxMessageSize=32*1024*1024}send(t,n){return this._send([{event:t,payload:n}])}getEvents(){return this._events}on(t,n){return super.on(t,r=>{n({...r,respond:o=>this.send(r.eventResponseKey,o)})})}_emit(t){typeof t=="string"?this.emit(t):this.emit(t.event,t.payload)}_send(t){return this._sendingQueue.push(t),this._nextSend()}_nextSend(){if(!this._sendingQueue.length||this._sending)return Promise.resolve();this._sending=!0;let t=this._sendingQueue.shift(),n=t[0],r=`${n.event}.${le()}`,o=r+".result";return new Promise((s,a)=>{let c=[],l=u=>{if(u!==void 0&&u._chunkSplit){let d=u._chunkSplit;c=[...c,...u.data],d.lastChunk&&(this.off(o,l),s(c))}else this.off(o,l),s(u)};this.on(o,l);try{let u=t.map(d=>({...d,payload:{data:d.payload,eventResponseKey:o}}));this.wall.send(u)}catch(u){let d="Message length exceeded maximum allowed length.";if(u.message===d&&Array.isArray(n.payload)){let x=j(n);if(x>this._maxMessageSize){let v=Math.ceil(x/this._maxMessageSize),h=Math.ceil(n.payload.length/v),F=n.payload;for(let E=0;E<v;E++){let A=Math.min(F.length,h);this.wall.send([{event:n.event,payload:{_chunkSplit:{count:v,lastChunk:E===v-1},data:F.splice(0,A)}}])}}}}this._sending=!1,setTimeout(()=>this._nextSend(),16)})}};var fe=(e,t)=>{window.addEventListener("message",n=>{if(n.source===window&&n.data.from!==void 0&&n.data.from===t){let r=n.data[0],o=e.getEvents();for(let s in o)s===r.event&&o[s](r.payload)}},!1)};var ve=Y(pe());var Ue=chrome.runtime.getURL("assets/config.js"),me,P=(me=globalThis.browser)!=null?me:globalThis.chrome;async function He(){let e=await P.storage.local.get("defaultConfig");if(e.defaultConfig)return e.defaultConfig;let t={},n=["DelayTime","RepeatTimes","port"],r=["enabledFor","useCapsolver","manualSolving","useProxy"],o=/\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$/gm,c=(await(await fetch(Ue)).text()).replace(o,""),l=c.slice(c.indexOf("{")+1,c.lastIndexOf("}")),u=JSON.stringify(l).replaceAll('\\"',"'").replaceAll("\\n","").replaceAll('"',"").replaceAll(" ",""),d=u.indexOf("blackUrlList"),x=u.slice(d),v=x.indexOf("],"),h=x.slice(0,v+1);u.replace(h,"").split(",").forEach(Te=>{let[k,G]=Te.split(":");if(k&&G){let w=G.replaceAll("'","").replaceAll('"',"");for(let y=0;y<n.length;y++)k.endsWith(n[y])&&(w=Number(w));for(let y=0;y<r.length;y++)k.startsWith(r[y])&&(w=w==="true");t[k]=w}}),h=h.replaceAll("'","").replaceAll('"',"");let A=h.indexOf(":["),Me=h.slice(A+2,h.length-1);return t.blackUrlList=Me.split(","),P.storage.local.set({defaultConfig:t}),t}var M={manualSolving:!1,apiKey:"",appId:"",enabledForImageToText:!0,enabledForRecaptchaV3:!0,enabledForHCaptcha:!0,enabledForGeetestV4:!1,recaptchaV3MinScore:.5,enabledForRecaptcha:!0,enabledForFunCaptcha:!0,enabledForDataDome:!1,enabledForAwsCaptcha:!0,useProxy:!1,proxyType:"http",hostOrIp:"",port:"",proxyLogin:"",proxyPassword:"",enabledForBlacklistControl:!1,blackUrlList:[],isInBlackList:!1,reCaptchaMode:"click",reCaptchaDelayTime:0,reCaptchaCollapse:!1,reCaptchaRepeatTimes:10,reCaptcha3Mode:"token",reCaptcha3DelayTime:0,reCaptcha3Collapse:!1,reCaptcha3RepeatTimes:10,reCaptcha3TaskType:"ReCaptchaV3TaskProxyLess",hCaptchaMode:"click",hCaptchaDelayTime:0,hCaptchaCollapse:!1,hCaptchaRepeatTimes:10,funCaptchaMode:"click",funCaptchaDelayTime:0,funCaptchaCollapse:!1,funCaptchaRepeatTimes:10,geetestMode:"click",geetestCollapse:!1,geetestDelayTime:0,geetestRepeatTimes:10,textCaptchaMode:"click",textCaptchaCollapse:!1,textCaptchaDelayTime:0,textCaptchaRepeatTimes:10,enabledForCloudflare:!1,cloudflareMode:"click",cloudflareCollapse:!1,cloudflareDelayTime:0,cloudflareRepeatTimes:10,datadomeMode:"click",datadomeCollapse:!1,datadomeDelayTime:0,datadomeRepeatTimes:10,awsCaptchaMode:"click",awsCollapse:!1,awsDelayTime:0,awsRepeatTimes:10,useCapsolver:!0,isInit:!1,solvedCallback:"captchaSolvedCallback",textCaptchaSourceAttribute:"capsolver-image-to-text-source",textCaptchaResultAttribute:"capsolver-image-to-text-result"},de={proxyType:["socks5","http","https","socks4"],mode:["click","token"]};async function he(){let e=await He(),t=Object.keys(e);for(let n of t)if(!(n==="proxyType"&&!de[n].includes(e[n]))){{if(n.endsWith("Mode")&&!de.mode.includes(e[n]))continue;if(n==="port"){if(typeof e.port!="number")continue;M.port=e.port}}Reflect.has(M,n)&&typeof M[n]==typeof e[n]&&(M[n]=e[n])}return M}var We=he(),b={default:We,async get(e){return(await this.getAll())[e]},async getAll(){let e=await he(),t=await P.storage.local.get("config");return b.joinConfig(e,t.config)},async set(e){let t=await b.getAll(),n=b.joinConfig(t,e);return P.storage.local.set({config:n})},joinConfig(e,t){let n={};if(e)for(let r in e)n[r]=e[r];if(t)for(let r in t)n[r]=t[r];return n}};function g(e){return new Promise(t=>setTimeout(t,e))}function N(e,t){function n(r,o,s){let a=["mouseover","mousedown","mouseup","click"],c={clientX:o,clientY:s,bubbles:!0};for(let l=0;l<a.length;l++){let u=new MouseEvent(a[l],c);r.dispatchEvent(u)}}e.forEach(r=>{n(t,r.x,r.y)})}var T="",m="",H="",I="",U=0,ge=0;function W(){let e=document.querySelector("canvas");return e==null?void 0:e.toDataURL()}function qe(){return{image:m==="toycarcity"?T:JSON.parse(T),question:m==="toycarcity"?"aws:toycarcity:carcity":`aws:grid:${H}`}}async function Ke(e){var c;let t=(c=e==null?void 0:e.box)!=null?c:[],n=0,r=0,o=[],s=document.querySelector("canvas"),a=s.getBoundingClientRect();for(let l=0;l<t.length;l++)l%2===0?n=t[l]+a.left:(r=t[l]+a.top,o.push({x:n,y:r}));N(o,s),I=W(),await g(500),ye()}function ze(e){let n=document.querySelector("canvas").getBoundingClientRect(),r=n.width,o=n.height,s=Math.floor(e%3*(r/3)+r/6)+n.left,a=Math.floor(Math.floor(e/3)*(o/3)+o/6)+n.top;return{x:s,y:a}}async function Ve(e){var r;let t=(r=e==null?void 0:e.objects)!=null?r:[],n=document.querySelector("canvas");for(let o=0;o<t.length;o++){let s=ze(t[o]);N([s],n),await g(200)}I=W(),await g(500),ye()}function ye(){let e=document.querySelector("#amzn-btn-verify-internal");e==null||e.click()}function Ge(){return document.querySelector("#captcha-container")&&document.querySelector("#amzn-captcha-verify-button")}function Je(){document.querySelector("#amzn-captcha-verify-button").click()}async function Xe(){let e=W();if(e===I)return!1;let t=document.querySelector("#amzn-btn-verify-internal");return!t||t.style.display==="none"?!1:(I=e,!0)}async function Ye(){let e=await b.getAll();if(!e.useCapsolver||!e.enabledForAwsCaptcha||!e.apiKey||e.enabledForBlacklistControl&&e.isInBlackList||e.awsCaptchaMode!=="click")return!1;if(ge<U||!m)return;let t=qe(),n={action:"solver",captchaType:"awsCaptcha",params:t};chrome.runtime.sendMessage(n).then(r=>{var o,s,a;if(!(r!=null&&r.response)||((o=r==null?void 0:r.response)==null?void 0:o.error)){T="",m="",U++,z();return}m==="toycarcity"?Ke((s=r.response.response)==null?void 0:s.solution):Ve((a=r.response.response)==null?void 0:a.solution)})}function be(){let e=setInterval(async()=>{await Xe()&&(clearInterval(e),await Ye())},1e3)}async function q(e){try{let t=JSON.parse(e);if(!(t!=null&&t.problem_type))return;m=t.problem_type,T=t.assets.image||t.assets.images,m!=="toycarcity"&&(H=JSON.parse(t.assets.target)[0]),be()}catch(t){console.error(t)}}async function K(e){var t;try{let n=JSON.parse(e);if(n.token)return;if(n.success){chrome.runtime.sendMessage({action:"solved"});return}if(!((t=n==null?void 0:n.problem)!=null&&t.problem_type))return;m=n.problem.problem_type,T=n.problem.assets.image||n.problem.assets.images,m!=="toycarcity"&&(H=JSON.parse(n.problem.assets.target)[0]),U++,be()}catch(n){console.error(n)}}function z(e){e&&(ge=e.awsRepeatTimes);let t=setInterval(()=>{Ge()&&(Je(),clearInterval(t))},1e3)}function Qe(){let e=document.createElement("script");e.src=chrome.runtime.getURL("assets/inject/inject-aws.js");let t=document.head||document.documentElement;if(t.children.length!==0)t.appendChild(e);else{let n=setInterval(()=>{document.querySelector("#amzn-btn-verify-internal")&&(document.head.appendChild(e),clearInterval(n),window.addEventListener("message",function(o){var s,a;if(((s=o==null?void 0:o.data)==null?void 0:s.type)==="xhr"||((a=o==null?void 0:o.data)==null?void 0:a.type)==="fetch"){let c=o.data.url;c.includes("/problem")&&q(o.data.data),c.includes("/verify")&&K(o.data.data)}}),g(1e3).then(()=>{document.querySelector("#amzn-btn-refresh-internal").click()}))},300)}}Qe();window.addEventListener("message",function(e){var t,n;if(((t=e==null?void 0:e.data)==null?void 0:t.type)==="xhr"||((n=e==null?void 0:e.data)==null?void 0:n.type)==="fetch"){let r=e.data.url;r.includes("/problem")&&q(e.data.data),r.includes("/verify")&&K(e.data.data)}});function Ce(e){z(e)}async function $e(e){!e.useCapsolver||!e.enabledForAwsCaptcha||!e.apiKey||e.enabledForBlacklistControl&&e.isInBlackList||e.awsCaptchaMode!=="click"||(await g(e.awsDelayTime),Ce(e))}var O=null;O&&window.clearInterval(O);O=window.setInterval(async()=>{let e=await b.getAll();!e.isInit||(e.manualSolving?chrome.runtime.onMessage.addListener(t=>{t.command==="execute"&&Ce(e)}):$e(e),window.clearInterval(O))},100);var xe=(0,ve.bexContent)(e=>{});var V=chrome.runtime.connect({name:"contentScript"}),we=!1;V.onDisconnect.addListener(()=>{we=!0});var Le=new L({listen(e){V.onMessage.addListener(e)},send(e){we||(V.postMessage(e),window.postMessage({...e,from:"bex-content-script"},"*"))}});function Ze(e){let t=document.createElement("script");t.src=e,t.onload=function(){this.remove()},(document.head||document.documentElement).appendChild(t)}document instanceof HTMLDocument&&Ze(chrome.runtime.getURL("dom.js"));fe(Le,"bex-dom");xe(Le);})();