if("undefined"===typeof BLK||!BLK)var BLK={};var globalMapAppObjects={centered:null},productExposureAreas=["global","regional"],emergingMarketCountries="CN KR TW BR ZA IN MX RU MY ID TH TR PL CL PH CO HK PE GR AE QA CZ HU EG".split(" ");BLK.tools=BLK.tools||{};
BLK.tools.dynamicMapSelection=function(){$("#dynamicMapControls input.dynamic-map-buttons").change(function(){$("#dynamicMapResults").html("").addClass("display-none");var b=$(this).val();BLK.tools.dynamicMap("dynamicMap",b);BLK.tools.productPreview()});$("#dynamicMapControls input.dynamic-map-buttons").first().change()};
BLK.tools.getEmAreaData=function(b){var g={};b="undefined"===typeof b?"#1794d2":b;for(var k=0;k<emergingMarketCountries.length;k++){var l=emergingMarketCountries[k];g[l]={code:l,color:b}}return g};BLK.tools.dynamicMap=function(b,g){BLK.tools.renderDynamicMap(g,geoCountriesJsonUrl,dynamic_map_data[g],b+" .dynamic-map-app")};
BLK.tools.renderDynamicMap=function(b,g,k,l){$("#dynamicMapContainer .dynamic-map-exposures").remove();var x=!1;-1<$.inArray(b,productExposureAreas)&&(x=!0,k=BLK.tools.getEmAreaData(k.EM.color));exposeMapResults=function(f,a){var d="";a="undefined"===a.tickers?[]:a.tickers.split(",");var h,p=[];if(a&&!(1>a.length)){for(h=0;h<a.length;h++){var e=a[h],c=relatedFunds[e.toLowerCase()];p.push(c);d+='\x3ca href\x3d"#NEWHREF" class\x3d"product-page-link" target\x3d"_blank"\x3e\x3cdiv class\x3d"dynamic-map-result" product\x3d"@0@"\x3e@1@\x3c/div\x3e\x3cinput type\x3d"hidden" value\x3d"@2@"\x3e\x3c/a\x3e'.replace("@0@",
e).replace("@1@",c.shortName).replace("#NEWHREF",c.productPageLink).replace("@2@",c.portId)}$("#"+f.replace("Container","")+"Results").html(d).removeClass("display-none");BLK.tools.productPreview()}};clickAreaMap=function(f,a){var d=this.parentNode.id,h=this.parentNode.parentNode.parentNode.parentNode.parentNode.id;a=dynamic_map_data.country[globalMapAppObjects.countriesArray[a].code];var p=globalMapAppObjects.path,e=d3.select("#"+d),c=$("#"+d+"DynamicMap");d=c.width();c=c.height();var m=globalMapAppObjects.centered;
if("undefined"!==typeof a&&!x){clickAreaMap;resetMapColor(e);if(f&&m!==f){var n=p.centroid(f);p=n[0];n=n[1];var r=2.5;m=f;d3.select(this).attr("code")}else p=d/2,n=c/2,r=1,m=null;globalMapAppObjects.centered=m;e.selectAll(".area.active").classed("active",!1);d3.select(this).classed("active",m&&function(q){return q===m});e.transition().duration(750).attr("transform","translate("+d/2+","+c/2+")scale("+r+")translate("+-p+","+-n+")").style("stroke-width",1.5/r+"px");null===m?$("#"+h.replace("Container",
"")+"Results").html("").addClass("display-none"):exposeMapResults(h,a)}};resetMapColor=function(f){f.selectAll(".area").attr("style",function(a,d){a=globalMapAppObjects.topAreaArray;d=globalMapAppObjects.countriesArray[d].code;if("undefined"!==typeof a[d])return"fill: "+a[d].color})};var F="#"+b;b.charAt(0).toUpperCase();b.slice(1);"#"!==l.charAt(0)&&(l="#"+l);var t=$(l);if(t.length){t.empty();var u=t.width(),y=.75*u;if("states"==b){var A=d3.geo.albersUsa().scale(500).translate([u/2,y/2]);var w=exposureMapStateAreaData}else A=
d3.geo.mercator().scale((u+1)/2/Math.PI).translate([u/2,y/2]).center([0,30]),w=k,globalMapAppObjects.topAreaArray=w;var B=d3.geo.path().projection(A);globalMapAppObjects.path=B;var C=d3.select(l).append("svg").attr("width",u).attr("height",y).attr("id",b+"DynamicMap"),D=d3.select(l).append("div").attr("class","tooltip "+b),G=C.append("g").attr("id",b);d3.json(g,function(f,a){if("states"==b){var d=a.objects.states.geometries;f=topojson.feature(a,a.objects.states).features;var h=a.objects.states.geometries;
globalMapAppObjects.statesArray=h}else{d=a.objects.countries.geometries;f=topojson.feature(a,a.objects.countries).features;var p=a.objects.countries.geometries;globalMapAppObjects.countriesArray=p}G.selectAll(F).data(f).enter().append("path").attr("class","area").attr("code",function(e,c){return d[c].code}).attr("style",function(e,c){e=d[c].code;return"undefined"!==typeof w[e]?"fill: "+w[e].color:"fill: rgb(226,227,226)"}).attr("d",B).on("click",clickAreaMap).on("mouseover",function(e,c){d3.select(this).classed("active")||
d3.select(this).classed("hover",e)}).on("mousemove",function(e,c){e=d3.mouse(C.node()).map(function(v){return parseInt(v)});var m="states"==b?h:p;var n=k[m[c].code];if("undefined"!==typeof n){var r=m[c].name;c=0;var q="undefined"===typeof n.tickers?[]:n.tickers.split(",");0<q.length&&(c=20*Math.floor(q.length/2));percentage=n.percent;D.classed("hidden",!1).attr("style","left:"+(e[0]-65)+"px;top:"+(e[1]-60-c)+"px").html(function(){var v=r+'\x3cbr\x3e\x3cdiv style\x3d"text-align: center; font-weight: bold;"\x3e';
if(q&&0<q.length)for(var z=0;z<q.length;z++){var E=q[z];E.toLowerCase();v+='\x3cdiv style\x3d"float:left;width:50%;text-align:center;"\x3e{0}\x3c/div\x3e'.replace("{0}",E)}"undefined"!==typeof percentage&&(v+="\x3cdiv\x3e{0}\x3c/div\x3e".replace("{0}",percentage));return v+"\x3c/div\x3e"})}}).on("mouseout",function(e,c){D.classed("hidden",!0);d3.select(this).classed("hover",!1)})});renderExposureTable=function(f){var a='\x3cdiv class\x3d"dynamic-map-exposures"\x3e\x3ctable class\x3d"dynamic-map-exposure-table"\x3e\x3ctbody\x3e',
d;for(d in f){var h=f[d];a+='\x3ctr\x3e\x3ctd\x3e{1}\x3c/td\x3e\x3ctd class\x3d"exposure-percent"\x3e{2}\x3c/td\x3e\x3c/tr\x3e'.replace("{1}",h.name).replace("{2}",h.percent)}a+="\x3c/tbody\x3e\x3c/table\x3e\x3c/div\x3e";$("#dynamicMapContainer .geographic-exposure").after(a)};x&&(exposeMapResults("dynamicMap",dynamic_map_data[b].EM),$("#dynamicMapResults a.product-page-link").click(function(f){$(this).siblings().removeClass("selected-product");$(this).addClass("selected-product");var a=$(this).find("div").attr("product").toLowerCase();
$("#dynamicMap").css("height",$("#dynamicMap").height()+"px");t.fadeOut("500");setTimeout(function(){t.empty().show();BLK.tools.renderDynamicMap("countryExposure",g,countryExposureData[a],l);renderExposureTable(countryExposureData[a])},500);f.preventDefault()}))}};
BLK.tools.productPreview=function(){$("#dynamicMapResults a.product-page-link").qtip({content:{text:function(b,g){b=this.find("div").attr("product");g=relatedFunds[b.toLowerCase()];b.toLowerCase();return'\x3ch4 class\x3d"dynamic-map product-preview-link"\x3e\x3ca href\x3d"{0}"\x3e{1}\x3c/a\x3e\x3cspan\x3e ({2})\x3c/span\x3e\x3c/h4\x3e\x3ca href\x3d"#" class\x3d"hide-product-preview"\x3e\x3cdiv style\x3d"position: absolute; top: 5px; right: 5px; height: 20px; width: 20px;"\x3e\x3c/div\x3e\x3c/a\x3e\x3cdiv style\x3d"min-width:400px; min-height: 75px;"\x3e{3}\x3c/div\x3e'.replace("{0}",g.productPageLink).replace("{1}",
g.name).replace("{2}",g.ticker).replace("{3}",g.rollover)}},position:{my:"center right",at:"center left",viewport:$("body")},show:{solo:!0,event:"mouseover",delay:500},hide:{event:"inactive unfocus click"},style:{classes:"qtip-bootstrap tooltip-width mytip-qtip"},events:{render:function(b,g){setTimeout(function(){$(".hide-product-preview").click(function(k){g.hide();k.preventDefault()})},500)}}})};
$(document).ready(function(){"undefined"!==typeof dynamic_map_data&&("undefined"===typeof d3?setTimeout(function(){BLK.tools.dynamicMapSelection()},1E3):BLK.tools.dynamicMapSelection())});