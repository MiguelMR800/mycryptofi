// MyCryptoFI news renderer
(async function(){
  const list = document.getElementById('news-list');
  const empty = document.getElementById('news-empty');
  const err = document.getElementById('news-error');

  function sourceLabel(item){
    return item.source_id || item.source || new URL(item.url).hostname.replace('www.','');
  }

  try{
    const res = await fetch('./news.json', {cache:'no-cache'});
    if(!res.ok) throw new Error('HTTP '+res.status);
    const data = await res.json();
    if(!Array.isArray(data) || data.length === 0){
      empty.hidden = false;
      return;
    }
    // Map to minimal fields, prefer title_en if fi missing
    const items = data.slice(0, 15).map(x => ({
      title: x.title_fi && x.title_fi.trim() ? x.title_fi : (x.title_en || x.title || 'Untitled'),
      url: x.url || '#',
      source: sourceLabel(x)
    }));

    const frag = document.createDocumentFragment();
    for(const it of items){
      const li = document.createElement('li');
      const left = document.createElement('div');
      const a = document.createElement('a'); a.href = it.url; a.target = '_blank'; a.rel = 'noopener'; a.textContent = it.title;
      const src = document.createElement('small'); src.textContent = it.source;
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