// MyCryptoFI news renderer (v2)
(async function(){
  const list = document.getElementById('news-list');
  const empty = document.getElementById('news-empty');
  const err = document.getElementById('news-error');

  function label(item){
    try{
      if(item.source_id) return item.source_id;
      if(item.source) return item.source;
      if(item.url) return new URL(item.url).hostname.replace('www.','');
    }catch(e){}
    return 'source';
  }

  try{
    const res = await fetch('./news.json', {cache:'no-cache'});
    if(!res.ok) throw new Error('HTTP '+res.status);
    const raw = await res.json();
    if(!Array.isArray(raw) || raw.length === 0){ empty.hidden = false; return; }

    // Prefer newest first if timestamp exists
    const data = [...raw].slice(0, 20);

    const frag = document.createDocumentFragment();
    for(const x of data){
      const title = x.title_en || x.title || 'Untitled';
      const url = x.url || '#';
      const source = label(x);
      const li = document.createElement('li');
      const left = document.createElement('div');
      const a = document.createElement('a'); a.href = url; a.target = '_blank'; a.rel = 'noopener'; a.textContent = title;
      const src = document.createElement('small'); src.textContent = source;
      left.appendChild(a); left.appendChild(document.createElement('br')); left.appendChild(src);
      li.appendChild(left);
      frag.appendChild(li);
    }
    list.appendChild(frag);
  }catch(e){
    console.error('News load failed:', e);
    err.hidden = false;
  }
})();