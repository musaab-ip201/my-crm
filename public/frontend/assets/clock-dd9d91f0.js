import{X as g,b as m,c as f,e as s,ag as u}from"./index-02024f03.js";const C={class:"lucide lucide-calendar",xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":"1.5","stroke-linecap":"round","stroke-linejoin":"round"};function v(e,t){return m(),f("svg",C,[...t[0]||(t[0]=[s("path",{d:"M8 2v4"},null,-1),s("path",{d:"M16 2v4"},null,-1),s("rect",{width:"18",height:"18",x:"3",y:"4",rx:"2"},null,-1),s("path",{d:"M3 10h18"},null,-1)])])}const j=g({name:"lucide-calendar",render:v});/**
 * @license lucide-vue-next v0.564.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const x=e=>{for(const t in e)if(t.startsWith("aria-")||t==="role"||t==="title")return!0;return!1};/**
 * @license lucide-vue-next v0.564.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const h=e=>e==="";/**
 * @license lucide-vue-next v0.564.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const y=(...e)=>e.filter((t,o,r)=>!!t&&t.trim()!==""&&r.indexOf(t)===o).join(" ").trim();/**
 * @license lucide-vue-next v0.564.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const w=e=>e.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase();/**
 * @license lucide-vue-next v0.564.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const _=e=>e.replace(/^([A-Z])|[\s-_]+(\w)/g,(t,o,r)=>r?r.toUpperCase():o.toLowerCase());/**
 * @license lucide-vue-next v0.564.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const B=e=>{const t=_(e);return t.charAt(0).toUpperCase()+t.slice(1)};/**
 * @license lucide-vue-next v0.564.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */var n={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":2,"stroke-linecap":"round","stroke-linejoin":"round"};/**
 * @license lucide-vue-next v0.564.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const A=({name:e,iconNode:t,absoluteStrokeWidth:o,"absolute-stroke-width":r,strokeWidth:c,"stroke-width":d,size:a=n.width,color:k=n.stroke,...l},{slots:i})=>u("svg",{...n,...l,width:a,height:a,stroke:k,"stroke-width":h(o)||h(r)||o===!0||r===!0?Number(c||d||n["stroke-width"])*24/Number(a):c||d||n["stroke-width"],class:y("lucide",l.class,...e?[`lucide-${w(B(e))}-icon`,`lucide-${w(e)}`]:["lucide-icon"]),...!i.default&&!x(l)&&{"aria-hidden":"true"}},[...t.map(p=>u(...p)),...i.default?[i.default()]:[]]);/**
 * @license lucide-vue-next v0.564.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const M=(e,t)=>(o,{slots:r,attrs:c})=>u(A,{...c,...o,iconNode:t,name:e},r);/**
 * @license lucide-vue-next v0.564.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const L=M("clock",[["path",{d:"M12 6v6l4 2",key:"mmk7yg"}],["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}]]);export{L as C,j as _,M as c};
//# sourceMappingURL=clock-dd9d91f0.js.map
