/* ============================================================
   AgriBot — Floating Chatbot Widget
   Works on every page. Supports Hindi + English.
   ============================================================ */
(function () {
  'use strict';

  /* ── State ── */
  let isOpen = false;
  let isTyping = false;
  let messageHistory = []; // sent to API

  /* ── Inject CSS ── */
  const style = document.createElement('style');
  style.textContent = `
    /* Floating button */
    #agribot-btn {
      position: fixed; bottom: 28px; right: 28px; z-index: 9999;
      width: 62px; height: 62px; border-radius: 50%;
      background: linear-gradient(135deg, #2D6A4F, #40916C);
      border: none; cursor: pointer; box-shadow: 0 4px 20px rgba(45,106,79,.45);
      display: flex; align-items: center; justify-content: center;
      font-size: 1.7rem; transition: transform .25s, box-shadow .25s;
      animation: botPulse 2.5s ease-in-out infinite;
    }
    #agribot-btn:hover { transform: scale(1.1); box-shadow: 0 6px 28px rgba(45,106,79,.55); }
    @keyframes botPulse {
      0%,100% { box-shadow: 0 4px 20px rgba(45,106,79,.45); }
      50%      { box-shadow: 0 4px 28px rgba(45,106,79,.75); }
    }

    /* Unread badge */
    #agribot-badge {
      position: fixed; bottom: 80px; right: 24px; z-index: 10000;
      background: #ef4444; color: #fff; border-radius: 50%;
      width: 20px; height: 20px; font-size: .72rem; font-weight: 700;
      display: flex; align-items: center; justify-content: center;
      display: none;
    }

    /* Chat window */
    #agribot-window {
      position: fixed; bottom: 102px; right: 28px; z-index: 9998;
      width: 370px; max-height: 540px;
      background: #fff; border-radius: 20px;
      box-shadow: 0 12px 48px rgba(0,0,0,.18);
      display: flex; flex-direction: column; overflow: hidden;
      transform: scale(.85) translateY(20px); opacity: 0;
      pointer-events: none;
      transition: transform .28s cubic-bezier(.34,1.56,.64,1), opacity .22s;
    }
    #agribot-window.open {
      transform: scale(1) translateY(0); opacity: 1; pointer-events: all;
    }

    /* Header */
    #agribot-header {
      background: linear-gradient(135deg, #2D6A4F, #40916C);
      padding: .9rem 1.1rem; display: flex; align-items: center; gap: .75rem;
      color: #fff; flex-shrink: 0;
    }
    #agribot-avatar {
      width: 40px; height: 40px; background: rgba(255,255,255,.2);
      border-radius: 50%; display: flex; align-items: center;
      justify-content: center; font-size: 1.3rem; flex-shrink: 0;
    }
    #agribot-header .info { flex: 1; }
    #agribot-header .name { font-weight: 700; font-size: .98rem; }
    #agribot-header .status {
      font-size: .75rem; opacity: .85; display: flex; align-items: center; gap: 4px;
    }
    .status-dot {
      width: 7px; height: 7px; background: #4ade80;
      border-radius: 50%; display: inline-block;
    }
    #agribot-close {
      background: none; border: none; color: #fff; font-size: 1.3rem;
      cursor: pointer; opacity: .8; padding: 4px; line-height: 1;
    }
    #agribot-close:hover { opacity: 1; }

    /* Messages */
    #agribot-messages {
      flex: 1; overflow-y: auto; padding: 1rem; display: flex;
      flex-direction: column; gap: .65rem; scroll-behavior: smooth;
    }
    #agribot-messages::-webkit-scrollbar { width: 4px; }
    #agribot-messages::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 2px; }

    .bot-msg, .user-msg {
      max-width: 82%; padding: .6rem .9rem; border-radius: 16px;
      font-size: .88rem; line-height: 1.55; word-break: break-word;
      animation: msgIn .2s ease;
    }
    @keyframes msgIn { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:none} }
    .bot-msg  { background: #f3f4f6; color: #111; align-self: flex-start;
                border-bottom-left-radius: 4px; }
    .user-msg { background: linear-gradient(135deg,#2D6A4F,#40916C);
                color: #fff; align-self: flex-end; border-bottom-right-radius: 4px; }

    /* Typing dots */
    .typing-bubble { display: flex; gap: 4px; padding: .65rem .9rem;
      background: #f3f4f6; border-radius: 16px; border-bottom-left-radius: 4px;
      align-self: flex-start; width: 56px; }
    .typing-bubble span {
      width: 7px; height: 7px; background: #9ca3af; border-radius: 50%;
      animation: bounce .9s infinite;
    }
    .typing-bubble span:nth-child(2) { animation-delay: .15s; }
    .typing-bubble span:nth-child(3) { animation-delay: .30s; }
    @keyframes bounce {
      0%,60%,100% { transform: translateY(0); }
      30%          { transform: translateY(-6px); }
    }

    /* Quick replies */
    #agribot-quickreplies {
      display: flex; gap: .4rem; padding: .5rem 1rem 0;
      flex-wrap: wrap; flex-shrink: 0;
    }
    .quick-btn {
      padding: .3rem .7rem; border: 1.5px solid #2D6A4F; border-radius: 20px;
      font-size: .78rem; color: #2D6A4F; background: #fff;
      cursor: pointer; transition: all .18s; white-space: nowrap;
    }
    .quick-btn:hover { background: #2D6A4F; color: #fff; }

    /* Input */
    #agribot-input-area {
      padding: .75rem 1rem; display: flex; gap: .5rem; align-items: flex-end;
      border-top: 1px solid #f0f0f0; flex-shrink: 0;
    }
    #agribot-input {
      flex: 1; border: 1.5px solid #e5e7eb; border-radius: 22px;
      padding: .55rem .95rem; font-size: .88rem; outline: none;
      resize: none; max-height: 90px; overflow-y: auto;
      font-family: inherit; transition: border-color .2s; line-height: 1.45;
    }
    #agribot-input:focus { border-color: #2D6A4F; }
    #agribot-send {
      width: 38px; height: 38px; border-radius: 50%; background: #2D6A4F;
      border: none; color: #fff; cursor: pointer; display: flex;
      align-items: center; justify-content: center; flex-shrink: 0;
      font-size: 1rem; transition: background .2s;
    }
    #agribot-send:hover { background: #40916C; }
    #agribot-send:disabled { background: #9ca3af; cursor: not-allowed; }

    /* Tooltip label */
    #agribot-tooltip {
      position: fixed; bottom: 42px; right: 98px; z-index: 9999;
      background: #1a1a1a; color: #fff; padding: .35rem .75rem;
      border-radius: 8px; font-size: .82rem; white-space: nowrap;
      pointer-events: none; opacity: 0; transition: opacity .3s;
    }
    #agribot-tooltip.show { opacity: 1; }

    @media (max-width: 420px) {
      #agribot-window { width: calc(100vw - 24px); right: 12px; bottom: 96px; }
    }
  `;
  document.head.appendChild(style);

  /* ── Build DOM ── */
  document.body.insertAdjacentHTML('beforeend', `
    <div id="agribot-tooltip">Ask AgriBot 🌾</div>
    <div id="agribot-badge"></div>

    <button id="agribot-btn" title="AgriBot — Farming Assistant" onclick="agriBot.toggle()">🤖</button>

    <div id="agribot-window">
      <div id="agribot-header">
        <div id="agribot-avatar">🌾</div>
        <div class="info">
          <div class="name">AgriBot</div>
          <div class="status"><span class="status-dot"></span> Online — Hindi &amp; English</div>
        </div>
        <button id="agribot-close" onclick="agriBot.toggle()" title="Close">✕</button>
      </div>

      <div id="agribot-messages"></div>

      <div id="agribot-quickreplies">
        <button class="quick-btn" onclick="agriBot.quickSend('Best crops for sandy soil?')">Sandy Soil Crops</button>
        <button class="quick-btn" onclick="agriBot.quickSend('मेरी फसल पीली हो रही है, क्या करूं?')">पीली फसल</button>
        <button class="quick-btn" onclick="agriBot.quickSend('PM-KISAN scheme details')">PM-KISAN</button>
        <button class="quick-btn" onclick="agriBot.quickSend('Wheat sowing tips for November')">Wheat Tips</button>
      </div>

      <div id="agribot-input-area">
        <textarea id="agribot-input" rows="1" placeholder="Type in Hindi or English…"
          onkeydown="agriBot.handleKey(event)"
          oninput="agriBot.autoResize(this)"></textarea>
        <button id="agribot-send" onclick="agriBot.send()" title="Send">➤</button>
      </div>
    </div>
  `);

  /* ── Public API ── */
  window.agriBot = {

    toggle() {
      isOpen = !isOpen;
      document.getElementById('agribot-window').classList.toggle('open', isOpen);
      document.getElementById('agribot-badge').style.display = 'none';
      if (isOpen) {
        this._greet();
        setTimeout(() => document.getElementById('agribot-input').focus(), 300);
      }
    },

    _greeted: false,
    _greet() {
      if (this._greeted) return;
      this._greeted = true;
      const hour = new Date().getHours();
      const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';
      this._addMsg(`${greeting}! 🌾 I'm **AgriBot**, your farming assistant.\n\nAsk me anything about crops, soil, diseases, fertilizers, or government schemes — in **Hindi or English**!`, 'bot');
    },

    handleKey(e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); this.send(); }
    },

    autoResize(el) {
      el.style.height = 'auto';
      el.style.height = Math.min(el.scrollHeight, 90) + 'px';
    },

    quickSend(text) {
      document.getElementById('agribot-input').value = text;
      this.send();
    },

    async send() {
      const input = document.getElementById('agribot-input');
      const text = input.value.trim();
      if (!text || isTyping) return;

      input.value = '';
      input.style.height = 'auto';
      this._addMsg(text, 'user');
      messageHistory.push({ role: 'user', content: text });

      isTyping = true;
      document.getElementById('agribot-send').disabled = true;
      const typingEl = this._addTyping();

      try {
        const resp = await fetch('/chatbot/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ messages: messageHistory })
        });
        const data = await resp.json();
        typingEl.remove();

        const reply = data.reply || data.error || 'Sorry, something went wrong.';
        this._addMsg(reply, 'bot');
        messageHistory.push({ role: 'assistant', content: reply });

        // Keep history manageable
        if (messageHistory.length > 20) messageHistory = messageHistory.slice(-20);

      } catch (err) {
        typingEl.remove();
        this._addMsg('Network error. Please check your connection.', 'bot');
      }

      isTyping = false;
      document.getElementById('agribot-send').disabled = false;
      document.getElementById('agribot-input').focus();
    },

    _addMsg(text, role) {
      const msgs = document.getElementById('agribot-messages');
      const div = document.createElement('div');
      div.className = role === 'bot' ? 'bot-msg' : 'user-msg';
      // Simple markdown: **bold**, newlines
      div.innerHTML = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
      msgs.appendChild(div);
      msgs.scrollTop = msgs.scrollHeight;
      return div;
    },

    _addTyping() {
      const msgs = document.getElementById('agribot-messages');
      const div = document.createElement('div');
      div.className = 'typing-bubble';
      div.innerHTML = '<span></span><span></span><span></span>';
      msgs.appendChild(div);
      msgs.scrollTop = msgs.scrollHeight;
      return div;
    }
  };

  /* ── Tooltip on hover ── */
  const btn = document.getElementById('agribot-btn');
  const tip = document.getElementById('agribot-tooltip');
  btn.addEventListener('mouseenter', () => { if (!isOpen) tip.classList.add('show'); });
  btn.addEventListener('mouseleave', () => tip.classList.remove('show'));

})();
