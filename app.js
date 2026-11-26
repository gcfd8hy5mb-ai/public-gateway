'use strict';
const query=document.getElementById('query'), cards=[...document.querySelectorAll('#results article')], status=document.getElementById('status');
function filter(q='',category='',region=''){const words=q.toLowerCase().trim().split(/\s+/).filter(Boolean);let count=0;for(const card of cards){const hay=card.textContent.toLowerCase();const match=words.every(w=>hay.includes(w))&&(!category||card.dataset.categoryName===category)&&(!region||card.dataset.regionName===region);card.hidden=!match;if(match)count++;}status.textContent=count?count+' resource'+(count===1?'':'s')+' found in the initial directory.':'No matching resources in the initial directory. Coverage is still expanding.';document.getElementById('records').scrollIntoView({block:'start'});}
document.getElementById('search').addEventListener('submit',e=>{e.preventDefault();filter(query.value);});
document.querySelectorAll('[data-category]').forEach(el=>el.addEventListener('click',()=>{query.value='';filter('',el.dataset.category);}));
document.querySelectorAll('[data-region]').forEach(el=>el.addEventListener('click',e=>{e.preventDefault();query.value='';filter('','',el.dataset.region);}));
document.getElementById('reset').addEventListener('click',()=>{query.value='';filter();});
