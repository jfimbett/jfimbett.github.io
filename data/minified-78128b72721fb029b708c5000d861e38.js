/*
 lazysizes - v5.2.2 */
!function(X){var qa=function(x,t,G){var C,d;if(function(){var c,b={lazyClass:"lazyload",loadedClass:"lazyloaded",loadingClass:"lazyloading",preloadClass:"lazypreload",errorClass:"lazyerror",autosizesClass:"lazyautosizes",fastLoadedClass:"ls-is-cached",iframeLoadMode:0,srcAttr:"data-src",srcsetAttr:"data-srcset",sizesAttr:"data-sizes",minSize:40,customMedia:{},init:!0,expFactor:1.5,hFac:.8,loadMode:2,loadHidden:!0,ricTimeout:0,throttleDelay:125};d=x.lazySizesConfig||x.lazysizesConfig||{};for(c in b)c in
d||(d[c]=b[c])}(),!t||!t.getElementsByClassName)return{init:function(){},cfg:d,noSupport:!0};var H=t.documentElement,ra=x.HTMLPictureElement,E=x.addEventListener.bind(x),y=x.setTimeout,da=x.requestAnimationFrame||y,Y=x.requestIdleCallback,ea=/^picture$/i,sa=["load","error","lazyincluded","_lazyloaded"],R={},ta=Array.prototype.forEach,J=function(c,b){R[b]||(R[b]=new RegExp("(\\s|^)"+b+"(\\s|$)"));return R[b].test(c.getAttribute("class")||"")&&R[b]},K=function(c,b){J(c,b)||c.setAttribute("class",(c.getAttribute("class")||
"").trim()+" "+b)},Z=function(c,b){var e;(e=J(c,b))&&c.setAttribute("class",(c.getAttribute("class")||"").replace(e," "))},aa=function(c,b,e){var n=e?"addEventListener":"removeEventListener";e&&aa(c,b);sa.forEach(function(f){c[n](f,b)})},L=function(c,b,e,n,f){var g=t.createEvent("Event");e||(e={});e.instance=C;g.initEvent(b,!n,!f);g.detail=e;c.dispatchEvent(g);return g},ba=function(c,b){var e;!ra&&(e=x.picturefill||d.pf)?(b&&b.src&&!c.getAttribute("srcset")&&c.setAttribute("srcset",b.src),e({reevaluate:!0,
elements:[c]})):b&&b.src&&(c.src=b.src)},fa=function(c,b,e){for(e=e||c.offsetWidth;e<d.minSize&&b&&!c._lazysizesWidth;)e=b.offsetWidth,b=b.parentNode;return e},M=function(){var c,b,e=[],n=[],f=e,g=function(){var l=f;f=e.length?n:e;c=!0;for(b=!1;l.length;)l.shift()();c=!1},p=function(l,v){c&&!v?l.apply(this,arguments):(f.push(l),b||(b=!0,(t.hidden?y:da)(g)))};p._lsFlush=g;return p}(),S=function(c,b){return b?function(){M(c)}:function(){var e=this,n=arguments;M(function(){c.apply(e,n)})}},ua=function(c){var b,
e=0,n=d.throttleDelay,f=d.ricTimeout,g=function(){b=!1;e=G.now();c()},p=Y&&49<f?function(){Y(g,{timeout:f});f!==d.ricTimeout&&(f=d.ricTimeout)}:S(function(){y(g)},!0);return function(l){if(l=!0===l)f=33;if(!b){b=!0;var v=n-(G.now()-e);0>v&&(v=0);l||9>v?p():y(p,v)}}},ha=function(c){var b,e,n=function(){b=null;c()},f=function(){var g=G.now()-e;99>g?y(f,99-g):(Y||n)(n)};return function(){e=G.now();b||(b=y(f,99))}},pa=function(){var c,b,e,n,f,g,p,l,v,A,N,T,va=/^img$/i,wa=/^iframe$/i,xa="onscroll"in x&&
!/(gle|ing)bot/.test(navigator.userAgent),U=0,z=0,I=-1,ia=function(a){z--;if(!a||0>z||!a.target)z=0},ja=function(a){null==T&&(T="hidden"==(getComputedStyle(t.body,null)||{}).visibility);return T||!("hidden"==(getComputedStyle(a.parentNode,null)||{}).visibility&&"hidden"==(getComputedStyle(a,null)||{}).visibility)},la=function(){var a,h,k,u,q=C.elements;if((n=d.loadMode)&&8>z&&(a=q.length)){var r=0;for(I++;r<a;r++)if(q[r]&&!q[r]._lazyRace)if(!xa||C.prematureUnveil&&C.prematureUnveil(q[r]))O(q[r]);
else{(u=q[r].getAttribute("data-expand"))&&(k=1*u)||(k=U);if(!D){var D=!d.expand||1>d.expand?500<H.clientHeight&&500<H.clientWidth?500:370:d.expand;C._defEx=D;var m=D*d.expFactor;var P=d.hFac;T=null;U<m&&1>z&&2<I&&2<n&&!t.hidden?(U=m,I=0):U=1<n&&1<I&&6>z?D:0}if(ya!==k){g=innerWidth+k*P;p=innerHeight+k;var Q=-1*k;var ya=k}m=q[r].getBoundingClientRect();if((m=(N=m.bottom)>=Q&&(l=m.top)<=p&&(A=m.right)>=Q*P&&(v=m.left)<=g&&(N||A||v||l)&&(d.loadHidden||ja(q[r])))&&!(m=b&&3>z&&!u&&(3>n||4>I))){var F=q[r];
var B=k;m=F;F=ja(F);l-=B;N+=B;v-=B;for(A+=B;F&&(m=m.offsetParent)&&m!=t.body&&m!=H;)(F=0<((getComputedStyle(m,null)||{}).opacity||1))&&"visible"!=(getComputedStyle(m,null)||{}).overflow&&(B=m.getBoundingClientRect(),F=A>B.left&&v<B.right&&N>B.top-1&&l<B.bottom+1);m=F}if(m){O(q[r]);var ka=!0;if(9<z)break}else!ka&&b&&!h&&4>z&&4>I&&2<n&&(c[0]||d.preloadAfterLoad)&&(c[0]||!u&&(N||A||v||l||"auto"!=q[r].getAttribute(d.sizesAttr)))&&(h=c[0]||q[r])}h&&!ka&&O(h)}},w=ua(la),na=function(a){var h=a.target;h._lazyCache?
delete h._lazyCache:(ia(a),K(h,d.loadedClass),Z(h,d.loadingClass),aa(h,ma),L(h,"lazyloaded"))},za=S(na),ma=function(a){za({target:a.target})},Aa=function(a,h){var k=a.getAttribute("data-load-mode")||d.iframeLoadMode;0==k?a.contentWindow.location.replace(h):1==k&&(a.src=h)},Ba=function(a){var h,k=a.getAttribute(d.srcsetAttr);(h=d.customMedia[a.getAttribute("data-media")||a.getAttribute("media")])&&a.setAttribute("media",h);k&&a.setAttribute("srcset",k)},Ca=S(function(a,h,k,u,q){var r,D;if(!(D=L(a,
"lazybeforeunveil",h)).defaultPrevented){u&&(k?K(a,d.autosizesClass):a.setAttribute("sizes",u));u=a.getAttribute(d.srcsetAttr);k=a.getAttribute(d.srcAttr);if(q)var m=(r=a.parentNode)&&ea.test(r.nodeName||"");var P=h.firesLoad||"src"in a&&(u||k||m);D={target:a};K(a,d.loadingClass);P&&(clearTimeout(e),e=y(ia,2500),aa(a,ma,!0));m&&ta.call(r.getElementsByTagName("source"),Ba);u?a.setAttribute("srcset",u):k&&!m&&(wa.test(a.nodeName)?Aa(a,k):a.src=k);q&&(u||m)&&ba(a,{src:k})}a._lazyRace&&delete a._lazyRace;
Z(a,d.lazyClass);M(function(){var Q=a.complete&&1<a.naturalWidth;if(!P||Q)Q&&K(a,d.fastLoadedClass),na(D),a._lazyCache=!0,y(function(){"_lazyCache"in a&&delete a._lazyCache},9);"lazy"==a.loading&&z--},!0)}),O=function(a){if(!a._lazyRace){var h=va.test(a.nodeName),k=h&&(a.getAttribute(d.sizesAttr)||a.getAttribute("sizes")),u="auto"==k;if(!u&&b||!h||!a.getAttribute("src")&&!a.srcset||a.complete||J(a,d.errorClass)||!J(a,d.lazyClass)){var q=L(a,"lazyunveilread").detail;u&&ca.updateElem(a,!0,a.offsetWidth);
a._lazyRace=!0;z++;Ca(a,q,u,k,h)}}},Da=ha(function(){d.loadMode=3;w()}),oa=function(){3==d.loadMode&&(d.loadMode=2);Da()},V=function(){b||(999>G.now()-f?y(V,999):(b=!0,d.loadMode=3,w(),E("scroll",oa,!0)))};return{_:function(){f=G.now();C.elements=t.getElementsByClassName(d.lazyClass);c=t.getElementsByClassName(d.lazyClass+" "+d.preloadClass);E("scroll",w,!0);E("resize",w,!0);E("pageshow",function(a){if(a.persisted){var h=t.querySelectorAll("."+d.loadingClass);h.length&&h.forEach&&da(function(){h.forEach(function(k){k.complete&&
O(k)})})}});x.MutationObserver?(new MutationObserver(w)).observe(H,{childList:!0,subtree:!0,attributes:!0}):(H.addEventListener("DOMNodeInserted",w,!0),H.addEventListener("DOMAttrModified",w,!0),setInterval(w,999));E("hashchange",w,!0);"focus mouseover click load transitionend animationend".split(" ").forEach(function(a){t.addEventListener(a,w,!0)});/d$|^c/.test(t.readyState)?V():(E("load",V),t.addEventListener("DOMContentLoaded",w),y(V,2E4));C.elements.length?(la(),M._lsFlush()):w()},checkElems:w,
unveil:O,_aLSL:oa}}(),ca=function(){var c,b=S(function(f,g,p,l){var v;f._lazysizesWidth=l;l+="px";f.setAttribute("sizes",l);if(ea.test(g.nodeName||"")){g=g.getElementsByTagName("source");var A=0;for(v=g.length;A<v;A++)g[A].setAttribute("sizes",l)}p.detail.dataAttr||ba(f,p.detail)}),e=function(f,g,p){var l=f.parentNode;l&&(p=fa(f,l,p),g=L(f,"lazybeforesizes",{width:p,dataAttr:!!g}),g.defaultPrevented||(p=g.detail.width)&&p!==f._lazysizesWidth&&b(f,l,g,p))},n=ha(function(){var f,g=c.length;if(g)for(f=
0;f<g;f++)e(c[f])});return{_:function(){c=t.getElementsByClassName(d.autosizesClass);E("resize",n)},checkElems:n,updateElem:e}}(),W=function(){!W.i&&t.getElementsByClassName&&(W.i=!0,ca._(),pa._())};return y(function(){d.init&&W()}),C={cfg:d,autoSizer:ca,loader:pa,init:W,uP:ba,aC:K,rC:Z,hC:J,fire:L,gW:fa,rAF:M}}(X,X.document,Date);X.lazySizes=qa;"object"==typeof module&&module.exports&&(module.exports=qa)}("undefined"!=typeof window?window:{});