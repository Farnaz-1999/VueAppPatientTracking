import{w as i}from"./index5-b9636d10.js";/*!
 * (C) Ionic http://ionicframework.com - MIT License
 */var o;(function(e){e.Body="body",e.Ionic="ionic",e.Native="native",e.None="none"})(o||(o={}));const d={getEngine(){var e;return((e=i===null||i===void 0?void 0:i.Capacitor)===null||e===void 0?void 0:e.isPluginAvailable("Keyboard"))&&(i===null||i===void 0?void 0:i.Capacitor.Plugins.Keyboard)},getResizeMode(){const e=this.getEngine();return e!=null&&e.getResizeMode?e.getResizeMode().catch(n=>{if(n.code!=="UNIMPLEMENTED")throw n}):Promise.resolve(void 0)}};export{d as K,o as a};
