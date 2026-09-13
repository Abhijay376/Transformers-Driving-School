/* ===================== NAV: active link + mobile toggle ===================== */
document.addEventListener('DOMContentLoaded', function(){
  var page = document.body.getAttribute('data-page') || 'home';
  document.querySelectorAll('.nav-links a').forEach(function(a){
    if(a.dataset.page === page) a.classList.add('active');
  });

  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');
  if(toggle && links){
    toggle.addEventListener('click', function(){
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    links.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){ links.classList.remove('open'); });
    });
  }

  renderHomeFaq();
  renderFullQuizQuestion();
});

/* ===================== NAV: Areas We Serve dropdown ===================== */
function toggleAreaDropdown(btn){
  var dd = btn.closest('.nav-dropdown');
  if(!dd) return;
  var open = dd.classList.toggle('open');
  btn.setAttribute('aria-expanded', String(open));
}
document.addEventListener('click', function(e){
  document.querySelectorAll('.nav-dropdown.open').forEach(function(dd){
    if(!dd.contains(e.target)) dd.classList.remove('open');
  });
});

/* ===================== TEST CENTRE SEARCH (home) ===================== */
var TEST_CENTERS = [
  {name:'Drive Test Pakenham', sub:'VicRoads Pakenham Customer Service Centre', href:'drive-test-pakenham.html'},
  {name:'Officer', sub:'Service area (nearest test centre: Pakenham)', href:'area-officer.html'},
  {name:'Beaconsfield', sub:'Service area (nearest test centre: Pakenham)', href:'area-beaconsfield.html'},
  {name:'Berwick', sub:'Service area (nearest test centre: Pakenham)', href:'area-berwick.html'},
  {name:'Nar Nar Goon', sub:'Service area (nearest test centre: Pakenham)', href:'area-nar-nar-goon.html'},
  {name:'Clyde', sub:'Service area (nearest test centre: Pakenham)', href:'area-clyde.html'},
  {name:'Cranbourne', sub:'Service area (nearest test centre: Pakenham)', href:'area-cranbourne.html'},
  {name:'Cardinia', sub:'Service area (nearest test centre: Pakenham)', href:'area-cardinia.html'},
  {name:'Devon Meadows', sub:'Service area (nearest test centre: Pakenham)', href:'area-devon-meadows.html'}
];

function filterCenters(value){
  var box = document.getElementById('searchResults');
  if(!box) return;
  var q = (value || '').trim().toLowerCase();
  if(!q){ box.hidden = true; box.innerHTML=''; return; }
  var matches = TEST_CENTERS.filter(function(c){ return c.name.toLowerCase().includes(q); });
  if(!matches.length){
    box.innerHTML = '<div class="search-empty">No match found for "' + escapeHtml(value) + '". Try Pakenham, Officer, Berwick, Cranbourne, Clyde or another local suburb.</div>';
    box.hidden = false;
    return;
  }
  box.innerHTML = matches.map(function(c){
    return '<a href="' + c.href + '"><span>' + c.name + '</span><span class="muted">' + c.sub + '</span></a>';
  }).join('');
  box.hidden = false;
}

function goToFirstCenterMatch(value){
  var q = (value || '').trim().toLowerCase();
  if(!q) return;
  var match = TEST_CENTERS.find(function(c){ return c.name.toLowerCase().includes(q); });
  if(match){ window.location.href = match.href; }
}

