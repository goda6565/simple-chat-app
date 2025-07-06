from fastapi import Request
from fastapi.responses import HTMLResponse


class UIHandler:
    async def handle(self, request: Request):
        """チャットストリーム用の簡易 UI を返す。"""

        html_content = """
        <!DOCTYPE html>
        <html lang=\"ja\">
          <head>
            <meta charset=\"UTF-8\" />
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
            <title>Chat Stream Demo</title>
            <style>
              body { font-family: Arial, Helvetica, sans-serif; margin: 0; padding: 0; }
              header { background: #3f51b5; color: #fff; padding: 1rem; text-align: center; }
              #chat-container { display: flex; flex-direction: column; height: 100vh; }
              #messages { flex: 1; overflow-y: auto; padding: 1rem; }
              .question { color: #1a237e; margin: 0.5rem 0; font-weight: bold; }
              .answer { color: #004d40; margin: 0.5rem 0 1rem; }
              #input-area { display: flex; padding: 1rem; border-top: 1px solid #ccc; }
              #question-input { flex: 1; font-size: 1rem; padding: 0.5rem; }
              #send-btn { padding: 0.5rem 1rem; font-size: 1rem; margin-left: 0.5rem; cursor: pointer; }
            </style>
          </head>
          <body>
            <div id=\"chat-container\">
              <header>
                <h2>Chat Stream Demo</h2>
              </header>
              <div id=\"messages\"></div>
              <div id=\"input-area\">
                <input id=\"question-input\" type=\"text\" placeholder=\"質問を入力してください...\" autofocus />
                <button id=\"send-btn\">送信</button>
              </div>
            </div>
            <script>
              (function () {
                // プロトコルに応じて ws / wss を切り替え
                const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
                const wsUrl = `${wsScheme}://${window.location.host}/chat/stream`;
                const socket = new WebSocket(wsUrl);

                // UUID を生成（古いブラウザ向けに fallback も用意）
                const chatId = (crypto.randomUUID ? crypto.randomUUID() : [...Array(36)].map((_, i) => {
                  if ([8, 13, 18, 23].includes(i)) return '-';
                  const r = (crypto.getRandomValues ? crypto.getRandomValues(new Uint8Array(1))[0] : Math.random() * 16) & 15;
                  return (i === 14 ? 4 : (i === 19 ? (r & 0x3) | 0x8 : r)).toString(16);
                }).join(''));

                const messagesEl = document.getElementById('messages');
                const questionInput = document.getElementById('question-input');
                const sendBtn = document.getElementById('send-btn');

                function appendMessage(text, className) {
                  const p = document.createElement('p');
                  p.className = className;
                  p.textContent = text;
                  messagesEl.appendChild(p);
                  messagesEl.scrollTop = messagesEl.scrollHeight; // 自動スクロール
                }

                sendBtn.addEventListener('click', sendQuestion);
                questionInput.addEventListener('keypress', function (e) {
                  if (e.key === 'Enter') {
                    sendQuestion();
                  }
                });

                function sendQuestion() {
                  const question = questionInput.value.trim();
                  if (!question) return;
                  socket.send(JSON.stringify({ chat_id: chatId, current_question: question }));
                  appendMessage(question, 'question');
                  questionInput.value = '';
                }

                socket.onmessage = function (event) {
                  appendMessage(event.data, 'answer');
                };

                socket.onerror = function (event) {
                  console.error('WebSocket error:', event);
                };
              })();
            </script>
          </body>
        </html>
        """

        return HTMLResponse(content=html_content, status_code=200)

def create_ui_handler() -> UIHandler:
    return UIHandler()