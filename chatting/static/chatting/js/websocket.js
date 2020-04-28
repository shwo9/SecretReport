// 어느 창가자 냐에 따라서 좌우 레이아웃이 반전되야하기 때문에 분기로 나눠줌
function returnChattingLine(chatting) {
  let result = "";

  if (WebSocketInstance.position === "lawyer") {
    if (chatting.lawyer === null || chatting.lawyer === "") {
      result += '<div class="chatting_line left">';
      result += `<div class="chatting_box">${ chatting.content }</div>`;
      result += `<div class="chatting_date">${ chatting.pub_date }</div>`;
    }
    else {
      result += '<div class="chatting_line right">';
      result += `<div class="chatting_date">${ chatting.pub_date }</div>`;
      result += `<div class="chatting_box">${ chatting.content }</div>`;
    }
  } else {
    if (chatting.lawyer === null || chatting.lawyer === "") {
      result += '<div class="chatting_line right">';
      result += `<div class="chatting_date">${ chatting.pub_date }</div>`;
      result += `<div class="chatting_box">${ chatting.content }</div>`;
    }
    else {
      result += '<div class="chatting_line left">';
      result += `<div class="chatting_box">${ chatting.content }</div>`;
      result += `<div class="chatting_date">${ chatting.pub_date }</div>`;
    }
  }
  result += '</div>';

  return result;
}

// 기존에 있던 채팅목록을 불러와서 띄워줌
function displayFetchedChattings(chattings) {
  let result = "";
  el = document.querySelector("#chatting_body");
  console.log(chattings)
  for (let key of Object.keys(chattings)) {
    result += returnChattingLine(chattings[key]);
  }
// 스크롤 최하단으로
  el.innerHTML = result;
  el.scrollTop = el.scrollHeight;
}
// 새로운 채팅 작성시
function displayNewChatting(chatting) {
  let result = "";
  el = document.querySelector("#chatting_body");

  result += returnChattingLine(chatting);

  el.innerHTML += result;
  // 스크롤 제일 아래로
  setTimeout(() => {
    el.scrollTop = el.scrollHeight;
  }, 0);
}

class WebSocketService {
  static instance = null;
  static position;
  // 현재 존재하지 않으면 생성
  static getInstance() {
    if (!WebSocketService.instance) WebSocketService.instance = new WebSocketService();
    return WebSocketService.instance;
  }

  constructor() {
    this.socketRef = null;
  }

  connect(path) {
    return new Promise((resolve, reject) => {
      this.socketRef = new WebSocket(path);
      
      // socket 이 열린걸 확인
      this.socketRef.onopen = () => {
        console.log('WebSocket Open');
        resolve();
      };
      
      // 메세지가 수신되면 onmessage 함수로 전달
      this.socketRef.onmessage = e => {
        try {
          let jsonData = JSON.parse(e.data);

          // 기존의 메세지 전달
          if (jsonData['command'] === "fetch_messages") displayFetchedChattings(jsonData['messages']);
          // 새로운 메세지 전달
          else if (jsonData['command'] === "new_message") displayNewChatting(jsonData['message']);
        }
        catch (err) {
          console.log(err);
        }
      };
      this.socketRef.onerror = e => {
        console.log(e.message);
        reject();
      };
      this.socketRef.onclose = () => {
        console.log("WebSocket closed let's reopen");
        this.connect(path);
      }
    });
  }
// room 에 대한 정보와 참가자에 대한 정보 
  initChat(room_id, position) {
    this.sendMessage({ command: 'init_chat', room_id: room_id, position: position });
  }
// 기존에 있던 메세지 불러오기
  fetchMessages(position) {
    this.position = position;
    this.sendMessage({ command: 'fetch_messages' });
  }
// 새로운 메세지 쓰기
  newChatMessage(message, position) {
    this.sendMessage({ command: 'new_message', message: message, position: position }); 
  }
  
  sendMessage(data) {
    try {
      // stringfy : json -> string
      this.socketRef.send(JSON.stringify({ ...data }));
    }
    catch(err) {
      console.log(err.message);
    }  
  }
}

// WebSocketService 객체 생성
const WebSocketInstance = WebSocketService.getInstance();