(function(){
var CFG={
  social:'',
  popunder:'',
  interstitial:'',
  native:{src:'',id:''},
  bannerTop:{key:'',src:'',w:320,h:50},
  bannerMid:{key:'',src:'',w:300,h:250},
  bannerBottom:{key:'',src:'',w:300,h:250},
  directLink:{url:'',text:''}
};

function addScript(src){
  if(!src) return;
  var s=document.createElement('script');
  s.src=src; s.async=true;
  s.setAttribute('data-cfasync','false');
  document.body.appendChild(s);
}
function place(el,where){
  if(where==='top'){
    var h=document.querySelector('header');
    if(h){h.parentNode.insertBefore(el,h.nextSibling);return;}
  }
  if(where==='mid'){
    var hs=document.querySelectorAll('.content h2, section h2');
    var t=hs[2]||hs[1];
    if(t){t.parentNode.insertBefore(el,t);return;}
  }
  var f=document.querySelector('footer');
  if(f){f.parentNode.insertBefore(el,f);}else{document.body.appendChild(el);}
}
function box(){
  var d=document.createElement('div');
  d.style.cssText='text-align:center;margin:22px auto;overflow:hidden';
  var l=document.createElement('div');
  l.textContent='विज्ञापन';
  l.style.cssText='font-size:11px;color:#a9bbb2;margin-bottom:4px';
  d.appendChild(l);
  return d;
}
function banner(c,where){
  if(!c.key||!c.src) return;
  var d=box();
  var f=document.createElement('iframe');
  f.width=c.w; f.height=c.h; f.style.border='0';
  f.setAttribute('scrolling','no');
  f.srcdoc='<html><body style="margin:0"><script>atOptions={"key":"'+c.key+'","format":"iframe","height":'+c.h+',"width":'+c.w+',"params":{}};<\/script><script src="'+c.src+'"><\/script></body></html>';
  d.appendChild(f);
  place(d,where);
}
function nativeAd(c){
  if(!c.src||!c.id) return;
  var d=box();
  var k=document.createElement('div');
  k.id=c.id;
  d.appendChild(k);
  place(d,'bottom');
  addScript(c.src);
}
function direct(c){
  if(!c.url) return;
  var d=box();
  var a=document.createElement('a');
  a.href=c.url; a.target='_blank';
  a.rel='sponsored nofollow noopener';
  a.textContent=c.text||'प्रायोजित लिंक';
  a.style.cssText='color:#b7f36b;text-decoration:underline';
  d.appendChild(a);
  place(d,'bottom');
}

banner(CFG.bannerTop,'top');
banner(CFG.bannerMid,'mid');
banner(CFG.bannerBottom,'bottom');
nativeAd(CFG.native);
direct(CFG.directLink);
addScript(CFG.social);
addScript(CFG.interstitial);
addScript(CFG.popunder);
})();
