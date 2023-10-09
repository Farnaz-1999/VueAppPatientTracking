import{W as w}from"./index-fddc52bf.js";const C=async e=>new Promise((t,o)=>{const n=new FileReader;n.onload=()=>{const s=n.result,a=s.substr(s.indexOf(",")+1);t(a)},n.onerror=s=>o(s),n.readAsDataURL(e)}),f=e=>encodeURIComponent(e).replace(/%(2[346B]|5E|60|7C)/g,decodeURIComponent).replace(/[()]/g,escape),k=e=>e.replace(/(%[\dA-F]{2})+/gi,decodeURIComponent),j=(e,t,o={})=>{const n=f(e),s=f(t),a=`; expires=${(o.expires||"").replace("expires=","")}`,c=(o.path||"/").replace("path=","");document.cookie=`${n}=${s||""}${a}; path=${c}`},y=()=>{const e=[],t={};if(!document.cookie)return e;const o=document.cookie.split(";")||[];for(const s of o){let[a,c]=s.replace(/=/,"CAP_COOKIE").split("CAP_COOKIE");a=k(a).trim(),c=k(c).trim(),t[a]=c}const n=Object.entries(t);for(const[s,a]of n)e.push({key:s,value:a});return e},x=e=>{const t=y();for(const o of t)if(o.key===e)return o;return{key:e,value:""}},$=e=>{document.cookie=`${e}=; Max-Age=0`},m=()=>{const e=document.cookie.split(";")||[];for(const t of e)document.cookie=t.replace(/^ +/,"").replace(/=.*/,`=;expires=${new Date().toUTCString()};path=/`)},v=(e={})=>{const t=Object.keys(e);return Object.keys(e).map(s=>s.toLocaleLowerCase()).reduce((s,a,c)=>(s[a]=e[t[c]],s),{})},E=(e,t=!0)=>e?Object.entries(e).reduce((n,s)=>{const[a,c]=s;let r,i;return Array.isArray(c)?(i="",c.forEach(d=>{r=t?encodeURIComponent(d):d,i+=`${a}=${r}&`}),i.slice(0,-1)):(r=t?encodeURIComponent(c):c,i=`${a}=${r}`),`${n}&${i}`},"").substr(1):null,g=(e,t={})=>{const o=Object.assign({method:e.method||"GET",headers:e.headers},t),s=v(e.headers)["content-type"]||"";if(typeof e.data=="string")o.body=e.data;else if(s.includes("application/x-www-form-urlencoded")){const a=new URLSearchParams;for(const[c,r]of Object.entries(e.data||{}))a.set(c,r);o.body=a.toString()}else if(s.includes("multipart/form-data")){const a=new FormData;if(e.data instanceof FormData)e.data.forEach((r,i)=>{a.append(i,r)});else for(let r of Object.keys(e.data))a.append(r,e.data[r]);o.body=a;const c=new Headers(o.headers);c.delete("content-type"),o.headers=c}else(s.includes("application/json")||typeof e.data=="object")&&(o.body=JSON.stringify(e.data));return o},l=async e=>{const t=g(e,e.webFetchExtra),o=E(e.params,e.shouldEncodeUrlParams),n=o?`${e.url}?${o}`:e.url,s=await fetch(n,t),a=s.headers.get("content-type")||"";let{responseType:c="text"}=s.ok?e:{};a.includes("application/json")&&(c="json");let r;switch(c){case"arraybuffer":case"blob":const d=await s.blob();r=await C(d);break;case"json":r=await s.json();break;case"document":case"text":default:r=await s.text()}const i={};return s.headers.forEach((d,h)=>{i[h]=d}),{data:r,headers:i,status:s.status,url:s.url}},A=async e=>l(Object.assign(Object.assign({},e),{method:"GET"})),P=async e=>l(Object.assign(Object.assign({},e),{method:"POST"})),T=async e=>l(Object.assign(Object.assign({},e),{method:"PUT"})),U=async e=>l(Object.assign(Object.assign({},e),{method:"PATCH"})),I=async e=>l(Object.assign(Object.assign({},e),{method:"DELETE"}));class D extends w{constructor(){super(),this.request=async t=>l(t),this.get=async t=>A(t),this.post=async t=>P(t),this.put=async t=>T(t),this.patch=async t=>U(t),this.del=async t=>I(t),this.getCookiesMap=async t=>{const o=y(),n={};for(const s of o)n[s.key]=s.value;return n},this.getCookies=async t=>({cookies:y()}),this.setCookie=async t=>{const{key:o,value:n,expires:s="",path:a=""}=t;j(o,n,{expires:s,path:a})},this.getCookie=async t=>x(t.key),this.deleteCookie=async t=>$(t.key),this.clearCookies=async t=>m(),this.clearAllCookies=async()=>m(),this.uploadFile=async t=>{const o=new FormData;o.append(t.name,t.blob||"undefined");const n=Object.assign(Object.assign({},t),{body:o,method:"POST"});return this.post(n)},this.downloadFile=async t=>{const o=g(t,t.webFetchExtra),n=await fetch(t.url,o);let s;if(!(t!=null&&t.progress))s=await n.blob();else if(!(n!=null&&n.body))s=new Blob;else{const a=n.body.getReader();let c=0,r=[];const i=n.headers.get("content-type"),d=parseInt(n.headers.get("content-length")||"0",10);for(;;){const{done:u,value:p}=await a.read();if(u)break;r.push(p),c+=(p==null?void 0:p.length)||0;const O={type:"DOWNLOAD",url:t.url,bytes:c,contentLength:d};this.notifyListeners("progress",O)}let h=new Uint8Array(c),b=0;for(const u of r)typeof u>"u"||(h.set(u,b),b+=u.length);s=new Blob([h.buffer],{type:i||void 0})}return{blob:s}}}}export{D as HttpWeb};