function escapeHtml(s){
  var d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

document.addEventListener('click', function(e){
  var wrap = document.querySelector('.search-wrap');
  var box = document.getElementById('searchResults');
  if(wrap && box && !wrap.contains(e.target)) box.hidden = true;
});

/* ===================== MINI QUIZ (Home) ===================== */
var miniQuizQuestions = [
  {q:'How confident are you with parallel or reverse parking?', area:'Parking manoeuvres'},
  {q:'How confident are you negotiating multi-lane roundabouts?', area:'Roundabouts'},
  {q:'How consistently do you check mirrors and blind spots?', area:'Observation checks'}
];
var miniStep = 0, miniScore = 0, miniWeak = [];

function miniAnswerQuiz(value){
  if(value >= 1) miniWeak.push(miniQuizQuestions[miniStep].area);
  miniScore += value;
  miniStep++;
  if(miniStep < miniQuizQuestions.length){
    document.getElementById('miniQuizProgress').textContent = 'Question ' + (miniStep+1) + ' of ' + miniQuizQuestions.length;
    document.getElementById('miniQuizFill').style.width = Math.round(((miniStep)/miniQuizQuestions.length)*100) + '%';
    document.getElementById('miniQuizQ').textContent = miniQuizQuestions[miniStep].q;
  } else {
    document.getElementById('miniQuizArea').style.display = 'none';
    var box = document.getElementById('miniQuizResult');
    var msg = miniScore <= 1
      ? 'Great sign! You look test-ready in these areas. A quick refresher lesson before test day is still a smart move.'
      : 'You may want a bit more focused practice on: ' + (miniWeak.length? miniWeak.join(', ') : 'a few key areas') + '.';
    box.className = 'tool-result show result-warn';
    box.innerHTML = '<strong>Quick result:</strong> ' + msg +
      '<div style="margin-top:10px"><a class="btn btn-wa" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I%20just%20did%20the%20mini%20readiness%20quiz%20and%20want%20to%20book%20a%20lesson.">Book a Lesson on WhatsApp</a></div>' +
      '<a href="readiness-quiz.html" class="tool-link">Take the full 8-question quiz for a detailed report →</a>';
  }
}

/* ===================== FULL QUIZ (readiness-quiz.html) ===================== */
var fullQuizQuestions = [
  {q:'How confident are you with parallel parking?', opts:['Very confident, consistent every time','Somewhat, I sometimes need extra attempts','Not confident, I avoid it if I can'], area:'Parallel parking'},
  {q:'How comfortable are you at multi-lane roundabouts?', opts:['Very confident','Somewhat confident','Not confident'], area:'Roundabouts'},
  {q:'How many supervised driving hours have you completed?', opts:['20+ hours','10–20 hours','Under 10 hours'], area:'Overall experience'},
  {q:'How confident are you merging onto highways or high-speed roads?', opts:['Very confident','Somewhat confident','Not confident'], area:'Highway merging'},
  {q:'How consistently do you check mirrors and blind spots?', opts:['Every time, automatically','Most of the time','I often forget'], area:'Observation checks'},
  {q:'How do you handle giving way at intersections?', opts:['Always correct','Sometimes hesitant or unsure','Often confused'], area:'Give-way rules'},
  {q:'How confident are you with a 3-point turn?', opts:['Very confident','Somewhat confident','Not confident'], area:'3-point turns'},
  {q:'Have you practised on or near your actual test route?', opts:['Yes, multiple times','Once or twice','Not yet'], area:'Test route familiarity'}
];
var fullStep = 0, fullScore = 0, fullWeak = [];

function renderFullQuizQuestion(){
  var progressEl = document.getElementById('fullQuizProgress');
  if(!progressEl) return;
  var qObj = fullQuizQuestions[fullStep];
  if(!qObj) return;
  progressEl.textContent = 'Question ' + (fullStep+1) + ' of ' + fullQuizQuestions.length;
  document.getElementById('fullQuizFill').style.width = Math.round(((fullStep)/fullQuizQuestions.length)*100) + '%';
  document.getElementById('fullQuizQ').textContent = qObj.q;
  var optsWrap = document.getElementById('fullQuizOptions');
  optsWrap.innerHTML = qObj.opts.map(function(opt, i){
    return '<button onclick="fullAnswerQuiz(' + i + ')">' + opt + '</button>';
  }).join('');
}

function fullAnswerQuiz(value){
  if(value >= 1) fullWeak.push(fullQuizQuestions[fullStep].area);
  fullScore += value;
  fullStep++;
  if(fullStep < fullQuizQuestions.length){
    renderFullQuizQuestion();
  } else {
    document.getElementById('fullQuizFill').style.width = '100%';
    document.getElementById('fullQuizArea').style.display = 'none';
    var box = document.getElementById('fullQuizResult');
    var lessonsRec, headline;
    if(fullScore <= 3){
      headline = 'You look test-ready!';
      lessonsRec = 'A 1–2 lesson refresher focused on test-day nerves and route familiarity should be enough.';
    } else if(fullScore <= 8){
      headline = 'Almost there, just a few gaps to close.';
      lessonsRec = 'We’d recommend our 5-Lesson Pass, focused on your weaker areas below, before booking your test.';
    } else {
      headline = 'More practice recommended before booking your test.';
      lessonsRec = 'We’d recommend the Ultimate Test Pass Pack, which combines multiple lessons with a mock test and test-day vehicle hire.';
    }
    var weakListHtml = fullWeak.length
      ? '<ul style="text-align:left;margin:12px 0;padding-left:18px">' + Array.from(new Set(fullWeak)).map(function(a){return '<li>' + a + '</li>';}).join('') + '</ul>'
      : '<p style="margin:12px 0">No major weak spots identified. Nice work!</p>';
    box.className = 'tool-result show result-warn';
    box.innerHTML = '<h3 style="color:var(--navy);margin-bottom:8px">' + headline + '</h3>' +
      '<p><strong>Areas to focus on:</strong></p>' + weakListHtml +
      '<p>' + lessonsRec + '</p>' +
      '<div style="margin-top:14px;display:flex;gap:10px;flex-wrap:wrap;justify-content:center">' +
      '<a class="btn btn-wa" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I%20just%20completed%20the%20Test%20Readiness%20Quiz%20and%20would%20like%20to%20book%20lessons.">Book on WhatsApp</a>' +
      '<a class="btn btn-outline-navy" href="index.html#packages">View Packages</a>' +
      '</div>';
  }
}

/* ===================== MINI LICENCE CHECKER (Home) ===================== */
function miniCheckLicence(){
  var country = document.getElementById('miniCountrySelect').value;
  var age = parseInt(document.getElementById('miniAgeInput').value, 10);
  var box = document.getElementById('miniLicenceResult');
  if(!country){
    box.className = 'tool-result show result-warn';
    box.innerHTML = 'Please select the country that issued your licence.';
    return;
  }
  var html = buildLicenceResult(country, age, null);
  box.className = 'tool-result show ' + html.cls;
  box.innerHTML = html.text + '<div style="margin-top:10px"><a href="licence-checker.html" class="tool-link">Open the full checker for a detailed breakdown →</a></div>';
}

/* ===================== FULL LICENCE CHECKER (licence-checker.html) ===================== */
function fullCheckLicence(){
  var country = document.getElementById('fullCountrySelect').value;
  var age = parseInt(document.getElementById('fullAgeInput').value, 10);
  var exp = parseInt(document.getElementById('fullExpInput').value, 10);
  var box = document.getElementById('fullLicenceResult');
  if(!country){
    box.className = 'tool-result show result-warn';
    box.innerHTML = 'Please select the country that issued your licence.';
    return;
  }
  var html = buildLicenceResult(country, age, isNaN(exp) ? null : exp);
  box.className = 'tool-result show ' + html.cls;
  box.innerHTML = html.text;
}

function buildLicenceResult(country, age, exp){
  if(country === 'recognised'){
    return { cls:'result-good', text:'<strong>Good news!</strong> Countries in this tier can usually exchange their licence directly for a Victorian licence with no knowledge or practical test required, subject to standard eligibility checks.<div style="margin-top:10px"><a class="btn btn-wa" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I%20have%20an%20overseas%20licence%20from%20a%20recognised%20country%20and%20want%20help%20converting%20it.">Ask Transformers for Help</a></div>' };
  }
  if(country === 'edr'){
    var youngUnknownAge = isNaN(age);
    var lightPathway = (!youngUnknownAge && age >= 25 && exp !== null && exp >= 3);
    var text = youngUnknownAge
      ? 'Experienced Driver Recognition countries have requirements that depend on your age and years of experience. Enter your age (and experience, on the full checker) for a precise answer.'
      : (lightPathway
          ? 'Based on your age (25+) and experience (3+ years), you may qualify for a more direct pathway, but a knowledge test is still commonly required. Book a chat with us to confirm your exact requirement.'
          : 'Based on your details, you’ll most likely need to complete a knowledge test, and, particularly if you’re under 25 or have less driving experience, a practical driving test as well.');
    return { cls:'result-warn', text:'<strong>Experienced Driver Recognition country.</strong> ' + text + '<div style="margin-top:10px"><a class="btn btn-wa" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I%20have%20an%20overseas%20licence%20and%20want%20help%20with%20my%20Victorian%20conversion%20pathway.">Ask Transformers for Help</a></div>' };
  }
  return { cls:'result-warn', text:'<strong>Full Victorian licensing process required.</strong> You’ll need to complete a knowledge test, a hazard perception test, and a practical driving test. Our instructors specialise in preparing overseas licence holders for exactly this pathway.<div style="margin-top:10px"><a class="btn btn-wa" target="_blank" rel="noopener" href="https://wa.me/61404119119?text=Hi%20Transformers%20Driving%20School!%20I%20need%20to%20complete%20the%20full%20Victorian%20driving%20test%20process%20and%20want%20lessons.">Book Lessons on WhatsApp</a></div>' };
}

/* ===================== HOME FAQ ===================== */
var homeFaqItems = [
  {q:'How many lessons before my test?', a:'Most students need 10–20 hours depending on experience. Take the readiness quiz above for a personalised estimate.'},
  {q:'Can I use your car for the actual test?', a:'Yes, our dual-control test vehicles are available for hire on test day, included in the Express Test Package and Ultimate Test Pass Pack.'},
  {q:'What if my licence isn’t from a recognised country?', a:'You’ll likely need a knowledge test, hazard perception test, and practical driving test. Our conversion checker above tells you exactly which apply to you.'},
  {q:'How do I book a lesson?', a:'Message us on WhatsApp using the button at the top or bottom of the page. We usually reply within the hour and can lock in a time straight away.'},
  {q:'Which VicRoads test centre do you cover?', a:'VicRoads Pakenham, with a dedicated guide on this site. We also provide lessons across Officer, Beaconsfield, Berwick, Nar Nar Goon, Clyde, Cranbourne, Cardinia and Devon Meadows.'}
];

function renderHomeFaq(){
  var wrap = document.getElementById('homeFaqList');
  if(!wrap) return;
  wrap.innerHTML = homeFaqItems.map(function(item){
    return '<div class="faq-item">' +
      '<button class="faq-q" aria-expanded="false" onclick="toggleFaq(this)">' + item.q +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></button>' +
      '<div class="faq-a"><div class="faq-a-inner">' + item.a + '</div></div>' +
      '</div>';
  }).join('');
}

function toggleFaq(btn){
  var expanded = btn.getAttribute('aria-expanded') === 'true';
  btn.setAttribute('aria-expanded', String(!expanded));
  var answer = btn.nextElementSibling;
  answer.style.maxHeight = expanded ? null : (answer.scrollHeight + 'px');
}

/* ===================== CONTACT MODAL (quick enquiry, available on every page) ===================== */
function openContactModal(){
  var modal = document.getElementById('contactModal');
  if(!modal) return;
  modal.hidden = false;
  document.body.style.overflow = 'hidden';
}
function closeContactModal(){
  var modal = document.getElementById('contactModal');
  if(!modal) return;
  modal.hidden = true;
  document.body.style.overflow = '';
}
document.addEventListener('keydown', function(e){
  if(e.key === 'Escape') closeContactModal();
});

/* ===================== WEB3FORMS EMAIL DELIVERY =====================
   1. Go to https://web3forms.com, enter transformers.com.au@gmail.com,
      and it will email you a free Access Key (no account needed).
   2. Paste that key below, replacing the placeholder text.
   Until you do this, submissions still work (they open WhatsApp) but are
   NOT emailed anywhere yet. The fetch() call below will silently fail
   and the form falls back to WhatsApp-only. */
var WEB3FORMS_ACCESS_KEY = 'PASTE_YOUR_WEB3FORMS_ACCESS_KEY_HERE';

function submitContactForm(event, formPrefix){
  event.preventDefault();
  var prefix = formPrefix || 'cf';
  var name = document.getElementById(prefix + 'Name').value;
  var phone = document.getElementById(prefix + 'Phone').value;
  var interest = document.getElementById(prefix + 'Interest').value;
  var message = document.getElementById(prefix + 'Message').value;
  var submitBtn = event.target.querySelector('button[type="submit"]');
  if(submitBtn){ submitBtn.disabled = true; submitBtn.textContent = 'Sending...'; }

  // Email the enquiry via Web3Forms (free, no backend needed)
  if(WEB3FORMS_ACCESS_KEY && WEB3FORMS_ACCESS_KEY.indexOf('PASTE_') !== 0){
    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        access_key: WEB3FORMS_ACCESS_KEY,
        subject: 'New enquiry from the Transformers Driving School website',
        from_name: 'Transformers Driving School website',
        name: name,
        phone: phone,
        interested_in: interest,
        message: message || '(no message provided)',
        page: window.location.pathname
      })
    }).catch(function(err){ console.error('Web3Forms submission failed:', err); });
  }

  // Also open WhatsApp with the same details for the fastest possible reply
  var text = 'Hi Transformers Driving School! My name is ' + name + ' (' + phone + '). I\'m interested in: ' + interest + (message ? ('. ' + message) : '.');
  var waLink = 'https://wa.me/61404119119?text=' + encodeURIComponent(text);
  window.open(waLink, '_blank', 'noopener');

  var formWrap = document.getElementById(prefix + 'FormWrap');
  var successWrap = document.getElementById(prefix + 'FormSuccess');
  if(formWrap) formWrap.style.display = 'none';
  if(successWrap) successWrap.classList.add('show');
}
